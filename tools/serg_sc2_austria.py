"""Bounded Austria audit; no installer when historical-to-bitmap mapping is unresolved."""
import collections as C
import json
import subprocess
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import serg_sc2_austrian_silesia as prior
import serg_closure_roadmap as rm

ROOT=prior.ROOT
OUT=ROOT/'docs/reports/map/SERG_CLOSURE/SC2-AUSTRIA'
TASK='SC2-AUSTRIA'
CONCURRENT=prior.CONCURRENT | {
    'common/building_groups/1776_land_fortifications.txt',
    'common/buildings/1776_land_fortifications.txt',
    'common/modifier_type_definitions/1776_land_fortification_construction.txt',
    'common/on_actions/1776_land_fortification_construction.txt',
    'common/script_values/1776_land_fortification_construction.txt',
    'common/scripted_effects/1776_land_fortification_construction.txt',
    'common/scripted_triggers/1776_land_fortification_construction.txt',
    'common/static_modifiers/1776_land_fortification_construction.txt',
    'localization/english/1776_land_fortification_construction_l_english.yml',
    'localization/french/1776_land_fortification_construction_l_french.yml',
}


def load(p):return prior.load(p)
def dump(name,obj):(OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf8')


def inventory():
    b=load(OUT/'BASELINE.json');inv=b['inventory'];a=prior.prior.core.packed(ROOT/'map_data/provinces.png')
    own={r['key'][0]:r['key'][1:] for r in inv['owners']};rows=[];reg={r['rgb']:r for r in b['registry']}
    for k,sid in inv['geometry'].items():
        if sid!='STATE_AUSTRIA':continue
        y,x=np.where(a==int(k[1:],16));contacts=C.Counter()
        for yy,xx in zip(y,x):
            for dy,dx in [(0,1),(0,-1),(1,0),(-1,0)]:
                q='x'+format(int(a[yy+dy,xx+dx]),'06X')
                if q!=k:contacts[q]+=1
        rows.append(dict(rgb=k,state_before=sid,state_after=sid,owner_before=own[k][1],owner_after=own[k][1],cells_before=len(x),cells_after=len(x),bounds=[int(x.min()),int(y.min()),int(x.max()),int(y.max())],centroid=[float(x.mean()),float(y.mean())],registry=reg.get(k),neighbors=[dict(rgb=q,state=own.get(q,['',''])[0],owner=own.get(q,['',''])[1],edges=n) for q,n in sorted(contacts.items())],historical_mapping='WESTERN_SCOPE_UNRESOLVED' if k=='xFDA6CB' else 'RETAINED_MACRO_ENVELOPE_NOT_CADASTRE'))
    rows.sort(key=lambda r:r['rgb'])
    for i,row in enumerate(rows,1):row['map_number']=i
    pop=[r for r in inv['regional_pop'] if r['key'][0]=='STATE_AUSTRIA']
    buildings=[r for r in inv['buildings'] if r['key'][0]=='STATE_AUSTRIA'];units=[r for r in inv['units'] if r['key'][2]=='STATE_AUSTRIA']
    dump('NATIVE_INVENTORY.json',dict(task_ids=[TASK],state_id=51,provinces=rows,total_cells=sum(r['cells_before'] for r in rows),total_population=sum(r['count'] for r in pop),population_groups=pop,building_declarations=buildings,units=units,cadastral_precision=False))
    dump('BOUNDARY_AUDIT.json',dict(task_ids=[TASK],provinces=rows,before_after_equal=True,runtime_changes=0,known_historical_issue='Innviertel remained Bavarian before 1779; installed western AUS polygon is a candidate scope, not a demonstrated exact Innviertel boundary',unresolved_mapping=['Innviertel/Hausruck','Salzburg peripheral interfaces','Passau Obernberg/Vichtenstein'],excluded_completion=['SC1-PASSAU-OUTLIERS','SC2-INNER-AUSTRIA','SC2-TESCHEN']))
    # Technical view with native river pixels; numbered polygons are not towns.
    x0,y0,x1,y1=4380,885,4490,940;scale=9
    im=Image.new('RGB',((x1-x0)*scale+90,(y1-y0)*scale+115),'#faf8ef');d=ImageDraw.Draw(im);f=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',13)
    rivers=np.array(Image.open(ROOT/'map_data/rivers.png'))
    for y in range(y0,y1):
        for x in range(x0,x1):
            rgb='x'+format(int(a[y,x]),'06X');tag=own.get(rgb,['',''])[1]
            col={'AUS':'#c8d6c0','BAV':'#e3d1a6','SLZ':'#d7ae60','PAS':'#cba6ce'}.get(tag,'#d2d6e5')
            if rgb=='xFDA6CB':col='#e4a79c'
            u,v=45+(x-x0)*scale,50+(y-y0)*scale
            d.rectangle((u,v,u+scale,v+scale),fill=col)
            if rivers[y,x]<=15:d.rectangle((u+3,v+3,u+5,v+5),fill='#197aba')
            if a[y,x]!=a[y,x-1]:d.line((u,v,u,v+scale),fill='#85827c')
            if a[y,x]!=a[y-1,x]:d.line((u,v,u+scale,v),fill='#85827c')
    for r in rows:
        x,y=r['centroid'];d.text((45+(x-x0)*scale,50+(y-y0)*scale),str(r['map_number']),font=f,fill='black',stroke_width=1,stroke_fill='white')
    for x,y,label in [(4471.257,915.264,'Vienne'),(4421.306,912.063,'Linz'),(4429.927,904.642,'Freistadt')]:
        u,v=45+(x-x0)*scale,50+(y-y0)*scale;d.ellipse((u-3,v-3,u+3,v+3),fill='#152d35');d.text((u+4,v+2),label+' (jeu)',font=f,fill='black',stroke_width=1,stroke_fill='white')
    d.text((12,10),'SC2-AUSTRIA : inventaire natif, numéros RGB; aucune frontière nouvelle',font=f,fill='black')
    d.text((12,im.height-43),'Rouge : xFDA6CB AUS, périmètre historique non résolu. Bleu ponctuel : rivières natives.',font=f,fill='black')
    d.text((12,im.height-22),'Les marqueurs nommés sont des locators du jeu, pas une preuve de souveraineté en 1776.',font=f,fill='black')
    im.save(OUT/'NATIVE_READING.png')
    dump('OPTIONS_REVIEW.json',dict(task_ids=[TASK],options=[dict(id='WHOLE_NATIVE_WESTERN_RGB',rgb='xFDA6CB',cells=179,status='REJECTED_FOR_INSTALLATION',reason='No evidence that this full native polygon equals Bavarian Innviertel; cannot exclude the distinct Salzburg, Passau and Austrian interfaces'),dict(id='NEW_SUBDIVISION_OR_SMALL_CORE',status='NOT_DEFINED_OR_INSTALLED',reason='No independently homologated placement excludes neighboring jurisdictions. The old R4 diagnostic has an independent residual 4.674389971210816 pixels and quantization sensitivity 3.4103733316009786–6.003840568577085; it is not an installation profile. No repeated fit/translation or arbitrary rectangle.' )],cadastre_required=False,political_B_allowed=True,blocker='Insufficient correspondence for a defensible political B transfer, not a demand for cadastral perfection',population_transfer=0))
    print(len(rows),'RGB',sum(r['cells_before'] for r in rows),'cells',sum(r['count'] for r in pop),'population',flush=True)


def validate():
    b=load(OUT/'BASELINE.json');session=load(OUT/'SESSION_BEFORE.json');inv=prior.prior.core.qa.inventory();checks=[]
    def ck(n,ok,detail=None):checks.append(dict(name=n,passed=bool(ok),detail=detail))
    for key in inv:ck('Effective inventory unchanged: '+key,inv[key]==b['inventory'][key])
    h=prior.prior.runtime_hashes();changed=sorted(p for p in set(h)|set(b['hashes']) if h.get(p)!=b['hashes'].get(p))
    ck('No territorial runtime edit; only known concurrent work permitted',set(changed)<=CONCURRENT,changed)
    ck('Entire bitmap unchanged',h['map_data/provinces.png']==b['hashes']['map_data/provinces.png'])
    ck('Moravia administration and tested population file retained',all(h[p]==b['hashes'][p] for p in [prior.prior.ADMIN_PATH,prior.prior.prior.POP_PATH]))
    ck('Full 574-row registry unchanged',load(prior.reg.active_registry_path())==b['registry'] and len(b['registry'])==574)
    ck('Current registry chain retained',prior.reg.approved_lot_dirs()[-1]==prior.prior.prior.prior.OUT)
    ck('Eleven Austria RGB and 2523 cells accounted for',len(load(OUT/'NATIVE_INVENTORY.json')['provinces'])==11 and load(OUT/'NATIVE_INVENTORY.json')['total_cells']==2523)
    ck('Austria population remains 1638057',sum(r['count'] for r in inv['regional_pop'] if r['key'][0]=='STATE_AUSTRIA')==1638057)
    s=load(rm.OUT/'ROADMAP_STATE.json');done=rm.qualifications(s)
    ck('All 23 accepted tasks justified',sum(done.values())==23 and all(done[k] for k,v in rm.qualifications(b['roadmap']).items() if v))
    t=next(t for t in s['tasks'] if t['id']=='SC2-AUSTRIAN-SILESIA')
    ck('Silesia approval is NA, never runtime PASS',t['status']=='NOT_APPLICABLE_VERIFIED' and t['runtime_validation']['attestation'] is None and t['runtime_validation']['status']!='PASS_RUNTIME_USER_VALIDATED')
    ck('Teschen still independent',next(t for t in s['tasks'] if t['id']=='SC2-TESCHEN')['status']=='NOT_STARTED')
    ck('No old report or receipt replaced',all(prior.prior.sha(ROOT/p)==digest for p,digest in session['report_hashes'].items() if any('/'+k+'/' in p for k in ['SC1-SALZBURG','SC2-BOHEMIA','SC2-MORAVIA','SC2-AUSTRIAN-SILESIA'])))
    ck('Inherited diagnostics unchanged: 44 duplicate RGB / 12 invalid references',len(inv['duplicates'])==44 and len(inv['errors'])==12)
    ck('Git HEAD branch index unchanged',subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==session['git_head'] and subprocess.check_output(['git','branch','--show-current'],text=True).strip()==session['git_branch'] and prior.prior.sha(ROOT/'.git/index')==session['git_index_sha256'])
    for r in load(OUT/'SOURCE_FILES.json'):ck('Source preserved: '+r['file'],prior.prior.sha(OUT/r['file'])==r['sha256'])
    v=dict(task_ids=[TASK],status='PASS' if all(r['passed'] for r in checks) else 'FAIL',total=len(checks),passed=sum(r['passed'] for r in checks),failed=[r['name'] for r in checks if not r['passed']],checks=checks,historical_completion=False,runtime_installation=False,automated_engine_test=False)
    dump('VALIDATION.json',v);dump('FILES_MODIFIED.json',dict(runtime_files_written_by_this_pass=[],concurrent_runtime_files=changed,concurrent_hashes={p:h.get(p) for p in changed},concurrent_files_not_written_by_this_pass=True));print('Static',v['passed'],'/',v['total'],v['failed'],flush=True);assert not v['failed']


def tests():
    # Same cumulative runner, redirected evidence only; old module globals stay intact.
    import types
    fn=types.FunctionType(prior.tests.__code__,dict(prior.tests.__globals__,OUT=OUT,TASK=TASK,dump=dump))
    fn()


def tracking():
    import copy
    v=load(OUT/'VALIDATION.json');assert v['status']=='PASS' and v['passed']==v['total'] and not v['failed']
    assert not load(OUT/'TESTS.json')['unexplained_failures'] and not load(OUT/'SCOPED_TESTS.json')['failed']
    state=load(rm.OUT/'ROADMAP_STATE.json');original=copy.deepcopy(state)
    assert state==load(OUT/'BASELINE.json')['roadmap'],'Concurrent tracker change requires review'
    t=next(t for t in state['tasks'] if t['id']==TASK);assert t['status']=='NOT_STARTED' and rm.progress(state)['next_task']==TASK
    p='docs/reports/map/SERG_CLOSURE/SC2-AUSTRIA/'
    reason="Innviertel encore bavarois en 1776, acquis par l'Autriche en 1779; correspondance suffisante au bitmap non démontrée pour distinguer la portion à transférer des interfaces Salzbourg/Passau/Hausruck. Nouveau périmètre politique B étayé ou contrôle indépendant requis; pas de reprise du calage R4 non homologué."
    t.update(status='BLOCKED',blocking_reason=reason,implementation_report=[p+'REPORT.md'],installed_lots=[],static_tests=dict(status='PASS',evidence=[p+'VALIDATION.json']),
        runtime_validation=dict(required=False,status='NOT_RUN',attestation=None,scope='No new functional installation. Optional conservation protocol does not resolve the historical mapping blocker.',new_details_invented=False),
        decision=dict(classification='HISTORICAL_GAP_PROVED_MAPPING_UNRESOLVED',no_correction_required=False,approved_by=None,reason=reason,evidence=[p+'SOURCES.md',p+'SECTOR_AUDIT.md',p+'OPTIONS_REVIEW.json',p+'BOUNDARY_AUDIT.json']),
        residual_uncertainty="P0 de couverture non clos : limites Innviertel/Hausruck et interfaces Salzburg/Passau non homologuées au bitmap, même pour un transfert politique B. Onze RGB/2523 cellules conservés; aucun cadastre, transfert ou point Autriche acquis. Ne pas confondre conservation technique avec conformité historique.",
        current_delivery_note="Audit AU-N/E/S/W/P/I/D livré, 11 RGB/2523 cellules et 1638057 habitants conservés. La cession de 1779 établit le problème Innviertel, mais ni RGB entier ni petit noyau non positionné indépendamment ne sont installés. P0 BLOCKED, aucun report approuvé ni crédit; tests de conservation réussis. SC2-INNER-AUSTRIA identifiée, non commencée.")
    t['historical_sources'].append(p+'SOURCES.md:1')
    t['identified_problem'].append('Précision du défaut R02 dans le périmètre existant : Innviertel bavarois avant 1779, correspondance à la portion native à corriger non démontrée')
    state['mission_status']='SC2_AUSTRIA_AUDITED_BLOCKED_MAPPING'
    after=rm.progress(state);assert (after['earned_weight'],after['total_weight'],after['percent'],after['next_task'])==(78,235,'33.19','SC2-INNER-AUSTRIA')
    state['events'].append(dict(id='SERG-RM-0011',date='2026-10-19',kind='SCOPED_AUDIT_BLOCKED',scope_version=state['scope_version'],source=p+'AUTHORIZATION.md',changes=[dict(task_id=TASK,before='NOT_STARTED',after='BLOCKED')],before_percent='33.19',after_percent='33.19',before_weight=78,after_weight=78,total_weight=235,
        evidence=[p+'REPORT.md',p+'SOURCES.md',p+'OPTIONS_REVIEW.json',p+'BOUNDARY_AUDIT.json',p+'VALIDATION.json',p+'TESTS.json',p+'PLAYER_TEST_PROTOCOL.md'],
        note="Une seule nouvelle étape : SC2-AUSTRIA P0 sans dépendance. Trois cartes anciennes lues, traité original de 1779 et sources institutionnelles confrontés aux onze RGB. Innviertel à résoudre, correspondance territoriale insuffisante pour transfert défendable excluant voisins; aucun RGB entier, rectangle arbitraire ou nouveau calage sur les mêmes points installé. Statut BLOCKED, ni conformité sans correction ni report P0 approuvé. Aucun fichier fonctionnel écrit, données et acquis conservés. 40/40 contrôles statiques; suite cumulative 328/332 avec trois assertions héritées et une exclusion, contrats 71/72 avec une exclusion. Concurrence fortifications/génie préservée; aucun Git écrit. 78/235 = 33,19 % maintenus. Prochaine candidate SC2-INNER-AUSTRIA non commencée; un test moteur de conservation ne résout pas le blocage cartographique."))
    assert state['events'][:-1]==original['events'] and [t for t in state['tasks'] if t['id']!=TASK]==[t for t in original['tasks'] if t['id']!=TASK]
    assert not rm.structural_errors(state)
    rm.write_json(rm.OUT/'ROADMAP_STATE.json',state);rm.render();check=rm.check();dump('TRACKER_VALIDATION.json',check);assert check['status']=='PASS'
    dump('TRACKER_PRESERVATION.json',dict(other_80_tasks_unchanged=True,all_10_previous_events_unchanged=True,qualified_tasks=23,earned_weight=78,total_weight=235,percent='33.19',austria_credit=False,scope_unchanged=True,next_task='SC2-INNER-AUSTRIA',next_task_started=False))
    print('Tracking PASS; Austria BLOCKED; 78/235=33.19%; next SC2-INNER-AUSTRIA, not started',flush=True)


if __name__=='__main__':{'inventory':inventory,'validate':validate,'tests':tests,'tracking':tracking}[sys.argv[1]]()
