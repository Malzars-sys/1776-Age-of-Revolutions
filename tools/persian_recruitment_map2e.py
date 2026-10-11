"""Focused military-only MAP-2E follow-up. No full snapshot, no game-save writes."""
from pathlib import Path
import collections as C, contextlib, io, json,re,sys,subprocess
import validate_map2a as qa
import validate_diplomacy_ottoman_1776 as cw
import validate_wallonia_start_1776 as w
from map_1776_audit import effective,values
from map2e_work import ROOT,GAME,GIT,sha
OUT=ROOT/'docs/reports/map/MAP2E/PERSIAN_RECRUITMENT_FIX'
PATH='common/history/military_formations/04_military_formations_middle_east.txt'
BASE=OUT/'BASELINE.json'
MOVES={
    'hussars':{'STATE_FARS':1,'STATE_ISFAHAN':3,'STATE_IRAKAJEMI':1,'STATE_LURISTAN':1,'STATE_URMIA':3},
    'irregular_infantry':{'STATE_ISFAHAN':1,'STATE_URMIA':1,'STATE_KERMAN':3,'STATE_MAZANDARAN':3,'STATE_PERSIAN_KURDISTAN':1,'STATE_SEMNAN':1,'STATE_KHORASAN':1},
}
def write(name,data):
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
def hashes():
    return {p.relative_to(ROOT).as_posix():sha(p) for f in ['common','map_data','gfx','events','localization','.metadata','docs/reports/map/MAP2A','docs/reports/map/MAP2B','docs/reports/map/MAP2C','docs/reports/map/MAP2D','docs/reports/map/MAP2E'] for p in (ROOT/f).rglob('*') if p.is_file() and OUT not in p.parents}
