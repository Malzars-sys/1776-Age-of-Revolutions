# MAP‑2H — Finition des gouvernements, noms et communautés

Correctif local terminé. **44 contrôles statiques passent.** Pas de test natif de cette finition : le premier MAP‑2H a été validé par le joueur, mais les nouveaux historiques demandent une nouvelle partie. Aucun commit, merge ou push ; MAP‑2I n'est pas commencé.

## 1. Viêt Nam : trêve temporaire

- **DAI–TSN : trêve bidirectionnelle native de 24 mois**, échéance nominale au **1er janvier 1778**, relations initiales **+20**.
- **TSN–NGN : relations −60 et rivalité réciproque**. Le conflit est représenté comme un antagonisme politique et diplomatique ; aucune guerre active ou objectif de guerre arbitraire n'est ajouté.
- Aucune alliance permanente, nouvelle sujétion, boucle de renouvellement ou événement obligeant à attaquer. Rien dans ce correctif ne bloque une évolution en 1786. Il ne crée pas non plus un scénario automatique pour cette année.

Le rapprochement après les affrontements de 1775 est compatible avec l'accord temporaire au nord décrit par le Musée national d'histoire du Viêt Nam. **La durée de deux ans et les valeurs de relations sont un réglage de gameplay**, pas les clauses attestées d'un traité historique. [Musée national d'histoire du Viêt Nam, événements 1774–1777](https://baotanglichsu.vn/vi/Articles/3096/12424/nguyen-nhac-voi-vuong-trieu-tay-son.html).

## 2. Kaurna : pays jouable, gouvernement coutumier

Conformément aux précisions du joueur, **KAU reste `unrecognized`**, et non décentralisé. Sa définition, ses huit provinces, sa capitale, ses **51 300 habitants**, sa technologie initiale et ses groupes de population restent identiques. Aucun personnage ou souverain historique fictif n'est créé.

| Domaine | Loi de départ après correction |
| --- | --- |
| Gouvernement | Chefferie — `law_chiefdom` |
| Distribution du pouvoir | Conseil des anciens — `law_elder_council` |
| Réforme agraire | Servage — `law_serfdom` |
| Droits des femmes | Tutelle légale — `law_no_womens_rights` |
| Citoyenneté | Sujétion — `law_subjecthood` |
| Liberté d'expression | Censure — `law_censorship` |
| Esclavage | Esclavage pour dettes — `law_debt_slavery` |

L'isolationnisme et la fiscalité de consommation restent en place. L'activation explicite des bureaucrates élus est retirée : le réglage traditionnel préexistant sert de valeur technique par défaut.

**Exception strictement ciblée :** les conditions natives de visibilité et d'adoption de la chefferie, ainsi que la visibilité du conseil des anciens, autorisent KAU non reconnu. Pour tous les autres pays, la restriction native aux pays décentralisés reste équivalente. Le modèle de contrôle teste **6 128 cas**, y compris l'absence de KAU, pour éviter une ouverture accidentelle à tous les pays.

Le gouvernement natif `gov_chiefdom` exige la loi de chefferie sans imposer un pays décentralisé. Il utilise néanmoins un représentant et une transmission du pouvoir classée **héréditaire** dans le moteur : c'est une limite de son abstraction, pas une monarchie européenne ajoutée par le correctif. Aucun nom de chef n'est inventé. Si KAU change ultérieurement de statut vers « reconnu », la visibilité de ces lois devra être réexaminée ; l'exception actuelle concerne le statut demandé de pays non reconnu.

Les lois foncières, de droits des femmes et d'esclavage suivent les choix explicites du joueur. Elles ne sont pas présentées comme une description exhaustive des institutions kaurna. L'esclavage pour dettes conserve son verrou technologique général ; l'historique l'active directement sans accorder de technologie moderne à KAU. Son affichage effectif au départ doit être vérifié en jeu.

La référence historique place le cœur kaurna dans les plaines d'Adélaïde et décrit des autorités fondées sur les connaissances, les responsabilités et les relations communautaires, non un parlement censitaire. Le bloc RGB actuel couvre ce cœur mais dépasse les limites fines, notamment vers l'île Kangourou et des marges côtières. **Frontières et populations conservées**, conformément au périmètre : pas de correction démographique ou territoriale kaurna dans cette finition. [History Trust of South Australia, Kaurna People](https://sahistoryhub.history.sa.gov.au/subjects/kaurna-people/).

L'audit de **23 pays autochtones australiens actifs** identifie KAU comme seul cas activant explicitement république parlementaire et vote censitaire. Les **22 autres** sont déjà décentralisés et leurs historiques n'activent pas de gouvernement républicain ou électoral moderne. Ils restent inchangés. KAU n'a ni unité explicite ni bâtiment explicite dépendant de ses anciennes lois ; son modèle natif de personnages est vide et laissé à la génération du moteur. Pas de pacte spécifique KAU dans la diplomatie effective du mod.

## 3. INDOP : découpage régional autorisé après clarification

Le joueur a explicitement autorisé à scinder **uniquement INDOP**, en utilisant les RGB existants et en conservant les véritables sultanats. L'inventaire initial trouve **71 RGB** dans cinq State Regions.

| Groupe après correction | Provinces | Habitants | Représentation |
| --- | ---: | ---: | --- |
| INDOP — Communautés de Sumatra / Sumatran Communities | 49 | 249 198 | Nord et sud de Sumatra, cultures primaires `sumatran batak` |
| TOB — Communautés batak / Batak Communities | 4 | 38 239 | Fragment de Tapanuli dans `STATE_ACEH`, culture primaire `batak` |
| KLT — Communautés dayak et bornéennes / Dayak and Bornean Communities | 18 | 56 520 | Deux fragments de Bornéo, cultures primaires `bornean dayak` |
| **Total ancien INDOP conservé** | **71** | **343 957** | Aucun nouveau TAG ou habitant |

**22 RGB sont réattribués**, tous auparavant INDOP. TOB et KLT existaient déjà dans les définitions mais étaient inactifs ; ils deviennent des regroupements décentralisés, pas des monarchies unitaires. Le fragment batak est nommé **Tapanuli** dans l'interface plutôt qu'« Aceh ». Les 19 provinces d'INDOP dans `STATE_NORTH_SUMATRA` et les 30 de `STATE_SOUTH_SUMATRA` restent INDOP.

RGB vers TOB : **x9A7E0B, x388ABB, x60E050, xE3CB2E**.

RGB de Bornéo occidental vers KLT : **xD735DB, xE3C4F2, xC29C28, xA67A6E, x638173, x76E306, xF9BDCB, xFCFD83, x029E85, x8A69A7, xFF8539, xF37396**.

RGB de Bornéo oriental vers KLT : **x018070, x9F4941, x8BD8AF, xB8D3B7, x0FFCAE, x4F7415**.

Les subdivisions complètes et leurs profils de population changent de TAG **sans modification de taille ou d'attribut**, donc sans répartition arbitraire de minorités entre petites provinces. Les groupes batak, sumatrans, bornéens, dayak, néerlandais, yue, libres/esclaves et leurs religions sont conservés. La composition du fragment de Tapanuli était déjà majoritairement batak.

**Limites :** la culture `bornean` est une catégorie large du jeu ; le nom mixte évite de prétendre que les habitants sont tous dayak. Les différents peuples dayak ne sont pas fusionnés en une ethnie homogène. Les communautés batak ne représentent pas uniquement les Toba ni une royauté unique. Le cœur autour du lac Toba, déjà attribué à d'autres TAGs dans la carte actuelle, n'est pas annexé pour agrandir TOB. Les parties d'INDOP restantes regroupent plusieurs communautés de Sumatra ; pas de nouveau découpage des sultanats de Siak, Jambi, Aceh, Banjar, Kutai, Pontianak, Sambas ou Sintang.

Les sources patrimoniales confirment les communautés batak de Tapanuli, dont Mandailing et Angkola, et la diversité des peuples regroupés sous l'appellation dayak. Elles ne constituent pas une carte cadastrale de 1776 : **les frontières sont des approximations documentées à l'échelle du jeu**. [Patrimoine indonésien, traditions de Tapanuli](https://kebudayaan.kemdikbud.go.id/bpnbaceh/tor-tor/), [ministère indonésien du Tourisme, diversité des peuples dayak](https://www.indonesia.travel/gb/en/travel-ideas/adventure/a-glimpse-of-kalimantan-the-exotic-beauty-of-borneo).

## 4. Conservation et validations

- Population mondiale **835 804 980**, inchangée. Profils démographiques et tous leurs champs conservés mondialement et par State Region ; populations kaurna strictement identiques.
- Bitmap, côtes, définition des provinces, hubs et locators **inchangés**. Aucune modification des attributions de pays autres qu'INDOP. Viêt Nam, Java, Hawaï et tous les autres lots restent intacts.
- Niveaux de bâtiments, PM, réserves et propriétaires économiques déclarés conservés. **Sept références de sièges privés INDOP** dans les fragments qu'il perd pointent désormais vers son fragment toujours possédé de Sumatra du Nord. Les bâtiments restent physiquement sur place ; leurs détenteurs restent INDOP. Aucun niveau d'infrastructure ajouté.
- Unités, formations, recrutements et commandants identiques. Les nouveaux regroupements n'inventent aucune garnison.
- Capitales possédées, noms français/anglais uniques, couleurs et composants natifs de bannières vérifiés. Bannières génériques, pas des emblèmes historiques authentifiés. Aucun nom dynamique contradictoire pour INDOP, TOB ou KLT.
- **44 doubles attributions anciennes**, inchangées ; aucune nouvelle référence orpheline. Modèles ottomans et IA des infrastructures réexécutés. HEAD, index et références du dépôt principal inchangés.

## 5. Fichiers de jeu touchés

**Définitions :** `common/country_definitions/00_countries.txt` (TOB/KLT), `common/country_definitions/02_modded_countries.txt` (INDOP). La définition KAU n'est pas modifiée.

**Historiques :** `common/history/states/00_states.txt`, `common/history/pops/12_indonesia.txt`, `common/history/buildings/12_indonesia.txt`, `common/history/buildings/98_build_start_1776_world_redistribution.txt`, `common/history/countries/kau - kaurna.txt`, `common/history/countries/1776_map2h_indop_communities.txt`, `common/history/diplomacy/1776_map2h_vietnam_rapprochement.txt`.

**Exception de lois :** `common/laws/00_governance_principles.txt`, `common/laws/00_distribution_of_power.txt`, `common/scripted_triggers/1776_map2h_kaurna_customary_laws.txt`.

**Noms et présentation :** `localization/english/NM_Countries_l_english.yml`, `localization/french/NM_Countries_l_french.yml`, `localization/english/replace/1776_map2h_communities_l_english.yml`, `localization/french/replace/1776_map2h_communities_l_french.yml`, `common/scripted_effects/1776_map2h_tapanuli_name.txt`, `common/on_actions/16_1776_map2h_tapanuli_name.txt`, `common/coat_of_arms/coat_of_arms/08_1776_map2h_communities.txt`.

La liste exacte et les tests figurent dans **VALIDATION.json** ; les décisions et sept références économiques dans **PLAN.json**. L'état antérieur est conservé dans une baseline légère et des empreintes, sans nouvelle copie complète ni ZIP volumineux.

## 6. Vérification en jeu

Dans une **nouvelle partie** : vérifier KAU jouable, intitulé « Chefferie », conseil des anciens et sept lois demandées ; vérifier qu'aucune république censitaire ne remplace ces lois. Inspecter la trêve DAI–TSN, son échéance, et la rivalité TSN–NGN. Vérifier TOB/Tapanuli, KLT à Bornéo et INDOP désormais limité à Sumatra, puis les sièges économiques, emplois et accès aux marchés après un mois.

La génération du représentant kaurna et l'agrégation des propriétaires économiques relèvent du moteur : ces aspects ne sont pas garantis par les tests statiques. Les nouvelles lois ont leurs effets de gameplay natifs, notamment sur les droits, la légitimité et l'emploi ; seule l'absence d'altération directe des populations de départ est attestée ici.
