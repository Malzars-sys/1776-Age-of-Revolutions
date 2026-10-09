# Ottoman 1776 : journaux, influence russe et armée permanente

Rapport du 9 octobre 2026. Branche **main**, sans commit, changement de branche, push ni fusion. Les modifications préexistantes ont été conservées. Ce rapport remplace les règles du précédent rapport pour les deux journaux ottomans et le comportement initial du bloc russe.

**Résultat intégré : 72 unités permanentes directement ottomanes, 114 conscrits inchangés ; Égypte indépendante du décompte, 15 permanents et 25 conscrits inchangés.** Les contrôles statiques passent. Aucun lancement, redémarrage ni pilotage du jeu n’a été effectué par l’agent après cette refonte : les finances et la stabilité diplomatique ne sont donc pas certifiées en jeu.

## 1. Fichiers modifiés et périmètre

| Fichier | Modification de ce lot |
|---|---|
| [common/history/military_formations/04_military_formations_middle_east.txt](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/history/military_formations/04_military_formations_middle_east.txt>) | 22 fantassins au mousquet permanents supplémentaires ; encodage corrigé. |
| [common/journal_entries/1776_ottoman_reforms.txt](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/journal_entries/1776_ottoman_reforms.txt>) | Dix objectifs visibles, impulsion hebdomadaire, malus politique, échéance de 1836. |
| [common/scripted_triggers/1776_ottoman_reform_triggers.txt](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/scripted_triggers/1776_ottoman_reform_triggers.txt>) | Dix conditions indépendantes et trois voies politiques identifiables. |
| [common/scripted_effects/1776_ottoman_reform_effects.txt](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/scripted_effects/1776_ottoman_reform_effects.txt>) | Score 0–10, allégement gradué, migration, compteurs, transition et retraits gardés. |
| [common/static_modifiers/1776_ottoman_reforms.txt](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/static_modifiers/1776_ottoman_reforms.txt>) | Base +100 points/−10 %, allégement unitaire, pression politique +0,15/−15 %. |
| [common/journal_entry_groups/1776_ottoman_reforms.txt](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/journal_entry_groups/1776_ottoman_reforms.txt>) | Nouvelle catégorie Crises de l’autorité impériale. |
| [events/1776_ottoman_reforms.txt](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/events/1776_ottoman_reforms.txt>) | Transition sans garde de date empêchant l’échec précoce. |
| [events/sick_man_events.txt](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/events/sick_man_events.txt>) | Surcharge homonyme du jeu : retraits vanilla gardés et infobulle fiscale conditionnelle. |
| [common/journal_entries/00_sick_man.txt](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/journal_entries/00_sick_man.txt>) | Retrait de l’ancien malus bureaucratique conditionnel ; héritage existant conservé. |
| [localization/french/1776_diplomacy_ottoman_l_french.yml](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/localization/french/1776_diplomacy_ottoman_l_french.yml>) | Textes narratifs et objectifs/seuils complets en français. |
| [localization/english/1776_diplomacy_ottoman_l_english.yml](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/localization/english/1776_diplomacy_ottoman_l_english.yml>) | Équivalents anglais. |
| [common/history/ai/00_secret_goals.txt](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/history/ai/00_secret_goals.txt>) | Russie : domination plutôt que conquête ; accommodation initiale des deux gouvernements. |
| [common/history/diplomacy/00_relations.txt](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/history/diplomacy/00_relations.txt>) | Russie/PLC à 0 ; Russie/CRI à −10, sans amitié artificielle. |
| [common/history/power_blocs/00_power_blocs.txt](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/history/power_blocs/00_power_blocs.txt>) | Levier initial russe +650/PLC et +550/CRI, non renouvelé. |
| [tools/validate_diplomacy_ottoman_1776.py](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/tools/validate_diplomacy_ottoman_1776.py>) | Régressions militaires, 1024 configurations, frontières de seuils, erreurs de retrait, transitions. |
| [common/history/buildings/03_north_africa.txt](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/history/buildings/03_north_africa.txt>) | Encodage UTF-8 BOM seulement dans ce lot. |
| [common/history/buildings/98_build_start_1776_world_redistribution.txt](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/history/buildings/98_build_start_1776_world_redistribution.txt>) | Encodage UTF-8 BOM seulement dans ce lot. |
| [common/history/states/00_states.txt](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/history/states/00_states.txt>) | Encodage UTF-8 BOM seulement dans ce lot. |
| [common/production_methods/03_mines.txt](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/production_methods/03_mines.txt>) | Encodage UTF-8 BOM seulement ; rendement diesel 85 du précédent lot préservé. |
| [docs/reports/diplomacy/DIPLOMACY_OTTOMAN_1776_2026-10-09.md](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/diplomacy/DIPLOMACY_OTTOMAN_1776_2026-10-09.md>) | Lien de priorité vers ce nouveau rapport ; ancien récit conservé. |
| [docs/reports/diplomacy/OTTOMAN_REFORMS_RUSSIAN_STABILITY_2026-10-09.md](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/diplomacy/OTTOMAN_REFORMS_RUSSIAN_STABILITY_2026-10-09.md>) | Ce rapport. |

