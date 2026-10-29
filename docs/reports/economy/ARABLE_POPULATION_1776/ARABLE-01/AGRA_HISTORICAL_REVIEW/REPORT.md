# Agra : contrôle historique de la population, 29 octobre 2026

## Réponse et niveau de certitude

**Les 23 928 236 habitants de la portion marathe ne sont pas une estimation historique locale vérifiée.** Le total régional, GAR compris, est 24 148 647. La valeur provient d'une redistribution provisoire d'un objectif indien de 190 millions, par conservation des proportions provinciales héritées. Ce mécanisme ne constitue aucune preuve locale.

Le contrôle géographique et démographique ci-dessous donne un **indice de surestimation**, sans démontrer une impossibilité ni fournir un chiffre de remplacement pour 1776. Aucun recensement de 1776 à ce périmètre n'a été trouvé. Le nombre exact et une fourchette locale suffisamment étayée restent ouverts. Aucune correction de POP n'est installée sur ce fondement.

## Périmètre réellement examiné

Lecture des 37 RGB de `map_data/state_regions/10_india.txt`, STATE_AGRA (id 918), et du bitmap courant. Les propriétaires restent MARATH (34 cellules) et GAR (3). Ces identifiants ne sont ni des numéros de districts historiques ni les identifiants d'instances de la sauvegarde.

Le diagnostic physique `GEOGRAPHIC_ANCHORS.json` et `AGRA_GEOGRAPHIC_DIAGNOSTIC.png` replace des repères approximatifs dans les trois calages antérieurs de DP-03. Agra, Mathura, Meerut, Saharanpur, Muzaffarnagar, Aligarh, Bareilly, Moradabad, Badaun, Mainpuri, Etah, Etawah, Fatehpur, Allahabad, Banda, Hamirpur, Dehra Dun, Garhwal et Almora tombent dans STATE_AGRA avec les trois modèles. Lucknow et Jhansi sont hors de cet État dans les trois modèles. Delhi, Farrukhabad et Kanpur sont proches des limites et changent d'attribution selon le modèle ; Shahjahanpur est hors de STATE_AGRA dans les trois.

**Limite de cette preuve :** des villes à l'intérieur ne prouvent pas l'inclusion intégrale de leur district. Les coordonnées modernes sont des repères arrondis, non une source de frontières de 1776. Le calage du Pendjab est extrapolé au sud et à l'est ; le dessin est un diagnostic approximatif, pas une superposition certifiée de districts. Aucun partage de population au prorata des pixels n'est effectué.

Le périmètre correspond ainsi à un grand ensemble occidental et central du bassin supérieur du Gange, avec des territoires himalayens. Ce n'est ni la ville d'Agra, ni toute la province britannique portant ce nom, ni toutes les Provinces unies avec l'Oudh. Une comparaison de l'ensemble de l'Uttar Pradesh avec ce seul État serait trompeuse.

## Contrôle chiffré indépendant et reproductible

Source primaire effectivement lue : *Census of India 1911*, vol. XV, United Provinces of Agra and Oudh, rapport, chapitre II, tableau subsidiaire II, **page imprimée 80, page PDF 97**. Les valeurs retenues sont la colonne **Actual population, 1911**, et non la population « naturelle » corrigée des migrations, ni les effectifs masculins, ni la population de la ville seule. Le rendu `CENSUS_TABLE-097.png` a été inspecté pour vérifier les chiffres de l'OCR.

`COMPARISON_1911.csv` additionne les districts associés au périmètre approximatif, les districts frontaliers en entier et, volontairement, Shahjahanpur voisin. Les deux États princiers sont ajoutés séparément, sans double compte : Rampur, 531 217 (page PDF 25), et Tehri-Garhwal, 300 819 (page PDF 95). Jalaun entier est inclus par prudence sur le bord sud-ouest.

