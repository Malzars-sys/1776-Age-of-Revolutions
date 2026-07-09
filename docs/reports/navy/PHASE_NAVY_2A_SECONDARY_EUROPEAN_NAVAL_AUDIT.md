# Phase NAVY-2A - Audit des puissances navales secondaires europeennes

## 1. Resume executif

Cette phase est un audit uniquement. Aucun fichier gameplay n'a ete modifie.

Le mod contient deja des flottes pour les principales puissances navales secondaires de 1776 : Provinces-Unies/Netherlands, Portugal, Danemark-Norvege, Suede, Empire ottoman, Venise et Deux-Siciles. Le probleme technique principal n'est donc pas l'absence totale de navires, mais l'usage massif d'anciens `hq_region` qui n'existent plus dans Victoria 3 The Great Wave / 1.13.

Constat prioritaire :

- `region_rhine`, `region_baltic`, `region_iberia`, `region_italy`, `region_anatolia` et `region_arabic` sont introuvables dans la vanilla 1.13 locale.
- Les flottes ciblees n'ont pas d'amiraux historiques attaches, a l'exception de la Russie qui a deja ete traitee dans NAVY-1A.
- Les puissances ciblees ont des ports et souvent des chantiers navals, mais presque aucune n'a de `building_naval_administration`.
- Aucune loi navale explicite du groupe The Great Wave (`law_merchant_navy`, `law_professional_navy`, `law_diplomatic_navy`) n'a ete trouvee dans les fichiers pays audites.
- Maroc/Algerie/Barbaresques sont incoherents techniquement : `MOR` et `MAS` sont utilises dans history/states, buildings ou diplomacy, mais aucune definition pays claire n'a ete trouvee pour eux dans les fichiers audites.

La phase suivante la plus sure est de separer la correction en deux blocs :

- NAVY-2B : Europe du Nord / Atlantique (`NET`, `POR`, `DENNOR`, `SWE`, plus `DEI` en note coloniale).
- NAVY-2C : Mediterranee (`TUR`, `VEN`, `SIC`, petits Etats italiens, `TUN`, `TRI`, `MOR`/`MAS` a clarifier).

## 2. Chemin vanilla utilise

Reference vanilla confirmee :

```txt
C:\Games\Victoria 3 The Great Wave\game
```

Le dossier existe et contient les strategic regions vanilla The Great Wave utilisees pour valider les `hq_region`.

## 3. Tags trouves pour les pays cibles

