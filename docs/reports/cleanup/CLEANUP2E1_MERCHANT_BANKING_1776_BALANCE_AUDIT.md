# CLEANUP-2E-1 — Merchant Banking 1776 — Historical & Balance Audit

## Statut et périmètre

- Phase : `CLEANUP-2E-1`
- Nature : audit et recherche uniquement
- Branche observée : `cleanup-post-release`
- HEAD observé au préflight : `61ee9578c65b505e662805c7da251308edc0f1a3`
- Runtime Victoria 3 : non lancé, conformément à l'interdiction
- Fichiers gameplay, militaires, technologiques et localisations : non modifiés
- Livrables créés : ce rapport et `docs/research/economy/CLEANUP2E1_MERCHANT_BANKING_MODIFIER_AUDIT.csv`

## Verdict exécutif

`law_merchant_banking` n'est pas une simple loi commerciale. Dans la build locale réellement auditée, c'est presque `law_agrarianism` transposé vers les élites urbaines, avec une pénalité capitaliste plus faible et un bonus commercial supplémentaire. Elle conserve en même temps 50 % d'allocation de construction privée, trois leviers favorables à la nationalisation/propriété publique, une charte gratuite et la protection contre la nationalisation sans compensation.

Verdicts distincts :

- loi isolée : **OVERPOWERED** pour une loi disponible dès 1776 sans technologie requise ;
- pile initiale commune VEN/GEN : **SEVERELY_OVERPOWERED** ;
- identité historique : juste sur le capital patricien, le crédit, le commerce et les chartes, mais brouillée par des bonus génériques d'économie publique moderne ;
- recommandation A/B/C : **OPTION B — ASYMMETRIC MERCHANT OLIGARCHY** ;
- recommandation territoriale pré-release : **OPTION B1 — oligarchie marchande + contraintes intrinsèques simples** ;
- cible de balance : **STRONG_BUT_SPECIALIZED**, excellente pour une puissance commerciale compacte mais nettement moins adaptée à un grand État territorial.

La cause du verdict sévère n'est pas le nombre de lignes. C'est la combinaison d'un pool alimenté à +50 % par deux groupes, d'une allocation privée de 50 %, d'une boucle complète de propriété publique, d'une charte gratuite et d'une pile commerciale externe déjà très forte.

## 1. Baseline vanilla locale exacte

Le chemin imposé et utilisé exclusivement est :

`C:\Games\Victoria 3`

Éléments vérifiés localement :

| Élément | Valeur |
|---|---:|
| Exécutable | `C:\Games\Victoria 3\binaries\victoria3.exe` |
| `FileVersion` | `1.13.9` |
| `ProductVersion` | `1.13.9` |
| Branche Caligula | `release/1.13.9` |
| Révision Caligula | `afea32b87c002fe0621f2f732d60a80ba914c14e` |
| Marqueur de données | `v1.13.9.xxh128` |

La demande évoquait 1.13.10, mais l'installation locale fournie est sans ambiguïté **1.13.9**. Les noms, valeurs et comparaisons ci-dessous sont donc ceux de 1.13.9 ; aucune valeur d'une autre version n'a été importée par mémoire ou par Internet.

Fichiers vanilla principaux inspectés :

- `game/common/laws/00_economic_system.txt`
- `game/common/laws/00_trade_policy.txt`
- `game/common/laws/00_navy_model.txt`
- `game/common/modifier_type_definitions/00_modifier_types.txt`
- `game/common/modifier_type_definitions/01_building_modifier_types.txt`
- `game/common/modifier_type_definitions/02_modifier_types_rules.txt`
- `game/common/modifier_type_definitions/99_todo_sort_into_other_files.txt`
- `game/localization/english/modifiers_l_english.yml`
- exemples vanilla de lois, technologies, modificateurs statiques, valeurs scriptées et on-actions.

## 2. Setup actuel VEN/GEN

### 2.1 Loi Merchant Banking

La loi est une variante de `law_agrarianism` via `parent = law_agrarianism`. Les commentaires vanilla sur d'autres variantes confirment que `parent` hérite des positions idéologiques du parent. Aucun fichier d'idéologie ou d'interest group du mod ne définit une position propre à Merchant Banking : politiquement, elle est donc traitée comme une variante d'Agrarianism, alors que ses effets sont urbains et marchands.

Elle est visible seulement pour VEN et GEN. Son bloc `unlocking_technologies` est vide, contrairement à Agrarianism (`romanticism`), Interventionism (`manufacturies`) et Laissez-Faire (`international_trade`). Les deux pays l'activent au démarrage.

