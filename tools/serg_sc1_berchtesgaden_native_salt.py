"""User-directed replacement of the special salt establishment with one ordinary mine."""
import contextlib,copy,io,re,shutil,subprocess,sys,unittest
from pathlib import Path
import serg_sc1_berchtesgaden as lot
import serg_sc1_berchtesgaden_salt_fix as cancelled
ROOT=lot.ROOT;rm=lot.rm;core=lot.core;sha=lot.sha;load=lot.load
OUT=lot.OUT/'SALT_NATIVE_R1';PREFIX=OUT.relative_to(ROOT).as_posix()+'/';TASK=lot.TASK
METHODS=['pm_picks_and_shovels_building_salt_mine','pm_no_explosives','pm_no_steam_automation','pm_road_carts','pm_no_salt_processing_building_salt_mine','pm_1776_raw_data_reporting']
PROTOCOL='Nouvelle partie au 1er janvier 1776 : BG-I-CORE, BGT/quatre cellules/1000 habitants, souverain et capitale ; vérifier un niveau de Mines de sel standard dans Ressources, propriété BGT, méthodes ordinaires et recrutement partiel sans exigence de 5000 employés. Aucun bâtiment ou PM spécial du sel. Chancellerie de 100 postes conservée. Vérifier sel et finances, voisins dont SLZ douze cellules, droits impériaux, puis un mois, sauvegarde/rechargement. Aucune validation humaine nouvelle.'
def dump(n,o):rm.write_json(OUT/n,o)