Les anciens transferts de provinces, populations, bâtiments et unités vers l’Égypte, les corrections polono-lituaniennes, la suppression du partage automatique, les traités antérieurs et les déblocages militaires ne sont pas annulés. Le fichier d’audit des logs demeure disponible, sans modification dans ce lot. Aucun nouvel asset graphique, fichier de preview ou chantier diplomatique scandinave/asiatique n’est créé.

## 2. Dix objectifs administratifs

Chaque ligne correspond à un trigger indépendant et à une condition visible dans la liste d’achèvement, avec son propre seuil.

| Nº | Objectif | Condition exacte | Justification de conception |
|---|---|---|---|
| 1 | Charges non héréditaires | Une loi bureaucratique autre que les bureaucrates héréditaires | Distinguer les offices au service de la Porte des privilèges familiaux. |
| 2 | Comptes bureaucratiques équilibrés | Bureaucratie ≥ 0 | L’administration doit pouvoir financer ses obligations courantes. |
| 3 | Réserve administrative | Aucune pénurie imminente de bureaucratie | Ne pas vivre continuellement au bord de la saturation, même avec un solde positif. |
| 4 | Offices approvisionnés | ≥ 90 % des administrations sans pénurie de biens ; au moins une administration | Les moyens matériels sont distincts de l’effectif employé. |
| 5 | Réforme de l’impôt foncier | Ne pas avoir la loi d’imposition foncière | Sortir du seul prélèvement foncier traditionnel. |
| 6 | Réforme de la fiscalité de consommation | Ne pas avoir la loi de fiscalité de consommation | Une réforme fiscale ne doit pas simplement déplacer l’impasse vers l’autre loi de départ. |
| 7 | Maintien de l’ordre | Police institutionnelle ≥ 2 | Permettre l’exécution des décisions impériales. |
| 8 | Formation | Institution scolaire ≥ 2 | Entretenir les compétences nécessaires à un État administré. |
| 9 | Capacité de recouvrement | Capacité fiscale ≥ besoins dans ≥ 75 % des États incorporés ; au moins un État incorporé | Représenter le réseau de recouvrement dans les provinces intégrées, sans exiger l’annexion de l’Égypte. |
| 10 | Offices effectivement pourvus | ≥ 90 % des administrations ont une occupation ≥ 80 % ; au moins une administration | Représenter des agents réellement en poste, indépendamment des fournitures ou d’une loi du XIXe siècle. |

