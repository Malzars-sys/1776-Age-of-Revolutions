# R9-06 — Guyanes et La Guajira

**IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION — référence : 1er janvier 1776.** Installation du 28 octobre 2026 ; contrôles joueur différés à sa demande. Les statuts et preuves des lots précédents sont conservés. Ce lot corrige des noyaux étayés ; il ne certifie pas toutes les frontières du nord du continent.

## Résultat installé

- **Wayuu : 2 provinces d'Antioquia, `xC564C3` et `xF2F0CC`, SC2 → WYU.** Le pays déjà défini dans le jeu est réactivé avec un profil initial explicite. Riohacha et la province mixte de Sinamaica/Maracaibo restent espagnols.
- **Fort Nassau / Berbice : `x7B4B5E`, AP7 → NET.** Le noyau néerlandais est rétabli sans inventer une colonie britannique ou une forteresse construite de toutes pièces.
- **Approuague : `x439BC2`, AP7 → FRA.** Les établissements français attestés avant 1776 sont reliés à la portion française existante.
- **Forêts profondes : `x148FB5` et `x9F0090`, FRA → AP7 ; `xC2E46E`, NET → AP7.** Les limites internes des peuples ne sont pas inventées.
- **Double attribution `x6C6251` résolue : NET seul**, en retirant l'inscription AP7 redondante. Ce défaut avait été signalé dès MAP0.

**7 provinces réattribuées et 1 double attribution corrigée. Aucun nouveau RGB, pixel ou State_ID.** Aucun nouveau identifiant national : WYU existait déjà. Un emblème générique et son profil de départ sont ajoutés pour sa réactivation.

[Avant/après de La Guajira](R9_06_GUAJIRA_AVANT_APRES.png) · [Avant/après des Guyanes](R9_06_GUYANES_AVANT_APRES.png) · [Sources et limites](SOURCES.md).

## Populations et bâtiments

**7 600 habitants guajiro existants passent de SC2 à WYU dans Antioquia**, sans changement de culture, de religion explicite ou de statut. Tous les effectifs régionaux et mondiaux restent identiques. Il s'agit d'une réattribution de données initiales, pas d'une migration ou d'un recensement neuf.

Les stocks par propriétaire des Guyanes restent inchangés : aucun décompte fiable à la province ne justifie leur redistribution. Les trois propriétaires conservent des portions habitées. Les 2 536 guajiro de Zulia ne sont pas artificiellement déplacés à travers une frontière régionale. La démographie fine, les populations marronnes et les incohérences éventuelles de statut servile dans les données héritées restent à traiter séparément.

**Tous les bâtiments, niveaux, PM, formations militaires et autres profils existants sont conservés.** Aucune nouvelle caserne, usine ou modernisation européenne n'est ajoutée.

## Fichiers du jeu modifiés ou ajoutés

1. `common/history/states/00_states.txt` — seuls les blocs Antioquia et Guayana : propriétaires, retrait du doublon et revendication SC2 sur sa région.
2. `common/history/pops/07_south_america.txt` — seule la cohorte guajiro d'Antioquia.
3. `common/history/countries/1776_r906_wayuu.txt` — transformation alimentaire et lois centrales explicitement initialisées.
4. `common/flag_definitions/1776_r906_wayuu.txt`.
5. `common/coat_of_arms/coat_of_arms/1776_r906_wayuu.txt` — emblème générique, sans prétention à un drapeau historique.

Les noms WYU français/anglais existants sont réutilisés. Ni les définitions nationales ni les fichiers de localisation partagés ne sont modifiés. Outil reproductible : `tools/r906.py` avec préparation, application gardée par empreintes, vérification et aperçus. Les baselines, fichiers avant/patch et manifestes sont conservés ; ne pas les appliquer aveuglément sur un workspace ultérieur.

## Vérifications

`python tools/r906.py --verify` : **25/25 contrôles ciblés réussis**, voir [VALIDATION.json](VALIDATION.json).

