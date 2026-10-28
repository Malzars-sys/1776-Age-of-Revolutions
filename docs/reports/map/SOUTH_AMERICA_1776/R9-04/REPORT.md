# R9-04 — Araucanie et Patagonie

**IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION — référence : 1er janvier 1776.** Installation du 28 octobre 2026. Aucun lancement moteur ni validation humaine de cette version. La passe concerne les principales erreurs de contrôle effectif ; elle ne clôt pas toutes les limites historiques ni les anciennes réserves R9.

## Résultat installé

| Secteur | Avant | Après |
|---|---|---|
| Cœur araucan, région technique LOS_RIOS | SC3 détenait les 31 provinces | **9 provinces réattribuées aux Mapuche (PAT)** ; SC3 garde 22 provinces, dont frontière fortifiée et Valdivia/Corral |
| Arrière-pays d'Osorno, région technique ARAUCANIA | SC3 détenait 10 provinces | **7 provinces réattribuées à H91**, ensemble décentralisé de chefferies huilliches du Futahuillimapu ; SC3 garde Maullín, Calbuco et Chiloé (3 provinces) |
| Communications de Chiloé | Aucun bâtiment initial dans la portion SC3 d'ARAUCANIA | **Un port commercial de niveau 1**, PM existants, sur le hub portuaire resté espagnol ; fonctionnement maritime à observer en jeu |
| Patagonie orientale et Terre de Feu | PAT, THL et SLK déjà autonomes sur l'essentiel du territoire | Aucun nouveau partage ethnique arbitraire ; propriétaires et habitants conservés |
| Cuyo/Mendoza, identifiant trompeur STATE_RIO_NEGRO | 43 provinces SC4 et 41 PAT | Inchangé : les fondations atlantiques de 1779 ne justifient pas de retirer Mendoza à SC4 |

