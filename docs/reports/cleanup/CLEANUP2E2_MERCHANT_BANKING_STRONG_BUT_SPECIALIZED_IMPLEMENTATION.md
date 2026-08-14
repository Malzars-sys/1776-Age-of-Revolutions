# CLEANUP-2E-2 — Merchant Banking 1776 — Strong but Specialized Implementation

## Statut

- Phase : `CLEANUP-2E-2`
- Nature : implémentation ciblée de l'option B + B1 décidée par CLEANUP-2E-1
- Cible : `STRONG_BUT_SPECIALIZED`
- Branche : `cleanup-post-release`
- HEAD de référence : `61ee9578c65b505e662805c7da251308edc0f1a3`
- Baseline vanilla locale : `C:\Games\Victoria 3`
- Version vanilla confirmée : `1.13.9`
- Runtime Victoria 3 : non lancé
- Git : aucun staging, commit ou push

Sources de décision lues intégralement :

- `docs/reports/cleanup/CLEANUP2E1_MERCHANT_BANKING_1776_BALANCE_AUDIT.md`
- `docs/research/economy/CLEANUP2E1_MERCHANT_BANKING_MODIFIER_AUDIT.csv`

## Résultat de design

Merchant Banking conserve une spécialité forte de république marchande compacte : capital patricien, investissement des shopkeepers, avantage commercial, compagnie privilégiée et protection de la propriété. Elle perd sa boucle générique de propriété publique moderne et devient moins adaptée à la croissance territoriale directe et à l'industrialisation capitaliste.

La conquête n'est jamais interdite. Le coût est continu et économique : la population incorporée demande davantage de bureaucratie, tandis que les nouveaux États sont incorporés plus lentement. Aucun palier territorial, événement, on-action, journal entry, variable, scripted value, trigger de taille ou modificateur temporaire n'a été créé.

## Validation vanilla 1.13.9 des contraintes territoriales

Les deux clés ont été confirmées directement dans les fichiers locaux vanilla 1.13.9 avant modification :

| Clé | Existence et portée | Sens du signe confirmé |
|---|---|---|
| `state_bureaucracy_population_base_cost_factor_mult` | Définie dans `game/common/modifier_type_definitions/00_modifier_types.txt`; sa localisation indique le coût administratif de base causé par la population incorporée. | La définition marque une valeur positive comme défavorable et les bonus administratifs vanilla utilisent des valeurs négatives. `+0.10` augmente donc bien ce coût de 10 %. |
| `state_incorporation_speed_mult` | Définie dans le même fichier; sa localisation vise la vitesse d'incorporation des États, sans restriction de contiguïté. | La définition marque une valeur positive comme favorable; des technologies donnent `+0.05` et le modificateur négatif vanilla `usa_capital_relocated` donne `-0.25`. `-0.15` ralentit donc bien l'incorporation de 15 %. |

L'exécutable local donne `FileVersion = 1.13.9` et `ProductVersion = 1.13.9`; `caligula_branch.txt` donne `release/1.13.9`. Aucune baseline 1.13.10 n'est revendiquée.

## Ancien bloc

```txt
modifier = {
	state_aristocrats_investment_pool_efficiency_mult = 0.5
	state_shopkeepers_investment_pool_efficiency_mult = 0.5
	state_trade_advantage_mult = 0.1
	state_capitalists_investment_pool_efficiency_mult = -0.1
	country_private_construction_allocation_mult = 0.5
	building_nationalization_investment_return_add = 0.5
	country_government_dividends_reinvestment_add = 0.5
	country_government_dividends_efficiency_add = 0.3
	country_free_charters_add = 1
	country_disable_nationalization_without_compensation_bool = yes
}
```

## Nouveau bloc

