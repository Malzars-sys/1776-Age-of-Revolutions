"""Read-only supplemental checks and explicit coverage-geometry PNG."""
import json,csv,collections,math
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from serg_global_closure_audit import ROOT,OUT,save
from serg_closure_delivery import RECEIPTS
from serg_closure_tables import BASE,V,I,P,D,N
import map2l_registry as registry

def run():
    inv=json.loads((OUT/'CURRENT_INVENTORY.json').read_text());colors=json.loads((OUT/'RGB_COUNTS.json').read_text())
    checks=[];byrgb=collections.defaultdict(list)
    for r in inv['owners']:byrgb[r['key'][0]].append(r['key'][1:])
    expected={'xD001A0':['STATE_WALLONIA','BEO'],'x9AC196':['STATE_LOMBARDY','SWI'],'x71E080':['STATE_MORAVIA','AUS'],'xF0E080':['STATE_MORAVIA','AUS'],'x9061E0':['STATE_WEST_GALICIA','AUS']}
    for c,pair in expected.items():checks.append(dict(id='early_'+c,pass_=byrgb[c]==[pair],actual=byrgb[c],expected=pair))
    layers=registry.approved_lot_dirs()
    geos=[json.loads((d/'GEOMETRY.json').read_text()) for d in layers if (d/'GEOMETRY.json').exists()]
    effective=registry.effective_assignments([g for g in geos if g.get('assignments')])
    for r in effective:
        if 'cells' not in r:
            checks.append(dict(id='cardinality_'+r['rgb'],pass_=colors.get(r['rgb'])==r.get('pixels'),actual=colors.get(r['rgb']),expected=r.get('pixels'),note='No original cell list: cardinality/owner checked, not fictitious coordinates'))
    arr=np.asarray(Image.open(ROOT/'map_data/provinces.png').convert('RGB'),dtype=np.uint32);packed=(arr[:,:,0]<<16)|(arr[:,:,1]<<8)|arr[:,:,2]
    belgium=json.loads((ROOT/BASE/'MAP2L/BELGIUM/GEOMETRY.json').read_text())
    for r in belgium['assignments']:
        xy=r['cells'];bad=[(x,y) for x,y in xy if packed[y,x]!=int(r['rgb'][1:],16)]
        checks.append(dict(id='belgium_'+r['rgb'],pass_=not bad and byrgb[r['rgb']]==[[r['state'],r['owner']]],bad_cells=bad))
    for r in registry.approved_territorial_extensions():
        checks.append(dict(id='piedmont_'+r['rgb'],pass_=byrgb[r['rgb']]==[[r['state'],r['beneficiary']]],actual=byrgb[r['rgb']]))
    checks.append(dict(id='Sardinia_not_in_registry',pass_=not any(r['state']=='STATE_SARDINIA' for r in json.loads(registry.active_registry_path().read_text()))))
    checks.append(dict(id='observed_Teschen_registry_gap_documented_not_fixed',pass_=not any(r['rgb']=='x9061E0' for r in json.loads(registry.active_registry_path().read_text())) and colors['x9061E0']==179,note='Coverage finding: MAP2A representation AUS in WEST_GALICIA, absent from registry. PASS confirms observation, not historical correctness or resolution.'))
    facts=json.loads((OUT/'COUNTRY_FACTS.json').read_text())
    checks.append(dict(id='R3_withdrawn_no_HLN_HKI_no_RGB',pass_=not {'HLN','HKI'}&set(facts) and not any(c in colors for c in ('xEDB900','xEDB901','xEDB902','xEDB903')) and not any('/R3' in str(d) and 'MAP2W' in str(d) for d in layers)))
    baseline=json.loads((ROOT/BASE/'MAP2W/R4/POLITICAL_REPRESENTATION/FREISING_REGENSBURG/BASELINE.json').read_text())['inventory']
    checks.append(dict(id='inherited_duplicates_exact',pass_=inv['duplicates']==baseline['duplicates']))
    checks.append(dict(id='inherited_errors_exact',pass_=inv['errors']==baseline['errors']))
    for tag,n in [('FSI',4994),('RBI',4993),('RCI',713),('PAS',14267),('HLB',9206)]:
        actual=sum(p['count'] for p in inv['regional_pop'] if p['key'][1]==tag)
        checks.append(dict(id='population_'+tag,pass_=actual==n,actual=actual,expected=n,note='Written population, not historical certification'))
    save('SUPPLEMENTAL_CHECKS.json',dict(passed=sum(c['pass_'] for c in checks),total=len(checks),checks=checks,engine_run=False))
    draw_map(packed,inv,belgium)
    print('supplemental',sum(c['pass_'] for c in checks),'/',len(checks))

