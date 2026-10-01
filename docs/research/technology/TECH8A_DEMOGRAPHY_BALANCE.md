# Natalité et mortalité — passe de base

Date : 2026-09-27. Les constantes du jeu se trouvent dans `common/defines/00_defines.txt` et les bonus médicaux dans `common/technology/technologies/30_tech3a_society.txt`.

## Références locales consultées

- Morgenröte (`Workshop/529340/2889925770`) applique surtout des modificateurs de mortalité dans ses technologies et événements : sa vaccination contre la variole donne `state_mortality_mult = -0.01`, avec un effet séparé sur la maladie. Aucun remplacement de la courbe générale n'a été trouvé dans ses `common/defines` installés.
- Tech & Res (`Workshop/529340/3472248460`) remplace la courbe : naissance mensuelle minimale/maximale 0,00160/0,00300 et mortalité minimale/maximale 0,00090/0,00400, avec une stabilisation du niveau de vie à 18. Plusieurs technologies médicales donnent chacune environ -1 % de mortalité.
- Le jeu et la version précédente de 1776 utilisaient les bornes naissance 0,00060/0,00450, mortalité 0,00045/0,00550 et le coefficient de mortalité au maximum de croissance 0,35.

## Réglage retenu pour 1776

Naissance minimale/maximale : 0,00110/0,00510 par mois. Mortalité minimale/maximale : 0,00095/0,00620 par mois. Le coefficient de mortalité au maximum de croissance passe à 0,50. Les seuils de niveau de vie 5/10/15/25 restent inchangés.

Projection de la **courbe de base seulement**, sans lois, institutions, maladies, technologies ni événements, exprimée en taux annuels approximatifs (`taux mensuel × 12`) :

| Niveau de vie | Avant : naissances / décès / solde | Maintenant : naissances / décès / solde |
|---:|---:|---:|
| 5 | 5,4 % / 5,4 % / 0 % | 6,1 % / 6,1 % / 0 % |
| 10 | 5,4 % / 3,4 % / +2,0 % | 6,1 % / 4,2 % / +1,9 % |
| 15 | 3,8 % / 1,3 % / +2,5 % | 4,5 % / 2,3 % / +2,3 % |
| 25 | 0,7 % / 0,5 % / +0,2 % | 1,3 % / 1,1 % / +0,2 % |

On relève donc les deux flux sans relever brutalement le solde de croissance. Les technologies ajoutent ensuite des réductions relatives de mortalité : variolisation -1 %, diplômes médicaux -1 %, vaccination -2 %, campagnes vaccinales -3 %, médecine clinicopathologique -2 % et principes actifs -1 %. La vaccination n'affiche ainsi plus « -0 % » par simple arrondi d'interface.

**Validation restant à faire en jeu :** croissance démographique par pays et niveau de vie, conséquences des lois de santé et des épidémies, taille des populations en 1800/1836, et cumul des technologies. Ces projections arithmétiques ne sont pas une simulation de partie.