### 2.2 Pile économique commune

| Source | Effets pertinents |
|---|---|
| Merchant Banking | aristocrates +50 % efficacité de contribution ; shopkeepers +50 % ; capitalistes -10 % ; avantage commercial +10 % ; construction privée 50 % ; retour de nationalisation +50 % ; réinvestissement des dividendes publics +50 % ; efficacité des dividendes publics +30 % ; 1 charte gratuite ; nationalisation sans compensation interdite |
| Merchant Republic | aristocrates +50 % force politique et +100 pouvoir électoral ; shopkeepers +50 % et +100 ; capitalistes +25 % et +50 ; clerks +25 % ; +100 autorité ; avantages de légitimité. Pas de bonus économique direct, mais renforcement massif des groupes bénéficiaires de la loi économique |
| Mercantilism | tarifs import +50 %, export +20 % ; subventions export +50 %, import +20 % ; avantage import -25 % ; avantage export +25 % |
| Merchant Navy | construction des supply ships +30 % ; troop ships +30 % ; construction navale générique -10 % ; ship interest gain -10 %. C'est une spécialisation navale avec deux contreparties, pas un pur bonus commercial |
| Centre of Commerce | throughput des centres de commerce +50 % ; minting plat `+10000` ; avantage export +20 % |

Somme commerciale lisible au démarrage :

- avantage export : **+45 %** (`+25 %` Mercantilism + `+20 %` Centre of Commerce) ;
- avantage commercial générique : **+10 %** supplémentaire ;
- throughput des centres de commerce : **+50 %** ;
- minting : **+10000** plat ;
- 1 charte gratuite ;
- allocation de construction privée : **50 %**.

Le +10 % de trade advantage ne doit pas être additionné comme s'il était la même clé que l'avantage export ; les deux effets se cumulent néanmoins dans la performance commerciale.

### 2.3 Asymétries VEN/GEN et autres effets trouvés

- VEN possède statiquement 7 scopes d'État au départ : Venetia, Ionian Islands, une partie du Montenegro, West Aegean Islands, Dalmatia, Istria et une partie du South Tyrol.
- GEN possède statiquement 1 scope d'État : une partie de Piedmont.
- GEN place les small arms au niveau d'import `high_subventions` ; c'est un réglage ciblé, non un bonus économique général.
- Les deux reçoivent le même tier technologique de départ, `academia`, `line_infantry`, un niveau de police et un niveau fiscal moyen ; aucun n'ajoute d'autre modificateur économique national permanent dans son fichier pays.
- `modifier_venetian_golden_age` et `modifier_venetian_empire` existent mais ne sont pas appliqués au démarrage : ils sont exclus de la pile initiale.
- Les government types `gov_1776_merchant_republic_doge` et `gov_merchant_republic` déterminent titre et transfert du pouvoir, sans modifier économique.
- Aucun effet Merchant Banking additionnel n'a été trouvé dans `common/interest_groups/` ou `common/ideologies/`.

Les autres lois initiales modifient toutefois l'environnement dans lequel cette pile opère :

| Loi/institution initiale | Effet pertinent pour l'audit économique |
|---|---|
| Presidential Republic | +100 autorité et effets de légitimité |
| Merchant Republic | +100 autorité, en plus de la pile politique détaillée plus haut |
| State Religion | +200 autorité ; salaires des bâtiments de religion d'État +10 % et des autres religions -10 % |
| Right of Assembly | +50 autorité ; bolster +30 %, suppression -30 % |
| National Supremacy | +150 autorité et règles de discrimination |
| Land-Based Taxation, niveau fiscal moyen | `tax_consumption_add = 0.25` et `tax_land_add = 0.70` |
| Hereditary Bureaucrats | coût bureaucratique de population -25 % ; force politique des aristocrates +25 % |
| Religious Schools, niveau 1 | coût de l'institution scolaire -20 % ; éducation +10 %, conversion +20 % et force politique devout +10 % au niveau 1 |
| Tenant Farmers | force politique des landowners +25 % ; migration interne des paysans interdite ; minimum d'arable land de subsistance incorporé +25 % |
| Migration Controls | restrictivité migratoire +60 % |
| Local Police, niveau 1 | force politique des landowners +5 % et effets de turmoil -5 % au niveau 1 |
| No Colonial Affairs | homeland acceptance +10 ; aucun outil colonial initial |

