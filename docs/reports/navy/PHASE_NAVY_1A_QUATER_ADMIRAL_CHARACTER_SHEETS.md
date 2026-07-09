# Phase NAVY-1A-quater - Admiral Character Sheets

## 1. Resume de la phase

Cette phase polit les fiches des amiraux GB/FRA/SPA crees ou corriges pendant NAVY-1A-bis et NAVY-1A-ter.

Objectif applique :

- garder les noms fixes via les cles `navy_*` ;
- ajouter `birth_date` quand la date est connue ou plausible ;
- ajouter `religion` ;
- ajouter `commander_rank = default` ;
- confirmer `interest_group = ig_armed_forces` ;
- utiliser uniquement des ideologies et traits trouves dans la vanilla The Great Wave ;
- corriger Rions en Francois-Hector d'Albert de Rions ;
- stabiliser Cordova sans accent dans les localisations du mod.

## 2. Problemes corriges

- Mojibake Cordova : la localisation francaise utilise maintenant `de Cordova y Cordova`, sans accent, pour eviter `CÃ³rdova` / `CÃƒ`.
- Rions : `navy_jean_baptiste` a ete remplace par `navy_francois_hector`.
- Ages : les blocs utilisent `birth_date`, champ vanilla confirme.
- Traits : maximum deux traits par amiral, uniquement avec des IDs valides.
- Ideologies : uniquement `ideology_moderate`, `ideology_royalist`.
- Groupes d'interet : tous les amiraux ciblés utilisent `ig_armed_forces`.

## 3. Syntaxe vanilla confirmee

La vanilla The Great Wave utilise des fiches de personnages dans `common/character_templates/*` avec des champs comme :

```txt
is_admiral = yes
first_name = "William"
last_name = "Brown"
historical = yes
culture = cu:irish
religion = rel:catholic
commander_rank = default
interest_group = ig_armed_forces
ideology = ideology_moderate
birth_date = 1777.6.22
traits = {
	experienced_naval_commander
}
```

Dans ce mod, les noms restent en cles `navy_*` parce que NAVY-1A-ter a montre que ces cles localisees corrigent l'affichage en jeu.

## 4. Champs utilisables dans une fiche d'amiral

Champs utilises et confirmes par les fichiers vanilla :

- `is_admiral = yes`
- `first_name`
- `last_name`
- `historical = yes`
- `birth_date`
- `culture`
- `religion`
- `interest_group`
- `ideology`
- `commander_rank`
- `traits`
- `save_scope_as`

`birth_date` est donc prefere a `age`.

## 5. Tableau complet

