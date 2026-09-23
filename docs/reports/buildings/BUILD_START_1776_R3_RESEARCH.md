# BUILD START 1776 — R3 Middle East / North Africa / Caucasus / Central Asia — Historical Research

**Date absolue : 1776-01-01. Recherche uniquement. Aucun changement gameplay.**

## 1. Périmètre et discipline

- **154** couples `Owner_TAG + State_ID` audités, couvrant **97 State_ID** et **65 TAG**.
- **73** bâtiments admissibles du catalogue ont été passés en revue; les auto-generated, `NO_ENGINE_GENERATED`, `NO_POST_1776` et VEN/GEN sont exclus.
- Les recommandations ne partent pas de la distribution actuelle des bâtiments. Elles sont une première proposition historique indépendante.
- `building_trade_center` est réservé aux entrepôts/places de redistribution ou commerce de longue distance; un port ou un marché urbain ordinaire ne suffit pas.
- `building_railway` est utilisé uniquement comme infrastructure terrestre régionale. Toutes les lignes ont `pm_no_rail_network`; routes et canaux sont justifiés séparément.
- Une porte technologique absente ne supprime jamais une recommandation historique : `Tech_Distribution_Review = YES`.

## 2. Résultat quantitatif

- Recommandations positives : **486** couples Owner/State/Building.
- Couples Owner/State sans seed positif après revue : **4**.
- `Tech_Distribution_Review = YES` : **107** recommandations.
- Centres de commerce : **33** recommandations, volontairement rares.
- Ports : **28** recommandations.
- Infrastructures régionales pré-rail : **72** recommandations, toutes sans rail actif.

### Répartition par catégorie

- `ADMINISTRATION` : 6
- `AGRICULTURE_COMMERCIAL` : 194
- `EDUCATION` : 5
- `INFRASTRUCTURE` : 72
- `MANUFACTURING` : 92
- `MILITARY` : 9
- `OTHER` : 5
- `PLANTATION` : 19
- `PORT` : 28
- `RESOURCE_EXTRACTION` : 12
- `SHIPBUILDING` : 11
- `TRADE_CENTER` : 33

## 3. Principes historiques par sous-région

### Empire ottoman — Anatolie, Levant et Égypte

L’économie ottomane du XVIIIe siècle reste largement préindustrielle mais conserve des manufactures urbaines et rurales importantes. Alep justifie clairement du textile organisé; Bursa/Hüdavendigâr justifie soie + textile; İzmir/Aydın est un cas net de grand port et de centre de commerce. L’Égypte demeure la plus riche province ottomane, exportant riz, sucre et blé, et redistribuant le café du Yémen. Les niveaux recommandés restent toutefois bas pour ne pas traduire des ateliers/guildes en industrie mécanisée.

Les mines de Keban–Ergani–Gümüşhane sont un des rares secteurs extractifs où les sources de la seconde moitié du XVIIIe siècle permettent une attribution ferme; Ergani est donc retenu dans Diyarbakir.

### Perse zand

Shiraz/Fars reçoit le profil le plus dense : capitale de Karim Khan, reconstruction urbaine, bazar/caravansérails, commerce indien et européen, accès à Bushehr. Isfahan reste un grand centre de crafts malgré son déclin politique. Kerman conserve laine, textiles et cuivre; Tabriz reste un nœud caravannier; Mazandaran est retenu pour riz/soie. Les routes persanes s’appuient sur le réseau ancien de caravansérails sans extrapoler un réseau routier européen moderne.

### Afghanistan durrani

Kandahar, Kabul, Herat et Balkh reçoivent les principaux seeds commerciaux. La documentation sur les marchands indiens installés dans les domaines durraniens justifie de vrais nœuds de redistribution à Kabul/Kandahar; les grandes passes justifient l’infrastructure régionale. Les régions tribales et montagneuses restent surtout pastorales, sans industrialisation artificielle.

### Asie centrale

Bukhara est le cas le plus fort : agriculture irriguée, coton, soie, textile, papier, food processing, metalworking et infrastructures commerciales documentées. Khiva/Kokand reçoivent un profil plus léger. Les zones turkmènes/kazakhes restent surtout pastorales. Les canaux d’irrigation ne sont **pas** automatiquement convertis en PM de canal de transport.

### Caucase

Tiflis reçoit un petit ensemble urbain — crafts, trade center, route, viticulture — appuyé par les centaines de boutiques de marchands/artisans documentées à la fin du XVIIIe siècle. Circassie, Tchétchénie/Dagestan restent plus rurales/pastorales; les arts métallurgiques locaux sont représentés par `tooling_workshop` plutôt que par une industrie d’armes standardisée.