L'autorité additive explicite de Presidential Republic, Merchant Republic, State Religion, Right of Assembly et National Supremacy atteint donc **+600**. Elle augmente la latitude pour décrets et chartes payantes ; la charte gratuite de Merchant Banking reste néanmoins un avantage borné distinct.

Hereditary Bureaucrats apporte surtout une compensation administrative réelle : son -25 % de coût bureaucratique de population amortirait le +10 à +15 % proposé sous B1. Les deux effets seuls laisseraient le pays à -15 % ou -10 % au départ. B1 resterait bien un coût marginal attaché au maintien de Merchant Banking — changer de loi supprimerait ce +10/+15 — mais pas un malus administratif absolu immédiat. Porter B1 à +25 % pour effacer cette compensation serait prématuré sans test runtime et risquerait de surcorriger VEN/GEN dès 1776.

Le mod donne donc à VEN et GEN la même pile de règles, mais le bonus plat de minting et les seuils territoriaux potentiels n'ont pas la même incidence sur un GEN d'un État et une VEN de sept États.

## 3. Comparaison quantitative aux systèmes économiques vanilla 1.13.9

### 3.1 Tableau principal

| Loi | Efficacité du pool par classe | Construction privée | Dividendes publics | Nationalisation | Compagnies/chartes | Contraintes structurantes |
|---|---|---:|---|---|---|---|
| Traditionalism | shopkeepers, bureaucrates, capitalistes, farmers, clergymen, aristocrates : -50 % | 25 % | réinvestissement +25 % | coût +100 %, retour +10 %, pas de nationalisation sans compensation | 0 | tax capacity -25 %, MAPI -15 %, leverage resistance +25 %, self-investment +25 % |
| Interventionism | aucun bonus/malus de classe | 50 % | réinvestissement +50 %, efficacité +25 % | retour +50 %, compensation obligatoire | 1 gratuite | aucune restriction sectorielle majeure |
| Agrarianism | aristocrates, clergymen, farmers +50 % ; capitalistes -25 % | 50 % | réinvestissement +50 %, efficacité +30 % | retour +50 %, compensation obligatoire | 1 gratuite | orientation rurale via les contributeurs |
| **Merchant Banking** | **aristocrates +50 %, shopkeepers +50 %, capitalistes -10 %** | **50 %** | **réinvestissement +50 %, efficacité +30 %** | **retour +50 %, compensation obligatoire** | **1 gratuite** | **trade advantage +10 % ; aucune contrainte territoriale ou sectorielle** |
| Laissez-Faire | shopkeepers +25 %, capitalistes +25 % | 75 % | réinvestissement +100 % | nationalisation désactivée ; privatisation forcée | 2 gratuites ; monopoles interdits | intérêts des prêts -25 % |
| Cooperative Ownership | shopkeepers +25 %, farmers +25 % | 35 % | réinvestissement +100 % | collectivisation autorisée sur plusieurs groupes | 1 gratuite ; dividendes travailleurs des compagnies +75 % | propriété collective/foreign collectivization |
| Command Economy | pool désactivé ; bureaucrates +25 % | 10 % | efficacité +40 % | coût -50 %, radicaux -75 % | 1 gratuite ; privatisation non-company interdite | autorité et force politique bureaucratique +25 % |

Les lois `Industry Banned` et `Extraction Economy` ont aussi été inspectées. Elles ont 50 % de construction privée et certains outils de nationalisation, mais imposent des destructions/interdictions industrielles, des malus de recherche, de niveau de vie ou de contribution. Elles ne fournissent pas de précédent pour la combinaison sans contrainte de Merchant Banking.

### 3.2 Différence réelle avec Agrarianism

Merchant Banking reprend exactement d'Agrarianism :

- construction privée 50 % ;
- retour de nationalisation 50 % ;
- réinvestissement des dividendes publics 50 % ;
- efficacité des dividendes publics 30 % ;
- une charte gratuite ;
- interdiction de nationaliser sans compensation ;
- bonus aristocrate +50 %.

Elle remplace :

- clergymen +50 % et farmers +50 % par shopkeepers +50 % et trade advantage +10 % ;
- pénalité capitaliste -25 % par seulement -10 %.

Pour VEN/GEN, pays urbains, portuaires et dotés d'un Centre of Commerce, ces remplacements ne sont pas neutres : les bénéficiaires deviennent mieux alignés avec les bâtiments rentables et la pile politique de Merchant Republic. La loi garde donc le budget de puissance d'Agrarianism tout en supprimant une grande partie de sa spécialisation rurale et de son coût de transition.

### 3.3 Lecture en puissance réelle

