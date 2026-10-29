# DP-01 — Sources et décisions bornées

Date de référence : **1er janvier 1776**. Consultation : 29 octobre 2026.

## Dossiers réutilisés

- R3, recommandations0017/0020/0045/0055/0056/0098/0105/0115 et sourcesS019/S020/S021/S035, sous `docs/reports/map/MAP1/inputs/regional_originals/`.
- R4, recommandations0009/0033/0036/0045/0046/0047/0049, sourcesS012/S014/S039/S043 et les incertitudes associées. Les anciens statuts `MAPPING_REQUIRED` sont conservés ; ils ne valent pas une installation ou une frontière démontrée.
- `docs/reports/map/MAP2I/MAP2I_EXECUTIVE_SUMMARY.md` et l'état courant des fichiers : capitale Kaboul, Timur Shah, nom de confédération sikh et Gwadar MAK déjà traités. Aucun retour à l'ancien CSV de propriétaires.
- `PRIOR_RECOMMENDATIONS.json` et `PRIOR_SOURCES.json` extraient les références pertinentes. Une erreur de bibliographie est repérée : R4S027 concerne Gwalior, pas la preuve des limites du Pendjab ; elle n'est pas utilisée.

## Sources effectivement consultées pour les arbitrages

| Source | Passage vérifié | Portée et limites |
| --- | --- | --- |
| Brian Spooner, *Baluchistan I. Geography, History and Ethnography*, Encyclopaedia Iranica, 1988 | [Article, passages Kalat/Nasir et accord avec les Durrani](https://www.iranicaonline.org/articles/baluchistan-index/baluchistan-i/), section historique, paragraphes sur Nasir et le règlement avec Qandahar, texte web autour des lignes228–245 | Kalat a un gouvernement propre ; Quetta et Pishin doivent être distingués. L'accord conserve la suzeraineté mais met fin au tribut régulier. Les districts nommés permettent de retenir un noyau ; ils ne donnent pas une frontière RGB. Le compromis du Makran n'a pas une date assez précise pour tout installer en janvier1776. |
| Daniel Balland, *Afghanistan X. Political History*, Encyclopaedia Iranica, 1983 | [Section Timur Shah](https://www.iranicaonline.org/articles/afghanistan-x-political-history/), paragraphes47–48 du texte web | Confirme le règne et la capitale déjà initialisés ; Multan est perdu en1772 puis repris en1780. Les contacts déjà PAN sont donc conservés. Les liens nominaux de périphérie ne prouvent pas leur administration uniforme. |
| Harbans Singh (dir.), *The Encyclopaedia of Sikhism*, Punjabi University, article « MISLS » | [MISLS](https://eos.learnpunjabi.org/MISLS.html), présentation de la confédération, territoires des misls, notices Bhangi/Phulkian/Ramgarhia | Contrôle sikh des plaines, nature collective du Dal Khalsa et diversité des chefferies. Les événements décrits comme survenus « en1776 » ou plus tard ne sont pas anticipés au1erjanvier. Pas de polygone exhaustif des douze misls installé. |
| Même encyclopédie, « Patiala » | [PAṬIĀLĀ](https://eos.learnpunjabi.org/PATIALA%20(30%C2%BA-20'N,%2076%C2%BA-26'E).html), début de la notice, installation du siège et succession de1765 | Justifie le propriétaire local et Amar Singh. Ne suffit pas à incorporer toute la région des chefferies voisines. |
| Même encyclopédie, « Sirhind » | [SIRHIND](https://eos.learnpunjabi.org/SIRHIND%20(30%C2%BA-37'N,%2076%C2%BA-23'E).html), passage sur janvier1764 puis transfert d'août1764 | Justifie le noyau Sirhind de Patiala. Les dimensions de la sarkar moghole ne sont pas assimilées aux frontières de Patiala en1776. |
| Même encyclopédie, « Rajas of the Punjab » | [RAJAS OF THE PUNJAB](https://eos.learnpunjabi.org/RAJAS%20OF%20THE%20PUNJAB.html), extrait indexé sur Amar Singh1748–1782 | Seule l'année de naissance est utilisée pour un âge approximatif de27ans, sans anniversaire inventé. Page intégrale non inspectée. |

## Pistes non promues en preuves consultées

- Schwartzberg, *A Historical Atlas of South Asia*, [sommaire DSAL](https://dsal.uchicago.edu/reference/schwartzberg/index.html) et liens des planches1707–1766/1766–1819 consultés. Le visualiseur est accessible, mais son manifeste n'a pas été récupéré par l'outil web et la lecture directe locale échoue sur la résolution réseau. **Aucune image de cette planche n'a été inspectée ou calée.** Ne pas citer ce sommaire comme une superposition historique réussie.
- Sajidi–Hussain, article sur Baloutchistan/Afghanistan : résumé/notice hérités seulement ; divergences sur la souveraineté de Kalat, pas un traité original intégral vérifié.
- R4S043, gouverneurs du Cachemire : ancien signalement, pas une preuve des limites du Ladakh/Jammu. Aucun transfert fondé sur cette seule liste.

## Correspondances retenues et incertitudes

Le bitmap et les **locators effectifs du mod**, et non les seuls anciens fichiers vanilla, sont échantillonnés dans `CURRENT_LOCATORS.json`. `HUB_REFERENCE_EVIDENCE.json` conserve les six corrections de pointeurs. En particulier, la référence de ville de Kalat pointait sur une province côtière, alors que son locator nommé est dans `xBAE3D2`. Les noms natifs attestent une convention du jeu, pas une souveraineté historique ; le choix du propriétaire repose sur les sources ci-dessus.

`GEO_EVALUATION.json` contient treize contrôles : erreurs importantes pour certains hubs de Lahore/Srinagar et leurs voisins. **Aucune précision indépendante établie.** Les enveloppes des19 provinces sont explicitement approximatives ; elles retiennent des noyaux et des terrains intermédiaires connectés, pas la taille totale des anciennes possessions ou leurs enclaves. Cette limite interdit de déclarer les juridictions himalayennes et baloutches intégralement résolues.

La provenance des cohortes conservées est retraçable dans `COHORT_LINEAGE.json`, `POP_LEDGER.json` et les préimages. Le vanilla sert ici à expliquer les anciennes fusions de données, **pas à importer sa démographie, ses frontières de1836 ou ses souverains**. Aucun quotient de pixels n'est présenté comme une population historique.

Les lois locales et le pacte de suzeraineté sont des approximations de gameplay : absence de tribut régulier explicitement représentée pour Kalat ; aide à certaines campagnes, portée réelle de la protection, jurisprudences et tolérances locales non reconstituées exhaustivement. Les effets du moteur demandent les contrôles en jeu.
