"""User feedback: shared bond text, reversible subject types and contribution rates.

Old validation receipts are immutable. New expectations and reports live in R1.
"""
import sys,json,subprocess,re,time,io,unittest
import hre_centralization_01 as h
ROOT=h.ROOT;OUT=h.OUT/'FEEDBACK_R1'

def dump(name,obj):
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf8')

def load(name):return json.loads((OUT/name).read_text(encoding='utf8'))

def capture():
    assert not (OUT/'BASELINE.json').exists(),'Do not replace this task baseline'
    native=['common/diplomatic_actions/37_subjects_decrease_autonomy.txt','common/diplomatic_actions/38_subjects_increase_autonomy.txt','common/subject_types/00_subject_types.txt']
    dump('BASELINE.json',dict(inventory=h.qa.inventory(),hashes=h.economy.runtime_hashes(),registry_sha256=h.qa.sha(h.active_registry_path()),git_head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),git_index_sha256=h.qa.sha(ROOT/'.git/index'),native_hashes={p:h.qa.sha(h.GAME/p) for p in native}))
    print('R1 baseline captured; no runtime writes.',flush=True)

def prepare():
    # Rebuild only the known components, not the costly whole constitutional compiler.
    paths=h.load('EXPECTED_TEXT.json');files={p:(ROOT/p).read_text(encoding='utf-8-sig') for p in paths}
    files['common/diplomatic_actions/1776_imperial_centralization.txt']=''.join(h.pact('aor1776_imperial_'+kind,typ,h.CONFIG[kind+'_tribute'],h.CONFIG[kind+'_influence'],'aor1776_imperial_'+kind) for kind,typ in [('estate',h.ESTATE),('elector',h.ELECTOR)])
    files.update(h.localizations(files));files=h.autonomy_feedback(files)
    dump('EXPECTED_TEXT.json',files)
    h.patcher.OUT=OUT;changes=h.patcher.emit(files,'INSTALL.patch')
    previous=set(load('PLAN.json')['files']) if (OUT/'PLAN.json').exists() else set()
    dump('PLAN.json',dict(files=sorted(previous|set(changes))))
    print('Prepared',len(changes),'scoped text changes; no startup conversions.',flush=True)

def compiler_check():
    import map2k_imperial_system as compiler
    compiler.OUT=OUT
    files=compiler.compile_system()
    rows=[dict(file=p,passed=(ROOT/p).read_text(encoding='utf-8-sig')==s.lstrip('\ufeff')) for p,s in files.items()]
    dump('COMPILER_REPRODUCTION.json',dict(passed=sum(r['passed'] for r in rows),total=len(rows),results=rows))
    print('Full compiler reproduction',sum(r['passed'] for r in rows),'/',len(rows),flush=True)
    assert all(r['passed'] for r in rows),[r for r in rows if not r['passed']]

def unit_tests():
    groups={'feedback_R1':['test_hre_subject_feedback_01'],'centralization_current_contract':['test_hre_centralization_01'],'Anhalt_preservation':['test_map2r_anhalt']};results={}
    for name,modules in groups.items():
        start=time.monotonic();stream=io.StringIO();result=unittest.TextTestRunner(stream=stream).run(unittest.TestLoader().loadTestsFromNames(modules))
        results[name]=dict(tests=result.testsRun,failures=[t.id() for t,_ in result.failures],errors=[t.id() for t,_ in result.errors],output=stream.getvalue(),seconds=round(time.monotonic()-start,2),engine_test=False)
        print(name,result.testsRun,'tests',len(result.failures),'failures',flush=True)
    dump('UNIT_TESTS.json',results)
    assert not any(r['failures'] or r['errors'] for r in results.values())