Les objectifs 9 et 10 sont des **abstractions de gameplay**, pas l’affirmation que ces statistiques existaient sous cette forme en 1776. Le réseau fiscal et le personnel effectivement présent permettent de représenter une meilleure exécution des décisions sans imposer une technologie ou une réforme religieuse ultérieure. Les travaux archivistiques sur les offices judiciaires ottomans montrent l’importance des intermédiaires, des revenus attachés aux charges et des agents qui exerçaient effectivement les fonctions ; il ne s’agit pas de présenter toute l’institution religieuse comme une corruption uniforme. [Jun Akiba, étude sur les offices ottomans, 1750–1839](https://www.cambridge.org/core/journals/bulletin-of-the-school-of-oriental-and-african-studies/article/farming-out-judicial-offices-in-the-ottoman-empire-c-17501839/D7668E06494236F52BE3EBCC9A9ED57E).

Vérification contre **Victoria 3 1.13.11 installé** : capacité fiscale et besoins sont utilisés dans `common/buildings/07_government.txt` et disposent des triggers de comparaison localisés ; `occupancy`, `any_scope_building`, `filter` et `percent` sont utilisés par les journaux natifs, notamment le journal éducatif ottoman. Les gardes de non-vacuité empêchent les succès sans administrations ou sans provinces incorporées. Les pourcentages comptent les bâtiments/États, pas les niveaux d’administration ni leur population. Police et école sont maintenant deux objectifs ; leur alternative OU est toutefois conservée pour la voie politique I.

Aucune nouvelle condition n’ajoute un déblocage technologique du XIXe siècle. La difficulté effective des lois, des institutions et du recrutement doit être mesurée dans la partie.

## 3. Modificateurs de 0 à 10 objectifs

| Objectifs | Gaspillage fiscal **supplémentaire** | Production bureaucratique |
|---:|---:|---:|
| 0/10 | +100 points | −10 % |
| 1/10 | +90 points | −9 % |
| 2/10 | +80 points | −8 % |
| 3/10 | +70 points | −7 % |
| 4/10 | +60 points | −6 % |
| 5/10 | +50 points | −5 % |
| 6/10 | +40 points | −4 % |
| 7/10 | +30 points | −3 % |
| 8/10 | +20 points | −2 % |
| 9/10 | +10 points | −1 % |
| 10/10 | +0 points | 0 % |

La base du journal est `state_tax_waste_add = 1.0` et `country_bureaucracy_mult = -0.10`. Un unique allégement `−0.10/+0.01` est multiplié par le score courant. Cette construction `add_modifier ... multiplier = var:...` existe dans le journal natif du Monténégro. Le score résulte exactement de dix incréments booléens, donc ne peut pas dépasser dix. Le moteur continue d’appliquer ses autres facteurs fiscaux : **+100 points n’est pas une garantie que le gaspillage final affiché sera exactement 100 %**.

Certains objectifs peuvent déjà être satisfaits au départ. Le cas 0/10 est une configuration de test, pas une promesse que chaque nouvelle partie restera à 0. La première impulsion hebdomadaire recalcule les objectifs et accorde les réductions correspondantes ; elles n’attendent pas la résolution.

Le modificateur n’est remplacé que si son multiplicateur change ou s’il a disparu. Les retraits sont gardés par `has_modifier` ; une régression remet le malus correspondant sans cumuler plusieurs exemplaires.

## 4. Confirmation pendant douze mois

- L’impulsion hebdomadaire recalcule X/10 et remet immédiatement le compteur final à zéro si X < 10.
- L’impulsion mensuelle refait ce calcul puis ajoute un mois uniquement si les dix conditions sont satisfaites.
- Douze impulsions mensuelles consécutives avec toutes les conditions permettent l’achèvement.
- Le drapeau définitif d’achèvement empêche toute réactivation. La fin retire l’allégement et le moteur retire le malus attaché au journal.
- Les anciennes sauvegardes à trois axes sont migrées une fois : leurs allégements sont nettoyés et leurs mois de confirmation remis à zéro, car ils ne prouvent pas dix objectifs simultanés.
- La précision est celle des impulsions : une variation très brève, survenue puis annulée entre deux contrôles, n’est pas observée par ce dispositif. Ce n’est pas un suivi continu de chaque changement économique.

L’interface distingue **Réformes X/10** et **Consolidation X/12 mois**. La barre native porte sur les douze mois, pas sur les dix réformes.

## 5. Textes des deux journaux, français et anglais

La catégorie devient **Crises de l’autorité impériale / Crises of Imperial Authority**, par un groupe natif `context = country`, sans modifier la catégorie des journaux Tanzimat ultérieurs. Les seuils restent dans les objectifs et le statut ; le texte d’ambiance n’explique plus les anciens paliers fiscaux.

### Français

#### Le fardeau de la Sublime Porte

Des bureaux de Constantinople aux provinces lointaines, les décisions de la Sublime Porte se heurtent aux charges héréditaires, aux fermiers d’impôts et aux privilèges des administrateurs locaux. Les revenus destinés au Trésor s’égarent parmi les intérêts de ceux qui prétendent servir l’Empire. Rendre les comptes vérifiables, pourvoir les offices et faire respecter les décisions impériales devient une nécessité.



Ces réformes concernent l’administration et ses pratiques, non la foi de ses habitants. Chaque progrès soulage le Trésor ; seule leur consolidation durable permettra de tourner cette page.

Statut :

Rendre au Trésor les revenus qui lui échappent.

Réformes administratives : [Country.MakeScope.Var('ottoman_1776_admin_score').GetValue|0]/10.

Consolidation : [Country.MakeScope.Var('ottoman_1776_admin_months').GetValue|0]/12 mois consécutifs.

Chaque objectif satisfait retire 10 points de gaspillage fiscal supplémentaire et 1 point de malus bureaucratique, à la prochaine impulsion hebdomadaire. Une régression rétablit sa pénalité et remet la consolidation à zéro.

#### Un empire aux multiples maîtres

Les firmans du sultan proclament une seule souveraineté ; dans les provinces, le pouvoir se partage entre gouverneurs, notables et autorités locales. Les beys d’Égypte disposent de leurs propres forces, et les dépendances impériales négocient les limites de leur obéissance. Leur fidélité n’est pas nécessairement perdue, mais elle ne peut plus être tenue pour acquise.



Des institutions solides, un compromis respecté ou une administration rétablie peuvent encore rassembler ces autorités. Sans règlement durable, leurs rivalités ouvriront la voie aux interventions étrangères.

Statut :

Consolider un accord entre le centre et les provinces.

Stabilité : [Country.MakeScope.Var('ottoman_1776_stability_months').GetValue|0]/36 points consécutifs ; 1 point par mois stable, 2 après résolution du fardeau administratif.

Échéance ferme : 1er janvier 1836. Un échec anticipé exige 120 points de crise et une pression grave persistante.

Tant que ce journal est actif : +0,15 de désir de liberté hebdomadaire pour chaque sujet et −15 % de résistance au soutien étranger au séparatisme.

### English

#### The Burden of the Sublime Porte

From the offices of Constantinople to distant provinces, the commands of the Sublime Porte encounter hereditary appointments, tax farmers and the privileges of local administrators. Revenues intended for the Treasury disappear among the interests of those who claim to serve the Empire. Reliable accounts, staffed offices and enforceable imperial decisions have become necessities.



These reforms concern administration and its practices, not the faith of its inhabitants. Every improvement eases the Treasury’s burden; only lasting consolidation will bring this chapter to a close.

Statut :

Restore the revenues that escape the Treasury.

Administrative reforms: [Country.MakeScope.Var('ottoman_1776_admin_score').GetValue|0]/10.

Consolidation: [Country.MakeScope.Var('ottoman_1776_admin_months').GetValue|0]/12 consecutive months.

Each fulfilled objective removes 10 percentage points of additional tax waste and 1 percentage point of the bureaucracy penalty at the next weekly pulse. A reversal restores its penalty and resets consolidation.

#### An Empire of Many Masters

The Sultan’s decrees proclaim a single sovereignty; in the provinces, power is shared among governors, notables and local authorities. Egypt’s beys command their own forces, while the imperial dependencies negotiate the limits of their obedience. Their allegiance is not necessarily lost, but it can no longer be taken for granted.



Strong institutions, a respected settlement or a restored administration may yet bring these authorities together. Without a lasting settlement, their rivalries will invite foreign intervention.

Statut :

Consolidate a settlement between the centre and the provinces.

Stability: [Country.MakeScope.Var('ottoman_1776_stability_months').GetValue|0]/36 consecutive points; 1 point per stable month, 2 after resolving the administrative burden.

Firm deadline: 1 January 1836. Early failure requires 120 crisis points and continuing severe pressure.

While this entry is active: +0.15 weekly liberty desire for each subject and −15% resistance to foreign support for separatism.

Les titres, descriptions et choix des trois événements sont également fournis dans les deux fichiers de localisation ; les événements de succès distinguent le rétablissement des comptes de la réconciliation politique.

## 6. Conditions politiques et malus distincts

Conditions communes inchangées : posséder intégralement Thrace orientale, Ankara, Albanie et Bosnie ; garder la Basse-Égypte OU l’Égypte comme sujet ; tous les sujets directs et indirects sous **50** de désir de liberté ; séparatisme maximal **< 25 %** ; aucune révolution, guerre ni faillite ; bureaucratie **≥ 0**.

Trois voies alternatives, explicitement nommées :

1. **Centralisation** : légitimité ≥ 60 et police OU écoles ≥ 2.
2. **Compromis** : légitimité ≥ 75 et tous les sujets sous 25 de désir de liberté.
3. **Rétablissement de l’État** : journal administratif définitivement achevé et légitimité ≥ 50.

Le journal conserve sa progression antérieure de 36 points mensuels consécutifs, avec 2 points/mois après achèvement administratif. Une instabilité remet cette progression à zéro.

Les infobulles précisent que les bornes 25 et 50 sont strictes. Le test utilise toujours le véritable itérateur natif des sujets, non un compteur de sept objectifs. **Une liste nominative dédiée des sujets en défaut n’a pas été ajoutée** : il faut vérifier les sous-infobulles natives et les sujets dans l’écran diplomatique. Le rendu détaillé de l’interface n’a pas été observé après modification ; ne pas confondre présence des textes et validation visuelle en jeu.

Pression uniquement politique tant que cette entrée est active :

- `country_liberty_desire_of_subjects_add = 0.15` : +0,15 dans le calcul hebdomadaire de chacun des sujets directs du pays porteur. Les tests de stabilité concernent aussi les sujets indirects, mais le modificateur ne se propage pas automatiquement à leurs suzerains intermédiaires.
- `country_support_separatism_resistance_mult = -0.15` : résistance au **soutien étranger** au séparatisme réduite de 15 %, sans supposer que toutes les populations soient déjà séparatistes.
- Le +0,15 est une contribution additive ; les autres facteurs natifs, les multiplicateurs et l’amortissement selon le désir de liberté/trêve peuvent modifier la variation nette affichée.

Le modificateur natif **sick_man_of_europe ne contient aucun malus bureaucratique**. L’ancien malus fiscal distinct **outmoded_bureaucracy** était celui qui aurait créé une superposition. Il n’est pas ajouté à la transition ; les traces d’anciennes sauvegardes sont retirées avec garde. Les textes vanilla ne promettent plus son ajout pour ce scénario. Le journal administratif reste la seule source de ces malus structurels. Les autres lois, pénuries et événements génériques du jeu conservent naturellement leurs effets.

## 7. Échéance de 1836 et échecs précoces

Au **1er janvier 1836**, une crise non résolue échoue quel que soit le score de crise. Une garde interdit également qu’une résolution concurrente le même jour l’emporte sur l’échéance. Avant cette date, l’échec exige :

- au moins 120 points de crise ;
- une stabilité politique encore insuffisante ;
- une pression grave actuelle : perte du noyau territorial/allégeance égyptienne, séparatisme ≥ 50 %, révolution, faillite, ou guerre accompagnée d’un déficit bureaucratique ou d’une légitimité < 40.

La crise augmente de 1 point/mois instable, +1 sous pression grave et +1 en déficit bureaucratique ; une période stable retire un point/mois. L’échec le plus rapide de la configuration testée survient en 40 mois à +3/mois. Une instabilité légère ne suffit pas à elle seule à un échec précoce.

Le drapeau d’échec est posé, l’ancien journal et son modificateur politique sont retirés, puis un événement différé d’un jour lance le journal natif **L’Homme malade de l’Europe** et ses six objectifs. La réconciliation mensuelle récupère une transition dont l’événement aurait été perdu. La garde d’entrée bloque les doublons et la relance d’un journal déjà achevé. **L’année 1836 et un éventuel déclenchement précoce sont des choix de scénario**, non une datation historique de l’expression.

Les deux journaux initiaux conservent `can_revolution_inherit = yes` et ne conditionnent pas la réforme à une monarchie ou une religion. Les tests de reprise utilisent les mêmes variables et scripts ; le transfert réel lors d’une révolution/remplacement de pays reste à tester dans le moteur.

## 8. Diagnostic des départs du bloc russe

La sauvegarde précédente montrait CRI sortie le 6 janvier et PLC le 7. L’initialisation les avait donc bien inclus.

Le mécanisme a été identifié dans les sources installées :

- `common/ai_strategies/00_default_strategy.txt` : poids de sortie 50, ramené à zéro si le pays accepterait une invitation du chef de son bloc.
- `common/diplomatic_actions/28_invite_to_power_bloc.txt` : acceptation de base −100 ; contribution de levier plafonnée à +200 ; attitudes antagoniste/domineering/belligerent à −1000 ; prudence/désintérêt généralement défavorables ; dépendance économique, identité, rang, relations et cohésion participent au calcul.
- Les objectifs initiaux contredisaient l’appartenance : Russie **conquer** envers CRI/PLC, PLC **antagonize** envers Russie ; relations −30 sur les deux paires. Augmenter le levier seul ne compense pas une pénalité d’attitude de −1000.
- Les levier/cohésion/attitudes effectivement calculés le jour des deux sorties ne sont pas enregistrés dans cette inspection. Les contradictions de script sont démontrées ; attribuer un score d’acceptation exact aux deux sorties serait inventer une mesure.

## 9. Ajustements russes et justification

| Paramètre initial | PLC | CRI |
|---|---|---|
| Relations avec Russie | 0 | −10 |
| Objectif de Russie | dominate | dominate |
| Objectif du gouvernement membre | comply | comply |
| Levier ajouté au bloc russe | +650 | +550 |
| Annexion/sujétion automatique | Aucune | Aucune |
| Traité amical inventé | Aucun | Aucun |

Ces objectifs d’IA représentent un **accommodement gouvernemental initial sous pression**, pas l’adhésion de toutes les élites. Devlet Giray n’est pas remplacé par Şahin Giray. Les objectifs demeurent révisables par l’IA ; aucun contrôle périodique ne réimpose l’appartenance. Le levier est ajouté une seule fois au véritable scope du bloc (`add_leverage`, construction native) ; le plafond natif est 1000 et la dérive hebdomadaire vers le levier-cible est maintenue. L’exception RUS→CRI à la règle des cinq années demeure inchangée et n’impose pas la subordination.

**Traité polonais étudié, pas transformé en alliance :** les articles IV–V du [traité du 24 février 1768](https://pl.wikisource.org/wiki/Traktat_wieczystej_przyja%C5%BAni_pomi%C4%99dzy_Rosj%C4%85_a_Rzecz%C4%85pospolit%C4%85_(1768)) portent sur l’organisation constitutionnelle et la garantie russe. L’article I du [traité de 1773](https://pl.wikisource.org/wiki/Traktat_pierwszego_podzia%C5%82u_pomi%C4%99dzy_Rzecz%C4%85pospolit%C4%85_i_Rosj%C4%85_(1773)) renouvelle le cadre de 1768 sous réserve des modifications liées au partage ; il fournit donc une base pour représenter cette influence en 1776, pas pour nier le partage précédent.

Aucun article diplomatique nouveau n’est ajouté : la garantie d’indépendance vanilla est une protection militaire, possède le flag **friendly** et améliore les relations de **1/jour jusqu’à 80**. L’utiliser comme une simple garantie constitutionnelle ferait précisément apparaître l’amitié enthousiaste qu’il fallait éviter. Le maintien de PLC dans le bloc avec domination/levier est l’abstraction retenue ; aucune constitution n’est verrouillée par un faux traité.

Pour CRI, la sortie de la suzeraineté ottomane après le traité russo-ottoman de 1774 est conservée ; aucune alliance bilatérale fictive ne la remplace. La neutralisation de l’hostilité automatique au départ est un choix d’équilibrage réversible. **La présence aux cinq dates demandées reste non mesurée après correction**, et doit être vérifiée plutôt que promise.

## 10. Contrôles réalisés et protocole en jeu

### Contrôles réellement exécutés

- Validation structurale des scripts modifiés, du groupe et des événements.
- Contrôle des conditions/scopes clés contre les fichiers du jeu installé.
- Exécution de 1024 configurations des dix conditions : score, amplitude et absence de duplication.
- Frontières 90 % d’administrations, occupation 80 %, capacité fiscale 75 %, égalité capacité/besoins et ensembles vides.
- Score hebdomadaire inchangé : aucun remplacement gratuit du modificateur.
- Douze mois, interruption à onze mois, remise à zéro et reprise à un mois.
- Migration des anciens allégements ; retrait absent traité comme une erreur dans le modèle pour empêcher la régression des logs.
- Résolutions administratives et politiques indépendantes, échéance ferme même à zéro crise, échec précoce, reprise différée et idempotence.
- Surcharge des événements Sick Man comparée au natif : seules les gardes de retrait et l’infobulle fiscale ont changé.
- Inventaires Égypte/Levant conservés ; 41 historiques de bâtiments égyptiens et leurs technologies vérifiés.
- Exactement +22 permanents ottomans, aucun changement aux conscrits ni à l’armée égyptienne ; les États recruteurs appartiennent à TUR et le mousquet est débloqué.
- Localisations FR/EN et BOM, chemins d’icônes et `git diff --check` validés.
- Lecture des **60 fichiers de logs**, rotations comprises. Dernier lancement enregistré : **9 octobre 2026, 22:22:31**, antérieur à cette refonte.

### Armée permanente

| Formation | Avant ce lot | Renfort | Après |
|---|---:|---:|---:|
| Premier corps | 18 | 8, Thrace orientale | 26 |
| Deuxième corps | 7 | 4 Bosnie + 4 Bulgarie | 15 |
| Troisième corps | 16 | 6 Ankara | 22 |
| Quatrième corps | 9 | 0 | 9 |
| **Total directement ottoman** | **50** | **22** | **72** |

Le 58 signalé dans la partie n’est pas le total des historiques actuels. Le transfert antérieur des forces égyptiennes est conservé ; elles ne sont pas comptées parmi les 72. L’ajout sera visible dans une **nouvelle partie** : il ne renforce pas rétroactivement une sauvegarde.

### Protocole minimal demandé au joueur

1. Redémarrer avec ce fork seul dans le jeu de mods concerné, lancer une nouvelle partie au 1er janvier 1776 et garder un exemplaire de référence. Vérifier deux journaux actifs, catégorie, dix lignes, statuts X/10 et X/12 et le total **72 permanents** (conscrits affichés à part).
2. Jouer une semaine en pause budgétaire contrôlée puis consulter la décomposition fiscale/bureaucratique et la variation de liberté de chaque sujet. Vérifier que le score hebdomadaire correspond aux dix conditions effectivement cochées.
3. Sur des copies de test du scénario, préparer 0, 5 et 10 objectifs via les lois/institutions et les conditions de recrutement/approvisionnement. Ces fixtures ne servent pas à juger le comportement autonome de l’IA. À chaque état, relever avant/après impulsion : impôts par État, gaspillage final, production et consommation de bureaucratie, balance du pays, trésorerie/dette, emplois administratifs et militaires, coût des biens et prélèvements des sujets. **Ne pas déduire le budget du seul tableau de modificateurs.**
4. Avec les dix objectifs, avancer onze mois puis en perdre un : le compteur doit revenir à zéro et la pénalité gagner 10 points/1 %. Restaurer l’objectif et attendre douze mois. Vérifier retrait du journal, absence de pénalités propres à ce journal, sauvegarder/recharger et avancer un mois.
5. Tester chaque voie politique séparément ; tester les limites exactes 49/50 et 24/25 de liberté, 24,9/25 % de séparatisme et les trois seuils de légitimité. Relever les noms des sujets en défaut dans la diplomatie si les sous-infobulles ne les exposent pas.
6. Pour 1836, préparer une sauvegarde de test au 31 décembre 1835 avec le journal non résolu, y compris une version stable à score de crise nul. Avancer jusqu’au 2 janvier : ancien journal absent, nouveau présent, ancien malus politique absent et fardeau administratif toujours indépendant. Tester l’échec précoce avec 120 points et pression grave, puis le cas 120 sans pression grave qui ne doit pas échouer avant la date.
7. Sauvegarder avant l’échec, pendant le jour de transition et après. Recharger chacun, avancer au prochain mois : un seul journal Sick Man et aucune superposition fiscale. Refaire lors d’un changement de gouvernement et d’une révolution gagnée/perdue ; vérifier que les variables d’initialisation/achèvement ont été héritées.
8. Pour le bloc russe, **sans interventions ni fixtures**, relever au 1 janvier, 8 janvier, 1 février, 1 juillet 1776 et 1 janvier 1777 : appartenance de CRI/PLC, relations, attitudes, levier actuel/cible, cohésion, autonomie et acceptation diplomatique si l’infobulle la fournit. En cas de sortie, conserver la sauvegarde juste avant/après et ses logs pour identifier le terme réel de refus.
9. Vérifier qu’un joueur CRI/PLC peut refuser cette trajectoire, quitter le bloc selon les règles natives ou changer sa diplomatie ; RUS→CRI doit disposer de l’action de subordination sans cinq ans de présence, mais ses autres conditions ne doivent pas être contournées.
10. Relire les nouveaux logs avec [tools/audit_1776_runtime_logs.py](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/tools/audit_1776_runtime_logs.py>) et comparer les erreurs au lancement de référence. Le validateur statique [tools/validate_diplomacy_ottoman_1776.py](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/tools/validate_diplomacy_ottoman_1776.py>) est reproductible et ne modifie ni sauvegarde ni logs.

## 11. Erreurs résiduelles et limites

Dans le dernier lancement antérieur à correction, deux erreurs de retrait d’allégements absents apparaissaient **4520 fois chacune** dans les logs analysés. Les gardes ajoutées couvrent maintenant les scripts personnalisés et les retraits vanilla susceptibles d’être concernés. Leur disparition des **futurs** logs doit encore être confirmée par lancement.

Les avertissements de BOM des bâtiments égyptiens, des États, des formations et des mines sont corrigés sans changement de gameplay supplémentaire. D’autres erreurs historiques du mod restent présentes dans les logs, notamment effets/templates d’on-actions hérités, anciens rôles de personnages et triggers navals, localisation de groupes de discrimination, et créations de populations sur des États nuls. Elles ne doivent pas être décrites comme nouvelles erreurs de cette refonte ni comme corrigées ici. L’absence d’une nouvelle exécution interdit une certification « zéro erreur » du moteur.

L’économie au départ, l’embauche des 22 renforts, le coût des institutions et la stabilisation durable du bloc russe sont **à mesurer en jeu**. La baisse de revenus due à +100 points et la hausse de dépenses militaires rendent ce contrôle particulièrement important. Aucun faux résultat de budget, d’attitude, de cohésion ou de maintien jusqu’en 1777 n’est fourni.

Les tests de logique exécutent les scripts réels avec des entrées économiques/diplomatiques synthétiques : ils ne simulent ni l’IA native, ni la fiscalité complète, ni le gestionnaire de révolution. Les gardes de sauvegarde/reprise sont testées statiquement, pas certifiées dans le moteur. La liste nominative spéciale des sujets n’a pas été réalisée. Les interfaces FR/EN requièrent une vérification visuelle. La surcharge homonyme de l’événement natif peut entrer en conflit avec un autre mod qui remplace le même fichier : tester le jeu de mods réel.

Aucune modification hors périmètre géographique demandé, aucun push, merge ou changement de branche.