```txt
modifier = {
	state_aristocrats_investment_pool_efficiency_mult = 0.40
	state_shopkeepers_investment_pool_efficiency_mult = 0.50
	state_trade_advantage_mult = 0.10
	state_capitalists_investment_pool_efficiency_mult = -0.20
	country_private_construction_allocation_mult = 0.40
	country_free_charters_add = 1
	country_disable_nationalization_without_compensation_bool = yes
	state_bureaucracy_population_base_cost_factor_mult = 0.10
	state_incorporation_speed_mult = -0.15
}
```

## CURRENT -> FINAL

| Effet | CURRENT | FINAL |
|---|---:|---:|
| Aristocrats | +50 | +40 |
| Shopkeepers | +50 | +50 |
| Trade advantage | +10 | +10 |
| Capitalists | -10 | -20 |
| Private construction | 50 | 40 |
| Nationalization return | +50 | REMOVED |
| Government dividends reinvestment | +50 | REMOVED |
| Government dividends efficiency | +30 | REMOVED |
| Free charters | 1 | 1 |
| No uncompensated nationalization | yes | yes |
| Population bureaucracy cost | 0 | +10 |
| Incorporation speed | 0 | -15 |

`MERCHANT_BANKING_MODIFIER_COUNT = 9`

## Justification de chaque changement

| Effet final | Justification |
|---|---|
| Aristocrats `+40 %` | Maintient un capital patricien puissant, mais légèrement inférieur à l'ancien maximum copié d'Agrarianism. |
| Shopkeepers `+50 %` | Reste le cœur de la spécialisation marchande et urbaine. |
| Trade advantage `+10 %` | Conserve l'identité commerciale sans renforcer avant runtime la pile déjà soutenue par Mercantilism et Centre of Commerce. |
| Capitalists `-20 %` | Représente l'accès oligarchique au capital et rend la transition vers le capitalisme industriel moderne moins fluide. |
| Private construction `40 %` | Convertit toujours fortement le capital marchand en construction, mais reste sous Agrarianism et Interventionism à 50 %, et sous Laissez-Faire à 75 %. |
| Free charters `1` | Marqueur borné et historique des compagnies privilégiées; inférieur aux deux chartes de Laissez-Faire. |
| No uncompensated nationalization `yes` | Protège la propriété et le capital privé/patricien; il s'agit d'une contrainte, non d'un bonus public. |
| Population bureaucracy cost `+10 %` | Crée un coût administratif naturel qui croît avec la population incorporée, sans bloquer la conquête. |
| Incorporation speed `-15 %` | Ralentit l'intégration territoriale directe sans interdire l'incorporation ni pénaliser spécifiquement les possessions maritimes non contiguës. |

Les trois effets suivants ont été supprimés sans remplacement :

- `building_nationalization_investment_return_add = 0.5`
- `country_government_dividends_reinvestment_add = 0.5`
- `country_government_dividends_efficiency_add = 0.3`

Ils formaient une boucle générique de propriété publique et de nationalisation moderne, étrangère au cœur historique de la loi en 1776 : oligarchie marchande, capital patricien, crédit, assurance maritime, compagnies privilégiées et finance commerciale.

## Interaction avec Hereditary Bureaucrats

VEN et GEN commencent avec `law_hereditary_bureaucrats`, qui fournit :

```txt
state_bureaucracy_population_base_cost_factor_mult = -0.25
```

Avec Merchant Banking, le cumul pertinent au départ est :

```text
-0.25 + 0.10 = -0.15
```

Les deux pays conservent donc un coût de population bureaucratique net inférieur de 15 % à la base tant que les seuls effets considérés sont ces deux lois. Merchant Banking impose néanmoins exactement un coût marginal de `+10` points par rapport à une autre loi économique sans ce modificateur. Hereditary Bureaucrats n'est ni neutralisée ni modifiée, et la pénalité Merchant Banking n'est pas portée à `+25 %`.

## Comparaison aux alternatives vanilla 1.13.9