### Maghreb

La source comparative sur les ports du Maghreb permet de distinguer les vrais ports équipés : Tétouan/Oran/Alger/Tunis sont explicitement mis en avant. Alger, Tunis, Tripoli et les grands ports marocains reçoivent donc des ports/shipyards limités; les trade centers sont réservés aux grandes places. Constantine est traité comme bassin céréalier exportateur. Fez et Marrakech reçoivent surtout crafts, textile et commerce intérieur.

### Sahara et Sahel

Le traitement est volontairement faible en bâtiments : pastoralisme, millet et quelques nœuds caravaniers. Timbuktu et Bornu sont retenus comme véritables places de longue distance; Darfur est plus prudent. Le futur axe direct Benghazi–Wadai ouvert seulement vers 1809–1810 n’est pas projeté en 1776. Les fragments de désert ne reçoivent pas de trade center par simple présence sur une route caravanière.

### Golfe, Oman, Hedjaz et Yémen

Muscat est un cas fort : port, trade center, shipyard et naval administration. Les sources officielles omanaises rapportent une flotte d’environ cent navires envoyée en 1775 pour lever le siège de Basra. Jeddah reçoit port + trade center comme porte du Hajj et du commerce yéménite/indien; le Yémen reçoit le café. Les petits littoraux du Golfe sont limités à pêche/ports modestes, avec un seul seed commercial supplémentaire lorsque l’échelle marchande le justifie.

### Tibet / Himalaya

Ces États sont conservés parce que la partition R3 du pack les y place. La source de George Bogle décrit directement le commerce tibétain des années 1770 : laine, sel, manufactures grossières en laine et marchands étrangers à Lhasa. D’où un seul trade center à Lhasa, pas une industrialisation générale des hauts plateaux.

## 4. Centres de commerce retenus