| Nom historique | Tag trouve | Fichiers concernes | Statut |
|---|---|---|---|
| Provinces-Unies / Netherlands | `NET` | `common/country_definitions/00_countries.txt`, `common/history/countries/net - netherlands.txt`, `common/history/military_formations/00_military_formations_europe.txt` | actif |
| Dutch East Indies Company | `DEI` | `common/history/countries/dei - dutch east indies company.txt`, `common/history/countries/net - netherlands.txt`, `common/history/military_formations/06_military_formations_asia.txt` | tag colonial lie a `NET`; pas de tag `VOC` trouve |
| Portugal | `POR` | `common/country_definitions/00_countries.txt`, `common/history/countries/por - portugal.txt`, `common/history/military_formations/00_military_formations_europe.txt` | actif |
| Danemark-Norvege | `DENNOR` | `common/country_definitions/02_modded_countries.txt`, `common/history/countries/dennor - denmark-norway.txt`, `common/history/military_formations/00_military_formations_europe.txt` | actif |
| Danemark | `DEN` | vanilla/mod country definitions et history country | present mais la flotte utilise `DENNOR` |
| Norvege | `NOR` | country definitions, history country, petite flotte dans formations | present; probablement lie au setup `DENNOR` |
| Suede | `SWE` | `common/country_definitions/00_countries.txt`, `common/history/countries/swe - sweden.txt`, formations Europe | actif |
| Empire ottoman | `TUR` | `common/country_definitions/00_countries.txt`, `common/history/countries/tur - ottoman empire.txt`, formations Middle East | actif |
| Ottoman alternatif | `OTT` | aucun resultat utile | absent |
| Venise | `VEN` | country definitions, `ven - venetia.txt`, formations Europe | actif |
| Deux-Siciles | `SIC` | country definitions, `sic - two sicilies.txt`, formations Europe | actif |
| Sicile separee | `GR3` | `common/country_definitions/02_modded_countries.txt`, `gr3 - sicily.txt`, buildings | present; sujet de `SIC` dans diplomacy |
| Naples separee | `GR4` | `common/country_definitions/02_modded_countries.txt`, `gr4 - naples.txt` | present; pas de flotte dediee trouvee |
| Sardaigne-Piemont | `SAR` | country definitions, formations Europe | petit Etat cotier avec flotte |
| Papal States | `PAP` | country definitions, formations Europe | petite flotte symbolique |
| Toscane | `TUS` | country definitions, formations Europe | petite flotte symbolique |
| Genes | `GEN` | `common/country_definitions/02_modded_countries.txt`, formations Europe | flotte existante, nom suspect |
| Maroc | `MOR` | utilise dans states/buildings/diplomacy | tag utilise mais pas defini dans les fichiers de pays audites |
| Mascara / Algerie occidentale | `MAS` | utilise dans states/buildings/formations/diplomacy | tag utilise mais pas defini dans country definitions auditees |
| Tunis | `TUN` | history country, formations North Africa | actif |
| Tripoli | `TRI` | history country, states/buildings/diplomacy | actif, pas de flotte trouvee |
| Alger / Algiers | `ALG` / `ALD` | aucun tag utile trouve | absent ou remplace par `MAS` |
| Oman | `OMA` | country definitions, history country, formations Middle East | present; a traiter en NAVY-3 |
| Russie | `RUS` | deja traitee en NAVY-1A | point de comparaison uniquement |

## 4. Flottes existantes par pays

| Pays | Flotte | Fichier / ligne | hq_region | Valide 1.13 ? | Vaisseaux de ligne | Fregates | Total | Amiral attache ? |
|---|---|---:|---|---|---:|---:|---:|---|
| `NET` | `Koninklijke_Marine` | `common/history/military_formations/00_military_formations_europe.txt:4265` | `region_rhine` | non | 9 | 25 | 34 | non |
| `DEI` | `Koloniale_Marine` | `common/history/military_formations/06_military_formations_asia.txt:586` | `region_indonesia` | oui | 0 | 1 | 1 | non |
| `POR` | `Marinha_Real_Portuguesa` | `common/history/military_formations/00_military_formations_europe.txt:4427` | `region_iberia` | non | 6 | 8 | 14 | non |
| `DENNOR` | `Kongelige_Danske_Marine` | `common/history/military_formations/00_military_formations_europe.txt:3556` | `region_baltic` | non | 6 | 8 | 14 | non |
| `NOR` | `Kongelige_Norske_Marine` | `common/history/military_formations/00_military_formations_europe.txt:3670` | `region_baltic` | non | 0 | 1 | 1 | non |
| `SWE` | `Hgsjflottan` | `common/history/military_formations/00_military_formations_europe.txt:3445` | `region_baltic` | non | 9 | 9 | 18 | non |
| `TUR` | `Donanmay_Humyn` | `common/history/military_formations/04_military_formations_middle_east.txt:194` | `region_anatolia` | non | 8 | 7 | 15 | non |
| `VEN` | `merchant_venice_fleet` | `common/history/military_formations/00_military_formations_europe.txt:530` | `region_italy` | non | 1 | 19 | 20 | non |
| `SIC` | `Armata_di_Mare_di_SM_il_Re_del_Regno_delle_Due_Sicilie` | `common/history/military_formations/00_military_formations_europe.txt:3922` | `region_italy` | non | 2 | 6 | 8 | non |
| `GEN` | `merchant_venice_fleet` | `common/history/military_formations/00_military_formations_europe.txt:496` | `region_italy` | non | 1 | 7 | 8 | non |
| `SAR` | `Marina_del_Regno_di_Sardegna` | `common/history/military_formations/00_military_formations_europe.txt:4038` | `region_italy` | non | 0 | 5 | 5 | non |
| `PAP` | `Marina_Pontificia` | `common/history/military_formations/00_military_formations_europe.txt:4100` | `region_italy` | non | 0 | 1 | 1 | non |
| `TUS` | `Marina_del_Granducato_di_Toscana` | `common/history/military_formations/00_military_formations_europe.txt:4144` | `region_italy` | non | 0 | 1 | 1 | non |
| `TUN` | `Bahriat_alTuwnusia` | `common/history/military_formations/03_military_formations_north_africa.txt:3` | `region_north_africa` | oui | 0 | 1 | 1 | non |
| `OMA` | `Bahriat_alMasqat` | `common/history/military_formations/04_military_formations_middle_east.txt:238` | `region_arabic` | non | 1 | 5 | 6 | non |
| `RUS` | `Baltiyskiy_Flot` + `Okhotskaya_Voyennaya_Flotiliya` | `common/history/military_formations/00_military_formations_europe.txt:2726`, `:2751` | `region_russia`, `region_northeast_asia` | oui | 14 | 10 | 24 | oui |

