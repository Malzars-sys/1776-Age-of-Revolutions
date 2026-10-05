# Lots 18, 19 et 20 — neuf icônes intégrées

Intégration approuvée par l'utilisateur le 5 octobre 2026 : « OK, c'est bon, tu peux tout intégrer. Et passez au lot suivant. »

| Lot | Sources exactes intégrées |
| --- | --- |
| 18 — Santé et prévention | Variolisation ; science vétérinaire ; campagnes vaccinales — [dossier](../asset21_preview_2026-10-05/README.md) |
| 19 — Cadastre, droit et abolition | Cadastre corrigé ; codification juridique ; deux mains brisant leurs chaînes — [révision 2](../asset22_preview_2026-10-05/revision_v2/README.md) |
| 20 — Canaux, presse et coopération | Canaux ; cinq journaux avec Allgemeine Zeitung à la place du Figaro répété ; coopération — [révision 4](../asset23_preview_2026-10-05/revision_v4/README.md) |

Les neuf DDS sont reliés aux technologies. **Seules neuf lignes de texture ont changé**, dans deux fichiers de définitions. Ni les coûts, ni les effets, ni les déblocages ne sont modifiés. Les 1 251 autres fichiers protégés préexistants restent identiques ; seuls neuf DDS nouveaux sont ajoutés.

Exports natifs BGRA8 A8R8G8B8, 256 × 256, neuf mipmaps. Décodage indépendant : couleurs et alpha correspondent exactement aux PNG sélectionnés et aux neuf niveaux de réduction. Transparence et planche des DDS inspectées sur fonds clair/sombre, dont les mains et les journaux.

- [Contrôle indépendant](integration_static_validation.json)
- [Planche des DDS réellement intégrés](LOTS_18_19_20_DDS_INTEGRES_QA.png)
- [Approbation et empreintes exactes](user_approval.json)
- [Manifeste d'intégration](integration_manifest.json)
- [Exports et mipmaps](integration_export_validation.json)
- [Plan des sources et prompts exacts](integration_plan.json)

Les images ont été créées avec le générateur intégré ImageGen et préparées mécaniquement sans recoloration. Les variantes antérieures, ainsi que la suspension temporaire demandée pour refaire l'abolitionnisme, sont conservées dans les dossiers de révision ; la dernière autorisation permet désormais l'intégration.

Le lot 17 était déjà intégré auparavant ; son [contrôle](../asset20_preview_2026-10-05/revision_v3/integration_static_validation.json) est indépendant de cette passe.

**Pas de test du moteur du jeu pendant cette étape.** Les contrôles des fichiers ne prouvent pas à eux seuls leur affichage en partie. Aucun commit, push, merge ou lancement du jeu n'est effectué.

Le prochain lot sera présenté séparément avant intégration. Le cuivre, la route pavée déjà approuvée et les sept anciens PM du laboratoire restent hors périmètre.

