# Mission 21 — proportions de population

**IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION**, 8 novembre 2026. Premier lot de reprise de la mission 21 : **quatre appels, huit lignes, trois fichiers**. La mission générale reste ouverte et son statut Project a été passé de Backlog à **In progress**. Aucun commit, push, changement de branche, merge ni fichier vanilla modifié.

## Diagnostic et correction

Le journal d’erreurs existant signale `pop_type_percent_country trigger [ Invalid pop type in scope ]` aux lignes 527 et 6289 du fichier de mouvements idéologiques du mod. La capture d’entrée contient respectivement **419 et 310 occurrences** ; ce sont des répétitions de deux signatures, pas 729 bugs distincts. L’empreinte du journal et un exemple de chaque message sont conservés dans le lot. Aucun nouveau lancement n’a été effectué pour cette livraison ; ces décomptes ne constituent pas un résultat après correctif.

Le contrat observé dans les trois fichiers natifs correspondants de `C:/Games/Victoria 3/game` est :

```text
pop_type_percent_country = {
    target = pop_type:peasants
    value > 0.25
}
```

L’ancien `pop_type = ...` ne fournit pas la cible typée attendue ; l’ancienne clé de comparaison `percent` devient `value`. L’inventaire a trouvé deux autres appels dans le même ancien format. Chaque appel a été comparé à son propre témoin natif, avec le même type de population, opérateur et seuil.

| Objet / ancien site | Contexte conservé | Condition après migration |
| --- | --- | --- |
| `movement_anti_slavery`, mouvements idéologiques :527 | Facteur supplémentaire de radicalité, pays `owner ?=` | Esclaves strictement au-dessus de 0 % |
| `movement_land_reform`, même fichier :6289 | Condition de création du mouvement | Paysans strictement au-dessus de 25 % |
| `agitators_election_events.13`, événements d’élection :1903 | Condition de l’événement pays | Paysans à au moins 35 % |
| `je_egalitarian_society`, objectifs égalitaires :162 | Condition existante dans `complete` | Paysans strictement en dessous de 10 % |

Les fractions **0 / 0,25 / 0,35 / 0,1** et les opérateurs **> / > / >= / <** sont conservés. Les scopes, autres conditions, facteurs de radicalité, effets d’événements, prérequis 1776 et déclarations de journal sont inchangés. Aucune loi, population ou technologie de départ n’est ajoutée ou modifiée.

## Vérifications exécutées

- Parsing des trois fichiers avant/après ; les quatre payloads migrés correspondent exactement aux payloads natifs.
- Types `slaves` et `peasants` présents dans les fournisseurs natifs de professions.
- Inversion bornée des huit substitutions reproduisant exactement chaque fichier avant intervention : octets hors champs autorisés, BOM et fins de ligne préservés.
- Inventaire des déclarations hors commentaires sous `common/` et `events/` : **sept appels**, tous au format `target` / `value` ; les trois appels d’urbanisation étaient déjà corrigés et restent inchangés. Les exemples commentés de `test_events.txt` sont exclus.
- **2 482 autres fichiers de scripts/données** contrôlés par empreinte ; aucune différence concurrente observée pendant cette exécution, notamment dans les lois, ressources de cuivre, objectifs de guerre et sélection des objectifs.

Les commandes exécutées sont des scripts Python en entrée standard, via le Python du runtime (`python -B -`) et le parseur en lecture seule de `tools/validate_diplomacy_ottoman_1776.py`. Aucun outil de correction globale ni remplacement aveugle n’a été lancé. `BASELINE.json` fournit les snapshots et le mappage précis des quatre appels ; `CHANGES.patch` contient les huit lignes ; `VALIDATION.json` décrit les fichiers installés et l’inventaire final.

## Limite explicite du journal d’égalité

Le fichier `00_player_objectives_egalitarian_society.txt` conserve **14 champs directs de conclusion hérités**, relevés dans `VALIDATION.json`. Ce lot corrige seulement l’argumentaire du trigger. Il **ne migre pas** ses `complete/on_complete/...` vers les outcomes 1.15 et ne rétablit donc pas à lui seul les conclusions de ce journal. Cette dépendance reste dans la mission **27**. Aucune conclusion ni effet n’a été recopié depuis le scénario vanilla.

## Essai moteur à réaliser

1. Relancer le mod livré et créer une nouvelle partie en 1776. Noter build, playset et DLC réellement chargés. Conserver les nouveaux logs distincts de la capture d’entrée.
2. Examiner le facteur de radicalité du mouvement antiesclavagiste dans un pays avec esclaves puis dans un pays sans esclaves. Vérifier le pays évalué et l’absence des anciennes erreurs de cible.
3. Examiner le mouvement de réforme agraire et ses conditions avec une proportion paysanne au-dessus puis au-dessous de 25 %. À 25 % exactement, le test reste faux. Les autres conditions d’apparition doivent aussi être réunies ; ne pas attribuer leur refus à ce seul trigger.
4. Dans une copie de test appropriée, vérifier l’éligibilité de `agitators_election_events.13` autour de 35 %, en conservant ses conditions et scopes d’agitateur. Ne pas forcer l’événement sans les scopes sauvegardés attendus. Aucune disponibilité de cet événement dès 1776 n’est revendiquée.
5. Après migration indépendante des conclusions dans la mission 27, tester le journal égalitaire autour de 10 %, avec ses autres conditions de niveau de vie et alphabétisation. Ne pas prendre un `complete` encore hérité pour un outcome fonctionnel.
6. Comparer les logs, puis sauvegarder/recharger une copie de test et vérifier les mouvements suivis. Relever les observations et durées réelles ; aucun résultat moteur ou reçu humain n’est encore fourni.

Les erreurs de culture ou de religion visibles dans le même journal sont d’autres signatures et ne sont pas annoncées comme corrigées par ce lot. Le statut Done attend les validations nécessaires ; ce lot ne clôt pas la mission générale 21.