1. **Le moteur d'investissement est double.** Deux classes reçoivent +50 %, contre une seule classe urbaine à +25 % sous Laissez-Faire. Laissez-Faire reste supérieur pour les capitalistes, les prêts et l'allocation privée, mais impose privatisation et interdiction de nationalisation.
2. **L'allocation de 50 % convertit immédiatement ce pool en construction.** Ce n'est pas un simple bonus de revenus dormant.
3. **La boucle publique est complète.** La compensation de nationalisation retourne au pool, la moitié des dividendes publics est réinvestie, puis le reste reçoit +30 % d'efficacité. Les trois effets sont conditionnels à la propriété publique, mais non redondants à long terme.
4. **La charte est un avantage borné et thématique.** Une charte est inférieure aux deux de Laissez-Faire et peut rester le marqueur institutionnel de la loi.
5. **Le commerce est déjà suralimenté hors de la loi.** +10 % de trade advantage arrive sur +45 % d'avantage export, +50 % de throughput des centres de commerce et un gros minting plat.
6. **Aucun coût de taille n'existe.** Les effets se répliquent dans chaque État et deviennent meilleurs, pas moins bons, à mesure que le pays absorbe population, centres urbains et capitalistes.

## 4. Audit historique — République de Venise en 1776

### 4.1 Forces encore réelles

Venise n'est plus l'intermédiaire global dominant des siècles antérieurs, mais reste le principal port adriatique, le Rialto demeure un centre commercial important et le crédit est omniprésent dans une structure segmentée : banchi autorisés, Monti di Pietà, prêteurs privés, intermédiaires et crédit sur gage. L'État réglemente étroitement certains prêteurs et protège les transactions et la propriété.

La thèse d'un déclin maritime uniforme est en outre trop simple. Les traités conclus avec les États barbaresques à partir de 1763 réduisent risques et coûts de protection ; la recherche récente conclut à une reprise vigoureuse et durable du shipping vénitien sur les routes méditerranéennes et au-delà jusqu'en 1797.

La République conserve aussi une économie proto-industrielle : verre, papier, imprimerie, produits de luxe et activités de la Terraferma. Dans les années 1770, les Cinq Sages du Commerce renforcent la collecte de données, modulent les droits de douane pour les matières premières et les manufactures, et préparent des réformes comme le cours d'architecture navale de 1777 et le code de marine marchande de 1786.

Ces éléments justifient :

- shopkeepers/merchant investment élevé ;
- aristocratic merchant capital ;
- trade advantage ;
- une charte gratuite ;
- protection de la propriété ;
- un avantage maritime séparé.

### 4.2 Limites

Venise est une oligarchie fermée : environ deux mille patriciens monopolisent conseils et offices, assistés d'un corps également fermé de cittadini. Cette fermeture a historiquement réduit mobilité et accès aux lignes commerciales les plus lucratives. Au XVIIIe siècle, une partie importante du capital patricien est aussi dirigée vers la terre, la rente, la culture et la consommation, même si les nobles peuvent être des gestionnaires compétents.

La République reste riche et adaptable, mais elle a perdu la primauté globale au profit des économies atlantiques anglaise et néerlandaise. Les finances publiques se détériorent et la pauvreté urbaine progresse. Cela justifie une transition capitaliste industrielle moins fluide et une capacité territoriale limitée, pas un effondrement artificiel du commerce.

### 4.3 Ce que l'histoire ne justifie pas

La réglementation commerciale, l'Arsenal et les magistratures publiques ne sont pas l'équivalent d'une efficacité générale de nationalisation industrielle. Les trois bonus de retour de nationalisation et de dividendes publics transforment une capacité de régulation en avantage d'économie publique moderne ; ils sont donc anachroniques comme cœur de loi.

## 5. Audit historique — République de Gênes en 1776

### 5.1 Forces encore réelles

Pour la seconde moitié du XVIIIe siècle, les travaux de Giuseppe Felloni identifient deux piliers :

1. les investissements étrangers, principale source de revenu de l'oligarchie aristocratique ;
2. le shipping et le commerce, pour compte propre ou pour des marchands étrangers.

Les études sur le financement maritime confirment pour la même période un marché actif et flexible du crédit à la grosse, de l'assurance maritime et du partage des risques. Gênes reste un centre international de commerce et de finance malgré le déclin relatif de ses institutions politiques. Le capital génois est particulièrement mobile : une étude de patrimoine citée dans l'historiographie estime qu'en 1785 seulement 18 % des actifs de l'aristocratie sont immobiliers.

