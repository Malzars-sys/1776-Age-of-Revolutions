# HOTFIX-5C2E4C1K - Test runtime Sepoy B-1

## 1. Resume

Le test runtime B-1 de l'option 2.b de `sepoy_mutiny_events.2` a ete execute depuis une nouvelle partie BIC avec le harnais jetable seul. La boucle se termine sans crash ni blocage, mais le resultat fonctionnel est invalide : BIC perd la totalite de son noyau bengali et ne conserve qu'une petite portion de `STATE_PEGU`.

**Verdict obligatoire : `FAIL_B1_BENGAL_CORE_LOST`.**

Sous-resultat des radicaux : **`PARTIAL_RADICALS` / `INCONCLUSIVE_ZERO_BASELINE`**. La partie commence avec zero radical ; une hausse proportionnelle de 10 % appliquee a zero reste nulle et ne permet donc pas de valider l'effet.

## 2. Etat Git initial

- Branche : `hotfix-dlc-audit`.
- HEAD : `4e5af04 Prepare Sepoy Bengal retreat test`.
- Le seul element deja non suivi etait `docs/research/technology/`.
- Aucun fichier gameplay ni fichier du harnais n'etait modifie dans le fork.

## 3. Exception docs/research/technology/

Le dossier non suivi `docs/research/technology/` est preexistant, hors perimetre et reste intact. Il n'est pas un produit de ce test.

## 4. Verification copie C1J

La copie jetable C1J a ete verifiee avant le test : 28 controles sur 28 reussis, 964 fichiers, aucun dossier `.git` et aucun identifiant de fichier distant. Les rapports C1J et leur manifeste restent inchanges.

## 5. Verification playset

Le playset confirme contenait uniquement `1776_Age_of_Revolutions_sepoy_test`. Le fork principal n'a pas ete charge comme second mod.

## 6. Baseline logs

Les empreintes et dates des logs precedents ont ete relevees avant la session. Les logs finaux sont plus recents et leurs empreintes ont change, ce qui confirme qu'ils correspondent a la session B-1.

## 7. Fiche operateur unique fournie

Le protocole operateur B-1 a ete suivi : nouvelle partie BIC, preparation B-1, sauvegarde pre-option immuable, ouverture manuelle de l'evenement reel, choix exclusif de l'option 2.b, controle territorial, sauvegarde post-option et fermeture complete du jeu.

## 8. Nombre ouvertures

Une seule ouverture de Victoria 3 a ete necessaire pour la session B-1.

## 9. Nombre fermetures

Une seule fermeture complete et propre a termine la session.

## 10. Justification ouverture supplementaire

Aucune ouverture supplementaire n'a ete effectuee ni necessaire.

## 11. Nouvelle partie BIC

Le test a utilise une nouvelle partie jouee avec BIC. Aucune sauvegarde A-1, A-2 ou A-3 n'a ete reutilisee.

## 12. West Bengal initial

Avant l'option 2.b, la portion BIC de `STATE_WEST_BENGAL` appartenait bien a BIC et comptait environ 17,2 millions d'habitants.

## 13. East Bengal initial

Avant l'option 2.b, la portion BIC de `STATE_EAST_BENGAL` appartenait bien a BIC et comptait environ 21,5 millions d'habitants.

## 14. Autres temoins initiaux

- `STATE_BIHAR` : BIC, environ 12,2 millions d'habitants.
- `STATE_AWADH` : partage entre AWA et BIC.
- `STATE_BUNDELKHAND` : partage entre MARATH et BIC.
- `STATE_NORTHERN_CIRCARS` : partage entre BIC et JEY.
- `STATE_PEGU` : partage entre BUR, BIC et DEN.

## 15. COO/JEY initiaux

COO et JEY etaient des sujets de BIC avant l'evenement.

## 16. Baseline radicaux

Le compteur national affichait zero radical au debut de la partie.

## 17. Preparation B1

La decision de preparation B-1 a ete executee. Elle n'avait pas vocation a changer les proprietaires et a seulement arme le scenario jetable.