La flotte russe est incluse comme reference : elle est deja corrigee et ne doit pas etre modifiee dans NAVY-2.

## 5. Pays avec 0 navire mais qui devraient en avoir

| Pays / zone | Tag probable | Situation actuelle | Commentaire |
|---|---|---|---|
| Maroc | `MOR` | pas de flotte trouvee | `MOR` est utilise dans states/buildings/diplomacy mais pas defini clairement dans les fichiers pays audites. A clarifier avant creation de flotte. |
| Alger / Mascara / Oran | `MAS` probablement | pas de flotte, seulement une armee terrestre | `MAS` couvre des states d'Alger/Oran et peut representer une regence ou un pouvoir local. Besoin d'audit tag avant NAVY-2C. |
| Tripoli | `TRI` | pas de flotte trouvee | Devrait probablement avoir une petite force corsaire/littorale si le tag est actif. |
| Naples separee | `GR4` | pas de flotte dediee | Si `SIC` est le suzerain principal, la flotte `SIC` suffit. Si `GR4` est jouable, une petite flotte napolitaine peut manquer. |
| Sicile separee | `GR3` | pas de flotte dediee | `GR3` est sujet de `SIC`; le besoin depend du setup politique final. |

## 6. hq_region invalides ou suspects

Regions vanilla 1.13 valides utiles confirmees :

- `region_western_europe`
- `region_northern_europe`
- `region_southern_europe`
- `region_near_east`
- `region_north_africa`
- `region_arabia`
- `region_indonesia`
- `region_russia`
- `region_northeast_asia`
- regions maritimes valides : `region_north_sea`, `region_southern_baltic_sea`, `region_baltic_entrances`, `region_adriatic_sea`, `region_aegean_sea`, `region_sea_of_marmara`, `region_eastern_mediterranean_sea`, `region_lusitanian_sea`, `region_western_indian_ocean`.

