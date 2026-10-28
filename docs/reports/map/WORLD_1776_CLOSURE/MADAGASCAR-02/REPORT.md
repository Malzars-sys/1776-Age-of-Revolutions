# MADAGASCAR-02 — restauration politique de1776

**28 octobre2026 — IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION.** Autorisation directe : «Ok, corrige Marina.», suivie de «fini». Référence : **1er janvier1776**. Frontières et initialisation nécessaire uniquement ; aucun nouveau personnage ni raffinement de bâtiments. Lissage cosmétique et test africain groupé restent différés.

## Corrections installées

Le pays MAD possédait les deux régions moteur entières, soit122RGB. **120 provinces natives sont réattribuées dans28groupes ; MAD en conserve2.** Aucun pixel recoloré, nouveau RGB, terrain, ressource ou locator. Énumération complète : [PLAN.json](PLAN.json), coordonnées/propriétaires : [GEOGRAPHIC_CROSSWALK.json](GEOGRAPHIC_CROSSWALK.json), cartes [avant](BEFORE.png) et [après](AFTER.png).

MAD représente désormais **Antananarivo** ; **Ambohimanga et Ambohidratrimo** sont séparés. **Boina, Menabe, Antankarana, Isandra, Lalangina, Manandriana, Arindrano, Ikongo, Antemoro, Antambahoaka, Antefasy, Antesaka et Fiherenana** ont des noyaux royaux distincts. Les profils **Tsimihety, Sihanaka, Bezanozano, Betsimisaraka, Imamo/Andratsay, Tanala, Bara, Mahafaly, Antanosy et Antandroy** représentent des ensembles locaux autonomes. Les agrégats pluriels reconnaissent leurs chefs/cours : catégorie décentralisée ne signifie pas absence d'organisation.

La province native **x606CE0**, rattachée à SOUTH_MADAGASCAR, couvre aussi les **Comores**. Elle devient l'agrégat autonome **Sultanats des Comores**. L'audit précédent parlait trop globalement de122provinces de l'île : la géométrie distingue121provinces continentales/littorales malgaches et cette province d'archipel. Pas de souveraineté merina sur les Comores, ni d'union politique comorienne moderne affirmée. Les cours insulaires restent agrégées faute de subdivision native séparée.

Un seul lien tributaire est installé : **Boina → Antankarana**. Les autres tributs, influences et hégémonies ne deviennent pas des annexions ou pactes généraux sans précision suffisante. Les cours merina ne sont donc pas subordonnées mécaniquement à un destinataire sakalava non établi. Les détails sont exposés dans SOURCES.md et GEOGRAPHIC_LIMITATIONS.md.

## Institutions et connaissances initiales

**26TAG nouveaux,27profils dont MAD conservé.** Les royaumes ont une monarchie non reconnue, les agrégats locaux des institutions de chefferies autonomes. Aucun roi daté ou personnage ajouté. Le modèle natif de personnage MAD_ranavalona_hova, hérité du scénario1836, est neutralisé dans une surcharge propre ; aucune généalogie de remplacement n'est inventée.

| TAG | Nom | Catégorie moteur | Technologies connues |
|---|---|---|---:|
| AVR | Ambohimanga | unrecognized | 7 |
| AHI | Ambohidratrimo | unrecognized | 7 |
| BOI | Boina | unrecognized | 7 |
| MEB | Menabe | unrecognized | 7 |
| ATK | Antankarana | unrecognized | 7 |
| TMH | Tsimihety | decentralized | 4 |
| BSM | Chefferies betsimisaraka | decentralized | 7 |
| SNK | Sihanaka | decentralized | 6 |
| BZN | Bezanozano | decentralized | 6 |
| ANR | Imamo et Andratsay | decentralized | 6 |
| ISD | Isandra | unrecognized | 7 |
| LLG | Lalangina | unrecognized | 7 |
| MDN | Manandriana | unrecognized | 6 |
| RND | Arindrano | unrecognized | 7 |
| ATM | Antemoro | unrecognized | 7 |
| BHK | Antambahoaka | unrecognized | 6 |
| ATF | Antefasy | unrecognized | 7 |
| ASK | Antesaka | unrecognized | 7 |
| MSR | Fiherenana | unrecognized | 7 |
| IKO | Ikongo | unrecognized | 7 |
| TNL | Communautés tanala | decentralized | 4 |
| BAR | Chefferies bara | decentralized | 4 |
| MHF | Royaumes mahafaly | decentralized | 4 |
| ATY | Chefferies antanosy | decentralized | 4 |
| TDY | Confédération antandroy | decentralized | 4 |
| CMO | Sultanats des Comores | decentralized | 6 |
| MAD | Antananarivo | unrecognized | 7 |

COUNTRY_PROFILES.json motive chaque capacité : agriculture/élevage, transformation alimentaire, artisanat, textile, échanges et organisation militaire sont distingués selon les pouvoirs. Les échanges côtiers ne donnent ni assurance commerciale ni fabrication industrielle d'armes. Loi privée de coutumes commerciales avec prérequis international_relations pour les royaumes concernés ; aucun changement d'un effet commun. **MAD garde exactement ses technologies héritées.** Graphe TECH, recettes et PM communs inchangés.