**Total de cet ensemble comparatif : 23 441 491 en 1911**, soit environ 23,4 millions. Cette somme correspond aux districts entiers énumérés ; **elle n'est pas la population calculée de STATE_AGRA en 1911**, ni une borne mathématique prouvée du territoire, ni une estimation de 1776. Elle inclut des terres hors du périmètre de jeu. Le total installé pour 1776 est même supérieur à ce repère tardif d'environ 3 % ; c'est un signal de contrôle, pas la preuve d'une croissance régulière entre les deux dates. Les famines, épidémies, migrations et déplacements des limites interdisent cette dernière hypothèse.

Le même rapport, chapitre II §23, **page PDF 56**, explique les faiblesses des estimations de 1826 et 1848 et des premières énumérations. Il décrit une densité nettement moindre à la fin du XVIIIe siècle dans certains secteurs, sans donner un total local exploitable de 1776. Son estimation de 1826 (32 millions) concerne une autre province et sa méthode est fragile : elle ne doit pas servir à homologuer les 24 millions du jeu.

L'article de Shireen Moosvi, « Une estimation de la population de l'Inde en 1601 », *Population* 39(1), 1984, **p. 10 effectivement consultée sur Persée**, explique l'absence de résultats de recensement mogol conservés et les limites des estimations antérieures au XIXe siècle. Il ne donne pas, sur cette page, la population du territoire du jeu en 1776. Les seuls 200 millions approximatifs pour l'Inde de 1801 ne sont pas ventilés ici au prorata des terres ou des habitants de 1911.

Conclusion de recherche : **valeur héritée non validée, probablement trop élevée, ampleur de l'écart non établie**. Une reconstruction locale exige encore des données régionales et une correspondance plus fine des districts et parganas. Aucun intervalle numérique de 1776 n'est inventé pour masquer cette lacune.

## Sources et accès

- [Recensement primaire de 1911, copie Université de Chicago](https://storage.lib.uchicago.edu/pres/2014/pres2014-0779-1911-15-01.pdf). Copie déjà archivée dans `../sources/UNITED_PROVINCES_CENSUS_1911.pdf`. Pages PDF 25, 56, 95, 96 et 97 lues localement ; page 97 rendue et examinée. L'ouverture du PDF par l'outil web échoue sur sa taille, pas la lecture de la copie locale.
- [Moosvi, Persée, p. 10](https://www.persee.fr/doc/pop_0032-4663_1984_num_39_1_17897?pageId=T1_10). Lecture effective de cette page, pas de l'article complet ; les essais d'autres pages ont échoué.
- [Visaria et Visaria, Population (1757–1947), Cambridge Economic History of India](https://www.cambridge.org/core/books/abs/cambridge-economic-history-of-india/population-17571947/8C5BA73CE34C431ACAD8FFC5FDC4C179). Résumé seul consulté, signalant la fragilité empirique de la période antérieure aux recensements de 1867–1872 ; chapitre payant non consulté et non utilisé pour inventer des chiffres.
- [Bayly, Agriculture, Ecology and Politics, Oxford](https://academic.oup.com/book/6151/chapter-abstract/149709465). Résumé seul consulté : croissance et déclin régionaux différenciés ; pas d'effectif numérique extrait d'un chapitre inaccessible.

Les transcriptions non relues du Gazetteer sur Wikisource et les extraits de recherche de sources secondaires restent des pistes. Une erreur OCR évidente sur le total des Provinces unies dans une transcription ne remplace pas le tableau primaire. Aucun chiffre provenant uniquement d'un extrait Scribd ou d'un site non vérifié n'est installé.

## Retour en jeu et données préservées

Le joueur confirme explicitement que l'ajout de terres a supprimé la famine à Agra. Voir `USER_RUNTIME_ATTESTATION_2026_10_29.json`. Cette observation valide cet effet fonctionnel ; elle ne certifie ni la population historique ni toute la batterie de contrôles économiques, ni une durée de stabilité, ni sauvegarde/rechargement.

`STATE_AGRA.arable_land` reste à **764**. Population, propriétaires, bâtiments, autres États et vanilla ne sont pas modifiés dans cette recherche. L'ancienne sauvegarde et le tableau de diagnostic conservent leur statut **avant correction**.