| Pays | Flotte | Amiral | Naissance | Age 1776 | Culture | Religion | IG | Ideologie | Traits | Confiance |
|---|---|---|---:|---:|---|---|---|---|---|---|
| GBR | Portsmouth Station | Augustus Keppel | 1725.4.25 | 50 | cu:british | rel:protestant | ig_armed_forces | ideology_moderate | experienced_naval_commander, cautious | Haute |
| GBR | Portsmouth Station | Peter Parker | 1721.1.1 | 54 | cu:british | rel:protestant | ig_armed_forces | ideology_moderate | experienced_naval_commander, brave | Moyenne |
| GBR | Portsmouth Station | Richard Kempenfelt | 1718.10.1 | 57 | cu:british | rel:protestant | ig_armed_forces | ideology_moderate | experienced_naval_commander, experienced_convoy_raider | Moyenne |
| GBR | Plymouth Station | Samuel Barrington | 1729.2.15 | 46 | cu:british | rel:protestant | ig_armed_forces | ideology_moderate | experienced_naval_commander, brave | Haute |
| GBR | Plymouth Station | Francis Geary | 1709.1.1 | 66 | cu:british | rel:protestant | ig_armed_forces | ideology_royalist | experienced_naval_commander, cautious | Moyenne |
| GBR | Mediterranean Station | Samuel Hood | 1724.12.12 | 51 | cu:british | rel:protestant | ig_armed_forces | ideology_royalist | brave, expert_naval_commander | Haute |
| GBR | North America and West Indies Station | Richard Howe | 1726.3.8 | 49 | cu:british | rel:protestant | ig_armed_forces | ideology_moderate | expert_naval_commander, cautious | Haute |
| GBR | East Indies and China Station | Edward Hughes | 1720.1.1 | 55 | cu:british | rel:protestant | ig_armed_forces | ideology_moderate | experienced_naval_commander, cautious | Moyenne |
| FRA | Escadre du Nord | Louis Guillouet d'Orvilliers | 1710.3.23 | 65 | cu:french | rel:catholic | ig_armed_forces | ideology_royalist | experienced_naval_commander, cautious | Haute |
| FRA | Escadre du Nord | Toussaint-Guillaume Picquet de la Motte | 1720.11.1 | 55 | cu:french | rel:catholic | ig_armed_forces | ideology_royalist | experienced_naval_commander, brave | Haute |
| FRA | Escadre du Nord | Luc Urbain de Guichen | 1712.6.21 | 63 | cu:french | rel:catholic | ig_armed_forces | ideology_royalist | experienced_naval_commander, cautious | Haute |
| FRA | Escadre de la Mediterranee | Pierre Andre de Suffren | 1729.7.17 | 46 | cu:french | rel:catholic | ig_armed_forces | ideology_royalist | expert_naval_commander, brave | Haute |
| FRA | Escadre de la Mediterranee | Francois-Hector d'Albert de Rions | 1728.2.19 | 47 | cu:french | rel:catholic | ig_armed_forces | ideology_moderate | experienced_naval_commander, cautious | Haute |
| FRA | Escadre de la Mediterranee | Charles Hector d'Estaing | 1729.11.24 | 46 | cu:french | rel:catholic | ig_armed_forces | ideology_royalist | experienced_naval_commander, ambitious | Moyenne |
| SPA | Real Armada Espanola | Luis de Cordova y Cordova | 1706.2.8 | 69 | cu:spanish | rel:catholic | ig_armed_forces | ideology_royalist | expert_naval_commander, cautious | Haute |
| SPA | Real Armada Espanola | Antonio de Ulloa | 1716.1.12 | 59 | cu:spanish | rel:catholic | ig_armed_forces | ideology_moderate | experienced_naval_commander, cautious | Moyenne |

## 6. Fiches individuelles

### Augustus Keppel

Amiral britannique plausible pour Portsmouth en 1776. Fiche prudente : commandant naval experimente, pas surpuissant.

### Peter Parker

Officier britannique actif dans le contexte americain. Date mensuelle inconnue dans cette phase, donc `1721.1.1` est utilise comme approximation technique.

### Richard Kempenfelt

Officier metropolitain competent. Le trait `experienced_convoy_raider` sert d'equivalent naval tactique valide.

### Samuel Barrington

Commandant britannique solide pour Plymouth. Traits : experience navale et bravoure.

### Francis Geary

Officier plus age, volontairement limite par `cautious`.

### Samuel Hood

Amiral majeur britannique. `expert_naval_commander` et `brave` sont assumes.

### Richard Howe

Choix fort pour North America and West Indies. `cautious` represente un profil naval methodique.

### Edward Hughes

Date de naissance conservee comme approximation `1720.1.1`, car les sources peuvent diverger. Profil limite a `experienced_naval_commander`.

### Louis Guillouet d'Orvilliers

Commandant francais senior et coherent pour l'Escadre du Nord.

### Toussaint-Guillaume Picquet de la Motte

Officier francais actif et plausible, avec `brave`.

### Luc Urbain de Guichen

Officier senior francais, profil prudent.

### Pierre Andre de Suffren

Amiral francais majeur ; le profil fort est assume avec `expert_naval_commander` et `brave`.

### Francois-Hector d'Albert de Rions

Corrige l'ancien affichage Jean-Baptiste. Profil experimente et prudent.

### Charles Hector d'Estaing

Profil royaliste et ambitieux, sans monter au niveau expert pour garder l'equilibre.

### Luis de Cordova y Cordova

Senior espagnol, profil expert mais prudent. Localisation stabilisee sans accents.

### Antonio de Ulloa

Officier savant et administrateur, mais traits conservateurs faute de trait scientifique naval garanti.

## 7. IDs de traits utilises

Tous trouves dans la vanilla The Great Wave :

- `experienced_naval_commander`
- `expert_naval_commander`
- `experienced_convoy_raider`
- `brave`
- `cautious`
- `ambitious`

## 8. IDs d'ideologies utilises

Tous trouves dans la vanilla The Great Wave :

- `ideology_moderate`
- `ideology_royalist`

## 9. Localisations modifiees