def validate():
    b=load('BASELINE.json');inv=h.qa.inventory();current=h.economy.runtime_hashes();expected=load('EXPECTED_TEXT.json');checks=[]
    def check(name,ok,detail=None):
        checks.append(dict(name=name,passed=bool(ok),detail=detail))
        if not ok:print('FAIL',name,detail,flush=True)
    changed=sorted(p for p in set(current)|set(b['hashes']) if current.get(p)!=b['hashes'].get(p))
    check('Only14 declared runtime text changes',set(changed)==set(load('PLAN.json')['files']) and len(changed)==14,changed)
    for key,value in b['inventory'].items():check('Historical effective inventory unchanged: '+key,inv[key]==value)
    for p,s in expected.items():
        check('Expected text '+p,(ROOT/p).read_text(encoding='utf-8-sig')==s.lstrip('\ufeff'))
        if p.endswith('.txt'):
            try:h.cw.parse(s);ok=True
            except Exception:ok=False
            check('Parsed '+p,ok)
    for lang in ['french','english']:
        p=f'localization/{lang}/replace/1776_imperial_autonomy_l_{lang}.yml'
        raw=(ROOT/p).read_text(encoding='utf-8-sig')
        keys=re.findall(r'(?m)^ ([\w.]+):0 ',raw)
        check('No duplicate UI locale keys '+lang,len(keys)==len(set(keys)))
        for native_key in ['SUBJECT_TYPE_ANNEX_TOOLTIP','SUBJECT_TYPE_DECREASED_AUTONOMY_TOOLTIP','SUBJECT_TYPE_INDEPENDENCE_TOOLTIP','SUBJECT_TYPE_INCREASED_AUTONOMY_TOOLTIP']:
            check('Conditional UI override with vanilla fallback '+lang+' '+native_key,native_key in keys and 'aor1776_vanilla_'+native_key.lower() in keys)
    check('No territorial registry delta',h.qa.sha(h.active_registry_path())==b['registry_sha256'])
    for p,digest in b['native_hashes'].items():check('Installed game untouched '+p,h.qa.sha(h.GAME/p)==digest)
    check('Git HEAD unchanged',subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==b['git_head'])
    check('Git index unchanged',h.qa.sha(ROOT/'.git/index')==b['git_index_sha256'])
    check('No startup subject conversion',not any(p.startswith('common/history/') for p in changed))
    check('Icons and graphical assets unchanged',not any(p.startswith(('gfx/','gui/','map_data/')) for p in changed))
    reproduction=load('COMPILER_REPRODUCTION.json');check('Full compiler regenerates installed files',reproduction['passed']==reproduction['total'])
    result=dict(status='STATIC_PASS_RUNTIME_PENDING' if all(c['passed'] for c in checks) else 'FAILED',passed=sum(c['passed'] for c in checks),total=len(checks),checks=checks,runtime_files_modified=changed,world_population=sum(p['count'] for p in inv['pops']),preexisting_anomalies=dict(duplicate_RGBs=len(inv['duplicates']),invalid_references=len(inv['errors'])),engine_test_executed=False,individual_native_subject_chain_enabled=True,initial_virtual_bonds_converted=False,bulk_centralization_enabled=False,succession_prototype_unchanged=True)
    dump('VALIDATION.json',result);print(result['status'],result['passed'],'/',result['total'],flush=True)
    assert result['status']=='STATIC_PASS_RUNTIME_PENDING'