La Casa di San Giorgio et la tradition de dette publique illustrent une protection élaborée des créanciers, des titres, de la comptabilité et des mécanismes de compensation. Elles soutiennent bien la protection de la propriété, les chartes et l'efficacité du capital patricien.

### 5.2 Limites

La richesse est concentrée dans une oligarchie aristocratique, l'accès au capital dépend de réseaux de confiance et de relations avec l'élite, et l'économie reste très exposée aux défauts souverains et aux ruptures du commerce. Felloni montre que les pertes d'investissements étrangers durant les guerres révolutionnaires, puis le blocus continental, détruisent successivement les deux piliers.

Cette structure est financièrement sophistiquée mais peu scalable comme appareil territorial et moins adaptée au financement diffus de l'industrialisation du XIXe siècle. L'industrialisation génoise ne décolle qu'après réorientation vers les manufactures au XIXe siècle.

### 5.3 Ce que l'histoire ne justifie pas

San Giorgio est une association de créanciers et une institution de gestion de la dette et de recettes publiques ; elle ne justifie pas trois bonus généraux de nationalisation, dividendes publics et propriété d'État. Assimiler dette publique, banque, entreprise privilégiée et bâtiment nationalisé est précisément l'anachronisme à éviter.

## 6. Audit territorial des clés vanilla réellement supportées

### 6.1 Modifiers utilisables sans invention

| Clé 1.13.9 | Effet confirmé par définition/localisation vanilla | Pertinence | Risque de design |
|---|---|---|---|
| `state_bureaucracy_population_base_cost_factor_mult` | modifie le coût administratif de base dû à la population incorporée | meilleure contrainte intrinsèque : coût croissant avec population administrée | pèse aussi sur la population compacte de départ ; valeur doit rester faible |
| `state_incorporation_speed_mult` | modifie la vitesse d'incorporation de tous les États | ralentit l'intégration d'une expansion | simple délai si aucun coût ne frappe les territoires non incorporés |
| `state_contiguous_incorporation_speed_mult` | vitesse des États reliés par terre ou détroit à la capitale | peut cibler l'expansion terrestre contiguë | clé contre-intuitive si la pénalité contiguë dépasse la non-contiguë |
| `state_non_contiguous_incorporation_speed_mult` | vitesse des États sans connexion terrestre/détroit à la capitale | permet de distinguer possessions lointaines | punirait précisément le réseau maritime historique de VEN ; mauvais cœur de modèle |
| `state_tax_capacity_mult` | multiplicateur de tax capacity | limite la capacité fiscale territoriale | malus général immédiat, peu spécialisé et déjà proche de Traditionalism |
| `state_tax_collection_mult` | modifie le montant final des taxes de pops | coût fiscal direct et scalable avec assiette | très punitif, contourne le jeu de tax capacity et touche le cœur compact |
| `country_bureaucracy_mult` | multiplicateur de la bureaucratie produite | rend l'appareil administratif moins efficace | punit tout usage de bureaucratie, y compris commerce/institutions, sans lien direct à la taille |
| `building_unincorporated_throughput_add` | bonus/malus de throughput pour tous les bâtiments non incorporés | rend une conquête brute moins rentable | affecte aussi ports et enclaves marchandes ; risque de contredire l'identité maritime |
| `building_group_bg_manufacturing_unincorporated_throughput_add` | throughput manufacturier dans les États non incorporés | empêche l'industrialisation facile des conquêtes | plus ciblé et déjà utilisé par une loi vanilla, mais n'agit pas sur agriculture/extraction |
| `state_disallow_incorporation_bool` | interdit l'incorporation | techniquement réel | rejeté : interdiction arbitraire contraire au cahier des charges |

La meilleure paire T1 est donc :

- `state_bureaucracy_population_base_cost_factor_mult = +0.10` à `+0.15` ;
- `state_incorporation_speed_mult = -0.10` à `-0.20`.

Ces valeurs sont des enveloppes de proposition, pas une implémentation validée. La première crée le vrai coût croissant et un coût d'opportunité par rapport aux autres systèmes économiques ; elle est initialement amortie par le -25 % d'Hereditary Bureaucrats sans être annulée comme différence entre lois. La seconde empêche une absorption instantanée. Un malus de throughput non incorporé peut être réservé à une itération ultérieure si le simple délai est trop facile à contourner.

### 6.2 Triggers et valeurs de taille réellement observés

