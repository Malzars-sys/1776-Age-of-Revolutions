"""Record preservation and a readable report for the completed user series."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json

HERE = Path(__file__).resolve().parent
OUT = HERE / 'MANUAL_RESULTS_2026_11_17'
read = lambda p: json.loads(p.read_text(encoding='utf-8-sig'))

before = read(HERE / 'BEFORE.json')
current = read(HERE / 'POST_MANUAL_2026_11_17.json')
analysis = read(OUT / 'ANALYSIS.json')
checks = {}
for name in ('protectedFiles', 'protectedNormal'):
    checks[name] = dict(compared=len(before[name]), changed=[key for key, value in before[name].items()
                      if current[name].get(key) != value])
checks['installations'] = dict(equal=before['installations'] == current['installations'])
checks['frozen_arms'] = dict(equal=before['armChecks'] == current['armChecks'])
checks['variants'] = dict(equal=before['variants'] == current['variants'])
checks['normal_playsets'] = current['dbComparisons']
passed = all(not checks[k]['changed'] for k in ('protectedFiles', 'protectedNormal')) and all(
    checks[k]['equal'] for k in ('installations', 'frozen_arms', 'variants')) and all(
    item['equalIgnoringSyncTimestamp'] for item in current['dbComparisons'].values())
receipt = dict(recorded_utc=datetime.now(timezone.utc).isoformat(),
               status='PASS' if passed else 'FINDINGS', checks=checks,
               reference='BEFORE.json', current='POST_MANUAL_2026_11_17.json',
               working_GUI_installed=False, experimental_merge=False)
with (OUT / 'PRESERVATION_COMPARE.json').open('x', encoding='utf-8') as stream:
    json.dump(receipt, stream, indent=2, ensure_ascii=False)

labels = {('closed_paused', 'none'): 'Carte en pause',
          ('tree_stationary', 'production'): 'Production fixe',
          ('tree_stationary', 'military'): 'Militaire fixe',
          ('tree_stationary', 'society'): 'Société fixe',
          ('tree_pan', 'society'): 'Société, un glissement'}
order = ['CONTROL1', 'COMPACT1', 'COMPACT2', 'CONTROL2']
fps_rows, cpu_rows = [], []
for item in analysis['comparisons']:
    title = labels[(item['phase'], item['category'])]
    fps_rows.append('| ' + title + ' | ' + ' | '.join(str(int(item['fps'][k])) for k in order) + ' |')
    cpu_rows.append('| ' + title + ' | ' + ' | '.join(f"{item['cpu_machine_percent'][k]:.2f}".replace('.', ',') for k in order) + ' |')
durations = [r['seconds'] for r in analysis['measurements']]
report = f'''# Issue 54 — comparaison manuelle témoin / COMPACT terminée

Les deux passages COMPACT améliorent nettement les FPS déclarés de l'arbre par rapport aux deux témoins. Le retour au témoin restaure la lenteur. **Le gain est reproduit dans cette configuration Steam 1.15.1 ; aucun correctif n'a été installé dans le mod principal.**

## Résultats FPS

Valeurs ponctuelles saisies par le joueur à partir du compteur affiché, avant le délai de cinq secondes de retour au jeu. Ce ne sont ni des moyennes continues, ni des centiles de temps de trame. Les vues sont préparées et déclarées par le joueur ; aucune capture d'écran automatique de ces phases n'est revendiquée.

| Vue | Témoin 1 | COMPACT 1 | COMPACT 2 | Témoin 2 |
| --- | ---: | ---: | ---: | ---: |
{chr(10).join(fps_rows)}

Pour chacune des trois branches fixes et du glissement Société, le plus faible des deux relevés COMPACT reste supérieur au plus élevé des deux témoins. La variation du témoin carte (60 puis 16 FPS) et celle des deux passages COMPACT montrent que les conditions système ou de vue n'étaient pas parfaitement identiques. Aucun facteur précis d'accélération ni intervalle statistique n'est certifié. Le glissement est unique et approximatif, pas un défilement continu instrumenté.

## CPU recalculé depuis les CSV

Pourcentage du processus rapporté à la capacité totale des seize processeurs logiques, pondéré par la somme des intervalles effectivement mesurés. Les virgules décimales des CSV français sont traitées explicitement.

| Vue | Témoin 1 | COMPACT 1 | COMPACT 2 | Témoin 2 |
| --- | ---: | ---: | ---: | ---: |
{chr(10).join(cpu_rows)}

COMPACT utilise une charge CPU totale comparable ou légèrement supérieure dans l'arbre, tout en affichant davantage de FPS. La baisse du CPU n'est donc pas le critère du gain de fluidité. L'échantillonneur lui-même n'est pas soustrait.

Vingt captures réelles sont présentes, quatorze échantillons chacune : 280 échantillons, {min(durations):.3f} à {max(durations):.3f} secondes par capture. Les horloges, la durée, le délai de retour au jeu, les noms de vues, les données non synthétiques, les formules CPU et les durées de vie des processus ont été contrôlés. **{analysis['passed']}/{analysis['total']} contrôles des fichiers de mesure réussissent.** Cela ne remplace pas l'observation humaine des vues. La tentative antérieure interrompue et les tests synthétiques SELFTEST sont exclus.

## Environnement effectif et limites

Les quatre processus sont distincts, dans l'ordre témoin–COMPACT–COMPACT–témoin, sur le même profil isolé, le même exécutable Steam 1.15.1, les mêmes réglages enregistrés et la même sauvegarde copiée France au 1er janvier 1776. Les contrôles d'empreinte sont faits avant chaque lancement par l'assistant et revérifiés actuellement. Pays, date, pause, zoom et vue sont déclarés par le joueur ; ils n'ont pas été revérifiés image par image par l'agent dans cette série.

Les journaux de lancement correspondants ont été sélectionnés par leur horloge, en excluant leurs rotations historiques. Ils confirment exactement la bonne copie A_current ou expression_probe selon le passage et le même DLC effectivement monté : `dlc/dlc001_preorder`, bande-son uniquement. Les quatre lancements directs signalent l'échec d'initialisation de l'API Steam. Il ne s'agit pas d'une session Steam authentifiée ni d'un essai avec DLC de gameplay.

Aucune erreur de liaison du GUI technologique n'est trouvée par le filtre dédié dans les quatre journaux d'erreurs. Les autres erreurs et avertissements hérités du mod sont conservés, sans prétendre qu'ils ont tous disparu. Les reçus de sortie -1 proviennent du nettoyage borné de l'assistant après les captures, pas d'un crash prouvé pendant la mesure. Les quatre processus possédés ont leur reçu de sortie.

La latence exacte d'ouverture, les temps de trame individuels, fréquences, températures et activité des autres applications ne sont pas mesurés. La version locale 1.15.0 avec DLC reste hors de cette comparaison et ne reçoit pas de validation par extrapolation.

## Diagnostic et correctif prêt à examiner

Le témoin et COMPACT ne diffèrent que dans les deux expressions de visibilité de `gui/tech_tree.gui`. Le reste des copies, dont toutes les données technologiques, reste identique à la référence figée. La comparaison répétée met donc en cause le coût de ces filtres dans ce contexte, sous les limites du protocole manuel. Aucun profil interne par fonction ou comptage réel des appels par image n'est disponible.

COMPACT utilise l'indicateur natif de recherche possible, conserve huit exceptions non recherchables affichées et les deux cartes forcées, et réduit les références textuelles GetTechnology de 42 à 8 pour les lignes, de 43 à 10 pour les cartes. Ces comptes textuels ne sont pas des comptes d'appels réellement exécutés par image.

Le contrôle statique réexécuté sur les définitions courantes passe 1168 cas, deux témoins négatifs, 291 technologies et 392 connexions. Il maintient les quarante alias masqués et les deux cartes forcées. Voir `VISIBILITY_RECHECK.json`. Les autres fichiers, les prérequis, coûts, déblocages et technologies initiales ne sont pas modifiés.

Le joueur répond dans cette conversation à la question sur d'éventuelles technologies manquantes, liens anormaux ou boutons cassés : **« Aucun problème remarqué »**. Ce retour est conservé comme observation humaine limitée aux deux passages COMPACT. Il ne certifie pas une visite exhaustive de tous les nœuds ni une simulation longue.

`COMPACT_REVIEW_ONLY.patch` contient les deux changements proposés, sans application au mod principal. Son contenu provient exactement du candidat mesuré. Aucun changement Git d'écriture, commit, PR, fusion ou publication n'est effectué. L'intégration au mod normal reste une décision explicite distincte.

## Préservation

Le reçu `PRESERVATION_COMPARE.json` indique **{receipt['status']}**. Les {checks['protectedFiles']['compared']} fichiers surveillés du dépôt, index Git inclus, et les {checks['protectedNormal']['compared']} fichiers surveillés du profil normal et des sauvegardes conservent leurs empreintes par rapport au début de la reprise. Les copies A/B/C et le probe, les variantes, les deux exécutables et les GUI vanilla conservent leurs empreintes. Les sept playsets, onze liens de mods et cinquante et un liens DLC restent identiques après exclusion du seul champ de synchronisation.

Le chantier Russie–Petite Horde kazakhe reste présent dans ses trois fichiers du mod principal et n'est pas inclus dans la correction de performance. Aucun ancien fichier normal n'a été restauré.

Sources primaires : `../MANUAL_20261117T000322802Z/`, `ANALYSIS.json`, `VISIBILITY_RECHECK.json`, `PRESERVATION_COMPARE.json` et le retour du joueur dans cette conversation. Le correctif est prêt pour la décision d'intégration ; il n'est pas déjà installé.
'''
with (OUT / 'REPORT_FR.md').open('x', encoding='utf-8') as stream:
    stream.write(report)
manifest = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in OUT.iterdir() if p.is_file()}
with (OUT / 'ARTIFACT_HASHES.json').open('x', encoding='utf-8') as stream:
    json.dump(manifest, stream, indent=2)
print(json.dumps(dict(preservation=receipt['status'], changed_repository=checks['protectedFiles']['changed'],
                     changed_normal=checks['protectedNormal']['changed'], report=str(OUT / 'REPORT_FR.md')), indent=2))
