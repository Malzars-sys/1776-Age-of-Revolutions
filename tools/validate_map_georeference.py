"""Retained-source, model comparison and HTTP diagnostics, never game edits."""
import argparse
import csv
import io
import json
import re
import time
import zipfile
from urllib.request import Request,urlopen
from urllib.error import HTTPError
import numpy as np
from PIL import Image
from georeference.model import KINDS,fit,evaluate,forward,inverse
from map_georeference import ROOT,ASSETS,DEFAULT,GAME,digest,load,output_path,render_grid

OUT=ROOT/'docs/reports/map/MAP2L/GEOREFERENCE_PROTOTYPE'

def source_check(rows):
    catalogue=ROOT/'docs/reports/map/MAP1/MAP1_HUB_LOCATOR_CHECKS.csv'
    archive=ROOT/'docs/reports/map/MAP1C/MAP1C_GEOGRAPHIC_EVIDENCE/cities1000.zip'
    records=list(csv.DictReader(catalogue.open(encoding='utf-8-sig')))
    ids={str(r['geonames_id']) for r in rows if 'geonames_id' in r};geo={}
    with zipfile.ZipFile(archive) as z:
        with z.open('cities1000.txt') as file:
            for raw in file:
                fields=raw.decode('utf-8').rstrip().split('\t')
                if fields[0] in ids:geo[fields[0]]=[float(fields[5]),float(fields[4])]
    verified=[]
    for row in rows:
        if row.get('pixel') is None:continue
        match=[r for r in records if r['Hub_Type']=='city' and abs(float(r['Locator_X'])-row['pixel'][0])<.0001 and abs(float(r['Locator_Y'])-row['pixel'][1])<.0001]
        expected=geo.get(str(row['geonames_id']))
        if len(match)!=1 or expected is None or not np.allclose(expected,row['geo'],atol=1e-7,rtol=0):
            raise ValueError('Repère non vérifié dans les sources retenues : '+row['name']+' '+str(expected))
        verified.append({'name':row['name'],'geonames_id':row['geonames_id'],'hub':match[0]['Hub_Name'],
            'source_file':match[0]['Source'],'catalogue_line':records.index(match[0])+2,'expected_rgb':match[0]['Locator_Sampled_RGB']})
    return {'verified':verified,'geonames_archive_sha256':digest(archive),'hub_catalogue_sha256':digest(catalogue)}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--port',type=int);args=parser.parse_args()
    start=time.perf_counter();rows=load(DEFAULT)['controls'];sources=source_check(rows)
    protected=[ROOT/'map_data/provinces.png',ROOT/'common/history/states/00_states.txt',
        ROOT/'common/history/pops/00_west_europe.txt',ROOT/'common/history/buildings/00_west_europe.txt',
        ROOT/'docs/reports/map/MAP2L/IMPERIAL_DE_JURE_REGISTRY.json']
    hashes={p.relative_to(ROOT).as_posix():digest(p) for p in protected}
    assert hashes['map_data/provinces.png']==digest(ROOT/'docs/reports/map/MAP2L/MILAN_CREMONESE/provinces_candidate.png')
    models=[]
    for kind in KINDS:
        model=fit(rows,kind);ev=evaluate(model);result={'model':model,'evaluation':ev}
        output_path(OUT/(kind+'.json')).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
        models.append({'kind':kind,'fit':ev['fit'],'check':ev['check'],'local_check':ev['local_check'],
            'accuracy_status':ev['accuracy_status'],'targets':[p for p in ev['points'] if p['role']=='TARGET']})
    targets=[]
    for i,row in enumerate(rows[:3]):
        pts=np.array([m['targets'][i]['predicted_pixel'] for m in models[:3]])
        targets.append({'name':row['name'],'empirical_prediction_range_xy':np.ptp(pts,axis=0).tolist(),
            'maximum_model_pair_distance_px':max(float(np.linalg.norm(a-b)) for a in pts for b in pts),
            'note':'Désaccord entre modèles, PAS marge d’erreur géographique.'})
    png=output_path(OUT/'grille_locale_0p5deg.png');render_grid(fit(rows),.5).save(png)
    with Image.open(png) as im:
        assert im.size==(8192,3616) and im.mode=='RGBA' and im.getpixel((0,0))[3]==0
    http=[]
    if args.port:
        base='http://127.0.0.1:'+str(args.port)
        def post(path,payload):
            req=Request(base+path,data=json.dumps(payload).encode(),headers={'Content-Type':'application/json','Origin':base})
            with urlopen(req,timeout=20) as response:return response.status,response.read()
        with urlopen(base+'/api/session',timeout=10) as r:session=json.load(r)
        assert session['bitmap_sha256']==hashes['map_data/provinces.png'];http.append('session_hash_PASS')
        status,data=post('/api/fit',{'controls':rows,'spacing':.5});assert status==200;http.append('fit_PASS')
        status,data=post('/api/convert',{'controls':rows,'point':rows[0]['geo']});p=json.loads(data)['result']
        status,data=post('/api/convert',{'controls':rows,'point':p,'direction':'pixel_to_geo'})
        assert np.allclose(json.loads(data)['result'],rows[0]['geo'],atol=1e-9,rtol=0);http.append('conversion_roundtrip_PASS')
        status,data=post('/api/export',{'controls':rows,'spacing':.5})
        with Image.open(io.BytesIO(data)) as im:assert im.size==(8192,3616) and im.mode=='RGBA'
        http.append('transparent_export_PASS')
        for payload in [{'controls':[{}]},{'controls':rows,'spacing':0}]:
            try:post('/api/fit',payload);raise AssertionError('Expected 400')
            except HTTPError as e:assert e.code==400
        http.append('invalid_requests_400_PASS')
        with urlopen(base+'/api/bitmap?box=4280,780,4420,865',timeout=10) as r:
            with Image.open(io.BytesIO(r.read())) as im:assert im.size==(140,85)
        http.append('crop_PASS')
    after={p.relative_to(ROOT).as_posix():digest(p) for p in protected};assert hashes==after
    report={'status':'PROTOTYPE_TECHNICAL_PASS_GEOGRAPHIC_ACCURACY_NOT_ESTABLISHED','models':models,
        'targets_model_disagreement':targets,'sources':sources,'protected_hashes_unchanged':after,'http_tests':http,
        'native_equator':{'file':str(GAME/'common/defines/00_graphics.txt'),'line':227,'fraction':.58,'y':2097.28,
            'qualification':'Repère graphique officiel ; longitude origine et projection exacte non établies.'},
        'elapsed_seconds':time.perf_counter()-start,'colgrep_agent_calls':1,
        'colgrep_timing_seconds':None,'codex_token_count':None,'exact_quota_saving':None}
    output_path(OUT/'VALIDATION.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'status':report['status'],'http':http,'sources_verified':len(sources['verified']),
        'models':[{k:m[k] for k in ['kind','fit','check']} for m in models],'targets':targets},ensure_ascii=False,indent=2))

if __name__=='__main__':main()
