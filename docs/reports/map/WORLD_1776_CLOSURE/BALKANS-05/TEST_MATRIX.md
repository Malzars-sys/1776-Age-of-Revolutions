# B05 — Tests exécutés et limites

- `python tools/validate_starting_technology_1776.py --tag TUR --output .../TECH_BEFORE.json` : sortie 1, FAIL_STATIC, trois constats préexistants.
- `python tools/world1776_balkans05.py --apply` : installation unique bornée avec empreinte immédiatement avant écriture ; refuse une seconde application.
- Même audit vers TECH_AFTER.json : sortie 1, trois constats identiques, aucun nouveau type ou grant.
- `python tools/world1776_balkans05.py --validate` : première exécution 50/52, deux différences tuples/listes dans le comparateur ; preuve brute conservée. Après normalisation JSON du comparateur, **52/52**, sortie 0.

Contrôles : reconstruction exacte des cinq fichiers, extérieur de TUR identique, effectifs mondiaux par pays/région/type/service, anciennes formations/personnages/affectations, références, scopes sans collision, traits sans bonus, ressources d’interface natives, clés FR/EN uniques avec BOM, propriétaires et POPs inchangés, empreintes hors lot et anciennes preuves, état Git identique, constats technologiques avant/après identiques.

Limites : aucun moteur lancé, aucune assertion de budget ou de contrôle administratif effectif. Le contrat technologique FAIL_STATIC n’est pas renommé PASS ; son absence d’aggravation est la seule assertion correspondante du lot. Aucun test hérité ni reçu humain n’est réécrit.