| Pays | hq_region actuel | Statut | Region recommandee a verifier en NAVY-2B/2C |
|---|---|---|---|
| `NET` | `region_rhine` | invalide | `region_western_europe` pour HQ terrestre ; `region_north_sea` ou `region_english_channel` si le systeme accepte un HQ maritime |
| `POR` | `region_iberia` | invalide | `region_southern_europe` ; eventuellement `region_lusitanian_sea` si HQ maritime accepte |
| `DENNOR` / `NOR` | `region_baltic` | invalide | `region_northern_europe` ; eventuellement `region_baltic_entrances` ou `region_southern_baltic_sea` pour une logique maritime |
| `SWE` | `region_baltic` | invalide | `region_northern_europe` ; eventuellement `region_southern_baltic_sea` |
| `VEN`, `SIC`, `GEN`, `SAR`, `PAP`, `TUS` | `region_italy` | invalide | `region_southern_europe`; Venise peut aussi viser `region_adriatic_sea` si HQ maritime accepte |
| `TUR` | `region_anatolia` | invalide | `region_near_east`; alternative maritime : `region_sea_of_marmara`, `region_aegean_sea`, `region_eastern_mediterranean_sea` |
| `OMA` | `region_arabic` | invalide | `region_arabia`; alternative maritime : `region_western_indian_ocean` |
| `TUN` | `region_north_africa` | valide | aucune correction HQ evidente |
| `DEI` | `region_indonesia` | valide | aucune correction HQ evidente |
| `RUS` | `region_russia`, `region_northeast_asia` | valide | ne pas modifier |

## 7. Batiments navals par pays

Synthese des niveaux trouves dans `common/history/buildings/*` :

| Pays | Ports | Chantiers navals | Naval administration | Autres notes |
|---|---:|---:|---:|---|
| `NET` | 12 | 4 | 0 | solide base commerciale et coloniale, mais pas d'administration navale The Great Wave |
| `DEI` | 6 | 0 | 0 | ports coloniaux, petite flotte seulement |
| `POR` | 16 | 6 | 0 | bonne logistique portuaire imperiale |
| `DENNOR` | 11 | 4 | 0 | ports metropole + outre-mer ; cohérent pour NAVY-2B |
| `SWE` | 5 | 2 | 0 | chantiers plus faibles que la flotte actuelle de 18 navires |
| `TUR` | 21 | 7 | 0 | infrastructure large, compatible avec une puissance regionale |
| `VEN` | 11 | 2 | 0 | bonne presence portuaire, flotte actuelle tres chargee en fregates |
| `SIC` | 4 | 0 | 0 | flotte existante mais aucun chantier detecte pour `SIC` |
| `GEN` | 3 | 2 | 0 | petite infrastructure valable |
| `SAR` | 2 | 3 | 0 | petite marine plausible |
| `PAP` | 1 | 0 | 0 | flotte symbolique seulement |
| `TUS` | 2 | 0 | 0 | flotte symbolique seulement |
| `MOR` | 2 | 0 | 0 | tag non defini clairement, mais buildings existent |
| `MAS` | 1 | 0 | 0 | tag non defini clairement, mais buildings existent |
| `TUN` | 1 | 0 | 0 | petite flotte presente |
| `TRI` | 1 | 0 | 0 | pas de flotte presente |
| `OMA` | 5 | 1 | 0 | a traiter en NAVY-3 |
| `RUS` | 9 | 3 | 0 | reference deja corrigee |

Aucun ancien ID naval obsolète de type `building_military_shipyard`, `building_naval_base` ou `pm_military_shipbuilding_*` n'a ete retrouve dans les fichiers audites. Les seuls `building_naval_administration` detectes concernent surtout les grandes puissances deja traitees (`GBR`, `FRA`, `SPA`) et quelques zones hors cible.

## 8. Lois navales actuelles par pays

Recherche effectuee dans `common/history/countries/*` pour :

- `law_merchant_navy`
- `law_professional_navy`
- `law_diplomatic_navy`
- `law_jeune_ecole`
- `lawgroup_navy_model`