## 18. Absence mutation

Aucune mutation territoriale n'a ete observee pendant la preparation B-1. La carte est restee identique jusqu'a l'ouverture de l'evenement reel.

## 19. Sauvegarde pre-option

`HOTFIX_5C2E4C1K_B1_PRE_OPTION_1776_01_01.v3` a ete creee avant le choix destructif.

- Taille : 7 901 193 octets.
- SHA-256 : `19ED98D357672806DFF4B9204E2A1D2DCCC859AD99A468509E57F0B5FBC19BB9`.

## 20. Ouverture event manuelle

`sepoy_mutiny_events.2` a ete ouvert manuellement par la decision B-1 du harnais.

## 21. Selection exclusive 2.b

Seule l'option 2.b, « Le fort William doit tenir bon », a ete selectionnee. Les options 2.a et 2.c n'ont pas ete utilisees.

## 22. Terminaison boucle

La redistribution s'est terminee normalement. Aucun gel, crash, blocage ou boucle infinie n'a ete observe.

## 23. Pays joue final

Le pays joue reste BIC apres l'option 2.b.

## 24. Existence/territoire final BIC

BIC existe toujours, mais ne conserve plus son noyau indien. Sa seule possession clairement constatee est une petite portion insulaire de `STATE_PEGU`.

## 25. West Bengal apres

La portion BIC de `STATE_WEST_BENGAL` a ete transferee a COO. BIC ne conserve aucune portion du Bengale occidental.

## 26. East Bengal apres

La portion BIC de `STATE_EAST_BENGAL` a ete transferee a COO. BIC ne conserve aucune portion du Bengale oriental.

## 27. Bihar apres

`STATE_BIHAR`, initialement BIC, appartient a NAG apres la redistribution.

## 28. Awadh apres

La portion BIC de `STATE_AWADH` revient a AWA.

## 29. Bundelkhand apres

La portion BIC de `STATE_BUNDELKHAND` revient a MARATH.

## 30. Circars apres

La portion BIC de `STATE_NORTHERN_CIRCARS` revient a HYD. La portion JEY reste a JEY.

## 31. Pegu apres

La majeure partie de la portion BIC de `STATE_PEGU` revient a BUR, mais une petite portion BIC subsiste. Le state reste partage entre BUR, BIC et DEN.

## 32. Reprises prioritaires

Les reprises de l'Awadh, du Bundelkhand, du Bihar et des Circars correspondent aux receveurs historiques ou voisins attendus. La branche prioritaire de Pegu n'absorbe toutefois pas toutes les provinces BIC.

## 33. Redistribution generique

Le bloc generique redistribue les states BIC restants aux pays sud-asiatiques voisins. Faute de protection explicite du noyau bengali dans l'option 2.b, il transfere egalement les deux Bengales a COO.

## 34. COO final

COO devient independant, conserve son territoire initial et recoit les portions BIC de West Bengal et East Bengal. Une exemption de service militaire avec GBR reste visible.

## 35. JEY final

JEY devient independant et conserve sa portion des Circars septentrionaux. Une exemption de service militaire avec GBR reste visible.

## 36. Noyau bengali

Le noyau bengali de BIC est entierement perdu. C'est la cause directe du verdict `FAIL_B1_BENGAL_CORE_LOST`.

## 37. Radicaux hindous

L'interface de l'option annonce une hausse de 10 % des radicaux hindous dans les states vises. Aucun radical n'apparait parce que la baseline vaut zero.

## 38. Radicaux sunnites

Le meme constat vaut pour les radicaux sunnites : une augmentation proportionnelle appliquee a zero reste egale a zero.

## 39. Portee regionale radicaux

Le tooltip cite notamment East Bengal, West Bengal, Bihar, la portion BIC de Bundelkhand et la portion BIC d'Awadh. La portee semble regionale, mais l'effet quantitatif ne peut pas etre valide avec cette baseline.