- `num_states` existe comme trigger de scope pays (`num_states > N`) et comme valeur (`scope:country.num_states`).
- `total_population` existe comme trigger et comme valeur de calcul.
- `any_scope_state` / `every_scope_state` existent au scope pays.
- `is_incorporated = yes/no` existe au scope État.
- aucun trigger direct `num_incorporated_states` ou `num_unincorporated_states` n'a été trouvé dans les fichiers locaux ; les compter exige une itération/valeur scriptée.
- `on_state_owner_change` et `on_state_incorporation` existent comme on-actions ; une variation de population exige en plus un pulse ou un autre mécanisme de réévaluation.

### 6.3 Métriques T2

| Métrique | Robustesse | Exploitabilité | Cohérence historique | Verdict |
|---|---|---|---|---|
| `num_states` | élevée, très simple | États partiels et densités très différentes ; VEN commence déjà à 7, GEN à 1 | mesure l'étendue administrative, pas la charge humaine | meilleure métrique simple, mais seuil compact obligatoirement ≥7 |
| `total_population` | élevée | migration, sujets et conquêtes peu peuplées ; pénalise une métropole compacte dense | mesure directement la charge de gouvernance | bon second signal, mauvais signal unique |
| États incorporés comptés par script | moyenne | laisser les conquêtes non incorporées évite le palier | mesure le territoire réellement intégré | insuffisant seul |
| États non incorporés comptés par script | moyenne | incorporation rapide ou jeu avec sujets | cible directement les conquêtes récentes | bon déclencheur secondaire |
| combinaison États + population + non-incorporés | moyenne à faible techniquement | la moins exploitable | la plus cohérente | meilleure qualité théorique, mais trop de script pour le premier patch |

La métrique la moins exploitable est une combinaison de `num_states` et `total_population`, avec présence d'États non incorporés comme aggravant. Elle n'est toutefois pas la meilleure option pré-release : maintenir quatre paliers corrects exige des valeurs scriptées, des réévaluations à chaque changement de propriétaire/incorporation et une réévaluation périodique de la population.

Enveloppe de seuils à tester, non gelée :

- `COMPACT_MERCHANT_REPUBLIC` : jusqu'à 7 États, afin que VEN et GEN commencent dans l'identité voulue ;
- `EXPANDING_MERCHANT_REPUBLIC` : 8–12 États ;
- `TERRITORIAL_MERCHANT_STATE` : 13–20 États ;
- `OVEREXTENDED_MERCHANT_OLIGARCHY` : 21 États ou plus.

Un seuil de population doit être calibré sur une extraction/observation runtime ultérieure ; le fixer dans cet audit sans runtime produirait une fausse précision. Si la population devient un trigger alternatif, elle doit pouvoir faire monter un pays d'un palier mais jamais le faire redescendre sous le palier imposé par son nombre d'États.

## 7. Modèles territoriaux T1 et T2

| Modèle | Identité | Robustesse | IA | Risque runtime | Conclusion |
|---|---|---|---|---|---|
| T1 — intrinsic scaling | coût administratif proportionnel à la population + incorporation plus lente | très élevée ; deux modifiers de loi réels | l'IA comprend les effets standards, sans état caché | faible | meilleur pour le premier patch |
| T2 — four tiers | identité très lisible et forte | moyenne ; nécessite suivi et nettoyage de modifiers | l'IA peut rester sous Merchant Banking malgré un palier sévère si `ai_will_do` n'est pas revu | moyen à élevé | futur mécanisme, après tests runtime |

T1 a une limite : un empire de protectorats et de ports commerciaux peut rester efficace. Ce n'est pas nécessairement un exploit ; c'est précisément une trajectoire cohérente pour une république marchande, tant que la conquête et l'incorporation directes sont moins rentables.

## 8. Trois propositions A/B/C

### Option A — Minimal numeric nerf

Structure inchangée :

| Modifier | Actuel | A proposé |
|---|---:|---:|
| aristocrats investment efficiency | +50 % | +35 % |
| shopkeepers investment efficiency | +50 % | +35 % |
| trade advantage | +10 % | +8 % |
| capitalists investment efficiency | -10 % | -15 % |
| private construction allocation | 50 % | 40 % |
| nationalization investment return | +50 % | +25 % |
| government dividends reinvestment | +50 % | +25 % |
| government dividends efficiency | +30 % | +15 % |
| free charters | 1 | 1 |
| no uncompensated nationalization | yes | yes |

| Critère | Évaluation |
|---|---|
| historical_fit | moyen |
| balance_quality | moyen |
| implementation_risk | très faible |
| runtime_risk | très faible |
| patch_release_safety | très élevée |