| Pays | Loi navale explicite trouvee | Recommandation future |
|---|---|---|
| `NET` | aucune | `law_diplomatic_navy` ou `law_merchant_navy`; privilegier commerce et convois |
| `DEI` | aucune | ne pas forcer sans audit colonial |
| `POR` | aucune | `law_diplomatic_navy` plausible pour empire atlantique |
| `DENNOR` | aucune | `law_professional_navy` plausible si prerequis tech confirme |
| `SWE` | aucune | `law_professional_navy` plausible pour battlefleet baltique |
| `TUR` | aucune | `law_professional_navy` plausible, sinon `law_merchant_navy` si prerequis manque |
| `VEN` | aucune | `law_professional_navy` ou `law_merchant_navy`; a calibrer avec flotte reduite |
| `SIC` | aucune | `law_merchant_navy` ou `law_professional_navy` selon tech |
| `GEN`, `SAR`, `PAP`, `TUS` | aucune | probablement aucune loi forcee avant audit des petits Etats |
| `TUN`, `TRI`, `MOR`/`MAS` | aucune | rester prudent; pas de doctrine oceanique |
| `OMA` | aucune | NAVY-3, probablement `law_merchant_navy` si implemente |
| `RUS` | aucune dans fichier pays actuel audite | deja traitee cote flotte/amiral; loi a ne pas changer dans NAVY-2A |

## 9. Classement historique approximatif

Base : `docs/research/WORLD_NAVIES_1776_THE_GREAT_WAVE_ROADMAP.md`.

| Tier | Pays |
|---|---|
| Grandes puissances deja traitees | Grande-Bretagne, France, Espagne |
| Reference regionale deja corrigee | Russie |
| Tier secondaire fort | `NET`, `POR`, `DENNOR`, `SWE`, `TUR` |
| Tier regional mediterraneen | `VEN`, `SIC`, `GEN`, `SAR` |
| Littoral / corsaire | `MOR`/`MAS`, `TUN`, `TRI` |
| Hors NAVY-2 | `OMA`, Inde, Qing, Japon, Coree, Siam |

Le point de balance important : ces pays doivent rester derriere le trio `GBR` / `FRA` / `SPA`, et en general derriere ou autour de la Russie corrigee, selon le bassin. Les Provinces-Unies doivent etre fortes commercialement, mais pas redevenir une super-battlefleet du XVIIe siecle.

## 10. Proposition de flotte future par pays

Ordre de grandeur seulement, sans implementation dans cette phase.

| Pays | Etat actuel | Proposition future prudente | Loi navale future | Note |
|---|---|---|---|---|
| `NET` | 9 SOL + 25 fregates | 6-8 SOL + 10-14 fregates, plus `DEI` 1-3 fregates coloniales | `law_diplomatic_navy` | reduire la surmasse en fregates ou la repartir entre metropole et commerce |
| `POR` | 6 SOL + 8 fregates | 5-6 SOL + 6-8 fregates | `law_diplomatic_navy` | actuel deja proche d'un bon niveau |
| `DENNOR` + `NOR` | 6 SOL + 9 fregates | 5-6 SOL + 6-8 fregates, eventuellement 1 fregate norvegienne | `law_professional_navy` | corriger d'abord HQ invalides |
| `SWE` | 9 SOL + 9 fregates | 6-7 SOL + 6-8 fregates | `law_professional_navy` | probablement un peu haut par rapport a la Russie corrigee |
| `TUR` | 8 SOL + 7 fregates | 5-7 SOL + 6-8 fregates | `law_professional_navy` si tech OK | puissance regionale forte, pas oceanique |
| `VEN` | 1 SOL + 19 fregates | 1-2 SOL + 4-6 fregates | a verifier | flotte actuelle tres lourde en fregates |
| `SIC` | 2 SOL + 6 fregates | 1-2 SOL + 3-5 fregates | a verifier | regional, pas grande puissance |
| `GEN` | 1 SOL + 7 fregates | 0-1 SOL + 2-4 fregates | probablement aucune loi forcee | nom de flotte actuellement suspect |
| `SAR` | 5 fregates | 2-4 fregates | aucune loi forcee | suffisant comme marine regionale |
| `PAP` / `TUS` | 1 fregate chacun | 0-1 fregate symbolique | aucune loi forcee | eviter surmodele |
| `TUN` | 1 fregate | 1-2 navires legers si modeles disponibles | aucune loi oceanique | corsaire/littoral |
| `TRI` | 0 | 1 navire leger/fregate max si tag actif | aucune loi oceanique | a traiter avec Barbaresques |
| `MOR`/`MAS` | 0 | 1-2 navires legers chacun si tags valides | aucune loi oceanique | clarifier tags d'abord |
| `OMA` | 1 SOL + 5 fregates | NAVY-3 : probablement moins de SOL, plus flotte de commerce/littoral | `law_merchant_navy` possible | hors NAVY-2B |

