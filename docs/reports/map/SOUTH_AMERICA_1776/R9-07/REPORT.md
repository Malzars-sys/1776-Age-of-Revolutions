# R9-07 — Grand Chaco et anomalies majeures de l'inventaire

**IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION — 1er janvier 1776.** Installé le 28 octobre 2026. Essais en jeu toujours différés à la demande du joueur.

## Corrections installées

| Secteur | Changement | Provinces |
|---|---|---:|
| San Jerónimo del Rey | Réduction rattachée à SC4, avec un raccord terrestre minimal | 2 |
| Malouines | Deux cellules de l'archipel, GBR → SC4 ; secteur nord-ouest et autres îles composites réservés | 2 |
| Intérieur méridional de Cuyo et des Pampas | SC4 → agrégat autochtone PAT, noyaux coloniaux et bâtiments préservés | 26 |

**30 changements de propriétaire ; aucun nouveau RGB, State_ID ou TAG.** GNI est nommé « Peuples du Chaco » et PAT « Peuples mapuche et pampéens », afin d'expliciter leur fonction d'agrégats régionaux. Les subdivisions politiques indigènes ne sont pas inventées. Concepción et Belén sont déjà du bon côté ; San Fernando, abandonné avant 1776, reste autonome.

Les **12 686 habitants déjà codés patagonian** dans les deux régions du complément sont transférés intacts à PAT, sans changer leurs identités. Les **115 habitants ajoutés à Puerto Soledad** sont un proxy documentaire de 1774, pas un recensement de janvier 1776. Variation mondiale de cette livraison : **+115**. Aucun stock existant supprimé ou artificiellement compensé. Les 10 469 Britanniques de la région insulaire composite restent sur sa portion GBR ; leur démographie détaillée demeure réservée.

Tous les bâtiments préexistants sont conservés. **Un seul port traditionnel de niveau 1** est ajouté pour la desserte des Malouines, sur le hub existant. Pas de modernisation technologique distribuée, de nouvelle unité, ou de déplacement des locators. Les noms modernes des hubs insulaires sont remplacés par Puerto Soledad et des désignations descriptives. Le port et la petite population nécessitent une vérification effective d'emploi et de marché.

## Fichiers de jeu

1. `common/history/states/00_states.txt` — uniquement Santa Fe, South Atlantic Islands, La Pampa et Rio Negro.
2. `common/history/pops/07_south_america.txt` — ajout de 115 dans la portion SC4 insulaire et réattribution de deux cohortes existantes.
3. `common/history/buildings/1776_r907_malvinas_port.txt` — nouveau port de desserte.
4. `localization/french/replace/1776_r907_chaco_malvinas_l_french.yml`.
5. `localization/english/replace/1776_r907_chaco_malvinas_l_english.yml`.
6. `localization/french/replace/1776_r907_pampas_l_french.yml`.
7. `localization/english/replace/1776_r907_pampas_l_english.yml`.
8. `common/scripted_effects/1776_r907_malvinas_names.txt` — noms des hubs limités à la portion possédée par SC4.
9. `common/on_actions/17_1776_r907_malvinas_names.txt` — initialisation et mise à jour lors de création/transfert d'État.

Outils : `tools/r907.py`, `tools/r907_pampas.py`, `tools/r907_survey.py`, `tools/r907_finalize.py`. L'installation a deux préparations successives, toutes deux prises depuis le workspace courant, puis les amendements bornés de sécurité et de noms. Les fichiers avant/patch, empreintes et preuves de chaque phase sont conservés. **Ne pas rejouer le premier patch sur le workspace final.** Les noms de Puerto Soledad ne sont pas des substitutions globales des noms régionaux : le script s'applique exclusivement à la portion SC4 et préserve les noms hérités de la portion GBR.

## Contrôles

