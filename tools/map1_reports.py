"""Build non-executable MAP-1 dossiers. Status never implies owner approval."""
import collections as C
import csv, html, json, re, textwrap, base64, io, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from map1_prepare import ROOT, OUT, INPUT, GAME, table, savecsv, protected, digest
from map1_geography import EVIDENCE, load_definitions

def esc(s): return html.escape(str(s),quote=True)
def font(n): return ImageFont.truetype('C:/Windows/Fonts/arial.ttf',n)

SOURCE_CHECKS={
 'R1_WESTERN_EUROPE-S001':('ACCESSED_CONTEXT_CONFIRMED','ANLux notice confirms two disputed 1776 maps; May dossier is after cutoff. Map endpoints could not be fetched.'),
 'R1_WESTERN_EUROPE-S008':('FETCH_FAILED','502/failed fetch. Regional conclusion retained as unverified externally.'),
 'R1_WESTERN_EUROPE-S009':('FETCH_FAILED','502. No historical polygon inspected.'),
 'R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-S003':('ACCESSED_CHRONOLOGY_CONFIRMED','Ernest Tucker, Vol XIII pp.561-564: occupation of Basra in April 1776 after siege. Not a boundary map.'),
 'R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-S004':('ACCESSED_CONTEXT_CONFIRMED','Fred M. Donner, Vol III pp.851-855: blockade, surrender during 1776, Persian garrison. Month corroborated separately.'),
 'R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-S006':('ACCESSED_NOT_FULLY_REVIEWED','Article accessible, Kioumars Ghereghlou. Afsharid control extent and final paragraphs still require detailed regional review.'),
 'R4_SOUTH_ASIA-S005':('ACCESSED_CHRONOLOGY_CONFIRMED','T. Bhujanga Rao, Triveni Oct-Dec 1940, paragraphs on 1766/1768 and Guntur acquisition in 1789; colonial argument, treaty citations not original scans.'),
 'R5_EAST_ASIA-S16':('FETCH_FAILED','LOC resource link failed; never used to draw 1776 frontier.'),
 'R8_NORTH_AMERICA_CARIBBEAN-S016':('ACCESSED_CHRONOLOGY_CONFIRMED','LOC exhibit separates fur trade after 1741 from colony in 1784. Exhibit map dated 1802 not overlaid.'),
 'R9_SOUTH_AMERICA-S009':('ACCESSED_CONTEXT_CONFIRMED','Nationaal Archief lists distinct Essequibo, Demerara and Berbice administrations; not an interior border map.'),
 'R9_SOUTH_AMERICA-S019':('ACCESSED_NOT_FULLY_REVIEWED','Wikisource transcription accessible; post-cutoff 1802 document, not a 1776 boundary proof.'),
 'R9_SOUTH_AMERICA-S001':('ACCESSED_NOT_FULLY_REVIEWED','Wikisource transcription accessible; post-cutoff August 1776 act, no automatic retroprojection.'),
 'R9_SOUTH_AMERICA-S031':('FETCH_FAILED','BNE returns 403/failed fetch. No map image or overlay inspected.')
}