def install():
    assert not (OUT/'BASELINE.json').exists();OUT.mkdir(exist_ok=True)
    b=load(cancelled.OUT/'BASELINE.json');previous=load(cancelled.OUT/'SESSION_AFTER_STATIC.json');now=lot.italian.runtime_hashes();assert now==previous['hashes'],'Concurrent runtime changes require review'
    s=load(rm.OUT/'ROADMAP_STATE.json');assert s==b['roadmap']
    dump('BASELINE.json',dict(roadmap=s,hashes=b['hashes'],inventory=b['inventory'],proofs={p.relative_to(ROOT).as_posix():sha(p) for p in rm.OUT.rglob('*') if p.is_file() and OUT not in p.parents},tools={p.relative_to(ROOT).as_posix():sha(p) for p in (ROOT/'tools').glob('*.py') if p.name!=Path(__file__).name},git=b['git'],intermediate_hashes=now))
    files={};preimages={}
    def read(p):raw=(ROOT/p).read_bytes().decode('utf8');preimages[p]=raw;return raw
    def remove_node(raw,key):
        off=int(raw.startswith('\ufeff'));nodes=[n for n in core.cw.parse(raw.lstrip('\ufeff')) if n.key==key];assert len(nodes)==1;node=nodes[0];return core.edits(raw,[(node.start+off,node.end+off,'')])
    p='common/buildings/1776_sc1_berchtesgaden.txt';files[p]=remove_node(read(p),'building_aor1776_berchtesgaden_saline')
    p='common/production_methods/1776_sc1_berchtesgaden.txt';files[p]=remove_node(read(p),'pm_aor1776_berchtesgaden_saline')
    p='common/production_method_groups/1776_sc1_berchtesgaden.txt';files[p]=remove_node(read(p),'pmg_aor1776_berchtesgaden_saline')
    p='common/history/buildings/1776_sc1_berchtesgaden.txt';raw=read(p);node=core.region(raw,lot.SID,lot.TAG).children('create_building')[1];assert node.one('building')=='"building_aor1776_berchtesgaden_saline"'
    new='create_building = {\n  building = "building_salt_mine"\n  add_ownership = { country = { country = "c:BGT" levels = 1 } }\n  reserves = 1\n  activate_production_methods = { '+ ' '.join('"'+m+'"' for m in METHODS)+' }\n }'
    files[p]=core.edits(raw,[(node.start,node.end,new)])
    for lang in ['french','english']:
        p='localization/'+lang+'/1776_sc1_berchtesgaden_l_'+lang+'.yml';raw=read(p)
        for key in ['building_aor1776_berchtesgaden_saline','building_aor1776_berchtesgaden_saline_desc','pmg_aor1776_berchtesgaden_saline','pm_aor1776_berchtesgaden_saline']:
            raw,n=re.subn(r'(?m)^ '+key+r':0 "[^"\n]*"\r?\n?', '', raw);assert n==1,(p,key)
        files[p]=raw
    # Remove just the intermediate repair, preserving all original naming effects and hooks.
    p='common/scripted_effects/1776_sc1_berchtesgaden.txt';raw=read(p);raw=remove_node(raw,'initialize_aor1776_berchtesgaden_salt');raw=raw.replace('# New-game repair only. Both start hooks may fire; an existing level is never added again.\n','');original=load(cancelled.OUT/'TEXT_BEFORE.json')[p];assert raw.strip()==original.strip();files[p]=raw[:len(original)] if raw.startswith(original) else raw
    p='common/on_actions/99_1776_sc1_berchtesgaden.txt';raw=read(p);raw=remove_node(raw,'aor1776_berchtesgaden_salt_initialize').replace('aor1776_berchtesgaden_names_initialize aor1776_berchtesgaden_salt_initialize','aor1776_berchtesgaden_names_initialize');original=load(cancelled.OUT/'TEXT_BEFORE.json')[p];assert raw.strip()==original.strip();files[p]=raw[:len(original)] if raw.startswith(original) else raw
    group='common/building_groups/1776_sc1_berchtesgaden_salt.txt';assert (ROOT/group).read_bytes()==load(cancelled.OUT/'EXPECTED_TEXT.json')[group].encode('utf8')
    for p,raw in files.items():
        if p.endswith('.txt'):core.cw.parse(raw.lstrip('\ufeff'))
        assert (ROOT/p).read_bytes()==preimages[p].encode('utf8')
    dump('TEXT_BEFORE_REPLACEMENT.json',preimages);dump('EXPECTED_TEXT.json',files)
    for p,raw in files.items():(ROOT/p).write_bytes(raw.encode('utf8'))
    (ROOT/group).unlink()
    dump('USER_REPORT.json',dict(task_ids=[TASK],reported_observations=['Initial screenshot shows generic salt mine 0/2; special saline not visible in building list','Second screenshot shows GDP 0.57K and salt contribution 29.2 pounds; activity may have existed but was not listed'],explicit_instruction='Annule. Annule ce bâtiment spécial. Donne-lui juste un niveau de mine de sel qui sera pas complètement rempli, c’est tout.',new_human_validation=False,actual_test_date=None,simulation_months=None,diagnosis='Visibility problem plausible; exact engine cause not established. User explicitly chooses ordinary mine rather than repairing a special building.',cancelled_intermediate_fix='SALT_FIX_R1: local special mine and startup repair removed, never runtime validated'))
    for name,source in [('INITIAL_USER_SCREENSHOT.png',cancelled.IMAGE),('GDP_USER_SCREENSHOT.png',Path('C:/Users/simeo/AppData/Local/Temp/codex-clipboard-12885afb-3f94-4b59-982c-24db9d5394ee.png'))]:shutil.copyfile(source,OUT/name)
    print('Special salt building, PM, group and initialization removed; one ordinary salt mine installed',flush=True)