- Syntaxe, seuls changements autorisés, appartenance des RGB, aucun nouvel orphelin ni doublon ; le seul compte d'attribution diminué est celui du doublon résolu.
- Tous les blocs d'États hors Antioquia/Guayana et toutes les autres populations sont identiques. La cohorte de 7 600 est transférée intacte ; les effectifs et identités régionales sont conservés.
- Capitales et portions possédées, profil WYU décentralisé, lois, ressources du drapeau, noms français/anglais hérités vérifiés.
- **Trajets de pixels de terre** entre la province de Nassau et le noyau néerlandais, et entre l'Approuague et Cayenne, sans traverser mer, provinces infranchissables ou barrières d'adjacence. [Témoins](LAND_WITNESSES.json). Cela ne certifie pas le calcul de marché ni l'accès militaire du moteur.
- Bitmap, régions, terrains, locators, tous les bâtiments et profils nationaux préexistants, diplomatie et unités conservés depuis la préparation. Témoins R9-03/04/05 et CENTRAL intacts. Aucun changement runtime non listé constaté depuis la préparation.
- Audit technologique : **WYU PASS_STATIC_ONLY, aucun signalement**. NET 11, FRA 6, AP7 2 et SC2 19 signalements : **38 préexistants, aucun ajouté ou retiré**. Ces quatre pays restent `FAIL_STATIC` pour cette dette héritée ; code retour 1 conservé. [Comparaison](TECH_COMPARISON.json).
- Deux aperçus calculés depuis les propriétaires installés et le bitmap courant ; examen visuel avant livraison.

**Contrôle final de concurrence :** après cette exécution des 25 contrôles, une autre passe a modifié Madagascar et ses dépendances. Le fichier partagé des États a donc une nouvelle empreinte globale. La comparaison par blocs avec le patch R9-06 ne relève que `STATE_NORTH_MADAGASCAR` et `STATE_SOUTH_MADAGASCAR` : Antioquia, Guayana et tous les autres blocs restent identiques à la livraison. Les quatre autres fichiers R9-06 correspondent toujours exactement aux empreintes installées. Ces travaux concurrents sont conservés et inventoriés dans `CLOSURE_CHECK.json` et `CONCURRENT_AFTER_VALIDATION.json` ; ils ne sont ni certifiés par les 25 contrôles antérieurs ni attribués à cette passe. Aucun fichier partagé n'est restauré depuis la baseline.

**Aucune nouvelle partie ou simulation effectuée.** Suivre [RUNTIME_PROTOCOL.md](RUNTIME_PROTOCOL.md) lors des contrôles différés. Les tests statiques ne sont pas une validation en jeu.

## Réserves et suite

Restent ouverts : profondeur exacte des colonies, Pomeroon/Moruca/Barima, ancien Kykoveral, pouvoirs marrons du Suriname/Maroni, frontières entre peuples, secteurs mixtes autour de Sinamaica, détail de l'Oyapock et de l'Orénoque. Les marges gardées ne sont pas déclarées uniformément administrées. Les 7 transferts de ce noyau ne représentent pas un audit cadastral exhaustif.

La feuille de route propose ensuite R9-07 — Grand Chaco et marges intérieures ; son ouverture demande une instruction distincte. Aucune écriture Git, aucun commit/push ni modification du vanilla dans cette mission.

## ColGrep et accès aux sources

Un appel local `colgrep.exe --agent`, limité au dossier MAP1, a abouti en **234,66 s — environ 3 min 55 s**, code retour 0. Commande exacte et temps : `COLGREP_METRICS.json` ; sortie complète : `COLGREP_SEARCH.txt`. **4 chemins/plages ont été vérifiés**, tous existants. Le dossier des colonies néerlandaises est pertinent, mais l'agent ne remplace ni le contrôle des RGB ni la recherche spécifique sur les Wayuu. Aucun compteur fiable de tokens Codex par recherche n'est fourni ; les recherches classiques n'ont pas été instrumentées intégralement. Aucune économie exacte de quota n'est revendiquée. Le modèle et les paramètres d'intégration n'ont pas été changés ; aucune reconstruction complète d'index n'a été lancée.

Le téléchargement local de copies PDF n'a pas été exécuté : **l'approbation automatique a échoué à cause de la limite d'usage**, sans détermination que l'action était dangereuse. Les lectures web accessibles, le PDF universitaire Wayuu et le bilan officiel DRAC ont fourni les passages utilisés ; les liens indisponibles et documents seulement repérés sont distingués dans SOURCES.md. Aucune copie manquante ou archive non lue n'est présentée comme preuve directement examinée.