## 11. Besoins en amiraux historiques

Les flottes ciblees n'ont pas d'amiraux historiques attaches dans les blocs audites. Les seuls amiraux historiques confirmes dans le perimetre de comparaison sont russes :

- Vasily Chichagov
- Samuel Greig
- Alexei Senyavin

Priorite amiraux future :

| Pays | Besoin | Priorite |
|---|---|---|
| `NET` | 1 amiral metropolitain, eventuellement 1 colonial si `DEI`/VOC devient important | haute |
| `POR` | 0-1 amiral, seulement si source fiable | moyenne |
| `DENNOR` | 1 amiral ou reformateur naval | haute |
| `SWE` | 1 amiral principal | haute |
| `TUR` | 1 amiral principal | haute |
| `VEN` | 1 amiral regional | moyenne-haute |
| `SIC` | 0-1, prudence historique | moyenne |
| `MOR`/`MAS`, `TUN`, `TRI` | aucun nom sans recherche dediee | basse |
| `OMA` | hors NAVY-2, recherche dediee NAVY-3 | basse |

Pour les personnages historiques majeurs, une phase future peut verifier le format vanilla des liens Wikipedia et l'appliquer aux amiraux fiables. Cette phase ne cree aucun personnage et n'ajoute aucun lien.

## 12. Amiraux et noms de flottes proposes

Liste preparatoire uniquement.

| Pays | Flotte proposee | Nom historique/plausible | Amiraux candidats | Confiance | Recommandation |
|---|---|---|---|---|---|
| `NET` | flotte metropolitaine | Escadre de Texel; Escadre de la Meuse/Maas; Escadre de Zelande | Jan Hendrik van Kinsbergen; Johan Zoutman; Lodewijk van Bylandt | moyenne-haute | utiliser Van Kinsbergen ou Zoutman apres verification du service exact en 1776 |
| `DEI` / VOC | flotte coloniale | Escadre des Indes orientales; Escadre de Batavia; Koloniale Marine | aucun candidat sur | moyenne-basse | verifier davantage; ne pas inventer |
| `POR` | flotte atlantique | Esquadra do Tejo; Esquadra de Lisboa; Esquadra do Brasil | Robert MacDouall; Jorge Hardcastle | faible-moyenne | verifier davantage avant usage; flotte nommee sans amiral si doute |
| `DENNOR` | flotte baltique | Kongelige Danske Marine; Escadre de Copenhague; Escadre du Sund | Frederik Christian Kaas; Henrik Gerner | moyenne | Kaas a verifier pour le rang; Gerner plutot reformateur/logistique |
| `SWE` | flotte suedoise | Orlogsflottan; Escadre de Karlskrona; Armens flotta; Flotte de l'archipel | Henrik af Trolle; Fredrik Henrik af Chapman; Carl August Ehrensvard | haute pour Trolle, moyenne pour les autres | utiliser Trolle; Chapman seulement comme profil technique si le jeu le permet |
| `TUR` | flotte ottomane | Donanma-yi Humayun; Flotte du Kapudan Pasha; Escadre de Constantinople | Cezayirli Gazi Hasan Pasha | haute | utiliser en NAVY-2C si la syntaxe amiral est confirmee |
| `VEN` | flotte venitienne | Armata Grossa; Squadra del Levante; Squadra dell'Adriatico | Angelo Emo; Giacomo Nani | haute pour Emo, moyenne pour Nani | utiliser Angelo Emo; verifier Nani |
| `SIC` / `GR4` | flotte napolitaine/sicilienne | Real Marina Napoletana; Escadre de Naples; Escadre de Sicile | John Acton; Francesco Caracciolo | faible-moyenne | Acton a verifier pour 1776; Caracciolo probablement trop jeune pour grand commandement |
| `GEN` | petite marine ligure | Marina Genovese; Escadre de Genes | aucun candidat fiable | faible | ne pas creer d'amiral historique sans recherche |
| `SAR` | marine sarde | Marina del Regno di Sardegna | aucun candidat fiable | faible | verifier davantage |
| `MOR` | flotte cherifienne | Escadre de Sale; Corsaires de Sale; Flotte cherifienne | a rechercher | faible | ne pas creer d'amiral historique pour l'instant |
| `MAS` / Alger | regence/corsaires | Escadre d'Alger; Taifa des rais d'Alger | a rechercher; ne pas utiliser Rais Hamidou en 1776 | faible | verifier tags et sources avant tout |
| `TUN` | flotte tunisienne | Escadre de Tunis | a rechercher | faible | laisser sans amiral historique pour l'instant |
| `TRI` | flotte tripolitaine | Escadre de Tripoli | a rechercher | faible | laisser sans amiral historique pour l'instant |
| `OMA` | flotte de Mascate | Flotte de Mascate; Escadre d'Oman; Flotte de l'ocean Indien | a rechercher | faible | reporter a NAVY-3 |

