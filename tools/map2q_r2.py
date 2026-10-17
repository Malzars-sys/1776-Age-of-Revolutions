"""MAP-2Q-R2: dated demographic observations, explicit estimates, guarded delta.

The original Q/R1 baselines are never replaced. This module reuses bounded
source retrieval and inventory helpers; no runtime write occurs on import.
"""
import sys,json,math,re,subprocess,os
from pathlib import Path
from collections import Counter
from html.parser import HTMLParser
import map2q_continue as previous

previous.OUT=previous.q.OUT/'CONTINUATION_R2'
q=previous.q
OUT=previous.OUT
POPFILE='common/history/pops/00_west_europe.txt'
TARGET=7600

def read(name):return json.loads((OUT/name).read_text(encoding='utf8'))

def apportion(weights,total):
    """Integer largest remainders; stable input-order tie break, no lost category."""
    denominator=sum(weights);floors=[w*total//denominator for w in weights]
    ranking=sorted(range(len(weights)),key=lambda i:(-(weights[i]*total%denominator),i))
    for i in ranking[:total-sum(floors)]:floors[i]+=1
    assert sum(floors)==total
    return floors

def transformed(raw,target=TARGET):
    region=q.core.region(raw,q.REGION,'HLB');pops=region.children('create_pop')
    sizes=[int(p.one('size')) for p in pops]
    assert sizes==[3424,18,73,183,7446,181],sizes
    # Aggregate equal culture/religion profiles first, then retain their split
    # across the original create_pop blocks without introducing new categories.
    keys=[(p.one('culture'),p.one('religion','DEFAULT')) for p in pops]
    unique=list(dict.fromkeys(keys));weights=[sum(n for k,n in zip(keys,sizes) if k==u) for u in unique]
    totals=apportion(weights,target);result=[0]*len(pops)
    for key,total in zip(unique,totals):
        indices=[i for i,k in enumerate(keys) if k==key]
        for i,n in zip(indices,apportion([sizes[i] for i in indices],total)):result[i]=n
    ops=[(p.children('size')[0].start,p.children('size')[0].end,'size = '+str(n)) for p,n in zip(pops,result)]
    output=q.core.edits(raw,ops)
    return output,[dict(culture=u[0],religion=u[1],before=w,after=n,delta=n-w) for u,w,n in zip(unique,weights,totals)]

def prepare():
    b=read('BASELINE.json')
    assert (q.ROOT/POPFILE).read_text(encoding='utf-8-sig')==b['original_pops']
    raw,profiles=transformed(b['original_pops'])
    previous.dump('EXPECTED_POPULATION.json',dict(target=TARGET,file=POPFILE,text=raw,profiles=profiles,
        policy='Historical estimate overrides fixed world population; no compensation',
        approval='User first chose retention, then explicitly corrected to the other answer: install 7600.'))
    q.core.OUT=OUT
    q.core.emit({POPFILE:raw},'POPULATION.patch')
    # Preserve previous current attestations before publishing their next version.
    for name in ['VALIDATION.json','INSTALLED_MANIFEST.json','TABLE_DATA.json']:
        dest=OUT/('PRE_R2_'+name)
        assert not dest.exists()
        dest.write_bytes((q.OUT/name).read_bytes())
    (OUT/'PRE_R2_VALIDATOR.py').write_bytes((q.ROOT/'tools/map2q_eutin.py').read_bytes())
    print('Prepared only HLB population sizes:',profiles)

def attest_applied():
    expected=read('EXPECTED_POPULATION.json');b=read('BASELINE.json')
    assert (q.ROOT/POPFILE).read_text(encoding='utf-8-sig')==expected['text']
    previous.dump('APPLIED_DEMOGRAPHY.json',dict(lot='MAP2Q_R2',state=q.REGION,tag='HLB',
        before=11325,after=TARGET,delta=TARGET-11325,profiles=expected['profiles'],
        baseline_sha256=q.core.sha(OUT/'BASELINE.json'),file=POPFILE,
        expected_source_sha256=q.core.sha(q.ROOT/POPFILE),confidence='Low; user-accepted historical approximation',
        acceptance='Latest human correction selects install 7600 instead of provisional retention.',
        plausible_interval_people=[6500,9000],not_a_census=True,not_a_statistical_confidence_interval=True))

def estimates():
    counts=read('AGGSH_COUNTS_EXTRACT.json')['tables']
    amt=[int(re.search(r'\d+',r[1])[0]) for r in counts[1:5]]
    assert amt==[2105,2211,2342,412]
    assert sum(int(re.search(r'\d+',r[1])[0]) for r in counts[:-1])==18721
    city_linear=2000+(2283-2000)*(1776-1755)/(1791-1755)
    rural_linear=5218+(sum(amt)-5218)*(1776-1769)/(1819-1769)
    rural_log=5218*(sum(amt)/5218)**((1776-1769)/(1819-1769))
    city_round=round(city_linear);rural_round=TARGET-city_round
    modeled=apportion(amt,rural_round)
    lows=apportion(amt,4500);highs=apportion(amt,6700)
    rows=[]
    def row(sector,kind,year,value,central=None,low=None,high=None,confidence='',scope='',method='',source=''):
        rows.append(dict(Secteur=sector,Nature=kind,Annee=year,Valeur_source_habitants=value,
            Estimation_1776_habitants=central,Borne_basse_habitants=low,Borne_haute_habitants=high,
            Confiance=confidence,Perimetre=scope,Methode=method,Sources=source))
    row('Ville Eutin','Recensement rapporte; arrondi',1755,2000,scope='Ville, pas Amt',source='S1')
    row('Ville Eutin','Denombrement historique rapporte',1791,2283,scope='Ville, pas Amt',source='S2')
    row('Ville Eutin','Reconstruction',1776,None,city_round,2000,2300,'Moyenne sous comparabilite urbaine','Ville seulement','Interpolation lineaire 1755-1791; dates intra-annuelles inconnues','S1;S2')
    row('Amt Eutin','Estimation de Hennings; pas recensement',1769,5218,scope='Amt rural sans ville; densite supposee',source='S5')
    row('Ville Eutin','Denombrement rapporte AGGSH',1819,2686,scope='Stadt Eutin; LAS Abt.260 Nr.10212',source='S3')
    row('Ville Eutin','Denombrement rapporte Kohli',1819,2652,scope='Ville avec maisons sous plusieurs juridictions',source='S4')
    row('Amt Eutin','Denombrement rapporte Kohli',1819,6824,scope='Amt Eutin; ventilation non identique a AGGSH',source='S4')
    for i,name in enumerate(['Stiftsdistrikt','Kirchspieldistrikt','Rothensander Ort','Hof Redingsdorf']):
        row('Amt Eutin - '+name,'Observation 1819; reconstruction 1776 conditionnelle',1819,amt[i],modeled[i],lows[i],highs[i],
            'Faible; ventilation modele non recensee',f'LAS Abt.260 Nr.{10213+i}; couverture raster non certifiee',
            'Poids relatifs 1819 maintenus dans le rural arrondi de 5435; hypothese non observee en 1776','S3;S5')
    row('Amt Eutin - total','Reconstruction; ne pas additionner avec detail',1776,None,rural_round,4500,6700,'Faible',
        'Comparable Amt suppose, sans Schwartau et chapitres','Interpolation geometrique 1769-1819; arrondi global a 7600','S3;S5')
    for name,n in [('Großvogtei',6031),('Collegiatstift',324),('Kaltenhof',2356),('Benz allodial',254)]:
        row(name,'Observe 1819; exclu du calcul central',1819,n,confidence='Estimation 1776 non etablie',
            scope='Autre juridiction ou inclusion exacte dans noyau non verifiee',method='Pas de report automatique dans HLB',source='S3')
    row('Noyau Eutin HLB - total','Estimation acceptee; ne pas sommer les sous-totaux',1776,None,TARGET,6500,9000,'Faible; approximation acceptee',
        '31 cellules figees, equivalent ville et Amt generalise sans certification village par village',
        'Centre arrondi de ville interpolee + Amt interpole; enveloppe de sensibilite non statistique','S1;S2;S3;S5')
    b=read('BASELINE.json');inv=q.core.qa.inventory()
    a=q.core.qa.counter(b['inventory']['regional_pop']);z=q.core.qa.counter(inv['regional_pop'])
    pop=[dict(State_ID=k[0],Pays=k[1],Culture=k[2],Religion=k[3],Avant_habitants=a[k],Apres_habitants=z[k],Variation_habitants=z[k]-a[k])
         for k in sorted(a.keys()|z.keys()) if k[0]==q.REGION and k[1]=='HLB']
    previous.dump('CSV_TABLES.json',{'1776_POPULATION_ESTIMATE.csv':rows,'POPULATION_BEFORE_AFTER.csv':pop})
    world_before=sum(r['count'] for r in b['inventory']['pops']);world_after=sum(r['count'] for r in inv['pops'])
    previous.dump('WORLD_POPULATION_DELTA.json',dict(before_people=world_before,after_people=world_after,
        actual_delta_people=world_after-world_before,justified_expected_delta_people=TARGET-11325,
        local_before_people=11325,local_after_people=sum(r['count'] for r in inv['regional_pop'] if r['key'][1]=='HLB'),
        changed_countries=['HLB'],compensation_elsewhere=False,world_total_is_fixed=False,
        observed_1776_census=False,target_is_user_accepted_estimate=True))
    previous.dump('ESTIMATE_CALCULATIONS.json',dict(city_linear=city_linear,rural_linear=rural_linear,rural_geometric=rural_log,
        total_linear=city_linear+rural_linear,total_geometric=city_linear+rural_log,selected_rounded_total=TARGET,
        city_rounded=city_round,rural_rounded=rural_round,modeled_rural_districts=modeled,
        aggsh_amt_1819=sum(amt),kohli_amt_1819=6824,amt_difference= sum(amt)-6824,
        aggsh_city_1819=2686,kohli_city_1819=2652,city_difference=34,
        hypothetical_total_difference=280,reason_difference='Not resolved from surviving transcriptions; never assert confirmed territorial cause.'))
    print('Calculated estimates and actual before/after tables; world delta',world_after-world_before)

def population_delta_ok(before,after,profiles):
    expected=q.core.qa.counter(before)
    for p in profiles:
        rel=p['religion'] if p['religion']!='DEFAULT' else 'DEFAULT:'+p['culture']
        expected[q.REGION,'HLB',p['culture'],rel]+=p['delta']
    actual=q.core.qa.counter(after)
    return +expected==actual and sum(actual.values())-sum(q.core.qa.counter(before).values())==sum(p['delta'] for p in profiles)

def validate():
    b=read('BASELINE.json');applied=read('APPLIED_DEMOGRAPHY.json');inv=q.core.qa.inventory();expected=read('EXPECTED_POPULATION.json')
    checks=[]
    def check(name,ok,detail=None):
        checks.append(dict(name=name,passed=bool(ok),detail=detail))
        if not ok:print('FAIL',name,detail)
    current=q.economy.runtime_hashes()
    changed=[p for p in b['runtime_hashes'].keys()|current.keys() if b['runtime_hashes'].get(p)!=current.get(p)]
    check('Only HLB population file changed at runtime',changed==[POPFILE],changed)
    generated,profiles=transformed(b['original_pops'])
    check('Only the six declared size tokens changed, including all text outside HLB',generated==(q.ROOT/POPFILE).read_text(encoding='utf-8-sig')==expected['text'])
    check('Approved profiles reconstructed independently of installed text',profiles==applied['profiles'])
    check('All regional demographic differences equal declared HLB delta',population_delta_ok(b['inventory']['regional_pop'],inv['regional_pop'],profiles))
    for key in ['owners','states','state_types','geometry','countries','buildings','building_levels_written','units','errors','duplicates']:
        check('Preserved '+key,inv[key]==b['inventory'][key])
    check('Every cultural and religious category preserved',all(p['before']>0 and p['after']>0 for p in profiles))
    # Largest remainder rounding may move a percentage by less than one person.
    check('Each profile differs from proportional target by less than one person',all(abs(p['after']-p['before']*TARGET/11325)<1 for p in profiles))
    check('Exact 7600 HLB inhabitants',sum(r['count'] for r in inv['regional_pop'] if r['key'][1]=='HLB')==TARGET)
    world=read('WORLD_POPULATION_DELTA.json')
    check('Recomputed world delta, not a fixed global total',world['after_people']==sum(r['count'] for r in inv['pops']) and world['actual_delta_people']==TARGET-11325==world['justified_expected_delta_people'])
    check('Imperial ledger byte-identical',q.core.sha(q.core.active_registry_path())==b['installed_manifest']['registry_sha256'])
    check('Git HEAD preserved',subprocess.check_output(['git','rev-parse','HEAD'],cwd=q.ROOT,text=True).strip()==b['git_head'])
    check('Git index preserved',q.core.sha(q.ROOT/'.git/index')==b['git_index_sha256'])
    modified_artifacts={'docs/reports/map/MAP2Q/'+n for n in ['REPORT.md','HISTORICAL_EVIDENCE.md','NEXT_STEPS.md','VALIDATION.json','INSTALLED_MANIFEST.json','TABLE_DATA.json']}
    changes=[p for p,h in b['earlier_q_artifacts'].items() if not (q.ROOT/p).exists() or q.core.sha(q.ROOT/p)!=h]
    check('Every earlier baseline and evidence preserved',set(changes)<=modified_artifacts,changes)
    for name in ['VALIDATION.json','INSTALLED_MANIFEST.json','TABLE_DATA.json']:
        check('Pre-R2 attestation archived '+name,q.core.sha(OUT/('PRE_R2_'+name))==b['earlier_q_artifacts']['docs/reports/map/MAP2Q/'+name])
    check('Previous validator archived',(OUT/'PRE_R2_VALIDATOR.py').exists())
    qval=json.loads((q.OUT/'VALIDATION.json').read_text(encoding='utf8'))
    check('Cumulative Q checks pass with nonzero historical delta',qval['passed']==qval['total'] and qval['population_world_after']-qval['population_world_before']==TARGET-11325)
    from csv import DictReader
    csvfile=OUT/'POPULATION_BEFORE_AFTER.csv'
    with csvfile.open(encoding='utf-8-sig',newline='') as f:pop=list(DictReader(f))
    check('CSV before/after independently reconciles',sum(int(r['Avant_habitants']) for r in pop)==11325 and sum(int(r['Apres_habitants']) for r in pop)==TARGET and sum(int(r['Variation_habitants']) for r in pop)==-3725)
    model=read('ESTIMATE_CALCULATIONS.json')
    check('AGGSH district sum and discrepancies explicit',model['aggsh_amt_1819']==7070 and model['amt_difference']==246 and model['city_difference']==34)
    check('Original Hennings PDF is genuine PDF, not the failed HTML response',(OUT/'EVIDENCE/HENNINGS_HTTP.pdf').read_bytes().startswith(b'%PDF-') and not (OUT/'EVIDENCE/HENNINGS_1769.pdf').read_bytes().startswith(b'%PDF-'))
    env={**os.environ,'PYTHONPATH':str(q.ROOT/'tools'),'PYTHONDONTWRITEBYTECODE':'1','GIT_OPTIONAL_LOCKS':'0'}
    command=[sys.executable,'-B','-X','utf8','-m','unittest','test_map2q_eutin','test_map2q_r2']
    test=subprocess.run(command,cwd=q.ROOT,env=env,capture_output=True,text=True,encoding='utf8',errors='replace')
    check('Targeted replay and negative demographic tests',test.returncode==0,test.stdout+test.stderr)
    previous.dump('VALIDATION.json',dict(status='MAP2Q_R2_ESTIMATE_INSTALLED_STATIC_PASS' if all(c['passed'] for c in checks) else 'MAP2Q_R2_STATIC_FAILURE',
        passed=sum(c['passed'] for c in checks),total=len(checks),checks=checks,runtime_test='NOT_RUN; fresh game user validation pending',
        historical_accuracy='Approximation accepted by user; no claim of a census or village-exact territorial coverage',
        world_population=world,unit_command=command,preexisting_duplicate_RGBs=len(inv['duplicates']),preexisting_reference_errors=len(inv['errors'])))
    print(test.stdout+test.stderr);print(sum(c['passed'] for c in checks),'/',len(checks),'R2 checks')
    if not all(c['passed'] for c in checks):raise SystemExit(1)

def read_sources():
    class Main(HTMLParser):
        def __init__(self):super().__init__();self.active=False;self.bits=[];self.rows=[];self.row=None;self.cell=None
        def handle_starttag(self,tag,attrs):
            if tag=='main':self.active=True
            if not self.active:return
            if tag=='tr':self.row=[]
            if tag in ['td','th']:self.cell=[]
        def handle_endtag(self,tag):
            if tag=='main':self.active=False
            if not self.active:return
            if tag in ['td','th'] and self.cell is not None:
                self.row.append(' '.join(' '.join(self.cell).split()));self.cell=None
            if tag=='tr' and self.row is not None:self.rows.append(self.row);self.row=None
        def handle_data(self,data):
            if self.active:self.bits.append(data)
            if self.active and self.cell is not None:self.cell.append(data)
    for name in ['AGGSH_COUNTS','AGGSH_HISTORY','AGGSH_PLACES']:
        p=Main();p.feed((previous.OUT/'EVIDENCE'/(name+'.html')).read_text(encoding='utf8'))
        text=' '.join(' '.join(p.bits).split())
        previous.dump(name+'_EXTRACT.json',dict(text=text,tables=p.rows))
        print(name,text)

if __name__=='__main__':
    previous.OUT.mkdir(parents=True,exist_ok=True)
    (globals().get(sys.argv[1]) or getattr(previous,sys.argv[1]))()