- `BHN + STATE_ABU_DHABI` — Trucial Coast — niveau 1 — Bahraini/Gulf merchant networks and pearling trade justify one conservative trade seed in the Bahrain-controlled coastal partition.
- `BOR + STATE_CHAD` — Chad — niveau 1 — Bornu was integrated into long-standing trans-Saharan commerce with Tripoli/Fezzan and regional markets.
- `BUK + STATE_UZBEKIA` — Uzbekia — niveau 1 — Bukhara had commercial infrastructure supporting long-distance trade and warehouse/caravanserai property.
- `CAUC + STATE_GREATER_CAUCASUS` — Tiflis — niveau 1 — Tiflis had a dense merchant/craftsman urban economy and functioned as a Caucasian trade hub.
- `DFR + STATE_DARFUR` — Darfur — niveau 1 — Darfur participated in long-distance caravan trade toward Egypt and the central Sudan; one conservative level.
- `DUR + STATE_BALKH` — Southern Turkestan — niveau 1 — Balkh was a major oasis and trans-Eurasian commercial center tied to Bukhara and Afghanistan.
- `DUR + STATE_HERAT` — Herat — niveau 1 — Herat sat on major Iran–Central Asia–Afghanistan routes and supported merchant communities.
- `DUR + STATE_KABUL` — Kabulistan — niveau 1 — Indian merchant communities expanded in Kabul during Durrani state formation, supporting long-distance trade.
- `DUR + STATE_KANDAHAR` — Kandahar — niveau 1 — Kandahar connected Indian, Persian and Central Asian commercial routes and merchant communities.
- `HDJ + STATE_HEDJAZ` — Hedjaz — niveau 1 — Jeddah was a genuine long-distance redistribution center tied to pilgrimage and Red Sea/Indian Ocean trade.
- `IR1 + STATE_BAGHDAD` — Baghdad — niveau 1 — Baghdad was a major caravan redistribution center between Persia, Syria and Basra.
- `IR1 + STATE_BASRA` — Basra — niveau 1 — Basra was a genuine international entrepôt with European factories and Indian Ocean connections.
- `KHI + STATE_TURKMENIA` — Turkmenia — niveau 1 — Khiva remained a khanate caravan center despite eighteenth-century instability; one conservative level.
- `KOK + STATE_TAJIKISTAN` — Tajikistan — niveau 1 — Fergana-region trade was important, but one level is the maximum conservative seed in this partition.
- `MAS + STATE_ALGIERS` — Algiers — niveau 1 — These were genuine Mediterranean commercial/corsair redistribution centers, not merely urban markets.
- `MAS + STATE_ORAN` — Oran — niveau 1 — These were genuine Mediterranean commercial/corsair redistribution centers, not merely urban markets.
- `MOR + STATE_FEZ` — Fez — niveau 1 — Fez was a major inland commercial and craft center with long-distance caravan links.
- `MOR + STATE_MARRAKECH` — Marrakech — niveau 1 — Marrakech was an important inland caravan/redistribution market; one level only.
- `MSN + STATE_TIMBUKTU` — Timbuktu — niveau 1 — Timbuktu was a genuine trans-Saharan redistribution and caravan market; one level only.
- `NEP + STATE_HIMALAYAS` — Western Himalayas — niveau 1 — Nepal was an important intermediary in trans-Himalayan trade with Tibet.
- `OMA + STATE_OMAN` — Oman — niveau 1 — Muscat was a genuine regional entrepôt with foreign agencies and long-distance Indian Ocean commerce.
- `PER + STATE_FARS` — Fars — niveau 1 — Shiraz/Bushehr formed the core of Zand foreign trade, including EIC agencies and Indian/Armenian merchants.
- `PER + STATE_ISFAHAN` — Isfahan — niveau 1 — Isfahan remained a central bazaar and caravan nexus even after losing capital status.
- `PER + STATE_KHORASAN` — Khorasan — niveau 1 — Mashhad/Khorasan lay on Iran–Central Asia–Afghanistan caravan routes; one conservative trade-center seed.
- `PER + STATE_TABRIZ` — Tabriz — niveau 1 — Tabriz sat on major routes to Anatolia, the Caucasus and central Iran; one long-distance trade-center level is justified.
- `RUS + STATE_ASTRAKHAN` — Astrakhan — niveau 1 — Astrakhan was a major gateway for Persian and Central Asian merchants into Muscovy/Russia.
- `TIB + STATE_LHASA` — Lhasa — niveau 1 — Lhasa hosted foreign merchant communities and long-distance trade with Nepal, Kashmir, India and China.
- `TRI + STATE_TRIPOLI` — Tripoli — niveau 1 — Tripoli was the Mediterranean terminus of important Fezzan/Sudan caravan traffic and maritime redistribution.
- `TUN + STATE_TUNISIA` — Tunisia — niveau 1 — Tunis was increasingly commercial in the eighteenth century and functioned as a major Mediterranean market.
- `TUR + STATE_ALEPPO` — Aleppo — niveau 1 — Aleppo was a major long-distance caravan and Levant commercial node; one level is deliberately conservative.
- `TUR + STATE_AYDIN` — Aydin — niveau 1 — İzmir was a genuine long-distance entrepôt with complex financial and merchant functions; one trade-center level is conservative.
- `TUR + STATE_LEBANON` — Lebanon — niveau 1 — Levantine redistribution through coastal merchant towns is significant enough for one conservative seed.
- `TUR + STATE_LOWER_EGYPT` — Lower Egypt — niveau 1 — Cairo/Delta formed a genuine redistribution hub for Egyptian grain and Yemeni/Red Sea commodities; one level is conservative.

## 5. Infrastructure régionale

Toutes les recommandations `building_railway` de ce rapport représentent **uniquement** le réseau terrestre régional pré-rail. `pm_no_rail_network` est imposé partout. Un niveau 2 n’est utilisé que pour les axes les plus structurants (Aleppo, İzmir, Lower Egypt, Shiraz, Isfahan, Tabriz, Kabul, Kandahar, Bukhara, etc.).

Les seules justifications de canal restent explicitement séparées dans le CSV. L’Égypte reçoit des cas à examiner sur la navigation/canaux nilotiques; les réseaux d’irrigation d’Asie centrale ne sont pas assimilés par défaut à des canaux de transport industriels.

## 6. Bâtiments volontairement non proposés

**39 des 73 bâtiments admissibles** ne reçoivent aucun seed R3 dans cette passe.