def validate():
    b=load(OUT/'BASELINE.json');now=lot.italian.runtime_hashes();inv=core.qa.inventory();checks=[]
    def ck(n,ok,d=None):checks.append(dict(name=n,passed=bool(ok),detail=d))
    old=b['inventory'];ep=core.qa.counter(old['buildings']);oldnode=core.region(load(lot.OUT/'EXPECTED_TEXT.json')['common/history/buildings/1776_sc1_berchtesgaden.txt'],lot.SID,lot.TAG).children('create_building')[1];newnode=core.region((ROOT/'common/history/buildings/1776_sc1_berchtesgaden.txt').read_text('utf8'),lot.SID,lot.TAG).children('create_building')[1]
    ep[lot.SID,lot.TAG,core.qa.signature(oldnode)]-=1;ep[lot.SID,lot.TAG,core.qa.signature(newnode)]+=1
    ep=+ep
    actual=core.qa.counter(inv['buildings']);ck('Only initial salt building replaced',+actual==+ep)
    expected_levels=core.qa.counter(old['building_levels_written']);expected_levels['building_aor1776_berchtesgaden_saline']-=1;expected_levels['building_salt_mine']+=1;ck('Exactly one standard salt level replaces one special level',+core.qa.counter(inv['building_levels_written'])==+expected_levels)
    for key in old:
        if key not in ['buildings','building_levels_written']:ck('Invariant '+key,inv[key]==old[key])
    changes=sorted(p for p in set(now)|set(b['hashes']) if now.get(p)!=b['hashes'].get(p));expected={'common/buildings/1776_sc1_berchtesgaden.txt','common/production_methods/1776_sc1_berchtesgaden.txt','common/production_method_groups/1776_sc1_berchtesgaden.txt','common/history/buildings/1776_sc1_berchtesgaden.txt','localization/french/1776_sc1_berchtesgaden_l_french.yml','localization/english/1776_sc1_berchtesgaden_l_english.yml'}
    ck('Only six final functional files differ from delivered core',set(changes)==expected,changes)
    for p in expected:
        if p.endswith('.txt'):
            try:core.cw.parse((ROOT/p).read_text('utf-8-sig'));ok=True
            except Exception:ok=False
            ck('Paradox syntax '+p,ok)
    ck('Special salt definition PM and group removed',all('berchtesgaden_saline' not in (ROOT/p).read_text('utf8') for p in ['common/buildings/1776_sc1_berchtesgaden.txt','common/production_methods/1776_sc1_berchtesgaden.txt','common/production_method_groups/1776_sc1_berchtesgaden.txt','common/history/buildings/1776_sc1_berchtesgaden.txt']))
    ck('Intermediate special building group deleted',not (ROOT/'common/building_groups/1776_sc1_berchtesgaden_salt.txt').exists())
    for p in ['common/scripted_effects/1776_sc1_berchtesgaden.txt','common/on_actions/99_1776_sc1_berchtesgaden.txt']:ck('All startup repair removed and original naming bytes retained '+p,sha(ROOT/p)==b['hashes'][p])
    mine=lot.italian.definitions('common/buildings')['building_salt_mine'];pms=lot.italian.definitions('common/production_methods');groups=lot.italian.definitions('common/production_method_groups')
    ck('Ordinary resource mine unchanged',mine.one('building_group')=='bg_salt_mining' and mine.one('city_type')=='mine')
    ck('One national BGT level',newnode.one('building')=='"building_salt_mine"' and newnode.children('add_ownership')[0].children('country')[0].one('levels')=='1' and newnode.children('add_ownership')[0].children('country')[0].one('country')=='"c:BGT"')
    pm= pms[METHODS[0]];mods=pm.children('building_modifiers')[0];jobs=sum(int(n.value) for n in mods.children('level_scaled')[0].children());ck('Unmodified ordinary mine 5000-job capacity intentionally underfilled',jobs==5000)
    ck('Ordinary base output and tools retained',mods.children('workforce_scaled')[0].one('goods_output_salt_add')=='20' and mods.children('workforce_scaled')[0].one('goods_input_tools_add')=='2')
    selected=[n.value for n in newnode.children('activate_production_methods')[0].children()];ck('Six ordinary PMs initialized exactly',selected==['"'+m+'"' for m in METHODS])
    ck('Every initialized method belongs to a standard mine group',all(any(m in [n.value for n in groups[g.value].children('production_methods')[0].children()] for g in mine.children('production_method_groups')[0].children()) for m in METHODS))
    ck('No unrequested shaft-mining research or custom fallback',not any(p.startswith(('common/technology/','common/history/countries/')) for p in changes))
    import localization_duplicate_audit as audit
    sets=[]
    for lang in ['french','english']:
        p=ROOT/('localization/'+lang+'/1776_sc1_berchtesgaden_l_'+lang+'.yml');matched=[audit.KEY.match(line) for line in p.read_text('utf-8-sig').splitlines()[1:]];keys={m.group(1) for m in matched if m};sets.append(keys);entries=audit.entries(lang)
        ck('Four obsolete salt labels removed BOM and no duplicates '+lang,len(keys)==14 and all(matched) and p.read_bytes().startswith(b'\xef\xbb\xbf') and all(len(entries[k])==1 for k in keys))
    ck('Same retained fourteen localization keys',sets[0]==sets[1])
    ck('All original nested reports and receipts preserved',all(sha(ROOT/p)==h for p,h in b['proofs'].items() if Path(p).parent!=rm.OUT.relative_to(ROOT)))
    ck('All prior tools and tests untouched',all(sha(ROOT/p)==h for p,h in b['tools'].items()))
    git=lambda *a:subprocess.check_output(['git',*a],cwd=ROOT,text=True).strip();ck('Git HEAD branch index preserved',git('rev-parse','HEAD')==b['git']['head'] and git('branch','--show-current')==b['git']['branch'] and sha(ROOT/'.git/index')==b['git']['index'])
    v=dict(task_ids=[TASK],status='PASS' if all(c['passed'] for c in checks) else 'FAIL',passed=sum(c['passed'] for c in checks),total=len(checks),failed=[c['name'] for c in checks if not c['passed']],checks=checks,automated_engine_test=False,engine_executed=False);dump('VALIDATION.json',v);print('Native mine static',v['passed'],'/',v['total'],v['failed'],flush=True);assert not v['failed'],v['failed'];dump('SESSION_AFTER_STATIC.json',dict(hashes=now,inventory=inv));dump('FILES_MODIFIED.json',dict(runtime_files=changes,sha256={p:now[p] for p in changes},standard_mine_global_files_changed=False))

