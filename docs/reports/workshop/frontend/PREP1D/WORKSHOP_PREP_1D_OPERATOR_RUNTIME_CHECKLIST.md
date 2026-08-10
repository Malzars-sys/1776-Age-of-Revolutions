# FICHE OPÉRATEUR — WORKSHOP_PREP_1D

## Règle absolue

Cette phase autorise **un seul lancement humain de Victoria 3**.

- Ne relance pas le jeu, même si un contrôle échoue ou est oublié.
- Ne change aucun fichier ni réglage du mod pendant la session.
- En cas d’échec, note simplement `FAIL` et ce que tu as vu ou entendu.
- À la fin, ferme le jeu **et** le launcher Paradox, puis préviens Codex.

Compteur au départ : `0 / 1`

## Avant de lancer

- [y] Le launcher et Victoria 3 sont fermés.
- [y] Le bon playset contient `1776 - Age of Revolutions`.
- [y] Aucun autre mod non prévu n’a été ajouté.
- [y] Un chronomètre est prêt.
- [y] La langue du jeu est le français.

## 1 — Lancement et écran de chargement

Lance le jeu une seule fois.

- [y] `TRAFALGAR_LOADING_SCREEN = PASS` — le tableau de Trafalgar apparaît avec un cadrage correct et les logos officiels.

Observation ou anomalie :

`aucune anomalie observé durant l'ecran de chargement`

## 2 — Menu principal et musique

Dès l’apparition du menu principal, démarre le chronomètre et ne quitte pas le menu avant **150 secondes**.

- [y] `DELAWARE_MAIN_MENU = PASS` — Washington n’est pas masqué par le panneau du menu.
- [y] `AGE_OF_REVOLUTION_SUBTITLE = PASS` — le sous-titre est blanc pur.
- [y] `CANTUS_FIRMUS_MENU_MASTER_STARTS = PASS` — Cantus Firmus commence bien.
- [y] `CANTUS_FIRMUS_DOES_NOT_END_AFTER_100_SECONDS = PASS` — le morceau continue au-delà de 100.301 secondes.
- [y] `CANTUS_FIRMUS_NO_DLC_THEME_TAKEOVER = PASS` — aucune musique vanilla ou DLC ne prend le relais.
- [y] Pas de silence anormal, chevauchement ou double musique.

Durée réellement observée : `3 minutes 20 secondes`

Observation ou anomalie :

`aucun anomalie detecté su le menue principale`

## 3 — Bataille pour l’Inde

Ouvre `Nouvelle partie` puis `Bataille pour l’Inde`.

- [y] `BATTLE_FOR_INDIA_ART = PASS` — tableau de chasse au lion, sans photographie moderne.
- [?] `BIC_OBJECTIVE_FLAG_RUNTIME = PASS` — enseigne rayée de la Compagnie britannique des Indes, sans étoile du Raj.
- [y] `VOC_OBJECTIVE_FLAG_RUNTIME = PASS` — drapeau portant les lettres VOC, sans simple tricolore néerlandais.
- [y] Introduction française visible et lisible.
- [y] Descriptions BIC et DEI visibles, sans clé brute ni anglais.
- [y] Pas de débordement visuel majeur.

Observation ou anomalie :

`je ne sais juste pas si c'est le bon drapeau pour la bic j'ai normalement join une image `

## 4 — Apprendre à jouer

Ouvre `Apprendre à jouer`.

Les quatre recommandations doivent être exactement :

- [y] Suède (`SWE`)
- [y] Belgique (`BEO`)
- [y] Đại Nam (`DAI`)
- [y] Danemark–Norvège (`DENNOR`)

Puis contrôle :

- [y] `TUTORIAL_RECOMMENDED_COUNTRIES_RUNTIME = PASS`
- [y] L’introduction enrichie est affichée en français.
- [y] La description de la Suède est complète et lisible.
- [y] La Belgique est présentée comme les Pays-Bas autrichiens et son texte est lisible.
- [y] La description du Đại Nam est complète et lisible.
- [y] La description du Danemark–Norvège est complète et lisible.
- [y] Aucun texte anglais, aucune clé brute, aucune troncature problématique.

Observation ou anomalie :

`la belgique à un drapeau blanc j'ai join une captur normalement`

## 5 — Contrôle rapide des autres objectifs

### Âge des Révolutions

- [y] Tableau de la Bastille correct et sans cadre physique.
- [y] France : étendard royal bourbonien.
- [y] Treize Colonies : treize étoiles et treize bandes.
- [y] République des Deux Nations : drapeau du Commonwealth.
- [y] Introduction et descriptions échantillonnées lisibles.

### Rivalités impériales

- [y] Tableau de la bataille d’Ouessant correct.
- [y] Grande-Bretagne : Union Flag d’époque.
- [y] Espagne : croix de Bourgogne.
- [y] Russie : aigle impérial.
- [y] Prusse : aigle prussien.
- [y] Introduction et descriptions échantillonnées lisibles.

### Républiques marchandes

- [y] Tableau de Venise correct et sans cadre physique.
- [y] Textes de Venise et de Gênes visibles et lisibles.

Verdict global :

- [?] `OBJECTIVE_PERIOD_FLAGS_RUNTIME = PASS`
- [y] `OBJECTIVE_TEXTS_RUNTIME = PASS`
- [y] `NO_RAW_KEYS = PASS`
- [y] `NO_MAJOR_TEXT_OVERFLOW = PASS`

Observation ou anomalie :

`tous est bon à par le drapeau montré de la belgique et mon doute sur la veracité du drapeau de la bic montré`

## 6 — Entrée en jeu

Depuis un objectif, sélectionne un pays recommandé et commence la partie. Laisse passer plusieurs jours.

- [y] `GAME_ENTRY = PASS`
- [y] `FRONTEND_MUSIC_STOPS_OR_TRANSITIONS = PASS`
- [y] `NO_DOUBLE_MUSIC = PASS`
- [y] `NO_CRASH = PASS`

Pays choisi : `france`

Date atteinte : `17 janvier 1776`

Observation ou anomalie :

`aucune anomalie detecté`

## 7 — Fermeture obligatoire

- [y] Quitter Victoria 3.
- [y] Fermer complètement le launcher Paradox.
- [y] Ne pas relancer le jeu.
- [y] Informer Codex que le jeu et le launcher sont fermés.

Compteur final obligatoire : `1 / 1`

## Compte rendu à transmettre à Codex

Copie ce bloc dans ton message et complète-le :

```text
PREP1D lancement humain : 1/1
Observation musique au menu : ... secondes
Cantus Firmus après 100 secondes : PASS/FAIL
Reprise par une musique vanilla/DLC : OUI/NON
BIC enseigne de la Compagnie : PASS/FAIL
DEI drapeau VOC : PASS/FAIL
Tutoriel SWE/BEO/DAI/DENNOR : PASS/FAIL
Textes du tutoriel : PASS/FAIL
Visuels des quatre objectifs : PASS/FAIL
Drapeaux principaux : PASS/FAIL
Clés brutes ou anglais inattendu : OUI/NON
Débordement important : OUI/NON
Entrée en jeu : PASS/FAIL
Transition musique menu → partie : PASS/FAIL
Double musique : OUI/NON
Date atteinte : ...
Crash : OUI/NON
Jeu fermé : OUI/NON
Launcher fermé : OUI/NON
Autres observations : ...
```