- `building_alloys_plant` — Alloy Works
- `building_angkor_wat` — Angkor Wat
- `building_artillery_foundry` — Artillery Foundry
- `building_banana_plantation` — Banana Plantations
- `building_chemical_works` — Chemical Works
- `building_chichen_itza` — Chichén Itzá
- `building_coal_mine` — Coal Mines
- `building_construction_sector` — Construction Sector
- `building_dye_plantation` — Dye Plantations
- `building_easter_island_heads` — Easter Island Moai
- `building_forbidden_city` — Forbidden City
- `building_gold_mine` — Gold Mines
- `building_hagia_sophia` — Hagia Sophia
- `building_iron_mine` — Iron Mines
- `building_lead_mine` — Lead Mines
- `building_limestone_quarry` — Limestone Quarry
- `building_machu_picchu` — Machu Picchu
- `building_maize_farm` — Maize Farms
- `building_manila_cathedral_original` — Manila Cathedral
- `building_martandsuntemple` — Martand Sun Temple
- `building_observatorygreenwich` — Royal Observatory Greenwich
- `building_opium_plantation` — Opium Plantations
- `building_palazzo_san_giorgio` — Palazzo San Giorgio
- `building_pena_convent` — Pena Convent
- `building_phosphate_mine` — Phosphate Mine
- `building_rialto_commercial_complex` — Rialto Commercial Complex
- `building_rye_farm` — Rye Farms
- `building_saint_basils_cathedral` — Saint Basil’s Cathedral
- `building_salt_pan` — Salt Works
- `building_spice_plantation` — Spice Plantations
- `building_steel_mill` — Steel Mills
- `building_sulfur_mine` — Sulfur Mines
- `building_taj_mahal` — Taj Mahal
- `building_tea_plantation` — Tea Plantations
- `building_temple_of_poseidon` — Temple of Poseidon
- `building_tobacco_plantation` — Tobacco Plantations
- `building_vatican_city` — Vatican City
- `building_wat_arun` — Wat Arun
- `building_whaling_station` — Whaling Stations

Cela inclut notamment les bâtiments franchement mécanisés/industriels sans preuve régionale solide, ainsi que les monuments situés hors R3. L’absence d’une recommandation n’est pas une preuve d’inexistence absolue; elle signifie que le seuil de placement initial n’est pas atteint.

## 7. Technologies : conflits à transmettre à la synthèse

- `traditional_food_processing` : 29 recommandations historiques concernées.
- `enclosed_dock_systems` : 28 recommandations historiques concernées.
- `GATE_NOT_IN_TECH_AUDIT_INDEX:organized_workshops` : 14 recommandations historiques concernées.
- `state_dockyard_systems` : 12 recommandations historiques concernées.
- `marine_chronometry` : 5 recommandations historiques concernées.
- `scientific_fortification_siegecraft` : 5 recommandations historiques concernées.
- `specialized_technical_academies` : 4 recommandations historiques concernées.
- `improved_husbandry` : 4 recommandations historiques concernées.
- `organized_textile_production` : 3 recommandations historiques concernées.
- `shaft_mining` : 1 recommandations historiques concernées.
- `traditional_papermaking` : 1 recommandations historiques concernées.
- `GATE_NOT_IN_TECH_AUDIT_INDEX:organized_military_establishments` : 1 recommandations historiques concernées.

Ces lignes **ne doivent pas être supprimées automatiquement**. Elles doivent être croisées avec la synthèse techno; le bâtiment et la distribution technologique restent deux décisions séparées.

## 8. Bibliographie régionale structurée