Cette option réduit la puissance mais conserve l'anachronisme public et ne crée aucune raison structurelle d'abandonner la loi lors d'une expansion territoriale.

### Option B — Asymmetric merchant oligarchy

Noyau proposé :

| Modifier | B proposé |
|---|---:|
| aristocrats investment efficiency | +35 à +40 % |
| shopkeepers investment efficiency | +45 à +50 % |
| trade advantage | +10 à +15 % |
| capitalists investment efficiency | -15 à -25 % ; cible -20 % |
| private construction allocation | 35 à 40 % ; cible 40 % |
| nationalization investment return | 0 |
| government dividends reinvestment | 0 |
| government dividends efficiency | 0 |
| free charters | 1 |
| no uncompensated nationalization | yes |

Ajouter la contrainte B1 :

- population bureaucracy cost : +10 à +15 % ;
- incorporation speed : -10 à -20 %.

| Critère | Évaluation |
|---|---|
| historical_fit | élevé |
| balance_quality | élevé |
| implementation_risk | faible |
| runtime_risk | faible |
| patch_release_safety | élevée |

Cette option supprime trois bonus génériques, assume une très forte spécialité marchande et fait du passage à Interventionism ou Laissez-Faire un vrai choix pour industrialiser et administrer un grand territoire.

### Option C — Deep merchant republic mechanic

Future architecture : dépendance à la marine marchande, vulnérabilité aux disruptions, quatre paliers territoriaux, effets liés aux trade centers et aux chartes, pouvoir patricien, et mécanisme d'abandon de Merchant Banking quand l'État devient territorial.

| Critère | Évaluation |
|---|---|
| historical_fit | très élevé si correctement calibré |
| balance_quality | potentiellement très élevée |
| implementation_risk | élevé |
| runtime_risk | élevé |
| patch_release_safety | faible avant une campagne de tests dédiée |

Option C exige événements/on-actions ou journal entry, variables/valeurs scriptées, localisation, logique de nettoyage au changement de loi, pondération IA et validation save/reload. Elle est rejetée pour le premier patch, non comme direction future.

## 9. Choix B1/B2/B3

| Critère | B1 — intrinsèque simple | B2 — quatre paliers | B3 — hybride, 1–2 paliers |
|---|---|---|---|
| historical_fit | élevé | très élevé | très élevé |
| gameplay_identity | élevé | très élevé | très élevé |
| balance | élevé mais continu | très élevé si seuils justes | très élevé |
| AI_behavior | bon avec modifiers standards ; revoir tout de même `ai_will_do` | risque de rester dans une loi devenue punitive | risque intermédiaire |
| exploitability | moyenne : sujets/ports restent attractifs | faible avec métrique combinée | faible à moyenne |
| implementation_complexity | faible | élevée | moyenne |
| runtime_risk | faible | élevé | moyen |
| release_safety | élevée | faible | moyenne |

**Recommandation : B1 pour le premier patch post-release.** B3 est la meilleure évolution après instrumentation et tests, avec un seul palier territorial déclenché par `num_states` comme première étape possible. B2 ne doit pas être introduit à la veille du patch.

## 10. Test des cinq choix stratégiques

1. **Une petite puissance commerciale a-t-elle une forte raison de conserver Merchant Banking ?** Oui sous B/B1 : meilleur investissement shopkeeper, capital patricien, trade advantage et charte gratuite forment une niche que les autres lois n'offrent pas ensemble.
2. **Un conquérant finit-il par avoir une forte raison de l'abandonner ?** Oui : le coût bureaucratique croît avec la population incorporée, l'incorporation ralentit, les capitalistes restent moins efficaces et les avantages modernes de propriété publique disparaissent.
3. **Une loi classique devient-elle réellement meilleure pour un État territorial ?** Oui. Interventionism devient meilleur pour la mixité public/privé et la nationalisation ; Laissez-Faire pour l'industrialisation capitaliste, le crédit et 75 % de construction privée.
4. **Est-ce un choix et non un simple nerf ?** Oui, parce que la réduction des bonus génériques finance le maintien, voire un léger rebuff conditionnel, des bonus de commerce et de shopkeepers.
5. **La loi peut-elle être plus forte dans sa spécialité sans devenir dominante ?** Oui : +15 % de trade advantage et +50 % shopkeepers restent envisageables si les trois bonus publics sont supprimés, l'allocation privée abaissée à 40 %, la pénalité capitaliste portée vers -20 % et B1 ajouté.

## 11. Recommandation finale de patch

