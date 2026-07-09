# Phase NAVY-1A-sexies - Russian Admirals 1776

## 1. Resume de la phase

Cette phase ajoute des amiraux historiques ou plausibles a la flotte russe initiale de 1776.

Fichiers modifies ou crees :

- `common/history/military_formations/00_military_formations_europe.txt`
- `localization/english/phase_navy_1a_russian_admirals_l_english.yml`
- `localization/french/phase_navy_1a_russian_admirals_l_french.yml`
- `PHASE_NAVY_1A_SEXIES_RUSSIAN_ADMIRALS.md`

La phase ne modifie aucun `count`, aucun `hq_region` et aucun `ship_type`.

## 2. Probleme observe en jeu

Les flottes russes existent apres NAVY-1A-quinquies, mais elles n'ont pas d'amiral historique assigne. La flotte affiche donc `Recruter un amiral`.

## 3. Flottes russes ciblees

| Pays | Flotte | Scope | hq_region | Navires |
|---|---|---|---|---|
| RUS | `Baltiyskiy_Flot` | `rus_baltic_fleet` | `sr:region_russia` | 14 vaisseaux de ligne, 9 fregates |
| RUS | `Okhotskaya_Voyennaya_Flotiliya` | `rus_okhotsk_fleet` | `sr:region_northeast_asia` | 1 fregate |

## 4. Syntaxe vanilla confirmee

La vanilla The Great Wave utilise des blocs `create_character` avec les champs suivants :

```txt
create_character = {
	is_admiral = yes
	first_name = ...
	last_name = ...
	historical = yes
	birth_date = ...
	culture = cu:...
	religion = rel:...
	interest_group = ig_armed_forces
	ideology = ...
	commander_rank = default
	traits = {
		...
	}
	save_scope_as = ...
}
scope:... = {
	transfer_to_formation = scope:...
}
```

La methode reutilisee est celle de NAVY-1A-quater : noms fixes via cles `navy_*` localisees.

## 5. Amiraux retenus

Trois amiraux sont retenus pour `Baltiyskiy_Flot` :

- Vasily Yakovlevich Chichagov ;
- Samuil Karlovich Greig ;
- Alexei Naumovich Senyavin.

Ils sont tous transferes vers `scope:rus_baltic_fleet`.

## 6. Amiraux examines mais non retenus

| Nom | Decision | Raison |
|---|---|---|
| Grigory Andreyevich Spiridov | Non retenu | Grand amiral de Tchesme, mais probablement retire de la marine active en 1774. |
| Alexei Grigoryevich Orlov | Non retenu | Figure politique et militaire majeure de Tchesme, mais pas un amiral professionnel classique. |
| Fyodor Ushakov | Non retenu | Futur grand amiral, mais encore trop jeune et pas commandant principal de flotte en 1776. |
| Commandant local d'Okhotsk | Non retenu | Aucun nom local assez solide n'a ete identifie pour justifier une fiche historique. |

## 7. Fiches individuelles

### Vasily Yakovlevich Chichagov

- Pays : RUS
- Flotte : `Baltiyskiy_Flot`
- Cles : `navy_vasily_yakovlevich` / `navy_chichagov`
- Naissance : `1726.3.11`
- Age au 1 janvier 1776 : 49
- Culture : `cu:russian`
- Religion : `rel:orthodox`
- IG : `ig_armed_forces`
- Ideologie : `ideology_moderate`
- Rang : `commander_rank = default`
- Traits : `experienced_naval_commander`, `cautious`
- Role : commandant naval russe senior, bon profil de chef prudent et organisateur pour la Baltique.
- Confiance historique : haute.

### Samuil Karlovich Greig

- Pays : RUS
- Flotte : `Baltiyskiy_Flot`
- Cles : `navy_samuil_karlovich` / `navy_greig`
- Naissance : `1735.11.30`
- Age au 1 janvier 1776 : 40
- Culture : `cu:scottish`
- Religion : `rel:protestant`
- IG : `ig_armed_forces`
- Ideologie : `ideology_moderate`
- Rang : `commander_rank = default`
- Traits : `experienced_naval_commander`, `brave`
- Role : officier ecossais au service russe, actif et coherent avec la tradition d'officiers etrangers dans la marine imperiale russe.
- Confiance historique : haute.

### Alexei Naumovich Senyavin