def documentation_and_tracking():
    b=load(OUT/'BASELINE.json');s=load(rm.OUT/'ROADMAP_STATE.json');assert s==b['roadmap'];assert load(OUT/'VALIDATION.json')['status']=='PASS'
    report='''**SERG TERRITORIAL 1.0 — PROGRESSION : 34,89 %**

# Berchtesgaden — remplacement demandé par une mine standard

La première capture montre la mine générique à 0/2 et le joueur signale que la saline spéciale n'est pas visible. La seconde montre un PIB de 0,57 K £ avec contribution du sel de 29,2 £ : une activité existe donc vraisemblablement malgré le défaut d'affichage. Ni cette capture ni le PIB ne constituent une validation intégrale du protocole. La cause moteur exacte de l'affichage n'a pas été isolée. Le joueur demande explicitement : « Annule. Annule ce bâtiment spécial. Donne-lui juste un niveau de mine de sel qui sera pas complètement rempli, c'est tout. » Cette décision remplace la tentative intermédiaire de petite mine spéciale SALT_FIX_R1, jamais validée en jeu.

## Installation finale

Un seul niveau de **building_salt_mine**, propriété nationale BGT, remplace la saline spécifique dans l'historique de STATE_TYROL/BGT. Méthodes ordinaires : pioches et pelles, aucun explosif, aucune automatisation vapeur, charrettes, aucun traitement supplémentaire du sel et déclaration ordinaire des données. Aucun niveau additionnel de mine n'est attribué à AUS ou à un voisin.

La mine conserve ses paramètres globaux : **5000 postes de capacité**, dont 4500 ouvriers et 500 commerçants ; sel 20 et outils 2 à plein emploi pour la méthode de base. Ces valeurs ne sont pas des effectifs initiaux ou une production effective promis. Avec 1000 habitants, le bâtiment est volontairement sous-occupé ; aucun habitant n'est ajouté pour le remplir. Aucun PM, technologie, subvention ou correctif d'effectifs spécial n'est créé. La capacité minière régionale reste identique ; aucune modification de la définition, des méthodes ou du groupe de la mine standard pour les autres pays.

La définition de saline spécifique, son PM, son groupe de PM et ses quatre clés dans chaque langue sont retirés. Le groupe de petite mine spéciale créé dans la tentative annulée est supprimé. Tous les effets et appels d'initialisation de cette tentative sont retirés ; les effets et appels de nommage Berchtesgaden retrouvent exactement leurs octets livrés avant cette passe. La chancellerie publique de 100 postes reste intégralement conservée.

## Conservation et état

Carte BGT xEDBF00/quatre cellules, populations (BGT 1000, monde 834926252), souverain, gouvernement, capitale, ressources, unités, diplomatie et registre impérial restent inchangés. Les douze cellules SLZ, BRX/TRT/MCA et tous les autres noyaux sont conservés. Travaux concurrents fortifications/génie, France/Anzin/Saint-Gobain/drainage et États-Unis conservés : seuls six fichiers fonctionnels diffèrent de la livraison précédente. Aucun retour d'un fichier partagé depuis une ancienne baseline, aucune écriture Git ou vanilla.

Les anciens rapports, preuves, attestations et 32 événements sont conservés intégralement. Le rapport original SC1-BERCHTESGADEN/REPORT.md décrit l'installation précédente ; le présent rapport la remplace seulement pour le sel. Les preuves de la tentative spéciale annulée demeurent des archives, sans rôle dans la livraison courante. Votre document joint répète la validation Brixen déjà enregistrée : aucun second reçu, événement de validation ou crédit n'est ajouté. BR-I-CORE reste PASS_RUNTIME_USER_VALIDATED ; SC1-BRIXEN reste BLOCKED P1 avec ses cinq obligations.

SC1-BERCHTESGADEN reste **BLOCKED P1**, six obligations régionales conservées ; seul BG-I-CORE révisé est **IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION**, avec **RETEST_REQUIRED**. Aucune attestation BGT. Progression **82/235 → 82/235**, **34,89 % → 34,89 %**, 24 tâches qualifiées, 81 tâches, périmètre 1.0.0 et poids inchangés.

## Contrôles et prochaine action

VALIDATION.json : **35/35 contrôles actuels**, dont remplacement exact d'un niveau, conservation démographique et cartographique, six PM ordinaires, suppression de tout bâtiment ou initialiseur spécial du sel et conservation des fichiers concurrents. TESTS.json/log consignent la suite cumulative réellement exécutée ; les huit échecs antérieurement classés restent distingués des régressions. Les anciens tests ne sont pas modifiés ; plusieurs contrats de l'ancienne saline lisent volontairement la preuve figée de la première livraison, pas la version courante. Les 35 contrôles actuels vérifient la nouvelle version. Le validateur canonique et FINAL_CHECKS.json contrôlent suivi et conservation après les tests.

**Prochaine action : nouvelle partie 1776 et test de la mine ordinaire**, selon PLAYER_TEST_PROTOCOL.md de ce dossier. L'agent n'a pas exécuté le moteur. Le démarrage en jeu n'est pas annoncé comme acquis. SC1-PASSAU-OUTLIERS reste la candidate indépendante non commencée ; aucun autre territoire n'est traité. Blocages Brixen, Trente, Autriche/Innviertel, Teschen et Italie inchangés.

Référence historique réutilisée : [Finanzamt Berchtesgaden-Laufen](https://www.finanzamt-berchtesgaden-laufen.de/ueber-uns/geschichte), mine du Petersberg depuis 1517 et saline de Frauenreuth antérieure à 1776. Le remplacement moteur demandé ne nie pas cette distinction historique ; il regroupe l'activité dans le bâtiment ordinaire du mod.
'''
    (OUT/'REPORT.md').write_text(report,encoding='utf8')
    protocol='''# Test joueur — BG-I-CORE, révision mine de sel standard

Statut : IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION / RETEST_REQUIRED. Aucune validation humaine nouvelle.

1. Fermer puis relancer le jeu pour charger les définitions modifiées ; commencer une **nouvelle partie au 1er janvier 1776**. Une sauvegarde issue du bâtiment spécial retiré ne valide pas ce remplacement d'historique.
2. Choisir Berchtesgaden (BGT), vérifier quatre cellules B et les 1000 habitants. Capitale Berchtesgaden intérieure, Franz Anton Josef von Hausen-Gleichenstorff prince-prévôt, théocratie et lois conservées.
3. Dans **Bâtiments → Ressources**, vérifier **Mines de sel : niveau 1** (capacité attendue inchangée de 2 d'après votre capture). Il s'agit de la mine standard du mod ; aucune saline ou petite mine spéciale supplémentaire.
4. Ouvrir la mine : propriété BGT, pioches et pelles, aucun explosif ni vapeur, charrettes, aucun traitement du sel supplémentaire. La méthode standard affiche 5000 postes de capacité, **pas 5000 travailleurs effectivement présents**. Le recrutement partiel est voulu. Relever l'effectif réellement employé, les outils, le sel, les finances et toute anomalie ; ne pas exiger le plein emploi.
5. Vérifier la chancellerie publique de 100 postes, les droits impériaux, neuf électeurs, absence de nouveau pacte. Contrôler Salzbourg douze cellules, voisins BAV/AUS, Brixen et Trente ainsi que les travaux concurrents utilisés.
6. Simuler **un mois complet**, sauvegarder et recharger ; vérifier que le niveau de mine, ses méthodes, la propriété, les noms et les voisins sont conservés. Rapporter les résultats réellement obtenus pour **BG-I-CORE révisé uniquement**.

Cette réussite éventuelle ne clôture pas les juridictions périphériques ou le cadastre régional. Prochaine candidate SC1-PASSAU-OUTLIERS identifiée sans commencement.
'''
    (OUT/'PLAYER_TEST_PROTOCOL.md').write_text(protocol,encoding='utf8')
    t=next(t for t in s['tasks'] if t['id']==TASK);t['implementation_report'].append(PREFIX+'REPORT.md');t['static_tests']=dict(status='PASS',evidence=[PREFIX+'VALIDATION.json'])
    t['installed_sub_lots'][0]['scope']='Four-cell prince-provost residence B: 1000 residents, Hausen, 100-job court and one ordinary salt mine, deliberately underfilled at its standard 5000-job capacity; pending fresh user protocol. Not whole principality.'
    t['runtime_validation'].update(status='RETEST_REQUIRED',scope=t['installed_sub_lots'][0]['scope'],protocol=PREFIX+'PLAYER_TEST_PROTOCOL.md',user_report=PREFIX+'USER_REPORT.json',attestation=None)
    t['blocking_reason']+=' Révision sel demandée par le joueur : bâtiment spécial retiré, un niveau de mine standard sous-occupée installé ; nouveau protocole BG-I-CORE en attente, aucun reçu humain.'
    t['current_delivery_note']='BG-I-CORE révisé : un niveau public de mine de sel standard, méthodes et capacité ordinaires de 5000 postes conservées, recrutement partiel voulu pour les 1000 habitants ; aucun bâtiment/PM/initialiseur spécial du sel. Chancellerie 100 postes, carte, populations, institutions, voisins et registre conservés. Installations IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION ; région BLOCKED P1, zéro point et aucun reçu BGT.'
    t['delivered_scope'].update(salt_installation_revision='SALT_NATIVE_R1',salt_building='building_salt_mine',salt_initial_levels=1,salt_standard_job_capacity=5000,intentionally_partial_employment=True)
    s['mission_status']='BERCHTESGADEN_ORDINARY_SALT_MINE_PENDING_RETEST_REGION_BLOCKED';s['runtime_validation_hold'].update(protocol=PREFIX+'PLAYER_TEST_PROTOCOL.md',reason='Correction du même BG-I-CORE selon demande directe : test de la mine ordinaire avant toute suite autorisée.',test_summary=PROTOCOL,scope_note=lot.SCOPE_NOTE.replace('une petite activité saline','une mine de sel standard volontairement sous-occupée'))
    s['events'].append(dict(id='SERG-RM-0033',date='2026-10-24',kind='USER_DIRECTED_STANDARD_SALT_MINE_REPLACEMENT_PENDING_RETEST',scope_version='1.0.0',source=PREFIX+'USER_REPORT.json',changes=[dict(task_id=TASK,before='BLOCKED',after='BLOCKED')],before_weight=82,after_weight=82,total_weight=235,before_percent='34.89',after_percent='34.89',evidence=[PREFIX+n for n in ['REPORT.md','VALIDATION.json','PLAYER_TEST_PROTOCOL.md']],note=t['current_delivery_note']+' La seconde capture montre une contribution du sel au PIB ; absence réelle du bâtiment non démontrée, défaut d’affichage possible. Le joueur demande néanmoins sa suppression et une mine ordinaire. Tentative intermédiaire spéciale annulée intégralement. Brixen déjà validé, pas de reçu dupliqué. Aucun autre territoire commencé ; 82/235=34,89 % avant/après.'))
    assert s['events'][:-1]==b['roadmap']['events'];assert [x for x in s['tasks'] if x['id']!=TASK]==[x for x in b['roadmap']['tasks'] if x['id']!=TASK]
    p=rm.progress(s);assert (p['earned_weight'],p['total_weight'],p['percent'],p['next_task'])==(82,235,'34.89',TASK),p
    assert not rm.structural_errors(s),rm.structural_errors(s);rm.write_json(rm.OUT/'ROADMAP_STATE.json',s)
    with contextlib.redirect_stdout(io.StringIO()):rm.render()
    checked=rm.check();dump('TRACKER_VALIDATION.json',checked);assert checked['status']=='PASS',checked;print('Tracker PASS; 82/235 unchanged; ordinary mine retest pending',flush=True)