**16 provinces existantes transférées ; aucun nouveau RGB, aucun nouveau State_ID, aucun pixel redessiné.** Les cellules frontalières mixtes restent des approximations. Voir [les sources et limites](SOURCES.md) et [l'avant/après](R9_04_AVANT_APRES.png).

**35 928 habitants réattribués, aucun ajouté ni supprimé** : cohortes existantes de 33 682 et 2 246 déplacées intactes vers PAT et H91, respectivement, dans leur région d'origine. Les autres cohortes et tous les bâtiments préexistants restent inchangés. C'est une redistribution technique, pas un nouveau recensement historique. La catégorie culturelle héritée `patagonian` est conservée comme agrégat grossier ; elle ne certifie pas une identité chon/tehuelche des Huilliches.

Les prétentions espagnoles restent distinctes du contrôle réel : revendications ARAUCANIA conservées, revendication SC3 explicite dans LOS_RIOS. Ni la fidélité déclarée au roi à Tapihue ni les missions ne deviennent une administration coloniale continue.

## Fichiers du jeu modifiés ou ajoutés

1. `common/history/states/00_states.txt` — seuls les blocs LOS_RIOS/ARAUCANIA : propriétaires et revendication.
2. `common/history/pops/07_south_america.txt` — seuls les deux transferts de cohortes.
3. `common/country_definitions/1776_r904_huilliche.txt` — H91 décentralisé, capitale dans sa portion d'ARAUCANIA.
4. `common/history/countries/1776_r904_huilliche.txt` — profil explicite de subsistance, lois et transformation alimentaire ; aucun tier technologique européen copié.
5. `common/flag_definitions/1776_r904_huilliche.txt`.
6. `common/coat_of_arms/coat_of_arms/1776_r904_huilliche.txt` — emblème générique du jeu, sans prétention à un drapeau historique.
7. `localization/french/replace/1776_r904_huilliche_l_french.yml`.
8. `localization/english/replace/1776_r904_huilliche_l_english.yml`.
9. `common/history/buildings/1776_r904_chiloe_port.txt` — seul bâtiment ajouté.

Outil reproductible : `tools/r904.py` (`--prepare`, `--apply`, `--verify`, `--preview`). Ne pas réappliquer les snapshots à un workspace ultérieur : les modifications partagées sont gardées par empreintes. Le dossier contient les baselines, les fichiers avant/patch, les SHA, le ledger des sources, l'inventaire, le calage et les résultats.

## Vérifications exécutées

- `python tools/r904.py --verify` : **24/24**, résultats dans [VALIDATION.json](VALIDATION.json). Syntaxe des scripts modifiés ; exactitude des seuls 16 transferts ; mêmes comptes d'attribution par RGB ; mêmes effectifs et identités de cohortes par région ; seuls deux changements de propriétaire des cohortes ; populations attachées à des portions possédées ; capitales, culture/religion, lois, technologie, drapeau et localisations vérifiés ; un seul port ajouté ; noyaux CENTRAL et Sacramento témoins conservés.
- Comparaison des empreintes : bitmap, terrains, régions, locators, bâtiments existants, définitions/histoires nationales préexistantes, diplomatie et formations militaires identiques à la préparation. Aucune modification runtime non listée constatée (`CONCURRENT_FILES.json` vide). Les changements du Congo déjà présents sont conservés.
- `validate_starting_technology_1776.py` exécuté avant/après pour SC3, PAT, THL et SLK, puis H91 avec attentes explicites. **H91 : PASS_STATIC_ONLY, aucun signalement.** SC3 : 18 signalements ; PAT : 2 ; THL : 2 ; SLK : 3. **25 signalements préexistants, aucun ajouté ou supprimé** ; les anciens pays restent `FAIL_STATIC`. Le code retour 1 de cet audit vient de cette dette inchangée, et ne doit pas être masqué. [Comparaison](TECH_COMPARISON.json).
- Aperçu produit depuis le bitmap et les propriétaires effectivement installés, puis examiné visuellement.
- Le jeu n'était pas détecté en cours d'exécution lors du contrôle de processus ; aucune nouvelle partie, simulation ou sauvegarde/rechargement n'a été exécutée. **Les contrôles statiques ne prouvent pas le chargement moteur, l'accès au marché, l'absence de famine ou les relations diplomatiques en jeu.**

Les doublons mondiaux hérités et la double revendication SC3 déjà présente dans ARAUCANIA ne sont pas supprimés pour verdir les résultats : le contrat vérifie l'absence de nouvelles duplications d'attribution, pas la guérison de toute la carte mondiale.

## Réserves et prochaine action

Tester cette version selon [RUNTIME_PROTOCOL.md](RUNTIME_PROTOCOL.md). Restent ouverts : finesse de la frontière des forts/Purén, missions de Valdivia, marges Maullín/Calbuco, divisions internes huilliches, démographie/ethnonymes détaillés, noms modernes hérités des hubs et répartition transandine PAT/THL/SLK. Le Cuyo avant août 1776 relève d'une dépendance institutionnelle à traiter séparément. Aucune frontière au mètre près n'est certifiée.

La prochaine région de la feuille de route doit faire l'objet d'une demande distincte ; cette installation ne lance pas automatiquement une passe amazonienne. Aucune écriture Git ni modification du vanilla.

## ColGrep : mesure prudente

**1 appel local** à l'exécutable demandé :

```powershell
& 'C:\Users\simeo\.cargo\bin\colgrep.exe' --agent "Locate existing R9 research evidence and implementation dependencies for correcting Araucania, Valdivia, Chiloe, and Patagonia in January 1776. Prioritize prior historical decisions, geographic province mapping tools, and current files defining PAT, THL, SLK and Spanish Chile. Return relevant file paths and line ranges only. Read-only research: no edits, no Git, no model changes." .
```

Code retour **0**, temps mesuré **291,52 secondes**, soit environ **4 min 52 s**. Réponse conservée dans `COLGREP_SEARCH.txt`, mesure dans `COLGREP_METRICS.json`. **4 emplacements** : trois dossiers R9 et le registre des incertitudes. Les quatre chemins existent et les plages de lignes ont été relues et vérifiées (`COLGREP_VERIFIED.json`). La sortie de cet appel ne fournit pas de télémétrie GPU ni d'identité détaillée du modèle : le mode local configuré a été invoqué sans changer de modèle, mais aucune mesure matérielle indépendante n'est revendiquée.

Intérêt observé limité à la localisation des recherches antérieures. Les résultats sont pertinents mais incomplets pour la demande : ils ne localisent pas directement l'ensemble des définitions/histoires/POPs/bâtiments nécessaires. Le dossier 0008 réutilise lui-même une description géographique trompeuse d'ARAUCANIA ; cette assertion n'a pas été appliquée. Une plage de 117 lignes est aussi peu sélective. Les recherches exactes, lecture du bitmap, analyse historique, choix, modifications et contrôles restent réalisés par Codex et les outils locaux.

Le nombre exact des recherches classiques n'a pas été instrumenté pour toute cette passe ; aucun chiffre reconstruit arbitrairement. Aucun compteur de tokens Codex par recherche n'a été exposé. Quatre pistes documentaires ont été déléguées, **pas quatre recherches économisées démontrées**. Sans expérience comparative équivalente, aucune économie exacte de quota ne peut être estimée. Pour ce lot, le gain de localisation est modeste au regard des presque cinq minutes de latence ; les identifiants déjà connus restent plus efficacement retrouvés avec `rg`.
