"""Show one imperial departure entry, without renaming other blocs' exit plays."""
import sys,json,subprocess,time,io,unittest
import hre_centralization_01 as h
ROOT=h.ROOT;OUT=h.OUT/'SECESSION_LENS_R2'
NATIVE='common/diplomatic_plays/00_diplomatic_plays.txt'
IMPERIAL='common/diplomatic_plays/1776_imperial_plays.txt'
TRIGGER='common/scripted_triggers/1776_imperial_secession_lens.txt'
MEMBER='aor1776_hre_imperial_bloc_member'

def dump(name,obj):
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf8')

def load(name):return json.loads((OUT/name).read_text(encoding='utf8'))

def augment(files):
    files=dict(files)
    # Membership rights and current bloc participation are different. Never
    # suppress the ordinary exit from a foreign bloc for a roster TAG alone.
    files[TRIGGER]=h.block(MEMBER,'''aor1776_hre_member = yes
exists = power_bloc
power_bloc = { has_identity = identity:identity_aor1776_imperial_federation }''')
    raw=files.get(NATIVE,h.existing(NATIVE))
    raw=h.append_guard(raw,'dp_leave_power_bloc','selectable_in_lens',MEMBER+' = no')
    raw=h.append_guard(raw,'dp_leave_power_bloc','possible','custom_tooltip = { text = aor1776_hre_bloc_departure_requires_secession_tt '+MEMBER+' = no }')
    files[NATIVE]=raw
    raw=files.get(IMPERIAL,h.existing(IMPERIAL))
    raw=h.append_guard(raw,'dp_aor1776_hre_secession','selectable_in_lens',MEMBER+' = yes')
    raw=h.append_guard(raw,'dp_aor1776_hre_secession','possible','custom_tooltip = { text = aor1776_hre_secession_in_imperial_bloc_tt '+MEMBER+' = yes }')
    files[IMPERIAL]=raw
    import re
    for lang,i in [('english',0),('french',1)]:
        p=f'localization/{lang}/1776_imperial_constitution_l_{lang}.yml'
        raw=files.get(p,h.existing(p))
        messages={
          'aor1776_hre_bloc_departure_requires_secession_tt':('Imperial members must use [Concept(\'concept_diplomatic_play\',\'$dp_aor1776_hre_secession$\')] to leave the Empire.','Les membres impériaux doivent recourir au [Concept(\'concept_diplomatic_play\',\'$dp_aor1776_hre_secession$\')] pour quitter l’Empire.'),
          'aor1776_hre_secession_in_imperial_bloc_tt':('Belongs to the imperial estates and is currently a member of the imperial [concept_power_bloc].','Appartient aux États impériaux et fait actuellement partie du [concept_power_bloc|l] impérial.')}
        for key,pair in messages.items():
            line=' '+key+':0 "'+pair[i]+'"'
            if re.search(r'(?m)^ '+key+r':',raw):raw=re.sub(r'(?m)^ '+key+r':[^\n]*$',lambda _:line,raw)
            else:raw=raw.rstrip()+'\n'+line+'\n'
        files[p]=raw
    return files

def capture():
    assert not (OUT/'BASELINE.json').exists(),'Never replace a baseline'
    dump('BASELINE.json',dict(inventory=h.qa.inventory(),hashes=h.economy.runtime_hashes(),registry_sha256=h.qa.sha(h.active_registry_path()),native_sha256=h.qa.sha(h.GAME/NATIVE),original_imperial=(ROOT/IMPERIAL).read_text(encoding='utf-8-sig'),git_head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),git_index_sha256=h.qa.sha(ROOT/'.git/index')))
    print('R2 baseline captured; existing autonomy/localization corrections protected.',flush=True)

def prepare():
    files=augment({IMPERIAL:(ROOT/IMPERIAL).read_text(encoding='utf-8-sig')})
    dump('EXPECTED_TEXT.json',files);h.patcher.OUT=OUT;changes=h.patcher.emit(files,'INSTALL.patch')
    previous=set(load('PLAN.json')['files']) if (OUT/'PLAN.json').exists() else set()
    dump('PLAN.json',dict(files=sorted(previous|set(changes))))
    print('Prepared',len(changes),'scoped departure-filter files.',flush=True)

def validate():
    b=load('BASELINE.json');inv=h.qa.inventory();now=h.economy.runtime_hashes();checks=[]
    def check(name,ok,detail=None):
        checks.append(dict(name=name,passed=bool(ok),detail=detail))
        if not ok:print('FAIL',name,detail,flush=True)
    changed=sorted(p for p in set(now)|set(b['hashes']) if now.get(p)!=b['hashes'].get(p))
    expected_paths={NATIVE,IMPERIAL,TRIGGER}|{f'localization/{lang}/1776_imperial_constitution_l_{lang}.yml' for lang in ['english','french']}
    check('Only five departure-filter runtime files changed',set(changed)==expected_paths,changed)
    for key,value in b['inventory'].items():check('Inventory unchanged: '+key,inv[key]==value)
    for p,s in load('EXPECTED_TEXT.json').items():
        check('Expected text '+p,(ROOT/p).read_text(encoding='utf-8-sig')==s.lstrip('\ufeff'))
        try:h.cw.parse(s);ok=True
        except Exception:ok=False
        check('Parse '+p,ok)
    check('Installed vanilla file untouched',h.qa.sha(h.GAME/NATIVE)==b['native_sha256'])
    check('Imperial territory registry unchanged',h.qa.sha(h.active_registry_path())==b['registry_sha256'])
    check('HEAD unchanged',subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==b['git_head'])
    check('Git index unchanged',h.qa.sha(ROOT/'.git/index')==b['git_index_sha256'])
    check('Secession war goal, costs and enforcement untouched',now['common/war_goal_types/1776_imperial_war_goals.txt']==b['hashes']['common/war_goal_types/1776_imperial_war_goals.txt'])
    check('Autonomy, contribution and unrelated localization files untouched',all(now[p]==digest for p,digest in b['hashes'].items() if p.startswith(('common/subject_types/','common/diplomatic_actions/','localization/')) and p not in expected_paths))
    result=dict(status='STATIC_PASS_RUNTIME_PENDING' if all(c['passed'] for c in checks) else 'FAILED',passed=sum(c['passed'] for c in checks),total=len(checks),checks=checks,runtime_files_modified=changed,engine_test_executed=False,vanilla_other_bloc_exit_preserved=True,historical_member_outside_imperial_bloc_exit_preserved=True,bulk_centralization_enabled=False)
    dump('VALIDATION.json',result);print(result['status'],result['passed'],'/',result['total'],flush=True)
    assert result['status']=='STATIC_PASS_RUNTIME_PENDING'