## 40. Owner nul/incoherent

Aucun owner nul, state sans proprietaire ou double attribution incoherente n'a ete observe dans les controles visuels.

## 41. Fraicheur logs

Logs frais de la session :

| Fichier | Taille | Derniere ecriture UTC | SHA-256 |
|---|---:|---|---|
| `error.log` | 76 069 | 2026-07-17 21:43:39 | `F544FD1C72DFDB9F27A40E4E2B91699FC9C9F7ED80BE1E8A5E07E3BF9AEFA16F` |
| `game.log` | 417 684 | 2026-07-17 21:43:39 | `38CBB73EFFDC330E93FA2EC737BBA641011969C4C956195C72BCDC365A1FDFB2` |
| `debug.log` | 412 051 | 2026-07-17 21:43:46 | `FD805F77BE23EE391574B0C67CE2A4AD1EE99A5B485DD339E39AC6289F1D7C7E` |

## 42. Analyse ciblee B1

Le log frais contient zero occurrence de `zz_sepoy_test_b1`, `sepoy_mutiny_events.2`, des sept state IDs controles et de `set_state_owner`. Il n'indique donc aucune erreur runtime ciblee B-1.

## 43. Diagnostics globaux hors perimetre

- 50 erreurs d'identifiant `sr` subsistent hors perimetre.
- Zero occurrence de `01_natural_borders_of_france.txt` et de `00_landowners.txt:459` dans ce log frais.
- Un warning `Unknown tooltip type` est present et non bloquant.
- Zero `Unexpected token`.

Ces diagnostics ne changent pas le verdict territorial B-1.

## 44. Integrite save

La sauvegarde post-option `HOTFIX_5C2E4C1K_B1_POST_OPTION_1776_01_01.v3` existe et est distincte de la baseline.

- Taille : 7 929 333 octets.
- SHA-256 : `4A07D59D0822605B57C344534F87B901BD5AC5EE9DE0DE1C3FC232647EAE2231`.

## 45. Integrite fichiers

Les fichiers Sepoy du fork et tous les fichiers du harnais sont inchanges par cette phase de documentation.

## 46. Resume CSV

Le CSV associe chaque checkpoint aux owners avant/apres, a la classe de redistribution, au statut des sujets, aux radicaux, a la terminaison de boucle et aux preuves runtime.

## 47. Verdict

**`FAIL_B1_BENGAL_CORE_LOST`**

## 48. Valide

- Le harnais B-1 se charge et prepare le test sans mutation.
- L'evenement reel s'ouvre manuellement.
- L'option 2.b se termine sans crash ni boucle.
- Les reprises historiques prioritaires principales fonctionnent.
- Aucun owner nul n'est visible.
- Les logs ne contiennent aucune erreur ciblee B-1.

## 49. Non valide

- BIC ne conserve ni West Bengal ni East Bengal.
- La survie de BIC sur une minuscule portion de Pegu ne satisfait pas l'intention « retraite vers le Bengale ».
- L'effet sur les radicaux ne peut pas etre confirme avec une baseline nulle.

## 50. Recommandation

Corriger dans une phase separee et minimale la selection territoriale de l'option 2.b afin de proteger explicitement le noyau bengali de BIC avant la redistribution generique. Refaire ensuite B-1 avec une baseline comportant des radicaux non nuls pour valider l'effet proportionnel.

## 51. Fichiers crees

- `docs/reports/hotfix/HOTFIX_5C2E4C1K_SEPOY_B1_RUNTIME_TEST.md`
- `docs/reports/hotfix/HOTFIX_5C2E4C1K_B1_RUNTIME_RESULTS.csv`

## 52. Aucun gameplay/harnais modifie

Cette phase ne modifie aucun fichier gameplay du fork et aucun fichier du harnais jetable.

## 53. docs/research intact

`docs/research/technology/` reste intact et hors perimetre.

## 54. Stash MARATH intact

`stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla` est toujours present et n'a pas ete applique, modifie ou supprime.