Les26nouveaux profils sont **PASS_STATIC_ONLY**. La comparaison MAD/FRA/POR n'introduit aucun P0/P1 ; les dettes natives de MAD, notamment les conditions de recrutement de certaines unités, restent documentées dans TECH_NON_REGRESSION.json. Aucune technologie distribuée pour dissimuler ces dettes. Les lois demandées et PM explicites sont vérifiés ; les défauts moteur et lois réellement actives ne sont pas certifiés.

## Population et armée

Monde : **837,328,539 → 837,328,539**, delta **0**. Les deux totaux régionaux et toutes les cohortes culturelles, religieuses et serviles sont conservés. La ventilation par nombre de provinces natives uniques, avec arrondis conservatifs, est **technique**, pas un recensement de1776. Les chiffres comoriens héritent du pool statistique natif de SOUTH_MADAGASCAR ; aucune conversion de POP ni reconstruction démographique de l'archipel.

| Pays/agrégat | Avant | Après |
|---|---:|---:|
| AHI | 0 | 32 748 |
| ANR | 0 | 65 493 |
| ASK | 0 | 27 225 |
| ATF | 0 | 27 225 |
| ATK | 0 | 180 106 |
| ATM | 0 | 40 834 |
| ATY | 0 | 27 225 |
| AVR | 0 | 32 747 |
| BAR | 0 | 136 118 |
| BHK | 0 | 32 746 |
| BOI | 0 | 259 014 |
| BSM | 0 | 212 855 |
| BZN | 0 | 49 120 |
| CMO | 0 | 13 613 |
| IKO | 0 | 27 225 |
| ISD | 0 | 40 834 |
| LLG | 0 | 27 223 |
| MAD | 1 826 330 | 32 746 |
| MDN | 0 | 40 834 |
| MEB | 0 | 152 491 |
| MHF | 0 | 68 059 |
| MSR | 0 | 54 447 |
| RND | 0 | 27 223 |
| SNK | 0 | 65 493 |
| TDY | 0 | 40 834 |
| TMH | 0 | 98 239 |
| TNL | 0 | 13 613 |

Détails : POPULATION_LEDGER.json et POPULATION_BEFORE_AFTER.csv. Cultures nationales moteur malagasy et, pour les Comores, swahili/malagasy sont des proxys documentés. Aucun profil culturel de POP n'est réécrit.

Les niveaux bâtis et PM ne sont pas modifiés : les portions natives des historiques de bâtiments examinées sont vides. Armée existante conservée par nombre/type/service ; les neuf conscrits référencés au sud sont rattachés au nord où MAD possède encore une portion. Aucun régiment créé, retiré ou attribué arbitrairement aux nouveaux royaumes. Manpower, budgets et capacité effective de mobilisation après le partage ne sont pas des résultats observés.

## Contrôles et concurrence

VALIDATION.json : **311/311 contrôles statiques**, dont delta exact des propriétaires mondiaux, absence de nouveau doublon, cultures référencées, capitales régionales possédées, continuité des noyaux et préservation hors blocs autorisés. Aucun nouveau noyau centralisé isolé dans des seuls pays décentralisés. Petites dépendances côtières héritées d'Antankarana et archipels sont distingués des poches continentales ; Imamo/Andratsay reste explicitement plural et non contigu.

**5fichiers existants ciblés et33ajouts fonctionnels.** Seuls deux nœuds d'états, deux nœuds POP, c:MAD de l'histoire nationale et militaire, et MAD des noms dynamiques sont modifiés. Les autres nations de ces fichiers sont conservées. Les versions WORLD antérieures, SERG, TECH/ECON et Amériques restent protégées ; aucun Git, vanilla ou suiviSERG écrit. Pas de retour à une ancienne baseline. FILES_MODIFIED.json est le reçu immédiat, FILES_DELIVERED.json et DELIVERY_MANIFEST.json la version livrée. Contrôle documentaire final : DELIVERY_VALIDATION.json.

Les noyaux sont des approximations sur cellules entières. À l'échelle native, les trois collines royales merina ne peuvent pas toutes être localisées exactement ; aucun cadastre fictif créé pour y remédier. Les noms/points de hubs natifs parfois inadéquats ne sont pas déplacés. Les frontières internes des agrégats, conditions tributaires restantes, installations européennes ponctuelles et densités historiques restent ouverts. Voir GEOGRAPHIC_LIMITATIONS.md.

Chargement, portraits/drapeaux, capitales affichées, marchés, budgets, fronts, simulation et sauvegarde/rechargement : **NOT_RUN**, intégrés au **test africain groupé**, aucun test intermédiaire demandé. Aucun reçu humain nouveau. WORLD reste **10/320 (3,13%)** ; aucun critère entier crédité pour une restauration partielle. L'Afrique australe/VOC est la suite demandée, non commencée par ce lot.