- **OTTOMAN** — https://www.cambridge.org/core/books/cambridge-economic-history-of-the-modern-world/ottoman-empire-17001870/959242AE1899EE1E65604E39DE555F80
- **OTTOMAN_GUILDS** — https://www.cambridge.org/core/journals/international-review-of-social-history/article/ottoman-guilds-in-the-early-modern-era/DBB9453C3BE34AEE2D4F8D3C9E390BAA
- **OTTOMAN_MARITIME** — https://www.cambridge.org/core/journals/international-journal-of-middle-east-studies/article/abs/international-and-domestic-maritime-trade-in-the-ottoman-empire-during-the-18th-century/969BB1866B6A501B7F4BCB43D8A45BD6
- **IZMIR** — https://www.cambridge.org/core/journals/new-perspectives-on-turkey/article/trade-between-ottoman-empire-and-western-europe-the-case-of-izmir-in-the-eighteenth-century/AC7D4DED87714CEB8B70DF9899AA7D27
- **EGYPT** — https://www.cambridge.org/core/books/abs/cambridge-history-of-egypt/egypt-in-the-eighteenth-century/D758288694AE203CDF5A78CD9A5CAE56
- **OTTOMAN_MINING** — https://dergipark.org.tr/tr/pub/iutarih/article/1139633
- **BASRA** — https://www.cambridge.org/core/journals/international-journal-of-middle-east-studies/article/ottoman-shipping-in-the-indian-ocean-circa-16501900/434125ABA76399828893476152D21D8E
- **REDSEA** — https://www.cambridge.org/core/journals/journal-of-global-history/article/between-commerce-and-sanctity-ottoman-policies-and-international-boundaries-in-the-early-modern-red-sea/940FD84400E0A8584345C5108C10956A
- **PERSIA_TRADE** — https://www.iranicaonline.org/articles/commerce-vi/
- **PERSIA_ROADS** — https://www.iranicaonline.org/articles/caravansary/
- **PERSIA_ZAND** — https://www.iranicaonline.org/articles/karim-khan-zand/
- **PERSIA_CRAFTS** — https://www.iranicaonline.org/articles/isfahan-xiii-crafts/
- **PERSIA_KERMAN** — https://www.iranicaonline.org/articles/kerman-08-afsharid-zand-period/
- **PERSIA_COPPER** — https://www.iranicaonline.org/articles/copper/ii-copper-resources-in-iran/
- **CENTRAL_ASIA** — https://www.iranicaonline.org/articles/central-asia-xi/
- **CENTRAL_ASIA_18** — https://www.iranicaonline.org/articles/central-asia-vii/
- **AFGHAN_TRADE** — https://www.iranicaonline.org/articles/india-xxxi-indian-merchants-in-19th-century-afghanistan/
- **AFGHAN_ROUTE** — https://www.iranicaonline.org/articles/gomal-gomal/
- **MAGHREB_PORTS** — https://www.cambridge.org/core/books/abs/sea-in-history-the-early-modern-world/les-ports-du-maghreb-a-lepoque-moderne/C8E93D4F023E97B301CF0783D1EF1ECD
- **ALGERIA** — https://www.cambridge.org/core/books/history-of-algeria/ecologies-societies-cultures-and-the-state-15161830/6C59DEAD9F70913EC060EDD1465FA6A5
- **TUNIS** — https://www.cambridge.org/core/journals/annales-histoire-sciences-sociales/article/abs/esclaves-chretiens-et-esclaves-noirs-a-tunis-au-xviiie-siecle/B6D63DDA1CDEE63BFF2CE876BB6F3657
- **LIBYA** — https://www.cambridge.org/core/journals/journal-of-african-history/article/abs/la-traite-des-esclaves-noirs-en-libye-au-xviiie-siecle/7245C0AEDD8C0103C7AF3AC0CE314C0F
- **SAHARA** — https://www.cambridge.org/core/books/abs/cambridge-history-of-africa/central-sahara-and-sudan/5D881D10F5663B3129D5604AB55DE183
- **MAURITANIA** — https://www.cambridge.org/core/journals/journal-of-african-history/article/abs/fortunes-commerciales-a-shingiti-adrar-mauritanien-au-dixneuvieme-siecle/11CB84108760623CA588046FACE1B916
- **OMAN** — https://omaninfo.om/en/pages/161/show/572
- **GULF** — https://www.cambridge.org/core/journals/itinerario/article/tolerated-terror-rahmah-bin-jabir-and-the-age-of-revolutions-in-the-gulf-17601830/4C332006F7B0981A66C3728281C458F9
- **CAUCASUS** — https://www.cambridge.org/core/journals/nationalities-papers/article/abs/russian-rule-and-caucasian-society-in-the-first-half-of-the-nineteenth-century-the-georgian-nobility-and-the-armenian-bourgeoisie-18011856/6C9A543D45C030E83A35A027905E79EE
- **ASTRAKHAN** — https://www.cambridge.org/core/journals/itinerario/article/passage-to-india-rhetoric-and-diplomacy-between-muscovy-and-central-asia-in-the-seventeenth-century/6F44E4354E2D87889FC2995CB1C1AEAF
- **TIBET** — https://www.cambridge.org/core/books/abs/narratives-of-the-mission-of-george-bogle-to-tibet/trade-of-tibet/9B11E89C4A170CD2B4DB5544656947DF

## 9. Contrôle final

- Owner_TAG + State_ID audités : **154/154**
- State_ID uniques : **97/97**
- TAG : **65/65**
- Bâtiments admissibles revus : **73/73**
- Possessions VEN/GEN utilisées : **0**
- Auto-generated / NO_ENGINE_GENERATED proposés : **0**
- Réseau ferroviaire actif proposé : **0**
- Recommandations positives : **486**
- Tech distribution reviews : **107**
- Changement gameplay : **aucun**
- Code mod / commit / push : **aucun**