Fichiers modifies :

- `localization/english/phase_navy_1a_admirals_l_english.yml`
- `localization/french/phase_navy_1a_admirals_l_french.yml`

Corrections :

- `navy_jean_baptiste` remplace par `navy_francois_hector`.
- `navy_de_cordova_y_cordova` en francais vaut maintenant `de Cordova y Cordova`.

Le fichier francais a ete verifie en UTF-8 BOM.

## 10. Liens Wikipedia

Demande additionnelle : ajouter des liens vers les pages Wikipedia anglaises des amiraux, comme pour certains personnages historiques majeurs.

Resultat de l'audit local :

- aucune syntaxe `wikipedia`, `wikipedia_url`, `url`, `external_link` ou equivalente n'a ete trouvee dans les fichiers vanilla `common/history` ou `common/character_templates` ;
- la recherche globale vanilla ne montre pas de champ scriptable clair pour associer une URL a une fiche de personnage ;
- aucun champ non documente n'a donc ete ajoute, afin d'eviter des erreurs `create_character` ou `PostValidate`.

URLs anglaises verifiees et gardees pour reference future si un champ compatible est trouve :

- Augustus Keppel : https://en.wikipedia.org/wiki/Augustus_Keppel,_1st_Viscount_Keppel
- Peter Parker : https://en.wikipedia.org/wiki/Sir_Peter_Parker,_1st_Baronet
- Richard Kempenfelt : https://en.wikipedia.org/wiki/Richard_Kempenfelt
- Samuel Barrington : https://en.wikipedia.org/wiki/Samuel_Barrington
- Francis Geary : https://en.wikipedia.org/wiki/Francis_Geary
- Samuel Hood : https://en.wikipedia.org/wiki/Samuel_Hood,_1st_Viscount_Hood
- Richard Howe : https://en.wikipedia.org/wiki/Richard_Howe,_1st_Earl_Howe
- Edward Hughes : https://en.wikipedia.org/wiki/Edward_Hughes_(Royal_Navy_officer)
- Louis Guillouet d'Orvilliers : https://en.wikipedia.org/wiki/Louis_Guillouet,_comte_d%27Orvilliers
- Toussaint-Guillaume Picquet de la Motte : https://en.wikipedia.org/wiki/Toussaint-Guillaume_Picquet_de_la_Motte
- Luc Urbain de Guichen : https://en.wikipedia.org/wiki/Luc_Urbain_de_Bou%C3%ABxic,_comte_de_Guichen
- Pierre Andre de Suffren : https://en.wikipedia.org/wiki/Pierre_Andr%C3%A9_de_Suffren
- Francois-Hector d'Albert de Rions : https://en.wikipedia.org/wiki/Fran%C3%A7ois_Hector_d%27Albert_de_Rions
- Charles Hector d'Estaing : https://en.wikipedia.org/wiki/Charles_Hector,_comte_d%27Estaing
- Luis de Cordova y Cordova : https://en.wikipedia.org/wiki/Luis_de_C%C3%B3rdova_y_C%C3%B3rdova
- Antonio de Ulloa : https://en.wikipedia.org/wiki/Antonio_de_Ulloa

## 11. Confirmation des limites

Cette phase n'a pas modifie :

- les `count` de navires ;
- les `hq_region` ;
- les `ship_type` ;
- les noms de flottes ;
- les batiments ;
- les lois ;
- les technologies ;
- les flottes hors GB/FRA/SPA.

## 12. Tests a refaire en jeu

1. Lancer une nouvelle partie propre en 1776.
2. Verifier les flottes GB/FRA/SPA.
3. Confirmer que les noms historiques apparaissent toujours.
4. Confirmer que Luis de Cordova y Cordova n'a plus de mojibake.
5. Confirmer que Francois-Hector d'Albert de Rions apparait.
6. Verifier que les ages sont plausibles.
7. Verifier que les groupes d'interet sont les Forces armees.
8. Verifier que les traits sont coherents.
9. Verifier que les navires restent inchanges :
   - GB : 28 navires de ligne / 28 fregates.
   - France : 18 navires de ligne / 16 fregates.
   - Espagne : 15 navires de ligne / 14 fregates.
10. Laisser tourner un mois.
11. Verifier `error.log` et `debug.log` pour `Missing localization`, `Invalid localization`, `create_character`, `admiral`, `fleet`, `PostValidate`.