def tests_and_finalize():
    import serg_sc4_ligurian_fiefs as lig
    modules=lig.MODULES+['test_serg_sc4_piombino','test_serg_sc4_massa_carrara','test_serg_sc1_trento','test_serg_sc1_brixen','test_serg_sc1_berchtesgaden'];known={f['id'] for f in load(lot.OUT/'TESTS.json')['failed']};stream=io.StringIO()
    result=unittest.TextTestRunner(stream=stream,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromNames(modules));failed=[dict(id=t.id(),traceback=s) for t,s in result.failures+result.errors];unknown=[f for f in failed if f['id'] not in known]
    (OUT/'TESTS.log').write_text(stream.getvalue(),encoding='utf8');dump('TESTS.json',dict(task_ids=[TASK],status='FAIL' if unknown else 'INHERITED_SNAPSHOT_FAILURES_ONLY' if failed else 'PASS',total=result.testsRun,passed=result.testsRun-len(failed)-len(result.skipped),failed=failed,skipped=[dict(id=t.id(),reason=s) for t,s in result.skipped],unexplained_failures=unknown,old_tests_unchanged=True,automated_engine_test=False));print('Cumulative',result.testsRun-len(failed)-len(result.skipped),'/',result.testsRun,'unknown',len(unknown),flush=True);assert not unknown,unknown
    b=load(OUT/'BASELINE.json');s=load(rm.OUT/'ROADMAP_STATE.json');now=lot.italian.runtime_hashes();static=load(OUT/'SESSION_AFTER_STATIC.json');p=rm.progress(s);checked=rm.check();dump('TRACKER_VALIDATION_FINAL.json',checked)
    checks={'Current runtime matches successful static validation':now==static['hashes'],'Canonical validator PASS':checked['status']=='PASS','Progress unchanged':(p['earned_weight'],p['total_weight'],p['percent'])==(82,235,'34.89'),'Only same Berchtesgaden task changed':[t for t in s['tasks'] if t['id']!=TASK]==[t for t in b['roadmap']['tasks'] if t['id']!=TASK],'Previous 32 events retained':s['events'][:-1]==b['roadmap']['events'],'Passau outliers not begun':next(t for t in s['tasks'] if t['id']=='SC1-PASSAU-OUTLIERS')['status']=='NOT_STARTED','No BGT human receipt':not list(lot.OUT.glob('RUNTIME_USER_ATTESTATION*')),'All old nested proof bytes retained':all(sha(ROOT/f)==h for f,h in b['proofs'].items() if Path(f).parent!=rm.OUT.relative_to(ROOT)),'All old tests and tools retained':all(sha(ROOT/f)==h for f,h in b['tools'].items()),'All previous terminal qualifications retained':rm.qualifications(s)==rm.qualifications(b['roadmap']),'Current protocol selected':s['runtime_validation_hold']['protocol']==PREFIX+'PLAYER_TEST_PROTOCOL.md' and PROTOCOL in (rm.OUT/'NEXT_ACTION.md').read_text('utf8'),'Eight classified cumulative failures only':len(failed)==8 and not unknown and len(result.skipped)==1}
    git=lambda *a:subprocess.check_output(['git',*a],cwd=ROOT,text=True).strip();checks['HEAD branch index retained']=git('rev-parse','HEAD')==b['git']['head'] and git('branch','--show-current')==b['git']['branch'] and sha(ROOT/'.git/index')==b['git']['index']
    diff=subprocess.run(['git','diff','--check'],cwd=ROOT,text=True,capture_output=True);white=[line for line in diff.stdout.splitlines() if 'trailing whitespace.' in line];checks['Only four inherited whitespace findings']=diff.returncode==2 and len(white)==4 and all(line.startswith('common/history/pops/00_west_europe.txt:') for line in white);dump('DIFF_CHECK.json',dict(returncode=diff.returncode,findings=white,inherited_count=4))
    v=dict(task_ids=[TASK],status='PASS' if all(checks.values()) else 'FAIL',passed=sum(checks.values()),total=len(checks),failed=[k for k,v in checks.items() if not v],checks=checks,automated_engine_test=False);dump('FINAL_CHECKS.json',v);print('Final checks',v['passed'],'/',v['total'],v['failed'],flush=True);assert not v['failed']
    paths=set(load(OUT/'FILES_MODIFIED.json')['runtime_files'])|set(load(lot.OUT/'FILES_MODIFIED.json')['runtime_files'])
    paths|={fp.relative_to(ROOT).as_posix() for fp in OUT.rglob('*') if fp.is_file() and fp.name!='DELIVERY_MANIFEST.json'};paths|={fp.relative_to(ROOT).as_posix() for fp in rm.OUT.iterdir() if fp.is_file()};paths|={Path(__file__).relative_to(ROOT).as_posix()}
    manifest={path:sha(ROOT/path) for path in sorted(paths)};dump('DELIVERY_MANIFEST.json',dict(task_ids=[TASK],files=manifest,supersedes_salt_installation_only='SC1-BERCHTESGADEN/DELIVERY_MANIFEST.json',status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',regional_status='BLOCKED',human_validated=False));assert all(sha(ROOT/path)==h for path,h in manifest.items());print('Native-mine delivery manifest verified',len(manifest),'files',flush=True)

if __name__=='__main__':globals()[sys.argv[1]]()