Implémenter ultérieurement, dans une phase autorisée et testée, **Option B + B1** :

1. conserver et hiérarchiser le capital marchand : shopkeepers au sommet, aristocrates légèrement en dessous ;
2. conserver une charte gratuite et la protection contre la nationalisation sans compensation ;
3. supprimer les trois bonus de nationalisation/dividendes publics ;
4. réduire l'allocation privée à environ 40 % ;
5. renforcer modérément la pénalité capitaliste vers -20 % ;
6. ajouter +10 à +15 % de coût bureaucratique lié à la population et -10 à -20 % de vitesse d'incorporation ;
7. conserver +10 % de trade advantage au premier test, puis n'envisager +15 % qu'après mesure de la pile complète ;
8. auditer séparément le `+10000` minting et le `+50 %` throughput du Centre of Commerce : même après correction de la loi, ils peuvent maintenir la pile au-dessus de `STRONG_BUT_SPECIALIZED` ;
9. remplacer l'`ai_will_do` copié d'Agrarianism par une logique future tenant compte de la taille, de la population, de l'urbanisation et de la loi actuelle ; ce point ne doit pas être glissé sans test dans le patch numérique.

Critère d'acceptation futur : VEN et GEN compacts doivent préférer Merchant Banking pour commerce/finance ; un État territorial doit objectivement préférer Interventionism ou Laissez-Faire selon sa stratégie. La loi ne doit jamais interdire la conquête : elle doit rendre l'administration directe et l'industrialisation générale progressivement moins efficaces.

## 12. Sources historiques

Sources académiques et institutionnelles consultées ; accès le 14 août 2026 :

- Giuseppe Felloni, « [The Population Dynamics and Economic Development of Genoa, 1750–1939](https://www.cambridge.org/core/books/population-and-society-in-western-european-port-cities-c-16501939/population-dynamics-and-economic-development-of-genoa-17501939/C69A2CA4F2C924974A764770E176D9F8) », *Population and Society in Western European Port Cities*, Liverpool University Press, 2002.
- Andrea Zanini, « [Financing and Risk in Genoese Maritime Trade During the Eighteenth Century: Strategies and Practices](https://link.springer.com/chapter/10.1007/978-3-031-04118-1_12) », Springer, 2023.
- Giuseppe Felloni et Guido Laura, *[Genoa and the History of Finance: Twelve Firsts?](https://www.giuseppefelloni.com/rassegnastampa/genovafinanza12primati_2017.pdf)*, 2017, avec archives de la Casa di San Giorgio.
- Catia Brilli, *[Genoese Trade and Migration in the Spanish Atlantic, 1700–1830](https://www.cambridge.org/core/books/genoese-trade-and-migration-in-the-spanish-atlantic-17001830/ABB1E2D50F949C9B584EDE11EA392453)*, Cambridge University Press, 2016.
- Matteo Pompermaier, « [Borrowing in a pre-industrial city: financial behaviour and economic rationality in eighteenth-century Venice](https://www.cambridge.org/core/journals/continuity-and-change/article/borrowing-in-a-preindustrial-city-financial-behaviour-and-economic-rationality-in-eighteenthcentury-venice/A3F420B07CEED5B4B5486048FD6B2C39) », *Continuity and Change*, 2025.
- Pierre Niccolò Sofia, « [The maritime consequences of peace: The impact of treaties with the Barbary states on Venetian shipping in the eighteenth century](https://journals.sagepub.com/doi/10.1177/08438714231207766) », *International Journal of Maritime History* 36/2, 2024.
- Giulia Delogu, *[Mediterranean Reflections: Venice as Myth and Model (18th–19th centuries)](https://pric.unive.it/fileadmin/user_upload/citta_porto/documenti/Reflections_ENG.pdf)*, Ca' Foscari University of Venice / Ibis, 2024.
- Maartje van Gelder, « [Papering Over Protest: Contentious Politics and Archival Suppression in Early Modern Venice](https://academic.oup.com/past/article/258/1/44/6532405) », *Past & Present* 258/1, 2023.
- Diego Puga et Daniel Trefler, « [International Trade and Institutional Change: Medieval Venice's Response to Globalization](https://academic.oup.com/qje/article/129/2/753/1868053) », *Quarterly Journal of Economics* 129/2, 2014, utilisé pour la genèse et les effets durables de la fermeture oligarchique, non comme description directe de 1776.

## 13. Arrêt de phase

Audit terminé. Aucune proposition de ce document n'est implémentée dans cette phase. Aucun runtime, staging, commit ou push n'a été effectué.
