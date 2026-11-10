# Mission 25 — intégration préparée, 9 novembre 2026

## Résultat

Les **62 fichiers** de la PR 34 ont été reconstruits depuis le diff conservé ou récupérés à la révision épinglée, puis contrôlés contre leurs identifiants de blob Git. La comparaison couvre la base commune, le main publié, la branche hotfix et le workspace. **Aucune résolution de contenu ne reste ouverte dans ce périmètre.** Les 16 contrôles de préparation passent, y compris deux témoins négatifs.

Le candidat d'intégration de la branche conserve **exactement l'arbre du main publié**. La divergence de graphe demeure : aucun commit, merge, push, changement de branche ou staging n'a été exécuté. Une fusion de l'ancienne branche sans cette revue pourrait réintroduire des versions dépassées.

## Révisions et candidat concret

| Objet | Identifiant |
| --- | --- |
| Base commune | `52c42808bdb0748e69fbde3423bb5004b5b1f20a` |
| Main, premier parent proposé | `0396b1133168c1721b61cee5ae5334f1a4f5e4e1` |
| Hotfix, second parent proposé | `b72dc3584e1225f8c675b7c6c9f295cde122b821` |
| Arbre résultant proposé | `ae449f27b1055c18b9581ee9a4deeb42be4030a2` |
| Diff du candidat contre main | **0 fichier modifié** |
| Écriture Git effectuée | **Aucune** |

`COMMITTED_CANDIDATE.json` décrit une fusion d'historique à ces deux parents et à cet arbre exact. Les deux têtes distantes ont été relues pendant cette passe et correspondent aux révisions ci-dessus. Les revérifier avant toute écriture ; si une tête bouge, refaire la comparaison. Utiliser une copie isolée : le workspace contient d'autres travaux qui ne font pas partie de cette proposition. Le candidat ne constitue pas la publication de tous les correctifs locaux.

Le fichier `common/defines/00_defines.txt`, supprimé sur les deux côtés, reste absent. Les 61 autres chemins ont une version de candidat archivée. Les fichiers hors du diff de la PR restent ceux du main engagé ; aucun contenu local supplémentaire n'est sélectionné.

## Résolutions

Sur le côté main : 52 fichiers ont déjà le contenu hotfix, quatre fusions à trois versions redonnent main, trois résolutions explicites conservent main et trois documents conservent la preuve main avec la preuve distante archivée. Les versions antérieures des résultats restent dans `history/` ; les anciens fichiers de conflit sont des preuves de la première tentative, pas des conflits actifs.

| Chemin / objet | Résolution et preuve |
| --- | --- |
| `common/goods/13_tech6c5b_copper.txt` | Conserver le fichier sans définition propre du bien. Le fournisseur vanilla courant définit un prix de **40**, l'ancienne branche **50**. La répartition des gisements du mod n'est pas modifiée. |
| `common/journal_entries/00_sick_man.txt` | Conserver main : **8 journaux, 17 conclusions identiques et dans le même ordre**, sans anciens champs de conclusion. Préserver le groupe des crises impériales, la visibilité inactive, le déclenchement et le calcul de progression protégé. Les champs différents sont listés par entrée dans `RESOLUTION_PROOFS.json`. |
| `tools/compatibility/issue27_journal_outcomes_audit.py` | Conserver main : les tables des deux premiers lots sont identiques et la couverture supplémentaire de l'indépendance américaine est préservée. |
| `common/ship_types/1776_usa_armed_merchantman.txt` | Main contient déjà exactement la version fonctionnelle de l'ancienne branche. La refonte locale plus récente reste dans le workspace, sans être incorporée au candidat de branche. |
| Deux journaux américains | Les différences avec hotfix portent sur leur classement dans le groupe du Destin des Amériques ; les fusions conservent main. |
| Mine de cuivre et carte d'Europe occidentale | Les fusions redonnent main. Aucune réécriture de carte, de ressources ou de loi n'est effectuée. Les changements locaux de carte restent exclus du candidat engagé. |

`RESOLUTIONS.json` lie les trois décisions explicites aux empreintes exactes des fichiers. Une résolution périmée provoque un refus du préparateur. Les conclusions ottomanes sont comparées en jetons, ordre compris : cette preuve ne certifie pas leur exécution moteur.

## Deux changements locaux installés

La déclaration de compatibilité du lanceur visait encore la 1.13. Elle est corrigée dans les deux fichiers du mod :

| Fichier | Avant | Après |
| --- | --- | --- |
| `descriptor.mod` | `supported_version="1.13.*"` | `supported_version="1.15.*"` |
| `.metadata/metadata.json` | `supported_game_version: 1.13.9` | `supported_game_version: 1.15.0` |

Version du mod **2.5.0**, noms, chemins de remplacement et tous les autres octets conservés. Avant/après et empreintes : `launcher_before/` et `LAUNCHER_VERSION_APPLIED.json`. Ces deux modifications locales sont séparées du candidat de fusion d'historique ; elles ne publient pas une nouvelle version et ne prouvent pas la compatibilité moteur.

## Journaux et concurrence

La [mission 39](https://github.com/Malzars-sys/1776-Age-of-Revolutions/issues/39) couvre maintenant **tout le catalogue effectif des journaux**, activation, visibilité, progression, réussite, échec, invalidation, délais, effets et continuation. Elle est rattachée comme sous-mission à la 24 et comme dépendance de sortie à la 25. La mission 27 reste terminée pour ses lots acceptés.

Hawk a pris la mission 39 après avoir livré la 22 en review. Son premier lot est un inventaire sans changement de gameplay et préserve la priorité d'intégration 25. Cette passe ne revendique aucun de ses changements. La capture `ISSUE39_SCREENSHOT.png` montre le rattachement et le statut In progress.

## Conditions de sortie encore ouvertes

- Autorisation de l'écriture Git puis exécution et contrôle de la fusion exacte proposée. W02 de `.agents/workflow.md` interdit ces écritures par défaut ; la préparation ci-dessus est terminée et consultable.
- Sélection ultérieure explicite des correctifs locaux à livrer : ce candidat d'historique ne les publie pas.
- Migration complète des journaux sous 39 et évaluation des diagnostics restants ; résultats de la 22 en review à reprendre.
- Unification de la 32 toujours non testée ; correction des marines de la cogue encore sans test moteur après correctif.
- Requalification des sept références économiques ambiguës et des assertions de conservation devenues divergentes dans les audits précédents. Leurs FAIL archivés ne sont ni effacés ni transformés en PASS.
- Test final d'un candidat réellement intégré et identifiable : version/build, DLC et playset, nouvelle partie, plusieurs mois, sauvegarde automatique et rechargement. Ne pas inférer de nouveau résultat humain des anciennes acceptations.

**25 reste In progress et 19 reste ouverte.** La préparation d'intégration passe ses contrôles ; la sortie globale n'est pas validée. Le vanilla et les fichiers de gameplay n'ont reçu aucune écriture de cette passe.

## Reproduction

`python -B tools/compatibility/issue25_prepare_integration.py --evidence docs/reports/compatibility/V1_15_ISSUE25_INTEGRATION_2026_11_09`

Le préparateur lit les objets Git et utilise `git merge-file --stdout` sur des copies de preuve. Il écrit uniquement son dossier de preuves ; il ne fusionne pas les branches et n'installe pas les versions proposées. La matrice `FILE_INTEGRATION_REVIEW.json`, les preuves de résolution, le candidat engagé et `VALIDATION.json` décrivent séparément ces résultats.
