import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const vanilla = 'C:/Games/Victoria 3/game';

function files(dir, ext) {
  if (!fs.existsSync(dir)) return [];
  return fs.readdirSync(dir, { withFileTypes: true })
    .flatMap(entry => entry.isDirectory()
      ? files(path.join(dir, entry.name), ext)
      : entry.name.endsWith(ext) ? [path.join(dir, entry.name)] : [])
    .sort();
}

function definitions(base) {
  const found = new Map();
  for (const file of files(path.join(base, 'common/technology/technologies'), '.txt')) {
    const source = fs.readFileSync(file, 'utf8');
    const starts = [...source.matchAll(/^([a-z][a-z0-9_]*)\s*=\s*\{/gm)];
    for (let i = 0; i < starts.length; i++) {
      const id = starts[i][1];
      const body = source.slice(starts[i].index, starts[i + 1]?.index ?? source.length);
      found.set(id, {
        id,
        body,
        file: path.relative(base, file).replaceAll('\\', '/'),
        era: body.match(/\bera\s*=\s*(\w+)/)?.[1] ?? '',
        category: body.match(/\bcategory\s*=\s*(\w+)/)?.[1] ?? '',
        prerequisites: body.match(/\bunlocking_technologies\s*=\s*\{([^}]*)\}/s)?.[1]?.replace(/#.*$/gm, '').trim().replace(/\s+/g, ' ') ?? '',
      });
    }
  }
  return found;
}

function localizations(base, language) {
  const out = new Map();
  for (const file of files(path.join(base, 'localization', language), '.yml')) {
    const source = fs.readFileSync(file, 'utf8').replace(/^\uFEFF/, '');
    for (const [i, line] of source.split(/\r?\n/).entries()) {
      const match = line.match(/^\s*([\w.\-]+):(?:\d+)?\s+"((?:\\.|[^"\\])*)"/);
      if (!match) continue;
      const rows = out.get(match[1]) ?? [];
      rows.push({ value: match[2], file: path.relative(base, file).replaceAll('\\', '/'), line: i + 1 });
      out.set(match[1], rows);
    }
  }
  return out;
}