Pays ou les candidats sont solides : `SWE`, `TUR`, `VEN`, puis `NET`.

Pays ou une recherche supplementaire est necessaire : `POR`, `DENNOR`, `SIC`, `DEI`, `GEN`, `SAR`.

Pays ou il vaut mieux ne pas creer d'amiral historique pour l'instant : `MOR`, `MAS`, `TUN`, `TRI`, `OMA`.

## 13. Besoins en logistique navale

| Pays | Besoin principal |
|---|---|
| `NET` | Revoir repartition metropole/colonies, eventuellement renforcer la logique commerciale plutot que le pur combat de ligne. |
| `POR` | Conserver Lisbonne/Bresil/Inde comme axe logistique, sans grossir la flotte au-dessus de l'Espagne. |
| `DENNOR` | Corriger HQ Baltique et garder Copenhague comme pivot. |
| `SWE` | Corriger HQ Baltique, verifier que les chantiers suffisent a soutenir 18 navires actuels. |
| `TUR` | Corriger HQ Anatolie, garder Constantinople/Marmara/Egee comme centre. |
| `VEN` | Reduire ou mieux calibrer les 19 fregates; l'Arsenal/Adriatique doit compter sans creer une puissance oceanique. |
| `SIC` | Ajouter eventuellement un chantier si la flotte reste a 8 navires, ou reduire la flotte. |
| `MOR`/`MAS`/`TUN`/`TRI` | Modeler comme corsaire/littoral, pas comme battlefleet. |
| `OMA` | Reporter a l'ocean Indien en NAVY-3. |

## 14. Decoupage recommande NAVY-2B / NAVY-2C / NAVY-3

NAVY-2B - Europe du Nord / Atlantique :

- Corriger uniquement `NET`, `POR`, `DENNOR`, `NOR` si necessaire, `SWE`.
- Remplacer les `hq_region` invalides.
- Ajouter ou verifier les lois navales seulement si les prerequis tech sont confirmes.
- Ajouter les amiraux fiables : `NET`, `DENNOR`, `SWE` en priorite.
- Ne pas traiter les Barbaresques ni Oman dans cette phase.

NAVY-2C - Mediterranee / puissances regionales :

- Corriger `TUR`, `VEN`, `SIC`.
- Auditer les petits Etats italiens (`GEN`, `SAR`, `PAP`, `TUS`) sans les transformer en grandes marines.
- Clarifier `MOR` / `MAS` / `TUN` / `TRI`, puis ajouter seulement de petites forces si les tags sont valides.
- Ajouter Cezayirli Gazi Hasan Pasha et Angelo Emo seulement si le format amiral est stable.