def unit_tests():
    groups={'departure_filter':['test_hre_secession_lens_01'],'autonomy_feedback_preserved':['test_hre_subject_feedback_01'],'centralization_preserved':['test_hre_centralization_01']};data={}
    for name,modules in groups.items():
        stream=io.StringIO();start=time.monotonic();result=unittest.TextTestRunner(stream=stream).run(unittest.TestLoader().loadTestsFromNames(modules))
        data[name]=dict(tests=result.testsRun,failures=[t.id() for t,_ in result.failures],errors=[t.id() for t,_ in result.errors],output=stream.getvalue(),seconds=round(time.monotonic()-start,2),engine_test=False)
        print(name,result.testsRun,'tests',len(result.failures),'failures',flush=True)
    dump('UNIT_TESTS.json',data);assert not any(v['failures'] or v['errors'] for v in data.values())

def compiler_check():
    import map2k_imperial_system as compiler
    compiler.OUT=OUT;files=compiler.compile_system()
    rows=[dict(file=p,passed=(ROOT/p).read_text(encoding='utf-8-sig')==s.lstrip('\ufeff')) for p,s in files.items()]
    dump('COMPILER_REPRODUCTION.json',dict(total=len(rows),passed=sum(r['passed'] for r in rows),results=rows))
    print('Full compiler reproduction',sum(r['passed'] for r in rows),'/',len(rows),flush=True)
    assert all(r['passed'] for r in rows),[r for r in rows if not r['passed']]

def report():
    v=load('VALIDATION.json');tests=load('UNIT_TESTS.json')
    text=f'''# SERG — une seule entrée de départ dans la lentille diplomatique

## Installé

Pour un pays reconnu comme membre impérial ET actuellement dans le bloc portant l’identité impériale, « Quitter le bloc de nations » est masqué dans les exigences diplomatiques. « Sécession impériale » reste l’entrée spécialisée, sous ses conditions préexistantes. Le dirigeant du bloc ne reçoit pas un droit de sécession : l’exclusion existante de l’empereur est conservée.

Le contrôle porte sur `selectable_in_lens`, pas seulement sur le texte ou le nombre affiché. La même garde dans `possible` empêche le lancement de la sortie générique par un autre point d’entrée scripté. Cela ne remplace pas tous les boutons natifs de l’interface du bloc ; l’identité impériale interdit déjà la sortie volontaire ordinaire.

Les autres blocs gardent la sortie native. Un TAG historiquement impérial appartenant à un bloc étranger n’est pas bloqué sur la seule foi de son TAG. Les pays hors de l’Empire ne voient pas apparaître la sécession impériale du fait de ce correctif.

## Préservé

Aucune fusion de mécanismes de paix, aucun renommage global des textes vanilla. Objectif de guerre, coût en manœuvres, infamie et effets de victoire de la sécession inchangés. Les conditions de sujétion, de cible impériale et de relations restent celles du coup existant. Aucun assouplissement pour les nouveaux sujets centralisés n’est introduit par cette correction d’affichage.

Taux15 %/10 %, chaîne d’autonomie, descriptions communes, mécanismes d’élection et prototype isolé inchangés. Aucun historique, territoire, habitant, bâtiment, unité ou registre modifié. Aucun commit, push, changement de branche ou d’index. L’installation du jeu reste en lecture seule.

## Technique et vérifications

Cinq fichiers fonctionnels : `{NATIVE}` (override local du fichier installé, tous les autres coups conservés à l’identique), `{IMPERIAL}` (deux gardes supplémentaires seulement), `{TRIGGER}` et deux ajouts de messages de validation FR/EN dans les localisations constitutionnelles. Le compilateur impérial applique cette couche en dernier pour préserver le correctif lors d’une régénération.

{v['passed']}/{v['total']} contrôles statiques et {sum(t['tests'] for t in tests.values())} tests réussis. Les tests comparent les arbres des autres coups natifs et la sécession existante après retrait des seules gardes déclarées. Les scénarios logiques ne sont pas des tests moteur.

**STATIC_PASS_RUNTIME_PENDING.** Après redémarrage : ouvrir les exigences diplomatiques avec un membre non empereur du SERG, constater l’absence de « Quitter le bloc de nations » et la présence de « Sécession impériale ». Les causes normales d’indisponibilité restent applicables. Contrôler ensuite un membre d’un autre bloc : sa sortie native doit rester disponible selon les règles habituelles. Aucun résultat en jeu n’est présumé acquis.
'''
    h.patcher.OUT=OUT;h.patcher.emit({(OUT/'REPORT.md').relative_to(ROOT).as_posix():text},'REPORT.patch')

if __name__=='__main__':globals()[sys.argv[1]]()