- Première phase : **24/24**, `VALIDATION.json` ; complément : **19/19**, `PAMPAS_CUYO/VALIDATION.json`.
- Comparaison finale combinée : **34/34 contrôles réussis**, voir `FINAL_VALIDATION.json`. Les chaînes d'empreintes et les **30 transferts finaux** sont confrontés au contenu courant, sans effacer les preuves intermédiaires.
- Pas de province nouvellement orpheline ou doublement attribuée. Autres blocs d'États et populations inchangés ; effectifs conservés hors ajout sourcé de 115.
- Capitales et hubs affectés, référence des RGB, terres franchissables, chemin terrestre de San Jerónimo, présence du port et références de PM contrôlés. Aucun changement du bitmap, des State Regions ou des locators.
- Profils technologiques, unités, pactes et bâtiments existants préservés. Témoins CENTRAL et R9 antérieurs contrôlés. Les changements concurrents présents avant préparation ne sont pas restaurés depuis une ancienne baseline.
- Audit technologique comparatif : **SC4 12, GNI 2, GBR 6, PAT 2 signalements**, soit **22 préexistants inchangés**, aucun ajouté ou supprimé. Le code retour d'échec statique hérité est conservé ; pas de présentation trompeuse d'un audit global vert. Le bâtiment portuaire ajouté et ses deux PM n'exigent aucune technologie absente.
- Localisations FR/EN avec BOM et clés vérifiées ; trois aperçus calculés depuis les fichiers installés puis examinés visuellement.

**Aucune validation moteur ou humaine.** Chargement, marchés, emplois, ravitaillement, noms affichés et sauvegarde/rechargement restent à tester selon [RUNTIME_PROTOCOL.md](RUNTIME_PROTOCOL.md).

## Cartes et réserves

[Grand Chaco](R9_07_CHACO_AVANT_APRES.png) · [Malouines](R9_07_MALOUINES_AVANT_APRES.png) · [Cuyo–Pampas](PAMPAS_CUYO/R9_07_CUYO_PAMPAS_AVANT_APRES.png).

Les transferts du Chaco et de Cuyo sont des approximations par cellules entières. Le raccord de San Jerónimo répond à la règle de jouabilité des postes reliés ; il n'établit pas une administration coloniale continue de chaque terrain. Les marges conservées ne sont pas certifiées. Les lectures britannique et espagnole de l'évacuation occidentale des Malouines divergent dans leur chronologie fine ; la revendication britannique reste présente.

**Amendement de sécurité final :** la première installation transférait aussi `x5E9DB3`. Le contrôle élargi a révélé qu'elle était la dernière cellule jouable restant disponible pour la portion GBR et sa population héritée ; les quatre îles éloignées sont marquées infranchissables dans les définitions actuelles. Ce seul transfert a donc été annulé par un patch borné, sans restaurer le fichier partagé. `x5E9DB3`, comprenant le secteur nord-ouest associé à Port Egmont, reste provisoirement GBR ; le maintien n'est pas une certification d'administration britannique en janvier 1776. La question doit être reprise avec la région insulaire composite et ses hubs. Les tests de première phase et de complément décrivent leurs versions intermédiaires ; `SAFETY_AMENDMENT.json`, `FINAL_VALIDATION.json` et `FINAL_PATCH_MANIFEST.json` décrivent la livraison effective. Le contrôle final impose désormais une terre **jouable** pour chaque portion peuplée affectée.

[SOURCES.md](SOURCES.md) distingue documents lus, notices et limites. **La Paz/Moxos, Santa Cruz–Chiquitos et Guaviare/haut Orénoque restent des anomalies importantes à traiter avec un mapping spécialisé**, ainsi que les réserves héritées. Ni ce lot ni l'Amérique du Sud ne sont déclarés historiquement clos. Aucune vague supplémentaire n'est lancée automatiquement.

## ColGrep

Deux lancements de l'exécutable : premier refusé par le verrou du cache hors du workspace, second abouti avec le cache existant autorisé, `--agent`, code retour 0. Trois plages retournées et vérifiées : deux dossiers Chaco utiles et un dossier mapuche hors cible, déjà traité en R9-04. Aucun changement du modèle ou de l'intégration, aucune reconstruction complète de l'index.

Le temps total du processus n'a pas été instrumenté de manière fiable ; il n'est pas reconstitué artificiellement. Aucun compteur précis de tokens Codex par recherche, aucun total exhaustif des recherches classiques et aucune télémétrie GPU indépendante sont disponibles. Cette délégation a fourni des pistes, mais pas les sources décisives ni le mapping. **Pas d'économie exacte de quota revendiquée.** Commande et vérification dans `COLGREP_METRICS.json` et `COLGREP_VERIFIED.json`.

**Aucun commit, push, merge, rebase ou changement du vanilla.**
