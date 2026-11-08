"""Add this design comparison to SERG tracking without changing any task."""
from pathlib import Path
import copy, json
import serg_silesia_layout_comparison as audit
import serg_closure_roadmap as roadmap

ROOT, CANON, OUT = audit.ROOT, audit.CANON, audit.OUT
REF = OUT.relative_to(ROOT).as_posix()

def main():
    old = audit.load('BEFORE_ROADMAP_STATE.json')
    current = roadmap.load_json(CANON/'ROADMAP_STATE.json')
    assert current == old, 'Tracking changed concurrently; reassess before writing'
    assert audit.runtime() == audit.load('BASELINE.json')['runtime'], 'Runtime changed concurrently'
    new = copy.deepcopy(current)
    new['prussian_silesia_comparison'] = dict(
        status='COMPARISON_COMPLETE_NO_FUNCTIONAL_CHANGE',
        authority='User answer: Comparer aussi une Silésie partagée',
        report=REF+'/REPORT.md',
        options=['A_CURRENT_AGGREGATE','B_SHARED_UPPER_SILESIA','C_SEPARATE_AUSTRIAN_SILESIA'],
        recommended_for_v1='A_CURRENT_AGGREGATE', user_selection=None,
        variants_b_c_installed=False, runtime_test_executed=False,
        approved_austrian_silesia_decision_preserved=True,
        next_independent_candidate='SC5-PRUSSIAN-WEST', next_candidate_started=False)
    p = roadmap.progress(new)
    assert p == roadmap.progress(current)
    assert current['events'][-1]['id'] == 'SERG-RM-0063'
    new['events'].append(dict(
        id='SERG-RM-0064', date='2026-11-05', kind='SILESIA_STATE_LAYOUT_COMPARISON_NO_INSTALL',
        scope_version='1.0.0', source=REF+'/REPORT.md', changes=[],
        before_weight=p['earned_weight'], after_weight=p['earned_weight'], total_weight=p['total_weight'],
        before_percent=p['percent'], after_percent=p['percent'],
        note='Comparaison demandée du découpage actuel, d’une Haute-Silésie partagée PRU/AUS et d’une région autrichienne distincte. Multiplicateur de valeur territoriale IA vérifié, effet diplomatique non mesuré. Aucun changement fonctionnel, aucune nouvelle option approuvée ; 81 tâches et reçus conservés. Candidate occidentale identifiée sans lancement.',
        evidence=[REF+'/CURRENT_INVENTORY.json',REF+'/AI_EVIDENCE.json',REF+'/PLAYER_TEST_PLAN.md']))
    assert (CANON/'ROADMAP_STATE.json').read_bytes() == (OUT/'BEFORE_ROADMAP_STATE.json').read_bytes()
    roadmap.write_json(CANON/'ROADMAP_STATE.json',new)
    summary = '''## Comparaison silésienne — 5 novembre 2026, aucune installation

À la demande du joueur, le découpage actuel est comparé à une Haute-Silésie partagée PRU/AUS et à une région autrichienne distincte. **Recommandation V1 : conserver l'actuel** ; aucune nouvelle option approuvée. Le facteur IA ×2 porte sur la valeur territoriale, pas une probabilité de guerre mesurée. [Comparaison et dépendances](SILESIA_STATE_LAYOUT_COMPARISON_2026_11_05/REPORT.md).

Les propriétaires, la carte et tous les fichiers fonctionnels sont inchangés. `SC2-AUSTRIAN-SILESIA` reste `NOT_APPLICABLE_VERIFIED` selon la décision antérieure ; `SC3-SILESIA-LUSATIA` demeure `BLOCKED` avec son noyau lusacien en attente du joueur. **93/235 = 39,57 %, 32/81**, aucun reçu ni point nouveau.

**Action joueur : [protocole groupé prussien existant](PRUSSIA_POLAND_2026_11_05/PLAYER_TEST_PROTOCOL.md).** Candidate indépendante suivante dans la priorité Prusse : `SC5-PRUSSIAN-WEST`, P1, NOT_STARTED, sans dépendance ; identifiée, non commencée ici. Les limites silésiennes non certifiées restent ouvertes ; aucune reprise de Teschen, micro-État ou Bavière. Les anciennes sections ci-dessous sont archivées dans leur contexte.

'''
    for name in ['ROADMAP.md','NEXT_ACTION.md','BLOCKERS.md']:
        prior = (OUT/('BEFORE_'+name)).read_bytes()
        assert (CANON/name).read_bytes() == prior, 'Concurrent change: '+name
        title, body = prior.split(b'\n',1)
        (CANON/name).write_bytes(title+b'\n\n'+summary.encode('utf-8')+body)
    name='PROGRESS_HISTORY.md'; prior=(OUT/('BEFORE_'+name)).read_bytes()
    assert (CANON/name).read_bytes()==prior
    addition='''

## SERG-RM-0064 — 5 novembre 2026 — Comparaison des régions silésiennes

Trois variantes comparées : agrégat actuel, Haute-Silésie partagée PRU/AUS, région autrichienne distincte. La règle IA ×2 pour une portion étrangère partagée ou revendiquée est confirmée dans le script effectif ; aucun effet moteur sur l’hostilité mesuré. Aucun fichier fonctionnel modifié, aucune nouvelle option approuvée, aucune attestation inventée. Décision SC2-AUSTRIAN-SILESIA et les 81 fiches intégralement conservées ; 93/235, 39,57 %, 32/81 inchangés. Les tests prussiens précédents restent attendus ; SC5-PRUSSIAN-WEST identifiée P1 sans dépendance, non commencée. [Comparaison](SILESIA_STATE_LAYOUT_COMPARISON_2026_11_05/REPORT.md).
'''
    (CANON/name).write_bytes(prior+addition.encode('utf-8'))
    assert (CANON/'PROGRESS_SNAPSHOT.json').read_bytes()==(OUT/'BEFORE_PROGRESS_SNAPSHOT.json').read_bytes()
    # Progress is identical, so the existing generated view is already current.
    assert roadmap.load_json(CANON/'PROGRESS_SNAPSHOT.json')==p
    print('Added SERG-RM-0064; all tasks and progress unchanged:',p['percent'])

if __name__=='__main__': main()
