# HOTFIX-4E4 - Pont Opium Wars / Tenpo

## 1. Resume

Le pont entre la defaite chinoise dans la guerre de l'opium et `tenpo_events.6` a ete restaure par un hunk limite dans `opium_wars.4`. Le caller etait isolable parce que l'evenement local possedait deja le scope du vainqueur du port de traite et s'executait deja sur le pays vaincu.

Apres restauration du caller, les trois applications de `je_sakoku_maybe_we_should_open_up` dans les options de `tenpo_events.6` ont ete mutualisees dans un bloc `after` protege contre une seconde initialisation.

## 2. Decision

**Import effectue.**

Le caller a pu etre ajoute sans importer d'autre evenement Opium Wars ni remplacer un fichier entier. Le fork conserve son architecture locale, sa date minimale de 1836 pour la chaine Opium Wars et le trigger prudent `CHI`/`GBR` de `tenpo_events.6`.

## 3. Comparaison Opium Wars fork / hotfix / vanilla

| Evenement Opium Wars | Fork avant | Hotfix | Vanilla | Caller Tenpo present ? | Risque |
|---|---|---|---|---:|---|
| `opium_wars.1` | Ajoute `year >= 1836` | Pas de garde annuelle explicite | Pas de garde annuelle explicite | Non | Le fork est plus prudent pour 1776. |
| `opium_wars.4` | Pays consommateur d'opium vaincu ; scope du vainqueur de port deja cree | Sauve le pays vaincu et appelle Tenpo sous conditions CHI/GBR | Appelle Tenpo dans une condition moins precise | Oui dans hotfix/vanilla | Faible avec le hunk hotfix conditionnel. |
| `opium_wars.5` | Victoire du pays importateur | Architecture proche | Architecture proche | Non | Hors perimetre. |

## 4. Caller exact identifie

Le caller appartient a `opium_wars.4`, dans son bloc `immediate`. Cet evenement represente l'echec du pays dont la population est obsede par l'opium.

Le hotfix appelle `tenpo_events.6` lorsque :

- le pays vaincu sauvegarde est `c:CHI` ;
- soit le vainqueur du port de traite est `c:GBR`, soit la Chine a adopte `law_free_trade` ;
- `c:JAP` existe comme scope valide.

L'appel est execute sur `c:JAP`, avec `popup = yes`, sans delai supplementaire.

## 5. Scope et conditions du caller

Le bloc `immediate` sauvegarde maintenant son root sous `opium_wars_defeated_country`. Le scope local `opium_wars_treaty_port_winner` existait deja avant cette phase et a ete conserve.

La garde `c:JAP ?=` empeche un appel sur un Japon inexistant. Le demarrage en 1776 est exclu par `year >= 1836` dans le trigger local de `opium_wars.1`, garde absente du hotfix et de la vanilla mais preservee ici.

## 6. Modification du fichier Opium Wars

Deux ajouts limites ont ete effectues dans `opium_wars.4.immediate` :

1. sauvegarde de root dans `opium_wars_defeated_country` ;
2. bloc conditionnel exact du hotfix appelant `tenpo_events.6` sur JAP.

Aucun autre effet, choix, evenement ou trigger Opium Wars n'a ete importe.

## 7. Modification de tenpo_events.6

Les trois options A, B et C ne posent plus separement `je_sakoku_maybe_we_should_open_up`. L'effet et son tooltip sont executes une seule fois dans `after`, quelle que soit l'option choisie.

Tous les autres effets des options sont conserves, notamment les radicaux, loyalistes, modifiers, conversion d'ideologie et ponderations IA.

## 8. Garde anti-double

Le bloc commun exige :

- que JAP possede encore `je_sakoku` ;
- que `je_sakoku_maybe_we_should_open_up` n'existe pas deja.

Le trigger propre de `tenpo_events.6` conserve en plus `NOT has_variable = opium_war_has_happened_jap_var`, variable posee dans son `immediate`. Son cooldown `never_fire_again_modifier_time` est egalement conserve.

## 9. Trigger CHI/GBR conserve

Le trigger de `tenpo_events.6` contient toujours :

```txt
exists = c:CHI
exists = c:GBR
```

Le trigger hotfix reduit au seul `has_dlc_feature = ep2_content` n'a pas ete importe.

## 10. Ce qui n'a pas ete importe

- Aucun autre hunk de `opium_wars_events.txt`.
- Aucun changement des conditions de selection du vainqueur de port local.
- Aucun changement du trigger `CHI`/`GBR` de `tenpo_events.6`.
- Aucun effet distinct des options A, B ou C de `tenpo_events.6`.
- Aucun changement de `tenpo_events.1`, `je_tenpo_crisis` ou du lancement local 1833-1835.
- Aucun changement Sakoku HOTFIX-4E1, 4E2 ou 4E3.
- Aucun contenu Meiji, Iwakura, Ryukyu, Hokkaido/Ezo ou Zaibatsu.

## 11. Risques restants

- Le pont ne peut etre teste completement sans jouer ou provoquer la resolution d'une guerre de l'opium impliquant CHI et GBR.
- Le scope `opium_wars_treaty_port_winner` reste construit selon l'architecture historique locale du fork, plus ancienne que celle du hotfix.
- Si CHI adopte librement `law_free_trade` avant la resolution, l'alternative hotfix peut tout de meme declencher l'evenement japonais, conformement au hunk importe.
- La variable Sakoku n'est posee que si la JE Sakoku est encore active.

## 12. Tests a faire en jeu

1. Demarrer en 1776 et confirmer qu'aucun evenement Opium Wars ou `tenpo_events.6` ne se lance prematurement.
2. Provoquer une defaite de CHI face a GBR avec port de traite et verifier un seul `tenpo_events.6` sur JAP.
3. Tester la branche dans laquelle CHI adopte `law_free_trade`.
4. Tester avec Sakoku encore active : le bouton de sortie doit devenir disponible une seule fois.
5. Tester apres resolution de Sakoku : aucune variable d'ouverture ne doit etre posee.
6. Choisir successivement A, B et C de `tenpo_events.6` sur des sauvegardes separees et verifier les effets propres.
7. Surveiller `error.log` pour `opium_wars.4`, `opium_wars_defeated_country`, `opium_wars_treaty_port_winner`, `tenpo_events.6`, `je_sakoku_maybe_we_should_open_up` et `invalid scope`.

## 13. Liste exacte des fichiers modifies ou crees

- Modifie : `events/opium_wars_events.txt`
- Modifie : `events/japan_events/ep2_tenpo_events.txt`
- Cree : `docs/reports/hotfix/HOTFIX_4E4_OPIUM_WARS_TENPO_BRIDGE.md`

## 14. Confirmation de perimetre

- Aucun lancement Tenpo en 1776 n'a ete ajoute.
- Aucune modification de la chaine locale `phase1_japan_*`.
- Aucun changement de `tenpo_gdp_goal` local.
- Aucun changement Sakoku HOTFIX-4E1, HOTFIX-4E2 ou HOTFIX-4E3.
- Aucun changement Meiji ou Iwakura.
- Aucun changement Ryukyu, Hokkaido/Ezo ou Zaibatsu.
- Aucun changement SKH/ULT, NAVY, ADMIN, IR1, BIC ou Inde.
- Le stash MARATH n'a pas ete applique ni modifie.
- Aucun commit n'a ete cree.
