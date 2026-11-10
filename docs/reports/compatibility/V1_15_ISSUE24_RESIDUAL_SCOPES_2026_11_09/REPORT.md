# Mission 24 — capitales et portées résiduelles, 9 novembre 2026

**IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION** pour quatre corrections techniques. Le parent 24 reste ouvert ; les arbitrages de frontières, les chaînes DLC et la sortie du hotfix ne sont pas acceptés par ce lot.

## Sélection et limites

Le joueur a demandé une nouvelle mission après l'acceptation groupée de 22/23/32/40/41 et les ajustements économiques suivants. Le tableau et les fiches ouvertes ont été relus ; le dernier échange de l'autre chat, « Audit migration 1.15 », confirme la livraison achevée de 41 et réserve l'IA 25 à Hawk. Ce sous-lot est déclaré dans 24 et dans CLAIM.md. Aucune mission différée américaine, aucun chantier 17/21, aucune opération Git ou écriture vanilla n'est lancé.

Les anciennes preuves de 24/39/40/41 restent historiques. Les deux lectures MAP_BEFORE/AFTER et QUALIFICATION_BEFORE/AFTER décrivent les fichiers de cette passe, après les derniers réglages du joueur. Le vanilla canonique consulté reste le jeu local 1.15.0.

## Corrections installées

| Source fonctionnelle | Changement borné | Justification technique |
| --- | --- | --- |
| `common/country_definitions/02_modded_countries.txt` | GR7 : capitale `STATE_BLUE_NILE` → `STATE_GREENLAND` | Le pays conserve la culture inuit et son type décentralisé ; son seul État possédé au départ est Greenland. Le Nil Bleu n'est pas dans ses possessions. Aucun chef-lieu municipal historique n'est inventé. |
| `common/history/countries/dio - diola.txt` | Ajouter le seul effet direct `set_capital = STATE_SENEGAL` dans le bloc initial DIO | Sa capitale native héritée est Sierra Leone, alors que le pays ne possède que Senegal. Toutes ses lois, technologies et autres instructions restent identiques ; le défaut natif n'est pas masqué ni son fichier entier copié. |
| `common/history/states/00_states.txt` | Retirer la seconde occurrence de `x26A0BA` dans la même liste ATB du Yukon | Les deux occurrences appartenaient au même pays, au même État et au même bloc ; une occurrence est conservée. Aucun ensemble de détenteurs n'est modifié. |
| Nouveau `common/scripted_effects/00_dynamic_state_names_europe.txt` | Masquage natif ciblé : une seule portée `s:STATE_LITHUANIA` → `s:STATE_KAUNAS` | Les deux régions ont exactement l'ID 153 et les mêmes 23 provinces. Le groupe géographique balte du mod contient déjà Kaunas. Le répartiteur de noms ciblait encore l'ancien identifiant absent. |

Le dernier fichier reprend le fichier canonique courant, avec tous les autres octets et les **141 définitions d'effets** conservés, hors ce seul identifiant de portée. L'auxiliaire `STATE_LITHUANIA_state_name_assign` reste un identifiant de fonction valide ; il n'est pas renommé. Ses conditions russe/polonaise/lituanienne, réinitialisations, noms FR/EN et noms de hubs restent natifs. Le contrôle « noms dynamiques désactivés » et les appels extérieurs sont inchangés.

Ce masquage devra être comparé à une prochaine mise à jour vanilla. Un premier candidat à directive REPLACE est conservé dans INSTALLATION_PLAN.json mais n'a jamais été installé ; le candidat final utilise le masquage de même chemin, sans hypothèse nouvelle sur une directive d'effet. Le plan installé est INSTALLATION_PLAN_R2.json.

## Qualification des autres alertes