- Pays : RUS
- Flotte : `Baltiyskiy_Flot`
- Cles : `navy_alexei_naumovich` / `navy_senyavin`
- Naissance : `1716.10.5`
- Age au 1 janvier 1776 : 59
- Culture : `cu:russian`
- Religion : `rel:orthodox`
- IG : `ig_armed_forces`
- Ideologie : `ideology_royalist`
- Rang : `commander_rank = default`
- Traits : `experienced_naval_commander`, `cautious`
- Role : veteran naval russe lie aux operations russo-turques et aux flottilles d'Azov/Don, utilise ici comme officier senior sans creer de flotte de mer Noire.
- Confiance historique : moyenne a haute.

## 8. Tableau synthetique

| Pays | Flotte | Amiral | Naissance | Age 1776 | Culture | Religion | IG | Ideologie | Traits | Confiance |
|---|---|---|---:|---:|---|---|---|---|---|---|
| RUS | Baltiyskiy_Flot | Vasily Yakovlevich Chichagov | 1726.3.11 | 49 | cu:russian | rel:orthodox | ig_armed_forces | ideology_moderate | experienced_naval_commander, cautious | Haute |
| RUS | Baltiyskiy_Flot | Samuil Karlovich Greig | 1735.11.30 | 40 | cu:scottish | rel:protestant | ig_armed_forces | ideology_moderate | experienced_naval_commander, brave | Haute |
| RUS | Baltiyskiy_Flot | Alexei Naumovich Senyavin | 1716.10.5 | 59 | cu:russian | rel:orthodox | ig_armed_forces | ideology_royalist | experienced_naval_commander, cautious | Moyenne a haute |

## 9. Localisations creees

Fichiers crees :

- `localization/english/phase_navy_1a_russian_admirals_l_english.yml`
- `localization/french/phase_navy_1a_russian_admirals_l_french.yml`

Cles creees :

- `navy_vasily_yakovlevich`
- `navy_chichagov`
- `navy_samuil_karlovich`
- `navy_greig`
- `navy_alexei_naumovich`
- `navy_senyavin`

Le fichier francais a ete reecrit en UTF-8 avec BOM.

## 10. Choix pour Okhotsk

`Okhotskaya_Voyennaya_Flotiliya` reste volontairement sans amiral historique.

Raison : la flottille ne possede qu'une fregate, et aucun commandant local autour de 1776 n'a ete identifie avec assez de confiance pour justifier une fiche. Les grands amiraux russes retenus restent donc rattaches a la flotte principale de Baltique.

## 11. Confirmation des limites

Cette phase n'a pas modifie :

- les `count` de navires ;
- les `hq_region` ;
- les `ship_type` ;
- les batiments ;
- les lois ;
- les technologies ;
- les flottes GB/FRA/SPA ;
- les amiraux GB/FRA/SPA ;
- le Japon, l'Australie, le Moyen-Orient ou les autres pays.

## 12. Tests a refaire en jeu

1. Lancer une nouvelle partie propre en 1776 avec le mod seul.
2. Ouvrir la Russie.
3. Verifier `Baltiyskiy_Flot` :
   - la flotte existe ;
   - elle garde 14 vaisseaux de ligne et 9 fregates ;
   - elle a des amiraux historiques assignes.
4. Verifier `Okhotskaya_Voyennaya_Flotiliya` :
   - la flotte existe ;
   - elle garde 1 fregate ;
   - elle reste sans grand amiral historique, choix volontaire.
5. Verifier qu'il n'y a pas de noms generes absurdes ni de mojibake.
6. Confirmer que GB/FRA/SPA n'ont pas change.
7. Laisser tourner un mois.
8. Surveiller `error.log` et `debug.log` pour `Missing localization`, `Invalid localization`, `create_character`, `admiral`, `fleet`, `hq_region` et `PostValidate`.

## 13. Risques restants

- Le jeu peut afficher les trois amiraux comme commandants actifs de la meme flotte ; c'est coherent avec la methode deja employee pour GB/FRA/SPA, mais a verifier en interface.
- L'absence d'amiral a Okhotsk est volontairement prudente, mais laisse le bouton `Recruter un amiral` sur cette petite flottille.
- Les noms sont romanises en ASCII pour eviter les problemes d'encodage ; une phase ulterieure pourra choisir des formes francaises plus elegantes si le pipeline de localisation est stabilise.