def draw_map(packed,inv,belgium):
    # Pixel support: no projected city point and no inferred historical boundary.
    x0,y0,x1,y1=4100,670,4660,1180; local=packed[y0:y1,x0:x1];h,w=local.shape
    current={r['key'][0]:(r['key'][1],r['key'][2]) for r in inv['owners']}
    reg=json.loads(registry.active_registry_path().read_text());allreg={r['rgb'] for r in reg}
    codes=np.zeros(local.shape,dtype=np.uint8)
    mask=np.isin(local,[int(r[1:],16) for r in allreg]);codes[mask]=1
    # 0 outside technical register; 1 no detailed audit; 2 partial; 3 deferred;
    # 4 installed no manual receipt; 5 inspected correction footprint.
    reviewed={'STATE_'+s for s in 'ANHALT BADEN BAVARIA BRANDENBURG BRUNSWICK ELBE FLANDERS FRANCONIA GELRE HANNOVER HESSE ISTRIA LOMBARDY LOWER_SILESIA MECKLENBURG MORAVIA NORTH_RHINE PIEDMONT POMERANIA RHINELAND RUHR SAXONY SCHLESWIG_HOLSTEIN SOUTH_TYROL UPPER_SILESIA WALLONIA WESTPHALIA WURTTEMBERG'.split()}
    for rgb in allreg:
        if current.get(rgb,('',''))[0] in reviewed:codes[(local==int(rgb[1:],16))&mask]=2
    footprints=[]
    def apply(rows,status,lot,previous=None):
        for r in rows:
            before=r.get('previous_owner',r.get('before_owner',(previous or {}).get(r.get('parent_rgb'))))
            # Unchanged residuals are not promoted to validated by a neighbour.
            if before==r.get('owner'):continue
            rgb=r['rgb']; owner=r.get('owner')
            if current.get(rgb)!= (r.get('state'),owner):continue
            selected=local==int(rgb[1:],16)
            if r.get('cells'):
                selected=np.zeros(local.shape,dtype=bool)
                for x,y in r['cells']:
                    if x0<=x<x1 and y0<=y<y1 and local[y-y0,x-x0]==int(rgb[1:],16):selected[y-y0,x-x0]=True
            if not selected.any():continue
            codes[selected]=status
            footprints.append(dict(lot=lot,rgb=rgb,code=status,displayed_cells=int(selected.sum()),manual_scope='Reported inspected changes; no per-cell user enumeration' if status==5 else 'No scoped receipt'))
    apply(belgium['assignments'],5,'MAP2L/BELGIUM')
    for directory in registry.approved_lot_dirs():
        lot=directory.relative_to(ROOT).as_posix().removeprefix(BASE);m=json.loads((directory/'REGISTRY_MIGRATION.json').read_text())
        previous={r['rgb']:r['beneficiary'] for r in m['previous']}
        status=5 if lot in RECEIPTS else 4
        if (directory/'GEOMETRY.json').exists():
            g=json.loads((directory/'GEOMETRY.json').read_text());apply(g.get('assignments',[]),status,lot,previous)
        # Existing-colour ownership migrations: Emden, Swedish coast, etc.
        for r in m['updated']:
            if r['rgb'] in previous and previous[r['rgb']]!=r['beneficiary'] and current.get(r['rgb'])==(r['state'],r['beneficiary']):
                sel=local==int(r['rgb'][1:],16);codes[sel]=status
                footprints.append(dict(lot=lot,rgb=r['rgb'],code=status,displayed_cells=int(sel.sum()),manual_scope='Changed current RGB only; not whole State_ID'))
    # De jure inclusion is installed but is not a redraw or a manual test.
    for r in registry.approved_territorial_extensions():codes[local==int(r['rgb'][1:],16)]=4
    codes[local==int('D001A0',16)]=4
    codes[local==int('9061E0',16)]=2  # earlier Teschen approximation outside registry
    palette=np.array([[239,242,245],[171,180,190],[233,185,93],[189,137,177],[91,158,207],[77,168,125]],dtype=np.uint8)
    rgb=palette[codes]; yy,xx=np.indices(codes.shape)
    hatch=((xx+yy)%7==0)&np.isin(codes,[1,2,3]);rgb[hatch]=(rgb[hatch].astype(np.float32)*.72).astype(np.uint8)
    edge=np.zeros(local.shape,dtype=bool);edge[1:,:]|=local[1:,:]!=local[:-1,:];edge[:,1:]|=local[:,1:]!=local[:,:-1]
    rgb[edge&mask]=(rgb[edge&mask].astype(np.float32)*.7).astype(np.uint8)
    scale=2;image=Image.new('RGB',(2160,1780),'#f7f5ef');d=ImageDraw.Draw(image)
    font=lambda size:ImageFont.truetype('C:/Windows/Fonts/arial.ttf',size)
    title,fontsub,fontbody,fonttiny=font(38),font(23),font(19),font(16)
    d.text((45,28),'SERG 1776 — couverture des travaux, pas carte des souverainetés',font=title,fill='#17313d')
    d.text((45,85),'Audit du dépôt au 18 octobre 2026 • noyaux, approximations et lacunes distingués',font=fontsub,fill='#344a53')
    px,py=40,180;image.paste(Image.fromarray(rgb).resize((w*scale,h*scale),Image.Resampling.NEAREST),(px,py))
    d.rectangle((px,py,px+w*scale,py+h*scale),outline='#6c7578',width=2)
    labels=json.loads((OUT/'REGIONAL_DATA.json').read_text())
    placements=[];occupied=[]
    # Native state-region centroids locate numbered sector callouts only.
    # These are not estimates of town coordinates.
    for number,r in enumerate(labels,1):
        scopes=r['Regions_techniques'].split(';')
        candidates=[int(rgb[1:],16) for rgb,pair in current.items() if pair[0] in scopes]
        sy,sx=np.nonzero(np.isin(local,candidates)&mask)
        if not len(sx):sy,sx=np.nonzero(np.isin(local,candidates))
        ax,ay=(float(sx.mean()),float(sy.mean())) if len(sx) else (w*.5,h*.5)
        tx,ty=px+ax*scale,py+ay*scale
        selected=None
        for rad in range(0,180,23):
            for angle in np.arange(0,2*math.pi,.55):
                cx=tx+rad*math.cos(angle);cy=ty+rad*math.sin(angle)
                if px+20<=cx<=px+w*scale-20 and py+20<=cy<=py+h*scale-20 and all((cx-a)**2+(cy-b)**2>29**2 for a,b in occupied):
                    selected=(cx,cy);break
            if selected:break
        cx,cy=selected or (tx,ty);occupied.append((cx,cy))
        d.line((tx,ty,cx,cy),fill='#65777c',width=1)
        color={'VALIDÉ EN JEU':tuple(palette[5]),'INSTALLÉ — NON VALIDÉ':tuple(palette[4]),'PARTIELLEMENT TRAITÉ':tuple(palette[2]),'AUDITÉ — BLOQUÉ OU DIFFÉRÉ':tuple(palette[3]),'NON AUDITÉ':tuple(palette[1])}[r['Statut']]
        d.ellipse((cx-14,cy-14,cx+14,cy+14),fill=color,outline='#23373c',width=1)
        text=str(number);bbox=d.textbbox((0,0),text,font=fonttiny);d.text((cx-(bbox[2]-bbox[0])/2,cy-9),text,font=fonttiny,fill='#101b20')
        placements.append(dict(number=number,sector_id=r['ID'],status=r['Statut'],native_sector_centroid=[ax+x0,ay+y0],note='Sector callout, NOT a geographic control or boundary'))
        r['Repere_carte']=number
        lx,ly=1210,150+(number-1)*27
        d.rectangle((lx,ly+3,lx+12,ly+16),fill=color)
        name=r['Secteur'];text=f"{number:02}  {r['ID']}  {name}"
        if len(text)>92:text=text[:89]+'…'
        d.text((lx+23,ly),text,font=fonttiny,fill='#24383d')
    # Legend and explicit semantics below the map.
    y=1240
    for code,label in [(5,'VALIDÉ EN JEU — seules corrections associées à un reçu'),(4,'INSTALLÉ — NON VALIDÉ — pas de reçu spécifique suffisant'),(2,'PARTIELLEMENT TRAITÉ — résidus non certifiés'),(3,'AUDITÉ — BLOQUÉ OU DIFFÉRÉ — repères, pas transferts'),(1,'NON AUDITÉ — pas d’audit territorial détaillé retrouvé')]:
        d.rectangle((45,y+3,73,y+25),fill=tuple(palette[code]),outline='#33464a');d.text((85,y),label,font=fontbody,fill='#25383d');y+=39
    notes=[
      'Les aplats verts ne valident jamais tout un State_ID ou toutes les possessions d’un TAG.',
      'Les hachures préservent les résidus et zones à statut mixte. Les cercles numérotés sont',
      'des repères de secteurs, pas des villes calibrées ni de nouveaux tracés politiques.',
      'Fond clair : hors registre technique actuel, PAS preuve certaine d’exclusion historique.',
      'Le masque de registre n’est pas le périmètre historique complet certifié du SERG.',
      'R4B/C : noyaux validés manuellement; possessions périphériques toujours ouvertes.',
      'Sources et portée : REGIONAL_COVERAGE.csv, COVERAGE_GEOMETRY.json et REPORT.md.']
    for line in notes:d.text((45,y+8),line,font=fonttiny,fill='#45575c');y+=25
    d.text((1210,1640),'Correspondance intégrale des numéros : REGIONAL_COVERAGE.csv',font=fonttiny,fill='#344c55')
    image.save(OUT/'SERG_COVERAGE_MAP.png')
    save('MAP_LABELS.json',placements);save('REGIONAL_DATA.json',labels)
    tables=json.loads((OUT/'TABLE_DATA.json').read_text());tables['REGIONAL_COVERAGE']=labels;save('TABLE_DATA.json',tables)
    save('COVERAGE_GEOMETRY.json',dict(crop=[x0,y0,x1,y1],scale=scale,legend={str(k):v for k,v in enumerate(['outside register','not detailed-audited','partial','deferred callout','installed not validated','inspected correction footprint'])},counts_in_crop=dict(collections.Counter(map(int,codes.ravel()))),footprints=footprints,limitation='Registry technical extent, not a certified historical perimeter; manual receipts do not enumerate every inspected cell; numbered markers show sectors only'))

if __name__=='__main__':run()