NAVY-3 - Puissances non europeennes :

- `OMA`, Inde, Qing, Japon, Coree, Siam et autres puissances littorales.
- Ne pas importer NAVY-2B/2C dans l'ocean Indien sans audit dedie.

## 15. Risques techniques

- Les `hq_region` invalides sont le risque le plus immediat pour `create_military_formation`.
- Certains tags sont utilises sans definition claire (`MOR`, `MAS`), ce qui peut casser ownership, buildings ou diplomacy si on ajoute des flottes avant de clarifier les pays.
- Plusieurs flottes sont probablement surdimensionnees par rapport a l'echelle post-NAVY-1A, surtout `NET`, `VEN` et peut-etre `SWE`.
- Les lois navales The Great Wave ont des prerequis technologiques : ne pas ajouter `law_professional_navy` ou `law_diplomatic_navy` sans verifier la tech de depart.
- Les regions maritimes existent, mais il faut verifier en jeu si `hq_region` accepte vraiment une region maritime ou s'il faut rester sur les strategic regions terrestres.
- Les petits Etats italiens peuvent devenir trop importants si leurs flottes sont traitees comme des battlefleets.

## 16. Liste exacte des fichiers lus

Fichiers et dossiers lus pendant l'audit :

- `docs/research/WORLD_NAVIES_1776_THE_GREAT_WAVE_ROADMAP.md`
- `docs/reports/navy/PHASE_NAVY_1C_GREAT_POWER_NAVAL_LAWS.md`
- `docs/reports/navy/PHASE_NAVY_1A_QUINQUIES_RUSSIAN_FLEET_HQ_AND_REBALANCE.md`
- `common/country_definitions/00_countries.txt`
- `common/country_definitions/02_modded_countries.txt`
- `common/history/countries/*.txt`
- `common/history/military_formations/00_military_formations_europe.txt`
- `common/history/military_formations/03_military_formations_north_africa.txt`
- `common/history/military_formations/04_military_formations_middle_east.txt`
- `common/history/military_formations/06_military_formations_asia.txt`
- `common/history/buildings/00_west_europe.txt`
- `common/history/buildings/01_south_europe.txt`
- `common/history/buildings/03_north_africa.txt`
- `common/history/buildings/04_subsaharan_africa.txt`
- `common/history/buildings/05_north_america.txt`
- `common/history/buildings/06_central_america.txt`
- `common/history/buildings/07_south_america.txt`
- `common/history/buildings/08_middle_east.txt`
- `common/history/buildings/09_central_asia.txt`
- `common/history/buildings/10_india.txt`
- `common/history/buildings/11_east_asia.txt`
- `common/history/buildings/12_indonesia.txt`
- `common/history/buildings/14_siberia.txt`
- `common/history/buildings/15_russia.txt`
- `common/history/states/00_states.txt`
- `common/history/diplomacy/00_subject_relationships.txt`
- `common/history/diplomacy/00_relations.txt`
- `common/history/diplomacy/00_rivalries.txt`
- `C:\Games\Victoria 3 The Great Wave\game\common\strategic_regions\*.txt`

## 17. Confirmation de perimetre

Cette phase n'a modifie aucun fichier gameplay :

- aucun navire cree ;
- aucun `count` modifie ;
- aucun `hq_region` modifie ;
- aucun amiral cree ;
- aucun batiment modifie ;
- aucune loi modifiee ;
- aucune technologie modifiee ;
- aucune localisation modifiee.

Le seul fichier cree par cette phase est :

```txt
docs/reports/navy/PHASE_NAVY_2A_SECONDARY_EUROPEAN_NAVAL_AUDIT.md
```

Note Git : le prompt indiquait un depot propre, mais le `git status --short` initial contenait deja de nombreux changements issus de phases precedentes. Ils n'ont pas ete modifies par cet audit.