def main():
    out_before=json.loads((OUT/'MAP1_RUNTIME_BEFORE.json').read_text(encoding='utf-8'))
    assert protected()==out_before, 'Runtime changed before report build'
    masters=table(INPUT/'map1_outputs/WORLD_BORDERS_1776_MASTER.csv'); master={r['Change_ID']:r for r in masters}
    sources=table(INPUT/'map1_outputs/WORLD_BORDERS_1776_SOURCES.csv'); source={r['Source_ID']:r for r in sources}
    queue=table(INPUT/'map1_outputs/WORLD_BORDERS_1776_MAPPING_QUEUE.csv')
    coverage=table(INPUT/'map1_outputs/WORLD_BORDERS_1776_COVERAGE.csv')
    region_pairs=table(INPUT/'map0_reference/MAP_1776_9_REGIONS.csv')
    cv={(r['State_ID'],r['Current_Owner_TAG']) for r in coverage}
    assert len(cv)==1043==len(coverage)
    cat={(r['State_ID'],r.get('Owner_TAG',r.get('Current_Owner_TAG'))) for r in region_pairs}
    assert cv==cat
    assert len({r['Region_ID'] for r in masters})==9
    for r in masters:
        assert r['Historical_Date']=='1776-01-01'
        assert r['Change_ID'] in master
        assert all(x in source for x in r['Source_IDs'].split('|') if x)
    originals=[]
    for p in (INPUT/'regional_originals').glob('*RECOMMENDATIONS.csv'): originals+=table(p)
    assert len(originals)==1005 and len({r['Change_ID'] for r in originals})==1005
    for r in originals:
        assert all(master[r['Change_ID']][k]==v for k,v in r.items()), r['Change_ID']
    priorities=table(INPUT/'map1_outputs/MAP1_PRIORITY_ARBITRATION.csv')
    notes=json.loads((ROOT/'tools/map1_review_notes.json').read_text(encoding='utf-8'))
    issues=table(INPUT/'map0_reference/MAP_1776_KNOWN_ISSUES.csv')
    baseline=table(OUT/'MAP1_BASELINE_PROVINCE_INDEX.csv')
    locators=table(OUT/'MAP1_HUB_LOCATOR_CHECKS.csv')
    defs,hubs,names,countries=load_definitions()
    geo=json.loads((EVIDENCE/'geometry_index.json').read_text())
    bitmap=np.load(EVIDENCE/'pixel_index.npz')['rgb']
    bystate=C.defaultdict(list); byrgb=C.defaultdict(list); pair=C.defaultdict(set); bymainstate=C.defaultdict(list)
    for r in baseline:
        bystate[r['State_ID']].append(r); byrgb[r['Province_ID']].append(r)
        pair[r['State_ID'],r['Owner_TAG']].add(r['Province_ID'])
    for r in masters: bymainstate[r['State_ID']].append(r)
    issuess=C.defaultdict(list)
    for i in issues:
        for sid in i['State_ID'].split('|'): issuess[sid].append(i)
    locby=C.defaultdict(list)
    for r in locators: locby[r['State_ID']].append(r)
    caseby={}
    for p in priorities:
        for cid in p['Linked_Change_IDs'].split('|'): caseby[cid]=p
    dossierdir=OUT/'MAP1_CASE_DOSSIERS'; dossierdir.mkdir(exist_ok=True)
    atlas=EVIDENCE/'STATE_ATLAS'; atlas.mkdir(exist_ok=True)
    viewmeta={}

    def color(tag):
        if not tag: return (126,134,148)
        import hashlib,colorsys
        b=hashlib.sha256(tag.encode()).digest()
        # Red is reserved for multiple written owners, yellow for disputed focus.
        return tuple(round(v*255) for v in colorsys.hsv_to_rgb(.28+.38*b[0]/255,.30+.20*b[1]/255,.65+.15*b[2]/255))

    def state_view(sid, highlights=None, title=None, target=None):
        ps=set(defs[sid]['provinces']); selected=set(highlights or [])
        boxes=[geo['bboxes'][v] for v in ps|selected if v in geo['bboxes']]
        x0=min(b[0] for b in boxes); x1=max(b[2] for b in boxes)
        y0=min(b[1] for b in boxes); y1=max(b[3] for b in boxes)
        # Minimum circular envelope handles states crossing the raster seam.
        if x1-x0>bitmap.shape[1]//2:
            occupied=np.zeros(bitmap.shape[1],dtype=bool)
            state_values=np.array([int(v[1:],16) for v in ps],dtype=np.uint32)
            for x in np.flatnonzero(np.isin(bitmap,state_values).any(axis=0)): occupied[x]=True
            e=np.flatnonzero(~occupied); cuts=np.r_[0,np.flatnonzero(e[1:]!=e[:-1]+1)+1,len(e)]
            lo,hi=max(zip(cuts[:-1],cuts[1:]),key=lambda p:p[1]-p[0])
            x0=int(e[hi-1])+1; x1=x0+bitmap.shape[1]-(hi-lo)
        pad=8; x0=int(x0)-pad; x1=int(x1)+pad; y0=max(0,int(y0)-pad); y1=min(bitmap.shape[0],int(y1)+pad)
        xs=np.arange(x0,x1)%bitmap.shape[1]; crop=bitmap[y0:y1][:,xs]
        canvas=np.full((*crop.shape,3),(42,52,63),dtype=np.uint8)
        present=np.unique(crop)
        for val in present:
            v='x%06X'%int(val); rs=byrgb.get(v,[])
            if v in ps or v in selected:
                tags=sorted({r['Owner_TAG'] for r in rs if r['Owner_TAG']})
                c=color('/'.join(tags)) if len(tags)<=1 else (208,113,113)
                if v in selected: c=(238,197,72)
                canvas[crop==val]=c
            elif rs and rs[0]['Territory_Type']=='LAND': canvas[crop==val]=(69,78,80)
        edges=np.zeros(crop.shape,dtype=bool)
        edges[:,1:]|=crop[:,1:]!=crop[:,:-1]; edges[1:]|=crop[1:]!=crop[:-1]
        canvas[edges]=(22,28,34)
        image=Image.fromarray(canvas)
        imgbytes=io.BytesIO(); image.save(imgbytes,format='PNG')
        data=base64.b64encode(imgbytes.getvalue()).decode()
        width,height=image.size
        parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="1800" height="1200" viewBox="0 0 {width} {height}" style="background:#202a32">',
               '<title>'+esc(sid+'; RGBs exacts, frontières historiques non vérifiées')+'</title>',
               f'<image width="{width}" height="{height}" href="data:image/png;base64,{data}"/>']
        for v in sorted(ps|selected):
            if v not in geo['anchors']: continue
            x,y=geo['anchors'][v]; xx=(x-x0)%bitmap.shape[1]; yy=y-y0
            if xx>=width or not(0<=yy<height): continue
            tags='/'.join(sorted({r['Owner_TAG'] or 'NO_OWNER' for r in byrgb[v]}))
            parts.append(f'<g><title>{esc(v+" ; "+tags)}</title><text x="{xx:.2f}" y="{yy:.2f}" text-anchor="middle" font-family="Arial" font-size="2.6" fill="white" stroke="#15202b" stroke-width="0.55" paint-order="stroke">{v}</text></g>')
        for loc in locby[sid]:
            xx=(float(loc['Locator_X'])-x0)%bitmap.shape[1]; yy=float(loc['Locator_Y'])-y0
            if xx>=width or not(0<=yy<height): continue
            parts.append(f'<circle cx="{xx}" cy="{yy}" r="1.1" fill="#fff" stroke="#000" stroke-width=".4"><title>{esc(loc["Hub_Name"]+" (locator vanilla, pas preuve historique) "+loc["Locator_Sampled_RGB"])}</title></circle>')
        parts.append('</svg>')
        stem=target or sid
        svg=atlas/(stem+'.svg'); svg.write_text('\n'.join(parts),encoding='utf-8')
        meta=dict(State_ID=sid,Province_RGBs=sorted(ps),Highlighted_RGBs=sorted(selected),Pixel_Crop=[x0,y0,x1,y1],
                  Wrap_X=True,Historical_Overlay='NONE',GPS_Projection='NONE',Source_Bitmap_SHA256=digest(GAME/'map_data/provinces.png'),
                  Labels='Technical province IDs; hubs are engine-localization anchors only',Historical_Match='NOT_VERIFIED')
        (atlas/(stem+'.json')).write_text(json.dumps(meta,indent=2),encoding='utf-8')
        return image,meta,svg

    # One exact technical view per state in the queue, with linked source dossiers for every row.
    for sid in sorted({r['State_ID'] for r in queue}):
        if sid in defs: _,meta,svg=state_view(sid); viewmeta[sid]=meta
    source_audit=[]
    for s in sources:
        status,note=SOURCE_CHECKS.get(s['Source_ID'],('CATALOG_ONLY_NOT_FETCHED','Regional bibliography preserved; content not independently accessed in this pass.'))
        source_audit.append(dict(s,MAP1_Access_Status=status,MAP1_Access_Date='2026-10-10' if s['Source_ID'] in SOURCE_CHECKS else '',
                                 MAP1_Review_Notes=note,Map_Overlay_Applied='NO'))
    savecsv('MAP1_SOURCE_REVIEW.csv',source_audit)
    # Supplemental official chronology is not silently injected into original bibliographies.
    savecsv('MAP1_SUPPLEMENTAL_SOURCES.csv',[dict(Source_ID='MAP1-SUP-001',Title='Nova Scotia',Author='Government of Canada',URL='https://www.canada.ca/en/canadian-heritage/services/provincial-territorial-symbols-canada/nova-scotia.html',Access_Date='2026-10-10',Finding='New Brunswick separated from Nova Scotia in 1784; no province boundary evidence',Geographic_Proof='NONE')])

    for p in priorities:
        sid=p['State_ID']; special=notes[p['Case_ID']]
        relevant=[master[c] for c in p['Linked_Change_IDs'].split('|')]
        focus=set(re.findall(r'x[0-9A-Fa-f]{6}',p['Required_Research_Or_Mapping']+' '+special['finding']))
        for i in issuess[sid]:
            if i['Context']=='MAIN_WORKING_TREE' and i['Province_ID']: focus.add(i['Province_ID'])
        image,meta,svg=state_view(sid,focus,target=p['Case_ID'])
        # Readable annotated overview. Zoomable SVG contains ALL province labels.
        page=Image.new('RGB',(1700,1120),(245,247,249)); draw=ImageDraw.Draw(page)
        draw.text((28,18),p['Case_ID']+'  '+sid,fill='#10202f',font=font(27))
        draw.text((28,58),'1776-01-01 | Carte technique actuelle - aucune frontière historique validée',fill='#8b301f',font=font(20))
        factor=min(1040/image.width,790/image.height)
        image=image.resize((round(image.width*factor),round(image.height*factor)),Image.Resampling.NEAREST)
        ox=28+(1040-image.width)//2; oy=112+(790-image.height)//2; page.paste(image,(ox,oy))
        sx=image.width/(meta['Pixel_Crop'][2]-meta['Pixel_Crop'][0]); sy=image.height/(meta['Pixel_Crop'][3]-meta['Pixel_Crop'][1])
        for v in sorted(focus or (set(defs[sid]['provinces']) if len(defs[sid]['provinces'])<=20 else set())):
            if v not in geo['anchors']: continue
            x,y=geo['anchors'][v]; xx=(x-meta['Pixel_Crop'][0])%bitmap.shape[1]; yy=y-meta['Pixel_Crop'][1]
            if xx>=meta['Pixel_Crop'][2]-meta['Pixel_Crop'][0] or yy<0: continue
            draw.text((ox+xx*sx,oy+yy*sy),v,anchor='mm',font=font(13),fill='white',stroke_fill='black',stroke_width=2)
        yy=112
        def paragraph(text,size=17,fill='#213345'):
            nonlocal yy
            for line in textwrap.wrap(text,58 if size==17 else 64):
                draw.text((1100,yy),line,font=font(size),fill=fill); yy+=size+5
            yy+=12
        paragraph(p['Issue'],21)
        paragraph(special['finding'])
        paragraph('Question ciblée : '+special['question'])
        paragraph('Jaune : RGB discutés. Rouge : attributions multiples. Autres couleurs : propriétaires écrits. Noir : contours RGB. Points blancs : hubs dans le SVG.',16)
        paragraph('Propriétaires écrits dans cet État : '+', '.join(sorted({r['Owner_TAG'] or 'NONE' for r in bystate[sid]}))+'. Un RGB jaune hors État est un indice technique à contrôler.',16)
        paragraph('Superposition de carte ancienne : aucune. Références et dates dans le dossier adjacent. Labels RGB zoomables dans le SVG; une liste complète est dans le dossier.',16)
        draw.text((28,940),'Fichier source : provinces.png, Victoria 3 1.13.11 | espace pixel, wrap_x | production 2026-10-10',font=font(17),fill='#354553')
        draw.text((28,974),'Le tracé historique discuté reste à établir. Aucun aplat de cette vue ne prouve une souveraineté en 1776.',font=font(17),fill='#8b301f')
        draw.text((28,1008),'Aperçu associé : STATE_ATLAS/'+p['Case_ID']+'.svg (zoom) ; RGB et source dans le dossier .md.',font=font(17),fill='#354553')
        page.save(EVIDENCE/(p['Case_ID']+'.png'))
        text=['# '+p['Case_ID']+' — '+p['Issue'],'','Statut : revue historique et géographique ouverte. Aucun transfert approuvé.','',
              f'![Vue technique]({p["Case_ID"]}.png)','',f'[Vue RGB zoomable](STATE_ATLAS/{p["Case_ID"]}.svg)','',
              '## Résultat de localisation technique','',special['finding'],'','Décision de cette passe : '+special['decision'],'',
              '## Question pour la recherche régionale','',special['question'],'','## Références et limites','']
        refs=set()
        for r in relevant: refs.update(r['Source_IDs'].split('|'))
        for ident in sorted(refs):
            s=source[ident]; status,note=SOURCE_CHECKS.get(ident,('CATALOG_ONLY_NOT_FETCHED','Notice importée, source originale non consultée indépendamment.'))
            text += [f'### {ident}','',f'{s["Author"]}. {s["Title"]}. Publication : {s["Publication_Date"]}. Document : {s["Document_Date"]}.',
                     '',f'Référence : {s["URL_or_Bibliographic_Reference"]}', '',f'Pages/carte : {s["Pages_or_Map"]}',
                     '',f'Pertinence : {s["Temporal_Relevance"]}', '',f'Biais/limites : {s["Limitations"]}', '',f'Accès MAP-1 : {status}. {note}','']
        text+=['## Géoréférencement','',
               'Bitmap exact et contours pixel extraits. Aucun fond historique superposé, aucune projection GPS adoptée, aucun résidu de calage inventé. Les points des locators sont contrôlés dans le raster, pas contre un cadastre historique. Les noms de hubs peuvent être anachroniques ou erronés. Trois points indépendants et un point de contrôle hors ajustement restent requis pour un calage local de carte ancienne.','',
               '## RGB et propriétaires écrits','', '| RGB | Propriétaire(s) | Pixels | Hub déclaré |','|---|---|---:|---|']
        for v in sorted(set(defs[sid]['provinces'])):
            rs=byrgb[v]; text.append('| '+v+' | '+' / '.join(sorted({r['Owner_TAG'] or 'NONE' for r in rs}))+' | '+rs[0]['Province_Pixels']+' | '+rs[0]['Hub_Anchors']+' |')
        (EVIDENCE/(p['Case_ID']+'.md')).write_text('\n'.join(text)+'\n',encoding='utf-8')

    matches=[]; unresolved=[]
    for q in queue:
        r=master[q['Change_ID']]; sid=r['State_ID']; cid=r['Change_ID']; p=caseby.get(cid)
        refs=r['Source_IDs'].split('|'); relevant_issues=issuess[sid]
        declared=set(re.findall(r'x[0-9A-Fa-f]{6}', ' '.join([r['Province_ID'],r['Province_IDs'],r['Research_Notes'],r['Geographic_Correspondence']])))
        candidates={v.upper().replace('X','x',1) for v in declared if v.upper().replace('X','x',1) in byrgb}
        domain=sorted(pair[sid,r['Current_Owner_TAG']])
        # No inferred polygon is promoted just because a research confidence is HIGH.
        status='MAPPING_REQUIRED'
        review='REGIONAL_CONCLUSION_IMPORTED_NOT_INDEPENDENTLY_VERIFIED'
        decision='No historic polygon overlaid. Current owner/domain is a search scope, not a historic match.'
        if p: decision=notes[p['Case_ID']]['finding']+' '+notes[p['Case_ID']]['decision']
        if cid=='R8_NORTH_AMERICA_CARIBBEAN-0065':
            decision+=' Official Canadian chronology corroborates the 1784 split, but not the precise 1776 controlled area.'
            review='CHRONOLOGY_CORROBORATED_MAPPING_PENDING'
        if p and p['Case_ID']=='MAP1-P0-005': review='CHRONOLOGY_CORROBORATED_MAPPING_PENDING'
        prop=r['Proposed_Owner_TAG']
        tagstatus='DEFINED' if prop in countries else ('NOT_A_TAG' if prop in ('','UNCHANGED','NEW_TAG_REQUIRED') else 'UNDEFINED')
        counterpart=[x for x in bymainstate[sid] if x['Region_ID']!=r['Region_ID']]
        artifact=f'MAP1_CASE_DOSSIERS/{cid}.md'
        matches.append(dict(Change_ID=cid,State_ID=sid,Research_Current_Owner_TAG=r['Current_Owner_TAG'],Research_Proposed_Owner_TAG=prop,
            Verified_Province_IDs='',Candidate_Reference_RGBs='|'.join(sorted(candidates)),Current_Owner_Search_Domain_RGBs='|'.join(domain),
            Mapping_Status=status,Evidence_Source_IDs=r['Source_IDs'],Historical_Conclusion=r['Historical_Conclusion'],
            Geographic_Proof_Artifact=artifact,Mapping_Method='EXACT_PIXEL_INDEX_AND_HUB_SCOPE; NO_HISTORICAL_OVERLAY',
            Mapping_Confidence='UNRESOLVED_HISTORICAL_EXTENT',Historical_Review_Status=review,
            Technical_Review_Status='ISSUES_PRESENT' if relevant_issues else 'PIXEL_IDS_CHECKED_NOT_ENGINE_TESTED',
            Cross_Region_Review_Status='NOT_REQUIRED' if r['Cross_Region_Conflict']=='NONE' else 'PENDING_DUAL_REGION_REVIEW',
            Decision_Notes=decision,De_Jure_Sovereign=r['De_Jure_Sovereign'],Effective_Controller=r['Effective_Controller'],
            Control_Status=r['Control_Status'],Relationship_Type=r['Relationship_Type'],Gameplay_Approximation=r['Gameplay_Approximation'],
            Proposed_TAG_Registry_Status=tagstatus,Apply_To_Mod='NO',Approved_By_User='NO'))
        question=(notes[p['Case_ID']]['question'] if p else
                  f'Pour {r["Historical_Polity_Name"]} ({sid}), fournir une carte/acte applicable au 1776-01-01 avec localités/cours d’eau repérables autour de {r["Geographic_Location"]}. '+
                  f'Lever cette incertitude : {r["Unresolved_Uncertainty"]}. Distinguer souveraineté, contrôle et autonomie. Identifier les RGB par confrontation des contours, pas par Owner_TAG.')
        doc=['# '+cid+' — '+r['Historical_Polity_Name'],'',
             'Statut : MAPPING_REQUIRED. Pas de province historiquement vérifiée ni de transfert autorisé.','',
             f'[Vue technique de l’État](../MAP1_GEOGRAPHIC_EVIDENCE/STATE_ATLAS/{sid}.svg)','',
             '## Conclusion régionale (non visa central)','',r['Historical_Conclusion'],'',
             'Souveraineté de jure : '+r['De_Jure_Sovereign']+'\n\nContrôle : '+r['Effective_Controller']+'\n\nStatut : '+r['Control_Status'],
             '', '## Localisation et incertitude','',r['Geographic_Location'],'',r['Geographic_Correspondence'],'',r['Unresolved_Uncertainty'],'',
             '## Résultat MAP-1','',decision,'','RGB cités (non vérifiés historiquement) : '+('|'.join(sorted(candidates)) or 'aucun'),
             '', 'Domaine actuel de recherche : '+('|'.join(domain) or 'aucune attribution pour ce couple'),
             '', 'Hubs/locators à confronter : '+json.dumps(locby[sid],ensure_ascii=False),
             '', '## Question ciblée','',question,'','## Sources','']
        for ident in refs:
            s=source[ident]; access=SOURCE_CHECKS.get(ident,('CATALOG_ONLY_NOT_FETCHED','Source non consultée indépendamment.'))
            doc += [f'- {ident} — {s["Author"]}; {s["Title"]}; publication {s["Publication_Date"]}; document {s["Document_Date"]}; {s["Pages_or_Map"]}.',
                    f'  Référence : {s["URL_or_Bibliographic_Reference"]}',f'  Limites : {s["Limitations"]}. Accès : {access[0]}. Compte rendu centralisé dans MAP1_SOURCE_REVIEW.csv.']
        doc += ['', '## Coordination','',r['Cross_Region_Conflict']+' ; région secondaire : '+(r['Secondary_Region_ID'] or 'aucune'),
                '', 'Fiches des autres régions dans le même State_ID : '+('|'.join(x['Change_ID'] for x in counterpart) or 'aucune : rechercher aussi les États voisins'),
                '', '## Méthodes A/B/C et dépendances','',
                'A : tester les polygones actuels après identification historique. B : recomposer/scinder les State Regions si A nécessite des scopes distincts; ne crée pas de polygone plus petit. C : aucune nécessité démontrée, aucune édition autorisée.',
                '', 'Conserver exactement populations par culture/religion, bâtiments/niveaux/PM/propriété économique, formations/recrutement. Auditer capitales, hubs, ports/naval exits, sujets/pactes/traités, journaux/décisions et localisations avant toute proposition intégrable.',
                '', '[Incertitudes régionales originales](../inputs/regional_originals/'+r['Region_ID']+'_UNCERTAINTIES.md)']
        (dossierdir/(cid+'.md')).write_text('\n'.join(doc)+'\n',encoding='utf-8')
        unresolved.append(dict(Record_Type='QUEUE_MAPPING',Change_ID=cid,Region_ID=r['Region_ID'],Secondary_Region_ID=r['Secondary_Region_ID'],
                          State_ID=sid,Cross_Region_Conflict=r['Cross_Region_Conflict'],Mapping_Status=status,
                          Related_Change_IDs='|'.join(x['Change_ID'] for x in counterpart),Source_IDs=r['Source_IDs'],
                          Outstanding_Question=question,Decision='DO_NOT_APPLY',Proof_Artifact=artifact))
    # All 150 cross-region records remain visible, including those outside the queue.
    for r in masters:
        if r['Cross_Region_Conflict']=='NONE': continue
        others=[x for x in bymainstate[r['State_ID']] if x['Region_ID']!=r['Region_ID']]
        unresolved.append(dict(Record_Type='CROSS_REGION',Change_ID=r['Change_ID'],Region_ID=r['Region_ID'],Secondary_Region_ID=r['Secondary_Region_ID'],
                          State_ID=r['State_ID'],Cross_Region_Conflict=r['Cross_Region_Conflict'],Mapping_Status='MAPPING_REQUIRED',
                          Related_Change_IDs='|'.join(x['Change_ID'] for x in others),Source_IDs=r['Source_IDs'],
                          Outstanding_Question=r['Unresolved_Uncertainty']+' Relire les deux côtés de l’interface et publier une décision commune sourcée. '+r['Research_Notes'],
                          Decision='PENDING_DUAL_REGION_REVIEW',Proof_Artifact='inputs/regional_originals/'+r['Region_ID']+'_UNCERTAINTIES.md'))
    assert sum(x['Record_Type']=='CROSS_REGION' for x in unresolved)==150
    savecsv('MAP1_GEOGRAPHIC_MATCHES.csv',matches)
    savecsv('MAP1_UNRESOLVED_AND_CROSS_REGION.csv',unresolved)
    # An empty manifest is intentional: exact pixel identities do not prove historic transfer extents.
    transferfields=['Change_ID','State_ID','Current_Owner_TAG','Proposed_Owner_TAG','Verified_Province_IDs','Mapping_Status',
                    'Historical_Evidence','Geographic_Proof_Artifact','TAG_Registry_Status','Map_Edit_Method','Inventory_Conservation',
                    'Province_Ownership_Dependency','State_Region_Dependency','Pops_Culture_Religion_Dependency','Building_Levels_PMs_Economic_Ownership_Dependency',
                    'Capital_Hubs_Ports_Naval_Exits_Dependency','Formations_Recruitment_Dependency','Subjects_Pacts_Treaties_Dependency',
                    'Journals_Decisions_Localization_Dependency','Apply_To_Mod','Approved_By_User']
    savecsv('MAP1_TRANSFER_PROPOSALS.csv',[],transferfields)
    summary={'Archive_Files':58,'Original_SHA256_PASS':36,'Master_Recommendations':1005,'Source_IDs':374,'Coverage_Unique_Pairs':1043,
             'Queue_Dossiers':len(matches),'State_Atlas_Views':len(viewmeta),'P0_Annotated_Previews':20,'RGB_Unique':40875,
             'Baseline_Attribution_Rows':len(baseline),'Mapping_Verified':0,'Mapping_Proposed':0,'Mapping_Required':410,
             'Transfer_Proposals_Admissible':0,'Cross_Region_Rows':150,'Cross_Region_Disputed':sum(r['Cross_Region_Conflict']=='DISPUTED' for r in masters),
             'Source_Access_Attempts':len(SOURCE_CHECKS),'Source_Catalog_Only':374-len(SOURCE_CHECKS),
             'Runtime_Files_Checked':len(out_before),'Runtime_File_Hashes_Unchanged':protected()==out_before,
             'Historical_Overlay_Count':0,'MAP2_Authorized':False,'Stage':'MAP1_TECHNICAL_ATLAS_COMPLETE_HISTORICAL_MAPPING_OPEN'}
    assert summary['Runtime_File_Hashes_Unchanged']
    (OUT/'MAP1_VALIDATION.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    print(json.dumps(summary,indent=2))

if __name__=='__main__': main()