def capture():
    assert not BASE.exists(),'Do not replace the pre-fix baseline'
    inv=qa.inventory()
    write('BASELINE.json',{'inventory':inv,'hashes':hashes(),'original':(ROOT/PATH).read_text(encoding='utf-8-sig'),'head':subprocess.check_output([GIT,'rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'refs':subprocess.check_output([GIT,'show-ref'],cwd=ROOT,text=True).strip(),'index':sha(ROOT/'.git/index')})
    print('Lightweight baseline captured; world',sum(r['count'] for r in inv['pops']))
def unit_counts(inv):
    out=C.Counter()
    for r in inv['units']:
        if r['key'][0]!='PER':continue
        attrs={k:v for k,op,v in json.loads(r['key'][3])[2]}
        out[(r['key'][2],attrs.get('service_type','regular'))]+=int(attrs['count'])*r['count']
    return out
def diagnose():
    b=json.loads(BASE.read_text(encoding='utf-8'));inv=b['inventory'];unit=unit_counts(inv)
    regions={s for s,t in inv['states'] if t=='PER'}
    pop=C.Counter();free=C.Counter();primary=C.Counter()
    countries=w.catalog('common/country_definitions');accepted=set(values(countries['PER'],'cultures'))
    for p in effective(ROOT,GAME,'common/history/pops'):
        for s in cw.walk(cw.parse(p.read_text(encoding='utf-8-sig'))):
            if not s.key.startswith('s:STATE_'):continue
            for r in s.children('region_state:PER'):
                for n in r.children('create_pop'):
                    size=int(n.one('size'));sid=s.key[2:];pop[sid]+=size
                    if cw.scalar(n.one('pop_type',''))!='slaves':
                        free[sid]+=size
                        if cw.scalar(n.one('culture')) in accepted:primary[sid]+=size
    bd=w.catalog('common/buildings');bg=w.catalog('common/building_groups');pm=w.catalog('common/production_methods');sr=w.catalog('map_data/state_regions');traits=w.catalog('common/state_traits')
    def usage(group):
        n=bg[group];v=n.one('infrastructure_usage_per_level')
        return float(v) if v is not None else usage(cw.scalar(n.one('parent_group'))) if n.one('parent_group') else 0
    # Keep per-file observations: replicated declarations are not blindly added.
    schedules=C.defaultdict(dict);holders=C.defaultdict(dict)
    for p in effective(ROOT,GAME,'common/history/buildings'):
        local=C.defaultdict(list);hlocal=C.Counter()
        for s in cw.walk(cw.parse(p.read_text(encoding='utf-8-sig'))):
            if not s.key.startswith('s:STATE_'):continue
            sid=s.key[2:]
            for r in s.children():
                if not r.key.startswith('region_state:'):continue
                for node in r.children('create_building'):
                    for h in node.children('add_ownership'):
                        for hh in h.children('building'):
                            if cw.scalar(hh.one('country',''))=='c:PER':hlocal[(cw.scalar(hh.one('region',sid)),cw.scalar(hh.one('type')))]+=int(hh.one('levels',0))
                    if r.key!='region_state:PER' or sid not in regions:continue
                    kind=cw.scalar(node.one('building'));levels=sum(int(n.value) for n in cw.walk(node.children()) if n.key=='levels')
                    levels=int(node.one('level',node.one('levels',levels)))
                    methods=values(node,'activate_production_methods');jobs=0;infra=0
                    for method in methods:
                        if method not in pm:continue
                        jobs+=sum(float(n.value) for n in cw.walk(pm[method].children('building_modifiers')) if re.fullmatch(r'building_employment_.+_add',n.key))
                        infra+=w.infrastructure_per_pm(pm[method])
                    if kind not in bd:
                        if kind=='building_barracks':kind='building_barrack'
                        else:raise ValueError(kind)
                    local[(sid,kind)].append({'levels':levels,'pms':methods,'jobs':jobs*levels,'infra':infra*levels,'usage':usage(cw.scalar(bd[kind].one('building_group')))*levels,'source':p.name})
        for key,rows in local.items():schedules[key][p.name]=rows
        for key,n in hlocal.items():holders[key][p.name]=n
    rows=[]
    for sid in sorted(regions):
        buildings=[r for (s,k),versions in schedules.items() if s==sid for r in versions[sorted(versions)[-1]]]
        civilian=sum(r['usage'] for r in buildings);jobs=sum(r['jobs'] for r in buildings)
        econ=[]
        for (s,k),versions in holders.items():
            if s!=sid or k not in ['building_manor_house','building_financial_district']:continue
            levels=versions[sorted(versions)[-1]];group=cw.scalar(bd[k].one('building_group'));civilian+=usage(group)*levels
            # Actual generated ownership employment/PMs are engine dependent.
            econ.append({'type':k,'levels':levels,'infra_usage':usage(group)*levels})
        trait_add=0;trait_mult=0;trait_names=values(sr[sid],'traits')
        for t in trait_names:
            if t not in traits:continue
            for n in cw.walk(traits[t].children('modifier')):
                if n.key=='state_infrastructure_add':trait_add+=float(n.value)
                if n.key=='state_infrastructure_mult':trait_mult+=float(n.value)
        road=sum(r['infra'] for r in buildings);floor=max(0,(3+road+trait_add)*(1+trait_mult))
        rows.append({'state':sid,'population':pop[sid],'free_population':free[sid],'primary_free_population':primary[sid],'workforce_model_25pct':int(free[sid]*.25),'primary_workforce_model_25pct':int(primary[sid]*.25),'civilian_jobs_explicit_full_capacity':jobs,'regular_before':unit[(sid,'regular')],'conscript_before':unit[(sid,'conscript')],'civilian_usage_model':round(civilian,3),'infrastructure_full_staffing_floor':round(floor,3),'roads_levels':sum(r['levels'] for r in buildings if 'railway' in ''.join(r['pms']) or any(x in r['pms'] for x in ['pm_traditional_road_network','pm_paved_road_network'])),'trait_names':trait_names,'buildings':buildings,'ownership_generated_proxy':econ,'explicit_barracks':[(p,rr) for (s,k),vers in schedules.items() if s==sid and k=='building_barrack' for p,rr in vers.items()]})
    write('CANDIDATES.json',{'rows':rows,'limitations':'Static full-staffing floor, no population/bloc bonus. Last-file per-kind civilian schedule approximates native startup overlay. Generated ownership employment and qualifications not known. Free/primary workforce 25% is a planning model, not observed unemployment. Conscripts counted in separate wartime estimate. No save was decoded.'})
    for r in rows:print(r['state'],r['population'],'freeW',r['workforce_model_25pct'],'jobs',r['civilian_jobs_explicit_full_capacity'],'regular',r['regular_before'],'conscripts',r['conscript_before'],'civilianInfra',r['civilian_usage_model'],'supplyFloor',r['infrastructure_full_staffing_floor'],'balancePeace',round(r['infrastructure_full_staffing_floor']-r['civilian_usage_model']-.2*r['regular_before'],3))
def validate():
    from validate_map2e import unit_totals
    import validate_regional_infrastructure_shortage as infr
    b=json.loads(BASE.read_text(encoding='utf-8'));before=b['inventory'];after=qa.inventory();checks=[]
    def check(name,passed,detail=None):
        checks.append({'test':name,'status':'PASS' if passed else 'FAIL','detail':detail})
    for field in before:
        if field!='units':check('Unchanged inventory: '+field,before[field]==after[field])
    check('Exact world population 835804980',sum(r['count'] for r in after['pops'])==835804980)
    check('All national types, formations and services conserved',unit_totals(before['units'])==unit_totals(after['units']))
    check('All non-Persian recruitment unchanged',[r for r in before['units'] if r['key'][0]!='PER']==[r for r in after['units'] if r['key'][0]!='PER'])
    def conscripts(inv):
        return [r for r in inv['units'] if r['key'][0]=='PER' and any(n[0]=='service_type' and n[2]=='conscript' for n in json.loads(r['key'][3])[2])]
    check('All 38 conscripts unchanged, including the transferred unit',conscripts(before)==conscripts(after))
    expected=unit_totals(before['units'],True)
    for kind,destinations in MOVES.items():
        source=next(k for k in expected if k[0]=='PER' and k[3]=='STATE_TABRIZ' and ('combat_unit_type_'+kind+'"') in k[2] and 'conscript' not in k[2])
        expected[source]-=sum(destinations.values())
        for sid,count in destinations.items():expected[(*source[:3],sid)]+=count
    check('Exactly the authorized 20-unit redistribution',+expected==unit_totals(after['units'],True))
    counts=unit_counts(after)
    check('Tabriz retains five regulars and all six conscripts',counts['STATE_TABRIZ','regular']==5 and counts['STATE_TABRIZ','conscript']==6)
    check('National strength remains 32 regulars and 38 conscripts',sum(v for (s,t),v in counts.items() if t=='regular')==32 and sum(v for (s,t),v in counts.items() if t=='conscript')==38)
    states={tuple(s) for s in after['states']}
    check('All Persian recruiting states are still Persian-owned',all((r['key'][2],'PER') in states for r in after['units'] if r['key'][0]=='PER'))
    def structural(raw):
        def filtered(n):
            if n[0]=='combat_unit':return None
            return [n[0],n[1],[v for child in n[2] if (v:=filtered(child)) is not None]] if isinstance(n[2],list) else n
        return [filtered(qa.norm(n)) for n in cw.parse(raw)]
    check('Commanders, formation names, headquarters and assignments unchanged',structural(b['original'])==structural((ROOT/PATH).read_text(encoding='utf-8-sig')))
    def repeated(inv):
        c=C.Counter()
        for r in inv['units']:
            if r['key'][0]!='PER':continue
            attrs=[n for n in json.loads(r['key'][3])[2] if n[0]!='count']
            c[(r['key'][1],r['key'][2],json.dumps(attrs))]+=r['count']
        return c
    old,new=repeated(before),repeated(after)
    check('No newly duplicated Persian recruitment record',all(n<=max(1,old[k]) for k,n in new.items()))
    current_hashes=hashes();changed=[p for p in b['hashes'] if b['hashes'][p]!=current_hashes.get(p)]
    check('Only one runtime file changed; old MAP reports protected',changed==[PATH],changed)
    check('No new runtime files',not(set(current_hashes)-set(b['hashes'])))
    check('Git HEAD, index and refs untouched',subprocess.check_output([GIT,'rev-parse','HEAD'],cwd=ROOT,text=True).strip()==b['head'] and subprocess.check_output([GIT,'show-ref'],cwd=ROOT,text=True).strip()==b['refs'] and sha(ROOT/'.git/index')==b['index'])
    candidates=json.loads((OUT/'CANDIDATES.json').read_text(encoding='utf-8'))
    check('No explicit Persian barracks added to automatic unit recruitment',all(not r['explicit_barracks'] for r in candidates['rows']) and before['buildings']==after['buildings'])
    groups=w.catalog('common/building_groups');types=w.catalog('common/combat_unit_types')
    military_usage=float(groups['bg_military'].one('infrastructure_usage_per_level'))
    check('Native military infrastructure cost 0.2 per level',military_usage==.2)
    manpower={kind:int(types['combat_unit_type_'+kind].one('max_manpower')) for kind in ['hussars','irregular_infantry','cannon_artillery']}
    check('Every concerned unit has 1000 manpower',set(manpower.values())=={1000},manpower)
    rows=[]
    for r in candidates['rows']:
        r=dict(r);regular=counts[r['state'],'regular'];capacity=r['infrastructure_full_staffing_floor'];civil=r['civilian_usage_model']
        r.update(regular_after=regular,military_jobs_before=r['regular_before']*1000,military_jobs_after=regular*1000,
                 demand_before=round(civil+military_usage*r['regular_before'],3),demand_after=round(civil+military_usage*regular,3),
                 reserve_before=round(capacity-civil-military_usage*r['regular_before'],3),reserve_after=round(capacity-civil-military_usage*regular,3),
                 reserve_with_all_conscripts=round(capacity-civil-military_usage*(regular+r['conscript_before']),3),
                 workforce_model_remaining=round(r['workforce_model_25pct']-r['civilian_jobs_explicit_full_capacity']-regular*1000))
        rows.append(r)
    check('Positive peacetime nominal reserve in every recipient and Tabriz',all(r['reserve_after']>0 for r in rows))
    check('Modeled free workforce exceeds explicit civilian and regular military jobs',all(r['workforce_model_remaining']>0 for r in rows))
    suites={}
    for name,fn in [('Ottoman journals',cw.model_tests),('Infrastructure AI',infr.model_tests)]:
        log=io.StringIO()
        try:
            with contextlib.redirect_stdout(log):answer=fn()
            suites[name]={'status':'PASS','result':answer,'output':log.getvalue()};check(name+' existing fixtures',True)
        except Exception as e:
            suites[name]={'status':'FAIL','error':str(e)};check(name+' existing fixtures',False,str(e))
    result={'status':'PASS_STATIC' if all(r['status']=='PASS' for r in checks) else 'FAIL_STATIC','native_post_fix':'NOT_RUN',
            'user_prior_MAP2E_test':'New game, Caucasus and Russian enclaves load, one month without blocker; prior 25 units in Tabriz confirmed by user',
            'units_relocated':20,'moves':MOVES,'regular_national':32,'conscript_national':38,'checks':checks,'regression_suites':suites,
            'modified_runtime_files':changed,'estimation_limitations':candidates['limitations'],'rows':rows}
    write('VALIDATION.json',result)
    render_report(result)
    print(result['status'],len(checks),'checks')
    for r in checks:
        if r['status']=='FAIL':print('FAIL',r['test'],r['detail'])
    return result['status']=='PASS_STATIC'

def render_report(result):
    names={'FARS':'Fars / Shiraz','IRAKAJEMI':'Irak-Ajemi','ISFAHAN':'Ispahan','KERMAN':'Kerman','KHORASAN':'Khorasan','LARISTAN':'Laristan','LURISTAN':'Luristan','MAZANDARAN':'Mazandéran','PERSIAN_KURDISTAN':'Kurdistan perse','SEMNAN':'Semnan','TABRIZ':'Tabriz','URMIA':'Ourmia'}
    def name(r):return names[r['state'].removeprefix('STATE_')]
    def n(v):return f'{v:,.1f}'.replace(',',' ').rstrip('0').rstrip('.')
    lines=['# MAP-2E — Redistribution finale du recrutement perse', '',
        '## Résultat', '',
        '20 unités déplacées de Tabriz (9 hussards, 11 infanteries irrégulières) vers dix autres États déjà possédés par PER. Tabriz conserve 2 artilleries, 1 hussard et 2 infanteries irrégulières. Les sept infanteries déjà présentes en Irak-Ajemi restent en place.', '',
        'La Perse conserve exactement **32 unités permanentes et 38 unités de conscription**, leurs types, la même formation et son commandant Moḥammad Ṣādeq Khan Zand. Les six conscriptions de Tabriz, dont celle transférée lors de MAP-2E, sont inchangées. Aucun recrutement n’est recréé dans les khanats indépendants.', '',
        'Seul fichier de gameplay modifié : `common/history/military_formations/04_military_formations_middle_east.txt`. Aucun bâtiment explicite de casernes ajouté : les unités créent leur recrutement automatiquement. Aucun niveau de route, bâtiment civil, population, frontière, PM ou accord diplomatique modifié. Aucun commit, merge ou push ; aucune nouvelle archive complète.', '',
        '## Infrastructure : calcul statique, pas observation en jeu', '',
        'Les unités sont comptées à 0,2 infrastructure et 1 000 emplois chacune. La capacité modélisée inclut les routes à plein emploi, la base de 3 et les traits régionaux ; elle exclut les bonus démographiques et de bloc. La demande civile inclut un proxy des bâtiments de propriété générés. Les historiques superposés sont estimés avec la dernière déclaration par type : ce calcul ne remplace pas le chargement natif.', '',
        '« Cons. » indique la capacité inchangée de conscription. La dernière colonne ajoute par prudence la demande de toutes ces unités : ce scénario de stress n’est pas une mesure de la consommation des centres inactifs.', '',
        '| État | Permanentes avant → après | Cons. | Demande totale avant → après | Capacité nominale | Réserve après | Réserve avec toutes les conscriptions |',
        '|---|---:|---:|---:|---:|---:|---:|']
    for r in result['rows']:
        lines.append(f"| {name(r)} | {r['regular_before']} → {r['regular_after']} | {r['conscript_before']} | {n(r['demand_before'])} → {n(r['demand_after'])} | {n(r['infrastructure_full_staffing_floor'])} | {n(r['reserve_after'])} | {n(r['reserve_with_all_conscripts'])} |")
    lines+=['', 'À Tabriz, la demande militaire nominale passe de 5 à 1 : la réserve de paix modélisée passe de −3 à +1. La mobilisation intégrale reste tendue à Tabriz (−0,2), Fars (−0,1) et Irak-Ajemi (−1,4). Les deux derniers sont déjà des centres civils ou militaires chargés : un seul hussard leur est attribué. Aucun accroissement automatique des routes pour masquer ces limites.', '',
        '## Population et personnel', '',
        'Le modèle de main-d’œuvre est **25 % de la population libre**, non une mesure du chômage ni une garantie de qualification ou de recrutement. Les emplois civils explicites sont calculés à pleine capacité ; ils n’incluent pas tous les emplois générés des propriétaires ni la subsistance. Les surplus ci-dessous ne sont donc pas des salariés réellement disponibles.', '',
        '| État | Population inchangée | Modèle travailleurs libres | Emplois civils explicites | Militaires avant → après | Marge modélisée après |',
        '|---|---:|---:|---:|---:|---:|']
    for r in result['rows']:
        lines.append(f"| {name(r)} | {r['population']:,} | {r['workforce_model_25pct']:,} | {int(r['civilian_jobs_explicit_full_capacity']):,} | {r['military_jobs_before']:,} → {r['military_jobs_after']:,} | {int(r['workforce_model_remaining']):,} |".replace(',',' '))
    lines+=['', 'Laristan n’accueille aucune unité supplémentaire : sa population et sa marge de personnel sont faibles. Semnan ne reçoit qu’une infanterie ; Ispahan, Ourmia, Kerman et Mazandéran prennent l’essentiel du complément au transfert initial de dix unités. Aucun habitant libre ou esclave n’est ajouté, retiré ou déplacé.', '',
        '## Justification et limites historiques', '',
        'Répartition administrative de gameplay, pas reconstitution des garnisons : Shiraz est la capitale zand ; Ispahan, Tabriz et Kerman font partie des principaux centres du pouvoir et des alliances provinciales. Le recrutement cavalier est réparti entre ces centres et les régions occidentales plutôt que concentré artificiellement dans l’ancien espace caucasien.', '',
        'Sources : [Zand Dynasty — Encyclopædia Iranica](https://www.iranicaonline.org/articles/zand-dynasty/), [Karim Khan Zand — Encyclopædia Iranica](https://www.iranicaonline.org/articles/karim-khan-zand/).', '',
        'Le Khorasan relève d’une autonomie afsharide historiquement distincte du pouvoir zand. Il reste une région PER dans la carte existante, avec son recrutement de conscription préexistant. L’unique infanterie permanente supplémentaire est une abstraction du pays PER actuel, non l’affirmation d’une garnison zand historiquement démontrée. Ce point territorial reste hors du présent correctif : aucune frontière ni dépendance n’est modifiée.', '',
        '## Validations et protections', '',
        f"Résultat : **{result['status']}**, {len(result['checks'])} contrôles. Conservation mondiale : 835 804 980 habitants. Comparaison avec l’état réellement présent après MAP-2E : tous les propriétaires RGB, populations détaillées, groupes culturels/religieux, statuts libres/esclaves, bâtiments et niveaux, PM, propriétaires économiques, États et pays restent identiques. Seul le recrutement permanent PER prévu diffère. Commandants, formation et quartiers généraux restent identiques. Aucun nouveau doublon ou recrutement orphelin.", '',
        'Empreintes de tous les fichiers de gameplay et des rapports MAP-2A/B/C/D/E contrôlées : seul l’historique militaire ciblé change. Les tests existants des journaux ottomans et des infrastructures IA passent. HEAD, références et index Git inchangés. La baseline légère `BASELINE.json`, le modèle `CANDIDATES.json` et le résultat `VALIDATION.json` rendent le correctif reproductible.', '',
        'Le rapport original MAP2E_VALIDATION.json est conservé comme résultat de l’étape précédente. Son ancien contrôle exigeant toutes les unités transférées à Tabriz est désormais remplacé, pour ce suivi, par la comparaison exacte avec la redistribution autorisée dans `tools/persian_recruitment_map2e.py validate` ; il ne faut pas réécrire la baseline ou présenter cet ancien contrôle comme encore applicable.', '',
        '## Vérifications dans une nouvelle partie', '',
        'Le test natif post-correctif n’a pas été exécuté. L’ancienne autosauvegarde est binaire et n’a pas fourni de chiffres de personnel/infrastructure exploitables ; aucune sauvegarde n’a été altérée.', '',
        '1. Nouvelle partie 1776 : Tabriz doit avoir 5 permanentes et 6 conscriptions ; la Perse entière 32 permanentes et 38 conscriptions.',
        '2. Contrôler Tabriz, puis Fars et Irak-Ajemi : infrastructure utilisée/disponible, emplois des routes, pénuries et accès au marché ; vérifier aussi les autres destinataires après un mois.',
        '3. Confirmer les 4 permanentes d’Ispahan, les 4 d’Ourmia et les 3 de Kerman/Mazandéran ; vérifier la même formation et le même commandant.',
        '4. Confirmer les pays caucasiens, enclaves russes et corrections MAP-2A/B/C/D/E. Un éventuel déficit résiduel devra être distingué d’un défaut de recrutement ou d’une mobilisation ; aucun résultat d’accès au marché à 100 % n’est promis.', '']
    (OUT/'REPORT.md').write_text('\n'.join(lines),encoding='utf-8')

if __name__=='__main__':
    answer={'capture':capture,'diagnose':diagnose,'validate':validate}[sys.argv[1]]()
    if answer is False:raise SystemExit(1)