| Loi | Investissement et construction | Propriété publique | Territoire et transition |
|---|---|---|---|
| Agrarianism | Aristocrats, clergymen et farmers `+50 %`; capitalists `-25 %`; construction privée `50 %`. | Retour de nationalisation `+50 %`, réinvestissement `+50 %`, efficacité `+30 %`, 1 charte. | Spécialisation rurale, sans contrainte territoriale intrinsèque. |
| Merchant Banking final | Aristocrats `+40 %`, shopkeepers `+50 %`, capitalists `-20 %`, trade advantage `+10 %`, construction privée `40 %`. | Aucun des trois bonus publics; compensation obligatoire; 1 charte. | Bureaucratie de population `+10 %` et incorporation `-15 %`; excellente niche commerciale compacte. |
| Interventionism | Aucun bonus ou malus de classe; construction privée `50 %`. | Retour `+50 %`, réinvestissement `+50 %`, efficacité `+25 %`, 1 charte. | Devient objectivement plus attractive pour un grand État mixte qui veut administrer et nationaliser. |
| Laissez-Faire | Shopkeepers et capitalists `+25 %`; construction privée `75 %`; prêts `-25 %`. | Réinvestissement `+100 %`, nationalisation désactivée, privatisation forcée, 2 chartes. | Devient objectivement plus attractive pour une industrialisation capitaliste moderne. |

Le choix n'est donc pas « forte contre faible ». Merchant Banking reste la meilleure expression spécialisée du capital marchand compact; Interventionism domine davantage la voie public/privé territoriale, et Laissez-Faire la voie capitaliste industrielle.

## Diff exact de gameplay

```diff
-	state_aristocrats_investment_pool_efficiency_mult = 0.5
-	state_shopkeepers_investment_pool_efficiency_mult = 0.5
-	state_trade_advantage_mult = 0.1
-	state_capitalists_investment_pool_efficiency_mult = -0.1
-	country_private_construction_allocation_mult = 0.5
-	building_nationalization_investment_return_add = 0.5
-	country_government_dividends_reinvestment_add = 0.5
-	country_government_dividends_efficiency_add = 0.3
+	state_aristocrats_investment_pool_efficiency_mult = 0.40
+	state_shopkeepers_investment_pool_efficiency_mult = 0.50
+	state_trade_advantage_mult = 0.10
+	state_capitalists_investment_pool_efficiency_mult = -0.20
+	country_private_construction_allocation_mult = 0.40
 	country_free_charters_add = 1
 	country_disable_nationalization_without_compensation_bool = yes
+	state_bureaucracy_population_base_cost_factor_mult = 0.10
+	state_incorporation_speed_mult = -0.15
```

Le reste de `law_merchant_banking`, notamment `ai_will_do`, est byte-equivalent à la référence après normalisation des fins de ligne. Toutes les autres lois de `common/laws/00_inject_laws.txt` sont inchangées.

## Localisation

Les descriptions anglaise et française expliquent désormais sans chiffres :

- l'oligarchie marchande;
- le crédit et le commerce maritime;
- les compagnies privilégiées;
- la protection de la propriété;
- la difficulté croissante à administrer et incorporer de vastes territoires.

Elles ne présentent pas la loi comme du capitalisme moderne, une économie libérale industrielle, une banque centrale ou une économie d'État.

## Fichiers de phase

Modifiés :

- `common/laws/00_inject_laws.txt`
- `localization/english/hotfix_laws_l_english.yml`
- `localization/french/hotfix_laws_l_french.yml`

Créés :

- `tools/cleanup2e2_validate.py`
- `docs/reports/cleanup/CLEANUP2E2_MERCHANT_BANKING_STRONG_BUT_SPECIALIZED_IMPLEMENTATION.md`

Les autres fichiers déjà modifiés ou non suivis avant la phase ont été préservés.

## Protections et éléments différés