def report():
    v=load('VALIDATION.json');t=load('UNIT_TESTS.json');reproduction=load('COMPILER_REPRODUCTION.json')
    report=f'''# HRE-CENTRALIZATION-01 — retour utilisateur R1

## Corrections installées

- Une seule description FR/EN : `concept_aor1776_hre_protectorate_desc`. Les descriptions du pacte constitutionnel initial, de la fiche diplomatique, du type de sujet et de l’ancien alias la réutilisent. Les mots liés ouvrent des concepts réels du jeu.
- Réduction : Lien impérial → État impérial, ou Électorat impérial si `aor1776_hre_elector` reconnaît la dignité électorale. Le choix est explicite dans l’effet, pas déduit de l’ordre des deux types natifs.
- Augmentation : État impérial / Électorat impérial → Lien impérial. Cela conserve le pays et sa relation de sujet, sans indépendance, annexion ou suppression des privilèges électoraux. Le même traitement est prévu pour l’action du suzerain et la demande acceptée du sujet.
- Paiement natif hebdomadaire : État impérial15 %, Électorat impérial10 %, Lien impérial0 %. Un paiement par pacte, du sujet au suzerain, sur les revenus du sujet. Les descriptions et le paramétrage utilisent les mêmes taux.
- Infobulles de la liste : chaîne impériale distincte de l’annexion et de l’indépendance ; repli natif inchangé pour les autres types de sujets. Les États/électorats restent protégés contre une nouvelle diminution conduisant à l’annexion.

## Portée et sécurité

Les transitions individuelles concernent les pactes de sujets natifs impériaux. Les liens constitutionnels virtuels présents en1776 ne deviennent pas tous des sujets par cette correction. Les boutons de centralisation générale restent verrouillés et le prototype de succession isolé reste à valider. Aucun changement à ses fichiers ou à la procédure de transfert électif.

La diminution native d’un Lien est réservée à l’empereur, hors élection, pour un pays déjà admissible à la dépendance impériale. Les pays mixtes demeurent exclus du filtre conservateur existant. Les conditions natives de désir de liberté, délai et conflit sont conservées. Les effets d’augmentation conservent les règles natives d’approbation et de délai. Les unions personnelles et les types de sujets non impériaux gardent leurs effets natifs exacts, vérifiés par normalisation des branches.

Aucun nouveau type « province impériale » n’est créé. « État impérial » et « Électorat impérial » sont les deux noms retenus.

## Vérifications

{v['passed']}/{v['total']} contrôles statiques. {sum(g['tests'] for g in t.values())} tests réussis (contrats R1, centralisation courante et préservation Anhalt). Le compilateur complet reproduit {reproduction['passed']}/{reproduction['total']} fichiers installés. Les tests de contrat ont été mis à jour pour la nouvelle règle explicite de retour vers le Lien, sans modifier les anciennes attestations ni les baselines territoriales.

Les14 fichiers fonctionnels modifiés figurent dans VALIDATION.json. Aucun changement aux historiques, frontières, populations, bâtiments, PM, propriétés économiques, unités, gouvernements, lois, souverains ou icônes. Population mondiale{v['world_population']}. Les44 doublons RGB et12 références invalides préexistants restent identiques. Les anciens échecs de snapshots MAP déjà documentés ne sont pas requalifiés en réussites et ne sont pas réparés par cette passe.

**STATIC_PASS_RUNTIME_PENDING. Aucun test moteur exécuté.** Les captures du joueur sont des preuves des problèmes d’affichage précédents, pas une validation de ces nouveaux effets.

## À vérifier en jeu après redémarrage

1. Comparer la description du Lien dans la liste et dans un pacte diplomatique : même texte, mêmes liens d’infobulle.
2. Vérifier la flèche de diminution du Lien et la flèche d’augmentation des deux types centralisés. Pas d’annonce d’annexion ou d’indépendance dans cette chaîne.
3. Dans une partie de test avec de vrais sujets natifs impériaux déjà installés, diminuer un Lien ordinaire puis un Lien électoral : destination correcte, aucun territoire ni pays disparu, vote conservé.
4. Augmenter l’autonomie de chacun par le suzerain, puis tester une demande acceptée par le sujet : retour au Lien sous le même suzerain, privilège électoral conservé, pas d’indépendance.
5. Contrôler les contributions après une échéance hebdomadaire :15 % /10 % /0 %. Les revenus réels et les arrondis dépendent du moteur.
6. Tester un sujet vanilla : descriptions et effets de ses transitions restent natifs. Ne pas activer une centralisation de tout l’Empire pour ce contrôle.

Aucun commit, merge, push, changement de branche ou écriture de l’index. Aucune écriture dans l’installation du jeu. MAP-2S et ses conclusions cartographiques ne sont pas modifiés.

Recherche locale : un appel ColGrep-Agent abouti a retrouvé le verrou d’autonomie et la description du concept, lignes vérifiées. Les clés exactes et le comportement d’interface ont ensuite été contrôlés dans les fichiers installés du jeu. Aucune mesure exacte d’économie de quota.
'''
    h.patcher.OUT=OUT;h.patcher.emit({(OUT/'REPORT.md').relative_to(ROOT).as_posix():report},'REPORT.patch')

if __name__=='__main__':globals()[sys.argv[1]]()