const modDefs = definitions(root);
const vanillaDefs = definitions(vanilla);
const en = localizations(root, 'english');
const fr = localizations(root, 'french');
const vanillaEn = localizations(vanilla, 'english');
const vanillaFr = localizations(vanilla, 'french');
function unlockedObjects(base, ids) {
  const result = new Map([...ids].map(id => [id, []]));
  for (const section of ['buildings', 'production_methods', 'production_method_groups', 'laws', 'institutions']) {
    for (const file of files(path.join(base, 'common', section), '.txt')) {
      const source = fs.readFileSync(file, 'utf8');
      const starts = [...source.matchAll(/^([a-z][a-z0-9_]*)\s*=\s*\{/gm)];
      for (let i = 0; i < starts.length; i++) {
        const object = starts[i][1];
        const body = source.slice(starts[i].index, starts[i + 1]?.index ?? source.length);
        for (const match of body.matchAll(/\bunlocking_technologies\s*=\s*\{([^}]*)\}/gs)) {
          const clean = match[1].replace(/#.*$/gm, '');
          for (const technology of clean.match(/[a-z][a-z0-9_]*/g) ?? []) {
            if (result.has(technology)) result.get(technology).push(`${section}:${object}`);
          }
        }
      }
    }
  }
  return result;
}
const unlocks = unlockedObjects(root, modDefs.keys());
const val = (mod, base, key) => mod.get(key)?.at(-1)?.value ?? base.get(key)?.at(-1)?.value ?? '';
const generic = /The practical development of|The adoption of .* advances the equipment|The development of .* advances the construction|The institutional development of .* expands scientific|Le développement pratique de|L’adoption de .* fait progresser|Le développement de .* améliore la construction|L’institutionnalisation de .* étend les capacités/i;
const lexicalWords = value => value.match(/[\p{L}\p{N}]+(?:[’'-][\p{L}\p{N}]+)*/gu) ?? [];

// Text-only decisions. Each pair is grounded in the corresponding technology
// definition and its place in the current, gameplay-authoritative tree.
const descriptionEdits = {
  coke_smelting: ["Coke-fired furnaces reduce ironmaking's dependence on charcoal and sustain hotter, more regular smelting.", "Les hauts fourneaux alimentés au coke réduisent la dépendance au charbon de bois et rendent la fonte du fer plus régulière."],
  improved_husbandry: ["Closer attention to feeding, shelter, and animal care raises the reliability of livestock farming before deliberate breed improvement becomes widespread.", "Une meilleure alimentation, des abris adaptés et des soins plus réguliers améliorent l'élevage avant la généralisation de la sélection des races."],
  improved_agricultural_implements: ["Stronger ploughs, harrows, and other farm tools make cultivation more reliable and reduce the labor needed to prepare the soil.", "Des charrues, herses et autres outils plus robustes facilitent le travail du sol et rendent les cultures plus régulières."],
  industrial_acids: ["Organized acid manufacture supplies the reagents needed by early chemical crafts, dyeing, and metalworking.", "La fabrication organisée d'acides fournit aux premiers métiers chimiques, à la teinture et au travail des métaux des réactifs plus réguliers."],
  advanced_crop_rotations: ["Alternating cereals with fodder and soil-restoring crops helps farms maintain fertility without leaving as much land fallow.", "L'alternance des céréales, des fourrages et des cultures régénératrices préserve la fertilité des sols tout en réduisant la jachère."],
  selective_breeding: ["Choosing breeding stock for desired traits turns inherited farming experience into a deliberate means of improving herds.", "La sélection volontaire des reproducteurs transforme l'expérience des éleveurs en un moyen méthodique d'améliorer les troupeaux."],
  mechanized_spinning: ["Powered spinning machinery draws and twists fibre more evenly than hand spinning, supplying growing weaving workshops with regular yarn."],
  applied_mineralogy: ["Identifying ores and useful minerals through systematic observation improves the search for deposits and the choice of extraction methods.", "L'observation méthodique des minerais et des minéraux utiles facilite la recherche des gisements et le choix des méthodes d'extraction."],
  industrial_ceramics: ["Better control of clays, kilns, and firing produces more consistent ceramics for households and industrial uses.", "Une meilleure maîtrise des argiles, des fours et de la cuisson permet de produire des céramiques plus régulières pour les ménages et l'industrie."],
  precision_boring: ["Accurate boring of metal cylinders and barrels makes demanding machines and artillery more dependable.", "L'alésage précis des cylindres et des canons rend les machines et les pièces d'artillerie plus fiables."],
  condensing_steam_engines: ["Separate condensation wastes less heat, allowing steam engines to pump and drive machinery with less fuel.", "La condensation séparée limite les pertes de chaleur et permet aux machines à vapeur de pomper ou d'entraîner des machines avec moins de combustible."],
  rotative_steam_power: ["Converting the piston's motion into steady rotation allows steam engines to drive workshop and factory machinery directly.", "La transformation du mouvement du piston en rotation régulière permet à la vapeur d'entraîner directement les machines des ateliers et des fabriques."],
  puddling_and_rolling: ["Puddling refines pig iron in a reverberatory furnace; rolling then shapes the metal into more uniform bars and sheets.", "Le puddlage affine la fonte dans un four à réverbère, puis le laminage façonne le métal en barres et en tôles plus uniformes."],
  deep_mine_engineering: ["Deeper shafts require coordinated drainage, ventilation, and supports to reach deposits beyond the limits of shallow workings.", "Des puits plus profonds exigent un drainage, une ventilation et un soutènement coordonnés pour atteindre les gisements inaccessibles aux exploitations superficielles."],
  automated_flour_milling: ["Linked milling and sifting machinery processes grain more continuously and produces flour of more consistent quality.", "L'enchaînement mécanique de la mouture et du blutage transforme le grain plus régulièrement et fournit une farine de qualité plus constante."],
  high_pressure_steam: ["Stronger boilers and controlled high-pressure steam make engines more compact and extend their use beyond fixed pumping sites.", "Des chaudières plus robustes et une vapeur mieux maîtrisée permettent de construire des moteurs plus compacts, utilisables au-delà des stations de pompage."],
  industrial_alkalis: ["Regular production of alkalis supports soapmaking, glassmaking, bleaching, and other chemical industries.", "La production régulière d'alcalis soutient la savonnerie, la verrerie, le blanchiment et d'autres activités chimiques."],
  systematic_field_drainage: ["Planned drains and channels remove excess water from fields, protecting crops and bringing wet land into regular cultivation.", "Des drains et fossés planifiés évacuent l'excès d'eau, protègent les cultures et rendent les terres humides plus faciles à exploiter."],
  mine_safety_engineering: ["Ventilation, safer supports, and closer attention to underground hazards reduce the dangers of deep extraction.", "La ventilation, des soutènements plus sûrs et une meilleure prévention des risques souterrains réduisent les dangers de l'exploitation profonde."],
  continuous_papermaking: ["Moving screens and continuous drying replace individual sheets with a steadier flow of paper.", "Des toiles mobiles et un séchage continu remplacent la fabrication feuille par feuille par une production de papier plus régulière."],
  coal_gasification: ["Processing coal into combustible gas creates a transportable source of heat and light for growing towns and industries.", "La transformation du charbon en gaz combustible fournit aux villes et aux industries une source d'éclairage et de chaleur distribuable."],
  professional_civil_engineering: ["Trained engineers combine surveying, mathematics, and practical design to plan durable roads, bridges, and waterways.", "Des ingénieurs formés associent levés, calculs et conception pratique pour aménager des routes, des ponts et des voies navigables durables."],
  interchangeable_manufacture: ["Standard dimensions and careful gauges let separately made parts fit the same machines, easing assembly and repair.", "Des dimensions normalisées et des instruments de contrôle permettent à des pièces fabriquées séparément de s'ajuster aux mêmes machines, facilitant montage et réparation."],
  geological_surveying: ["Mapping rock strata and mineral deposits gives miners and public authorities a firmer basis for exploration.", "La cartographie des couches rocheuses et des gisements donne aux exploitants et aux autorités une meilleure base pour la prospection."],
  hot_blast_smelting: ["Preheating the air blown into furnaces improves combustion and makes iron smelting less fuel-intensive.", "Le préchauffage de l'air insufflé dans les hauts fourneaux améliore la combustion et réduit la consommation de combustible."],
  hydraulic_cements: ["Cements that harden in damp conditions make stronger harbors, canals, and other works exposed to water possible.", "Les ciments capables de durcir en milieu humide permettent de bâtir des ports, des canaux et d'autres ouvrages exposés à l'eau."],
  hydraulic_turbines: ["Turbines extract rotary power from flowing water more efficiently than older waterwheels, broadening the reach of water-driven machinery.", "Les turbines tirent de l'eau courante une rotation plus efficace que les anciennes roues et étendent l'usage des machines hydrauliques."],
  pressed_glass: ["Pressing molten glass in molds makes common glassware more uniform and easier to produce in quantity.", "Le pressage du verre en fusion dans des moules rend les objets courants plus uniformes et plus faciles à produire en série."],
  scientific_fortification_siegecraft: ["Geometric planning of fortifications and siege works turns the attack and defense of strongholds into a specialized military science.", "Le tracé géométrique des fortifications et des travaux de siège fait de l'attaque et de la défense des places fortes une science militaire spécialisée."],
  regulated_small_arms: ["Common patterns and calibres make infantry weapons easier to procure, maintain, and supply across an army.", "Des modèles et des calibres communs facilitent l'achat, l'entretien et l'approvisionnement des armes d'infanterie."],
  light_infantry_tactics: ["Trained skirmishers use cover, open formations, and accurate fire where rigid battle lines are less effective.", "Des tirailleurs entraînés utilisent le couvert, les formations dispersées et le tir précis là où les lignes serrées sont moins efficaces."],
  standardized_field_artillery: ["Standard calibres, carriages, and drill make field guns easier to move, supply, and coordinate in battle.", "Des calibres, des affûts et des exercices communs facilitent le déplacement, le ravitaillement et la coordination de l'artillerie de campagne."],
  permanent_military_hospitals: ["Permanent hospitals give armies a stable place to treat sickness and wounds instead of relying entirely on improvised wartime care.", "Des hôpitaux permanents permettent aux armées de soigner malades et blessés sans dépendre uniquement de soins improvisés en campagne."],
  armament_standardization_inspection: ["Regular inspection and agreed measurements reveal faulty weapons before issue and support more consistent military supply.", "Des contrôles réguliers et des mesures communes permettent d'écarter les armes défectueuses et de fiabiliser l'approvisionnement militaire."],
  permanent_engineer_services: ["Standing engineer corps retain the skills needed for fortifications, field works, roads, and sieges between campaigns.", "Des corps permanents du génie entretiennent les compétences nécessaires aux fortifications, aux travaux de campagne, aux routes et aux sièges."],
  horse_artillery: ["Mounted crews and suitable gun teams let artillery keep pace with cavalry and redeploy quickly across the field.", "Des servants montés et des attelages adaptés permettent aux canons de suivre la cavalerie et de se redéployer rapidement."],
  military_topographic_surveying: ["Dedicated surveys turn roads, relief, and river crossings into usable maps for planning marches and operations.", "Des levés spécialisés transforment routes, reliefs et passages de rivière en cartes utiles à la préparation des marches et des opérations."],
  mysorean_iron_cased_rocketry: ["Iron-cased rockets developed in Mysore show how a more durable casing can extend the reach and practical use of military rockets.", "Les fusées à enveloppe de fer développées au Mysore montrent comment un corps plus résistant étend la portée et l'usage militaire de ces armes."],
  corps_organization: ["Large standing formations combine infantry, cavalry, artillery, and support troops under commands able to maneuver independently.", "De grandes formations permanentes réunissent infanterie, cavalerie, artillerie et soutien sous des commandements capables de manœuvrer séparément."],
  field_engineering_pontoon_trains: ["Organized sappers and portable bridging equipment help armies cross rivers and overcome obstacles during a campaign.", "Des sapeurs organisés et des équipements de pontage mobiles aident les armées à franchir les cours d'eau et les obstacles."],
  explosive_field_ammunition: ["Explosive shells add a bursting effect to field artillery, changing the damage guns can inflict beyond solid shot.", "Les obus explosifs ajoutent un effet d'éclatement à l'artillerie de campagne, au-delà des dommages causés par les boulets pleins."],
  battlefield_evacuation: ["Organized stretcher bearers and transport move wounded soldiers away from combat and toward medical care sooner.", "Des brancardiers et des moyens de transport organisés évacuent plus vite les blessés vers les lieux de soins."],
  military_veterinary_services: ["Veterinary care preserves the horses and draft animals on which cavalry, artillery, and military transport depend.", "Les soins vétérinaires préservent les chevaux et les animaux de trait dont dépendent la cavalerie, l'artillerie et les transports militaires."],
  casemated_fortifications: ["Protected gun chambers allow forts to maintain fire while sheltering crews and equipment from bombardment.", "Des chambres de tir protégées permettent aux forts de continuer à tirer tout en abritant leurs servants et leur matériel."],
  standardized_military_rockets: ["Consistent rocket designs, launch equipment, and drill make this weapon less dependent on isolated experiments.", "Des modèles de fusées, des dispositifs de lancement et des exercices communs rendent cette arme moins dépendante d'expériences isolées."],
  state_dockyard_systems: ["Permanent state dockyards coordinate shipbuilding, repairs, stores, and skilled labor for naval fleets.", "Des arsenaux permanents coordonnent la construction, la réparation, les réserves et la main-d'œuvre spécialisée des flottes."],
  enclosed_dock_systems: ["Sheltered basins and enclosed docks give ships safer places to be fitted out, repaired, and supplied.", "Des bassins protégés offrent aux navires des lieux plus sûrs pour l'armement, les réparations et l'avitaillement."],
  scientific_naval_architecture: ["Measured hull design and stability studies replace reliance on inherited proportions alone in the construction of warships.", "Le calcul des formes de coque et l'étude de la stabilité complètent les proportions héritées de la tradition dans la construction navale."],
  marine_chronometry: ["Reliable timekeepers help navigators determine longitude at sea and make long voyages less uncertain.", "Des chronomètres fiables aident les navigateurs à déterminer la longitude en mer et réduisent l'incertitude des longues traversées."],
  ship_classification_surveying: ["Regular surveys record a vessel's condition and construction, making maintenance and comparisons between ships more systematic.", "Des inspections régulières consignent l'état et la construction des navires, rendant leur entretien et leur classement plus méthodiques."],
  copper_sheathing: ["Copper plates protect hulls against marine growth and shipworms, allowing sailing vessels to retain speed between refits.", "Le doublage de cuivre protège les coques contre les organismes marins et préserve la vitesse des voiliers entre deux radoubs."],
  hydrographic_surveying: ["Soundings and coastal surveys produce charts of depths, hazards, and approaches needed for safer navigation.", "Les sondages et les levés côtiers cartographient profondeurs, dangers et accès aux ports pour rendre la navigation plus sûre."],
  standardized_naval_signals: ["Agreed flag signals and procedures let ships coordinate maneuvers beyond the reach of spoken orders.", "Des signaux par pavillons et des procédures communes permettent aux navires de coordonner leurs manœuvres à distance."],
  mechanized_naval_dockyards: ["Powered tools and lifting equipment speed the heavy work of building and repairing ships in dockyards.", "Des outils motorisés et des appareils de levage accélèrent les lourds travaux de construction et de réparation dans les arsenaux."],
  diagonal_ship_framing: ["Diagonal braces stiffen wooden hulls and help larger ships withstand strain at sea.", "Des renforts diagonaux rigidifient les coques en bois et aident les grands navires à résister aux efforts de la mer."],
  maritime_safety_standards: ["Shared practices for navigation, seaworthiness, and rescue reduce avoidable losses at sea.", "Des pratiques communes de navigation, de navigabilité et de secours réduisent les pertes évitables en mer."],
  modern_lighthouse_optics: ["Improved lenses concentrate lamp light into beams visible farther from dangerous coasts and harbor approaches.", "De meilleures lentilles concentrent la lumière des phares en faisceaux visibles plus loin des côtes dangereuses et des ports."],
  iron_hull_construction: ["Iron frames and plates permit stronger hulls and new ship forms beyond the limits of traditional timber construction.", "Les membrures et les plaques de fer permettent des coques plus résistantes et de nouvelles formes de navires au-delà des limites du bois."],
  institutionalized_scientific_exchange: ["Correspondence, learned societies, and regular meetings carry observations beyond individual workshops and courtly circles.", "La correspondance, les sociétés savantes et les réunions régulières diffusent les observations au-delà des ateliers et des cercles de cour."],
  institutionalized_public_credit: ["Reliable public accounts and recognized debt instruments let states borrow beyond the immediate resources of their treasuries.", "Des comptes publics fiables et des titres de dette reconnus permettent aux États d'emprunter au-delà des ressources immédiates de leur trésor."],
  commercial_insurance_markets: ["Merchants pool the risks of voyages and trade through increasingly regular insurance contracts and specialized intermediaries.", "Les négociants répartissent les risques des voyages et du commerce grâce à des contrats d'assurance et à des intermédiaires spécialisés."],
  periodical_print_networks: ["Regularly issued newspapers and journals carry news, debate, and practical knowledge between distant towns.", "Les journaux et périodiques diffusés régulièrement relient les villes par l'information, le débat et les savoirs pratiques."],
  systematic_administrative_statistics: ["Repeated surveys and comparable records give governments a clearer view of population, revenue, and productive resources.", "Des enquêtes répétées et des registres comparables donnent aux gouvernements une meilleure connaissance de la population, des recettes et des ressources."],
  variolation_networks: ["Practitioners spread smallpox variolation through organized contacts and shared procedures before vaccination becomes available.", "Des praticiens diffusent la variolisation contre la variole par des réseaux et des procédures partagées avant l'arrivée de la vaccination."],
  codified_practical_knowledge: ["Manuals and encyclopedic works record techniques once passed chiefly through apprenticeship, making them easier to compare and teach.", "Manuels et ouvrages encyclopédiques consignent des techniques jusque-là surtout transmises par l'apprentissage, ce qui facilite leur comparaison et leur enseignement."],
  political_economy: ["Writers and administrators examine production, trade, taxation, and wealth as connected parts of a wider economy.", "Auteurs et administrateurs étudient production, commerce, fiscalité et richesse comme les composantes liées d'une même économie."],
  specialized_technical_academies: ["Specialized schools provide sustained instruction in engineering and applied sciences beyond workshop apprenticeship.", "Des écoles spécialisées assurent un enseignement suivi du génie et des sciences appliquées au-delà de l'apprentissage en atelier."],
  veterinary_science: ["The study of animal anatomy and disease gives livestock owners and armies more reliable ways to care for working animals.", "L'étude de l'anatomie et des maladies animales donne aux éleveurs et aux armées des moyens plus fiables de soigner les bêtes de travail."],
  constitutional_government: ["Written constitutional rules define public offices and place recognized limits on the exercise of state power.", "Des règles constitutionnelles écrites définissent les pouvoirs publics et imposent des limites reconnues à leur exercice."],
  national_sovereignty: ["Political authority is increasingly justified in the name of the nation or people rather than the ruler alone.", "L'autorité politique se réclame de plus en plus de la nation ou du peuple, et non plus seulement du souverain."],
  organized_reform_movements: ["Associations, petitions, and public campaigns allow reformers to coordinate demands across local communities.", "Associations, pétitions et campagnes publiques permettent aux réformateurs de coordonner leurs revendications au-delà des communautés locales."],
  abolitionist_mobilization: ["Organized opponents of slavery turn moral arguments into petitions, publications, and sustained political pressure.", "Les adversaires organisés de l'esclavage transforment leurs arguments moraux en pétitions, publications et pressions politiques durables."],
  scientific_metrology: ["Comparable standards of weight and measure improve experiments, contracts, and exchange between regions.", "Des étalons comparables de poids et de mesure rendent les expériences, les contrats et les échanges entre régions plus fiables."],
  vaccination: ["Inoculation with cowpox offers a new means of protecting people against smallpox and changes the practice of preventive medicine.", "L'inoculation de la vaccine offre un nouveau moyen de protéger contre la variole et transforme la médecine préventive."],
  polytechnical_education: ["Schools joining mathematics, natural science, and engineering train specialists for public works and industry.", "Des écoles associant mathématiques, sciences naturelles et génie forment des spécialistes pour les travaux publics et l'industrie."],
  optical_telegraph_networks: ["Chains of signal stations relay messages across long distances much faster than couriers can travel.", "Des chaînes de stations à signaux transmettent les messages à grande distance bien plus vite que les courriers."],
  central_statistical_offices: ["Permanent offices collect and compare official figures, turning occasional surveys into a continuing administrative practice.", "Des bureaux permanents recueillent et comparent les chiffres officiels, faisant des enquêtes ponctuelles une pratique administrative suivie."],
  organized_immunization_campaigns: ["Coordinated vaccination efforts extend protection across larger populations than isolated practitioners can reach.", "Des campagnes de vaccination coordonnées protègent des populations plus vastes que ne peuvent le faire des praticiens isolés."],
  mechanized_printing: ["Powered presses multiply the number of sheets a printer can produce and widen the circulation of books and newspapers.", "Les presses motorisées multiplient les feuilles imprimées et élargissent la diffusion des livres et des journaux."],
  experimental_research_laboratories: ["Dedicated laboratories make controlled experiments and repeatable observations a regular part of scientific work.", "Des laboratoires spécialisés font des expériences contrôlées et des observations reproductibles une pratique scientifique régulière."],
  specialized_professional_societies: ["Specialists form lasting associations to exchange findings, debate methods, and establish shared professional practices.", "Des spécialistes créent des associations durables pour échanger leurs résultats, discuter des méthodes et établir des pratiques communes."],
  clinicopathological_medicine: ["Physicians relate symptoms observed in life to anatomical changes found after death, sharpening the study of disease.", "Les médecins rapprochent les symptômes observés chez les malades des lésions constatées après la mort, affinant l'étude des maladies."],
  active_principle_pharmacy: ["Isolating the active substances in remedies makes medicines easier to prepare, compare, and dose consistently.", "L'isolement des substances actives des remèdes facilite la préparation, la comparaison et le dosage régulier des médicaments."],
  professional_civil_policing: ["Permanent, salaried police forces take over duties once handled by irregular watches and temporary local arrangements.", "Des forces de police permanentes et rémunérées remplacent progressivement les gardes irrégulières et les arrangements locaux provisoires."],
  mass_circulation_press: ["Large print runs and wider distribution bring newspapers and other publications to an expanding reading public.", "De grands tirages et une distribution élargie mettent journaux et autres publications à la portée d'un lectorat croissant."],
  liberal_constitutionalism: ["Constitutional guarantees and representative institutions place civil liberties and limits on executive authority at the center of political reform.", "Les garanties constitutionnelles et les institutions représentatives placent les libertés civiles et les limites du pouvoir exécutif au cœur des réformes."],
  early_socialism_cooperativism: ["Reformers and workers propose cooperative ownership and new forms of association in response to the social costs of industrial change.", "Réformateurs et travailleurs proposent la propriété coopérative et de nouvelles associations face aux coûts sociaux des transformations industrielles."],
};

const nameEdits = {
  industrial_canals: [null, 'Voies navigables organisées'],
  mechanized_spinning: ['Early Mechanical Spinning', null],
  advanced_spinning: [null, 'Couture mécanisée'],
  mechanized_weaving: [null, 'Tissage mécanique'],
  high_pressure_steam: [null, 'Vapeur haute pression'],
  hot_blast_smelting: [null, 'Soufflage à chaud'],
  traditional_papermaking: [null, 'Papeterie traditionnelle'],
  traditional_glassmaking: [null, 'Verrerie traditionnelle'],
  industrial_paper_bleaching: [null, 'Blanchiment papetier industriel'],
  scientific_fortification_siegecraft: ['Fortification and Siegecraft', 'Fortification et poliorcétique'],
  ship_classification_surveying: ['Ship Classification', 'Classification navale'],
  armament_standardization_inspection: ['Armament Standards', 'Normes d’armement'],
  paddle_steamer: [null, 'Vapeur à roues'],
  mass_circulation_press: [null, 'Presse de masse'],
  automatic_bottle_blowers: [null, 'Soufflage automatique'],
  battlefleet_tactics: [null, 'Tactiques d’escadre'],
  battleship_tech: ['Super-Dreadnoughts', 'Super-dreadnoughts'],
  breech_loading_artillery: [null, 'Artillerie à culasse'],
  concrete_dockyards: [null, 'Arsenaux bétonnés'],
  electric_arc_process: [null, 'Fusion à l’arc'],
  electric_railway: [null, 'Réseaux ferroviaires électriques'],
  electrical_capacitors: ['Electrical Capacitors', 'Condensateurs électriques'],
  enlistment_offices: [null, 'Bureaux de recrutement'],
  law_enforcement: [null, 'Maintien de l’ordre'],
  monitor_tech: ['Modern Ironclads', 'Cuirassés modernes'],
  power_of_the_purse: ['Captains’ Purchasing', 'Achats délégués'],
  pre_dreadnought_tech: ['Pre-Dreadnoughts', 'Pré-dreadnoughts'],
  rotary_valve_engine: [null, 'Moteur à soupape'],
  sea_lane_strategies: [null, 'Stratégies maritimes'],
  steam_donkey: [null, 'Treuil à vapeur'],
  steel_frame_buildings: [null, 'Structures d’acier'],
  watertube_boiler: [null, 'Chaudière tubulaire'],
};

const rows = [...modDefs.values()].map(def => {
  const enName = val(en, vanillaEn, def.id);
  const frName = val(fr, vanillaFr, def.id);
  const enDesc = val(en, vanillaEn, `${def.id}_desc`);
  const frDesc = val(fr, vanillaFr, `${def.id}_desc`);
  const modAdded = !vanillaDefs.has(def.id);
  const modModified = !modAdded && def.body.replace(/\s+/g, ' ').trim() !== vanillaDefs.get(def.id).body.replace(/\s+/g, ' ').trim();
  return { ...def, enName, frName, enDesc, frDesc, modAdded, modModified, unlocks: [...new Set(unlocks.get(def.id) ?? [])],
    genericEn: generic.test(enDesc), genericFr: generic.test(frDesc),
    enWords: lexicalWords(enName).length, frWords: lexicalWords(frName).length,
    enNameSource: en.get(def.id)?.at(-1)?.file ?? vanillaEn.get(def.id)?.at(-1)?.file ?? '',
    frNameSource: fr.get(def.id)?.at(-1)?.file ?? vanillaFr.get(def.id)?.at(-1)?.file ?? '',
    enDescSource: en.get(`${def.id}_desc`)?.at(-1)?.file ?? vanillaEn.get(`${def.id}_desc`)?.at(-1)?.file ?? '',
    frDescSource: fr.get(`${def.id}_desc`)?.at(-1)?.file ?? vanillaFr.get(`${def.id}_desc`)?.at(-1)?.file ?? ''
  };
});

const mode = process.argv[2] ?? 'summary';
const csv = value => `"${String(value ?? '').replaceAll('"', '""')}"`;
const parseCsv = source => {
  const records = [];
  let record = [], field = '', quoted = false;
  for (let i = 0; i < source.length; i++) {
    const ch = source[i];
    if (quoted) {
      if (ch === '"' && source[i + 1] === '"') { field += '"'; i++; }
      else if (ch === '"') quoted = false;
      else field += ch;
    } else if (ch === '"') quoted = true;
    else if (ch === ',') { record.push(field); field = ''; }
    else if (ch === '\n') { record.push(field.replace(/\r$/, '')); records.push(record); record = []; field = ''; }
    else field += ch;
  }
  if (field || record.length) { record.push(field); records.push(record); }
  return records;
};
const writeCsv = (name, header, data) => {
  const content = '\uFEFF' + [header, ...data].map(row => row.map(csv).join(',')).join('\r\n') + '\r\n';
  fs.writeFileSync(path.join(root, 'docs/reports/technology', name), content, 'utf8');
};
if (mode === 'plan') {
  const noPlan = rows.filter(row => (row.genericEn || row.genericFr || !row.enDesc || !row.frDesc) && !descriptionEdits[row.id]);
  const noNamePlan = rows.filter(row => (!row.enName || !row.frName || row.enWords > 3 || row.frWords > 3) && !nameEdits[row.id]);
  const invalidNames = Object.entries(nameEdits).flatMap(([id, names]) => names.filter(Boolean).filter(name => lexicalWords(name).length > 3).map(name => [id, name]));
  console.log(JSON.stringify({descriptionEdits: Object.keys(descriptionEdits).length, nameEdits: Object.keys(nameEdits).length, noPlan: noPlan.map(x => x.id), noNamePlan: noNamePlan.map(x => x.id), invalidNames}, null, 2));
} else if (mode === 'enrich-audit-context') {
  const file = path.join(root, 'docs/reports/technology/TECH_TREE_LOCALIZATION_AUDIT.csv');
  const [header, ...data] = parseCsv(fs.readFileSync(file, 'utf8').replace(/^\uFEFF/, '')).filter(record => record.length > 1);
  if (header[0] !== 'Technology_ID' || header.at(-1) !== 'Notes' || data.length !== rows.length) throw new Error('Unexpected baseline audit shape');
  const byId = new Map(rows.map(row => [row.id, row]));
  for (const record of data) {
    const row = byId.get(record[0]);
    if (!row) throw new Error(`Audit ID not found: ${record[0]}`);
    record[record.length - 1] = [record.at(-1), row.prerequisites ? `prerequisites=${row.prerequisites}` : 'prerequisites=none', row.unlocks.length ? `unlocks=${row.unlocks.join('|')}` : 'unlocks=none'].join('; ');
  }
  writeCsv('TECH_TREE_LOCALIZATION_AUDIT.csv', header, data);
  console.log('Added prerequisite and unlock context to the preserved baseline audit.');
} else if (mode === 'include-retained-new-technologies') {
  const auditFile = path.join(root, 'docs/reports/technology/TECH_TREE_LOCALIZATION_AUDIT.csv');
  const proposalFile = path.join(root, 'docs/reports/technology/TECH_TREE_LOCALIZATION_PROPOSALS.csv');
  const [_auditHeader, ...audit] = parseCsv(fs.readFileSync(auditFile, 'utf8').replace(/^\uFEFF/, '')).filter(record => record.length > 1);
  const [header, ...proposals] = parseCsv(fs.readFileSync(proposalFile, 'utf8').replace(/^\uFEFF/, '')).filter(record => record.length > 1);
  const listed = new Set(proposals.map(record => record[0]));
  let added = 0;
  for (const record of audit) {
    if (!record[10].startsWith('MOD_ADDED') || listed.has(record[0])) continue;
    proposals.push([record[0], record[1], record[2], record[3], record[3], record[4], record[4], record[5], record[6], 'Existing concise and specific localization retained']);
    added++;
  }
  proposals.sort((a, b) => a[0].localeCompare(b[0], 'en'));
  writeCsv('TECH_TREE_LOCALIZATION_PROPOSALS.csv', header, proposals);
  console.log(`Added ${added} already-sound mod technologies to the proposal inventory; ${proposals.length} rows total.`);
} else if (mode === 'validate') {
  const target = rows.filter(row => row.modAdded || row.modModified);
  const failures = [];
  for (const row of target) {
    if (!row.enName || !row.frName || !row.enDesc || !row.frDesc) failures.push(`Missing localization: ${row.id}`);
    if (row.genericEn || row.genericFr) failures.push(`Generic description: ${row.id}`);
    if (row.enWords > 3 || row.frWords > 3) failures.push(`Long title: ${row.id}`);
  }
  for (const [language, index] of [['english', en], ['french', fr]]) {
    for (const [key, occurrences] of index) {
      if (occurrences.length > 1 && modDefs.has(key.replace(/_desc$/, ''))) failures.push(`Duplicate ${language} key: ${key}`);
    }
    const changedFiles = new Set([...Object.keys(descriptionEdits), ...Object.keys(nameEdits)].flatMap(id => [index.get(id)?.at(-1)?.file, index.get(`${id}_desc`)?.at(-1)?.file]).filter(Boolean));
    for (const relative of changedFiles) {
      const raw = fs.readFileSync(path.join(root, relative));
      if (!(raw[0] === 0xEF && raw[1] === 0xBB && raw[2] === 0xBF)) failures.push(`Missing UTF-8 BOM: ${relative}`);
    }
    for (const [key] of [...Object.entries(nameEdits), ...Object.entries(descriptionEdits).map(([id, pair]) => [`${id}_desc`, pair])]) {
      const occurrence = index.get(key)?.at(-1);
      if (!occurrence) continue;
      const line = fs.readFileSync(path.join(root, occurrence.file), 'utf8').split(/\r?\n/)[occurrence.line - 1];
      if (!/^\s*[\w.\-]+:(?:\d+)?\s+"(?:\\.|[^"\\])*"(?:\s*#.*)?$/.test(line)) failures.push(`Invalid Paradox quoting: ${occurrence.file}:${occurrence.line}`);
    }
  }
  console.log(JSON.stringify({status: failures.length ? 'FAIL' : 'PASS', technologies: target.length, failures}, null, 2));
  if (failures.length) process.exitCode = 1;
} else if (mode === 'proposals') {
  const header = ['Technology_ID', 'Era', 'Category', 'Old_EN_Name', 'New_EN_Name', 'Old_FR_Name', 'New_FR_Name', 'New_EN_Description', 'New_FR_Description', 'Reason'];
  const planned = rows.filter(row => descriptionEdits[row.id] || nameEdits[row.id]);
  writeCsv('TECH_TREE_LOCALIZATION_PROPOSALS.csv', header, planned.map(row => {
    const names = nameEdits[row.id] ?? [];
    const descriptions = descriptionEdits[row.id] ?? [];
    const reason = [names[0] || names[1] ? 'Shorter or clearer title' : '', descriptions[0] || descriptions[1] ? 'Specific historical description' : ''].filter(Boolean).join('; ');
    return [row.id, row.era, row.category, row.enName, names[0] ?? row.enName, row.frName, names[1] ?? row.frName, descriptions[0] ?? row.enDesc, descriptions[1] ?? row.frDesc, reason];
  }));
  console.log(`Wrote ${planned.length} localization proposals.`);
} else if (mode === 'apply') {
  const editsByLanguage = {
    english: new Map(),
    french: new Map(),
  };
  for (const [id, pair] of Object.entries(nameEdits)) {
    if (!modDefs.has(id)) throw new Error(`Unknown technology in name plan: ${id}`);
    if (pair[0]) editsByLanguage.english.set(id, pair[0]);
    if (pair[1]) editsByLanguage.french.set(id, pair[1]);
  }
  for (const [id, pair] of Object.entries(descriptionEdits)) {
    if (!modDefs.has(id)) throw new Error(`Unknown technology in description plan: ${id}`);
    if (pair[0]) editsByLanguage.english.set(`${id}_desc`, pair[0]);
    if (pair[1]) editsByLanguage.french.set(`${id}_desc`, pair[1]);
  }
  const escapeRegex = value => value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const escapeYaml = value => value.replaceAll('\\', '\\\\').replaceAll('"', '\\"');
  for (const language of ['english', 'french']) {
    const lookup = language === 'english' ? en : fr;
    const sourceUpdates = new Map();
    const additions = [];
    for (const [key, value] of editsByLanguage[language]) {
      const entry = lookup.get(key)?.at(-1);
      if (!entry) {
        additions.push([key, value]);
        continue;
      }
      const group = sourceUpdates.get(entry.file) ?? [];
      group.push([key, value]);
      sourceUpdates.set(entry.file, group);
    }
    for (const [relative, updates] of sourceUpdates) {
      const file = path.join(root, relative);
      let source = fs.readFileSync(file, 'utf8');
      for (const [key, value] of updates) {
        const pattern = new RegExp(`^(\\s*${escapeRegex(key)}:(?:\\d+)?\\s+\")((?:\\\\.|[^\"\\\\])*)(\"[^\\r\\n]*)$`, 'gm');
        let count = 0;
        source = source.replace(pattern, (_, prefix, _old, suffix) => {
          count++;
          return prefix + escapeYaml(value) + suffix;
        });
        if (count !== 1) throw new Error(`Expected exactly one ${key} in ${relative}; found ${count}`);
      }
      fs.writeFileSync(file, source, 'utf8');
    }
    if (additions.length) {
      const relative = `localization/${language}/replace/tech_tree_final_localization_replace_l_${language}.yml`;
      const file = path.join(root, relative);
      if (fs.existsSync(file)) throw new Error(`Refusing to overwrite existing file: ${relative}`);
      const source = `\uFEFFl_${language}:\n` + additions.map(([key, value]) => ` ${key}:0 "${escapeYaml(value)}"`).join('\n') + '\n';
      fs.writeFileSync(file, source, 'utf8');
    }
    console.log(`${language}: ${editsByLanguage[language].size} keys changed, ${additions.length} new override keys.`);
  }
  writeCsv('TECH_TREE_LOCALIZATION_REVIEW.csv', ['Technology_ID', 'Current_Name', 'Option_A', 'Option_B', 'Conceptual_Ambiguity', 'Recommended_Choice', 'Reason'], []);
} else if (mode === 'audit') {
  const descriptionCounts = new Map();
  for (const row of rows) for (const description of [row.enDesc, row.frDesc]) {
    if (description) descriptionCounts.set(description, (descriptionCounts.get(description) ?? 0) + 1);
  }
  const header = ['Technology_ID', 'Era', 'Category', 'Current_EN_Name', 'Current_FR_Name', 'Current_EN_Description', 'Current_FR_Description', 'Issue_Type', 'Needs_Name_Change', 'Needs_Description_Change', 'Notes'];
  writeCsv('TECH_TREE_LOCALIZATION_AUDIT.csv', header, rows.map(row => {
    const nameIssue = !row.enName ? 'MISSING_EN' : !row.frName ? 'MISSING_FR' : row.enName === row.id || row.frName === row.id ? 'ID_AS_NAME' : row.enWords > 3 || row.frWords > 3 ? 'BAD_TRANSLATION' : '';
    const descriptionIssue = !row.enDesc ? 'MISSING_EN' : !row.frDesc ? 'MISSING_FR' : row.genericEn || row.genericFr ? 'GENERIC_DESCRIPTION' : descriptionCounts.get(row.enDesc) > 1 || descriptionCounts.get(row.frDesc) > 1 ? 'DUPLICATED_DESCRIPTION' : '';
    const issue = nameIssue || descriptionIssue || 'OK';
    const notes = [row.modAdded ? 'MOD_ADDED' : row.modModified ? 'MOD_MODIFIED' : 'VANILLA_UNCHANGED', `definition=${row.file}`, `en=${row.enNameSource}`, `fr=${row.frNameSource}`, row.prerequisites ? `prerequisites=${row.prerequisites}` : ''].filter(Boolean).join('; ');
    return [row.id, row.era, row.category, row.enName, row.frName, row.enDesc, row.frDesc, issue, nameIssue ? 'YES' : 'NO', descriptionIssue ? 'YES' : 'NO', notes];
  }));
  console.log(`Wrote audit for ${rows.length} technologies.`);
} else if (mode === 'rows') {
  for (const row of rows) console.log(JSON.stringify(row));
} else if (mode === 'issues') {
  for (const row of rows.filter(r => r.modAdded || r.modModified).filter(r => !r.enName || !r.frName || !r.enDesc || !r.frDesc || r.genericEn || r.genericFr || r.enWords > 3 || r.frWords > 3)) {
    console.log([row.id, row.era, row.category, row.enName, row.frName, `words:${row.enWords}/${row.frWords}`, `desc:${row.genericEn ? 'EN_GENERIC' : row.enDesc ? 'EN_OK' : 'EN_MISSING'}/${row.genericFr ? 'FR_GENERIC' : row.frDesc ? 'FR_OK' : 'FR_MISSING'}`].join(' | '));
  }
} else {
  const target = rows.filter(r => r.modAdded || r.modModified);
  const repeatedDescriptions = language => {
    const groups = new Map();
    for (const row of target) {
      const value = language === 'english' ? row.enDesc : row.frDesc;
      if (value) groups.set(value, [...(groups.get(value) ?? []), row.id]);
    }
    return [...groups.values()].filter(ids => ids.length > 1);
  };
  console.log(JSON.stringify({
    defined: rows.length, modAdded: rows.filter(r => r.modAdded).length, modModified: rows.filter(r => r.modModified).length,
    missingEnName: target.filter(r => !r.enName).length, missingFrName: target.filter(r => !r.frName).length,
    missingEnDesc: target.filter(r => !r.enDesc).length, missingFrDesc: target.filter(r => !r.frDesc).length,
    genericEnDesc: target.filter(r => r.genericEn).length, genericFrDesc: target.filter(r => r.genericFr).length,
    longEnName: target.filter(r => r.enWords > 3).length, longFrName: target.filter(r => r.frWords > 3).length,
    duplicateEnDescriptions: repeatedDescriptions('english'), duplicateFrDescriptions: repeatedDescriptions('french'),
    duplicateEnTechKeys: [...en].filter(([key, vals]) => vals.length > 1 && modDefs.has(key.replace(/_desc$/, ''))).map(([key, vals]) => [key, vals.map(x => x.file)]),
    duplicateFrTechKeys: [...fr].filter(([key, vals]) => vals.length > 1 && modDefs.has(key.replace(/_desc$/, ''))).map(([key, vals]) => [key, vals.map(x => x.file)])
  }, null, 2));
}