- **PLC** : l'ancienne alerte de capitale est expliquée par son instruction initiale explicite `set_capital = STATE_GREATER_POLAND`. Aucune correction de ses données n'est nécessaire.
- **646 détenteurs initiaux** ont, après les deux corrections, un État de capitale cohérent avec leurs possessions dans le modèle limité aux définitions et instructions directes : 642 défauts et quatre overrides explicites. Avant : 641 défauts cohérents, trois overrides cohérents et deux capitales non possédées. Les effets auxiliaires/dynamiques et l'ordre moteur ne sont pas simulés.
- Les **13 écritures contradictoires restantes** sont non conditionnelles dans les sources : Kenya (2), Tanganyika (3), Mauritania (6), Eastern Himalayas (2). Les tableaux conservent les RGB, deux détenteurs, blocs et lignes. Cela confirme une contradiction littérale, sans certifier le propriétaire finalement retenu par le moteur ni choisir un propriétaire historique. Ces arbitrages restent au chantier cartographique 18.
- **Micronésie occidentale** : `xEF50C0` demeure sans instruction initiale d'attribution relevée, dans `STATE_WEST_MICRONESIA`. Ce n'est aucun des hubs déclarés de cet État. Aucun pays n'est créé et aucune attribution n'est inventée. L'intention historique et le chargement moteur restent à qualifier sous 18/24.

L'audit initial 24 reste volontairement inchangé. Il affiche encore les défauts de capitale PLC/DIO parce qu'il ne lit pas les overrides d'histoire ; le nouveau qualificateur conserve ces données puis les explique avec leurs sources. Aucun filtre n'efface indistinctement les conflits ou les conditions.

## Contrôles exécutés

- Nouvel outil en lecture seule `tools/compatibility/issue24_residual_scope_audit.py` : **8/8 cas de classification** réussis. Il distingue répétition dans une liste, répétition dans deux blocs, propriétaires/États différents, alternatives conditionnelles, capitale possédée, override correct et override incorrect. Une garde ne devient jamais une acceptation.
- **18/18 contrôles ciblés** passent : toutes les paires État/propriétaire de chaque province sont conservées ; une seule occurrence brute est retirée ; le Yukon reste à ATB ; les candidats installés correspondent aux empreintes ; toutes les différences des trois fichiers existants sont dans les spans autorisés ; seul l'identifiant prévu diffère du masque natif ; les 23 provinces et l'ID 153 sont identiques.
- Somme des jetons d'attribution : **41 085 → 41 084** ; provinces distinctes attribuées : **41 071 → 41 071**. La différence d'un jeton est le doublon du même propriétaire, pas une province supprimée.
- Audit complet 24 avant/après : **783 régions d'État, 677 terrestres, 142 régions stratégiques, 1 074 pays**, aucun changement d'inventaire ou erreur de lecture. Alertes d'attribution répétée **14 → 13**. Le statut global reste **FINDINGS_STATIC_ONLY**.
- **2 519 sources préexistantes protégées** : seules les trois sources autorisées diffèrent. Un fichier fonctionnel est ajouté et l'outil de qualification est nouveau ; aucun autre fichier de jeu n'est réécrit. Les dix fichiers économiques du dernier réglage, les sources IA/journaux, lois, technologies, ressources, provinces et populations restent identiques.
- Variation de population : **0**. Tous les fichiers sources de populations sont byte-identiques ; aucune redistribution ou nouvelle estimation historique n'est effectuée. La géométrie et les ensembles d'attribution de provinces sont conservés.

Les seuls chemins d'écriture sont ceux du plan, le nouvel outil et ce dossier de preuves. Aucun Git, vanilla, progression WORLD/SERG, diplomatie ou attestation humaine n'est écrit. Le contrôle de fichiers ne vaut pas rendu, chargement de capitale décentralisée ou bon déclenchement des noms dynamiques en partie.

## Suite

Le protocole moteur est dans RUNTIME_PROTOCOL.md. Le lot est prêt à relire et tester ; aucun test humain n'est demandé entre chaque correction. Le parent 24 ne doit pas être fermé sur ces résultats statiques. Pour la carte, conserver les treize conflits et la province de Micronésie comme points à arbitrer, sans réaffectation automatique.

Preuves : SOURCE_BASELINE.json, MAP_BEFORE/AFTER.json, QUALIFICATION_BEFORE/AFTER.json, INSTALLATION_PLAN_R2.json, before/, candidate/, candidate_R2/, INSTALLATION_RECEIPT.json, TARGETED_VALIDATION.json et SOURCE_PROTECTION.json.