- `law_merchant_republic`, `law_mercantilism`, `law_merchant_navy` et les autres lois initiales de VEN/GEN : inchangées.
- `common/history/countries/gen - genoa.txt` et `common/history/countries/ven - venetia.txt` : inchangés; Merchant Banking y reste activée.
- `common/history/military_formations/`, `common/history/characters/`, `common/character_templates/`, `common/dna_data/` : inchangés.
- Technologies gameplay : inchangées.
- Sept fichiers protégés de `docs/research/technology/` : hash-identiques et non stagés.
- `LAND_FORMATIONS = 214`
- `GENERAL_COMMAND_CAPACITY_SUFFICIENT = 214`
- `FLEETS = 41`
- `NAVAL_UNITS = 370`
- `FINAL_FIXED_HISTORICAL_ADMIRALS = 26`
- `MERCHANT_BANKING_AI_REWORK = DEFERRED`
- `CENTRE_OF_COMMERCE_BALANCE = DEFERRED_RUNTIME_OBSERVATION`

`modifier_centre_of_commerce_mod`, dont le throughput de centre de commerce, le minting et l'avantage exportateur, n'a pas été modifié. S'il reste manifestement excessif après runtime, il devra faire l'objet d'un hotfix séparé :

`FOLLOWUP_CANDIDATE = CENTRE_OF_COMMERCE_BALANCE`

## Validation statique

Commande :

```powershell
python tools/cleanup2e2_validate.py
```

Résultat :

```text
VANILLA_VERSION = 1.13.9
MERCHANT_BANKING_MODIFIER_COUNT = 9
MERCHANT_BANKING_REMOVED_PUBLIC_ECONOMY_BONUSES = 3
MERCHANT_BANKING_TERRITORIAL_CONSTRAINTS = 2
VEN_STARTS_WITH_MERCHANT_BANKING = 1
GEN_STARTS_WITH_MERCHANT_BANKING = 1
MILITARY_FILES_CHANGED = 0
TECHNOLOGY_FILES_CHANGED = 0
PROTECTED_TECH_FILES_CHANGED = 0
PROTECTED_TECH_FILES_STAGED = 0
STAGED_FILES = 0
STATIC_VALIDATION = PASS
```

Le validateur s'arrête avec `VANILLA_REFERENCE_UNAVAILABLE` si `C:\Games\Victoria 3` ou les fichiers locaux requis ne sont pas disponibles; il ne peut alors pas annoncer `STATIC_VALIDATION = PASS`.

## Checklist runtime — une seule session humaine

Ne tester que dans une nouvelle partie 1776, d'abord VEN puis GEN :

- [ ] Merchant Banking est active au démarrage dans les deux pays.
- [ ] Les neuf modificateurs finaux sont visibles et aucune clé brute/erreur de modificateur n'apparaît.
- [ ] Construction privée : `40 %`; capitalists : `-20 %`; shopkeepers : `+50 %`; aristocrats : `+40 %`.
- [ ] Le coût bureaucratique de population reflète Merchant Banking `+10 %` et le cumul initial attendu avec Hereditary Bureaucrats.
- [ ] L'incorporation affiche le malus de vitesse `-15 %`.
- [ ] Faire une expansion simple et comparer le coût administratif avant/après hausse de population ou de territoire.
- [ ] Lancer une incorporation et confirmer son ralentissement; ne pas poursuivre en campagne complète.
- [ ] Sauvegarder puis recharger dans la même session et vérifier que loi et modificateurs persistent sans erreur.

Évaluation à consigner :

```text
TRADE_SPECIALIZATION = ?
TERRITORIAL_COST_VISIBLE = ?
INDUSTRIAL_TRANSITION_COST_VISIBLE = ?
CENTRE_OF_COMMERCE_RESIDUAL_OVERPOWER = ?
```

Question de balance : Merchant Banking est-elle forte dans sa spécialité sans dominer les systèmes généralistes ? Si Centre of Commerce reste manifestement excessif, le noter seulement; ne pas le corriger pendant cette phase.

## Arrêt de phase

```text
STATIC_VALIDATION = PASS
RUNTIME = RUNTIME_PENDING_USER_SESSION
```
