"""Validate report structure, exact geometry reconstruction and runtime preservation."""
import collections as C
import base64,csv,gzip,hashlib,html,io,json,re,subprocess
import xml.etree.ElementTree as ET
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from map1_prepare import ROOT,OUT,INPUT,GAME,EXPECTED,table,savecsv,protected,digest

def main():
    baseline=table(OUT/'MAP1_BASELINE_PROVINCE_INDEX.csv')
    matches=table(OUT/'MAP1_GEOGRAPHIC_MATCHES.csv')
    priorities=table(INPUT/'map1_outputs/MAP1_PRIORITY_ARBITRATION.csv')
    originals=table(OUT/'MAP1_ORIGINAL_SHA256_CHECKS.csv')
    assert len(originals)==36 and all(r['Check']=='PASS' and digest(INPUT/'regional_originals'/r['Filename'])==r['SHA256'] for r in originals)
    assert len(baseline)==40928 and len({r['Province_ID'] for r in baseline})==40875
    assert len(matches)==len({r['Change_ID'] for r in matches})==410
    assert all(r['Apply_To_Mod']=='NO' and r['Approved_By_User']=='NO' for r in matches)
    assert all(r['Mapping_Status']=='MAPPING_REQUIRED' and not r['Verified_Province_IDs'] for r in matches)
    assert not table(OUT/'MAP1_TRANSFER_PROPOSALS.csv')
    assert len(table(OUT/'MAP1_TRANSFER_CANDIDATES_NOT_ADMISSIBLE.csv'))==80
    required=['MAP1_BASELINE_PROVINCE_INDEX.csv','MAP1_GEOGRAPHIC_MATCHES.csv','MAP1_TRANSFER_PROPOSALS.csv',
      'MAP1_UNRESOLVED_AND_CROSS_REGION.csv','MAP1_COLLABORATOR_MERGE_DECISIONS.md','MAP1_RELEASE_GATES.md','MAP1_EXECUTIVE_SUMMARY.md']
    assert all((OUT/p).exists() for p in required)
    assert all((OUT/r['Geographic_Proof_Artifact']).exists() for r in matches)
    evidence=OUT/'MAP1_GEOGRAPHIC_EVIDENCE'
    svgs=list((evidence/'STATE_ATLAS').glob('*.svg')); assert len(svgs)==300
    for p in svgs:
        root=ET.parse(p).getroot()
        node=root.find('{http://www.w3.org/2000/svg}image')
        png=Image.open(io.BytesIO(base64.b64decode(node.attrib['href'].split(',',1)[1])))
        assert png.width and png.height
    # Rebuild every color in a fresh array from saved half-open row runs.
    reconstructed=np.full((3616,8192),0xffffffff,dtype=np.uint32)
    counts={}; overlaps=0
    with gzip.open(evidence/'PROVINCE_PIXEL_RUNS.jsonl.gz','rt',encoding='utf-8') as f:
        for line in f:
            row=json.loads(line)
            rgb=row.get('Province_ID'); runs=row.get('runs_y_x0_x1_exclusive')
            if runs is None: raise AssertionError('Unexpected geometry schema: '+str(list(row)))
            value=int(rgb[1:],16); count=0
            for y,x0,x1 in runs:
                assert 0<=y<3616 and 0<=x0<x1<=8192
                assert np.all(reconstructed[y,x0:x1]==0xffffffff),'Overlapping runs'
                reconstructed[y,x0:x1]=value; count+=x1-x0
            counts[rgb]=count
    actual=np.array(Image.open(GAME/'map_data/provinces.png').convert('RGB'),dtype=np.uint32)
    actual=(actual[:,:,0]<<16)|(actual[:,:,1]<<8)|actual[:,:,2]
    assert np.array_equal(actual,reconstructed)
    assert all(counts[r['Province_ID']]==int(r['Province_Pixels']) for r in baseline)
    # Responsive, local navigation only; no network scripts, mutation or transfer command.
    escape=html.escape
    intro='''<!doctype html><html lang="fr"><meta charset="utf-8"><title>MAP-1 — Revue</title>
<style>body{font:16px/1.5 Arial;max-width:1200px;margin:30px auto;padding:0 20px;color:#213345}a{color:#15538a}input{width:95%;padding:12px;font:inherit}table{border-collapse:collapse;width:100%}th,td{padding:10px;text-align:left;border-bottom:1px solid #ccd4da}th{background:#edf1f4;position:sticky;top:0}.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(330px,1fr));gap:18px}.cards img{width:100%}.warning{border-left:5px solid #a24724;padding:12px;background:#fff3ec}</style>
<h1>MAP-1 — Atlas technique et recherches ouvertes</h1><p class="warning">0 mapping historique vérifié. 410 dossiers en attente. Aucun transfert admissible. Ces cartes représentent le bitmap actuel, pas un tracé de frontières historiques validé. Aucune modification du jeu.</p>
<p><a href="MAP1_EXECUTIVE_SUMMARY.md">Synthèse</a> · <a href="MAP1_COLLABORATOR_MERGE_DECISIONS.md">Collaborateur</a> · <a href="MAP1_RELEASE_GATES.md">Barrières MAP-2</a> · <a href="MAP1_GEOGRAPHIC_MATCHES.csv">Correspondances CSV</a></p><h2>20 priorités</h2><div class="cards">'''
    cards=[]
    for p in priorities:
        ident=p['Case_ID']; stem='MAP1_GEOGRAPHIC_EVIDENCE/'+ident
        assert Image.open(OUT/(stem+'.png')).size==(1700,1120)
        cards.append(f'<article><h3>{escape(ident)} — {escape(p["Issue"])}</h3><a href="{stem}.png"><img src="{stem}.png" alt="{escape(p["Issue"])}"></a><p><a href="{stem}.md">Sources et questions</a> · <a href="MAP1_GEOGRAPHIC_EVIDENCE/STATE_ATLAS/{ident}.svg">RGB zoomables</a></p></article>')
    rows=[]
    for r in matches:
        rows.append('<tr>'+f'<td><a href="{r["Geographic_Proof_Artifact"]}">{escape(r["Change_ID"])}</a></td><td>{escape(r["State_ID"])}</td><td>{escape(r["Research_Current_Owner_TAG"])}</td><td>{escape(r["Research_Proposed_Owner_TAG"])}</td><td><a href="MAP1_GEOGRAPHIC_EVIDENCE/STATE_ATLAS/{r["State_ID"]}.svg">Vue technique</a></td></tr>')
    tail='''</div><h2>410 dossiers</h2><p>Filtrer par Change_ID, State_ID ou TAG. Les TAG sont ceux de la recherche, pas des propriétaires approuvés.</p><input id="search" placeholder="Rechercher…" aria-label="Filtrer les dossiers"><table><thead><tr><th>Dossier</th><th>État</th><th>Actuel</th><th>Proposé par recherche</th><th>Carte</th></tr></thead><tbody>'''
    end='''</tbody></table><script>document.getElementById('search').addEventListener('input',function(){const q=this.value.toLowerCase();document.querySelectorAll('tbody tr').forEach(r=>r.hidden=!r.textContent.toLowerCase().includes(q));});</script></html>'''
    (OUT/'MAP1_REVIEW_INDEX.html').write_text(intro+''.join(cards)+tail+''.join(rows)+end,encoding='utf-8')
    sheet=Image.new('RGB',(1800,1480),'white'); d=ImageDraw.Draw(sheet); font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',18)
    for ix,p in enumerate(priorities):
        x=(ix%4)*450; y=(ix//4)*296
        im=Image.open(evidence/(p['Case_ID']+'.png')); im.thumbnail((440,260))
        sheet.paste(im,(x,y+28)); d.text((x+8,y+4),p['Case_ID'],font=font,fill='#213345')
    sheet.save(evidence/'P0_CONTACT_SHEET.png')
    hashes=protected(); before=json.loads((OUT/'MAP1_RUNTIME_BEFORE.json').read_text())
    assert hashes==before
    assert digest(GAME/'map_data/provinces.png')==EXPECTED
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    assert head=='c891b1d9bb2a21bc42409acbdccc268518110260'
    result=dict(Required_Deliverables_Present=True,Original_Files_Checked=len(originals),
       Geometry_Run_Reconstruction_Exact=True,All_Attribution_Pixel_Counts_Match=True,SVG_Parsed=300,
       P0_PNG_Checked=20,Queue_Artifact_Links_Checked=410,Historical_Polygons_Verified=0,Transfers_Admissible=0,
       Runtime_Files_Unchanged=len(hashes),HEAD=head,In_Game_Test='NOT_RUN')
    (OUT/'MAP1_FINAL_CHECK.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    manifest=[]
    for p in sorted(OUT.rglob('*')):
        if p.is_file() and p.name!='MAP1_DELIVERABLE_HASHES.csv':
            manifest.append(dict(File=p.relative_to(OUT).as_posix(),Bytes=p.stat().st_size,SHA256=digest(p)))
    savecsv('MAP1_DELIVERABLE_HASHES.csv',manifest)
    print(json.dumps(result,indent=2))
if __name__=='__main__': main()
