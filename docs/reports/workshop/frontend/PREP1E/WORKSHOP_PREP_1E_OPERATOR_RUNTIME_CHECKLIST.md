# FICHE OPÉRATEUR — WORKSHOP_PREP_1E

## Règle absolue

Cette phase autorise **un seul lancement humain de Victoria 3**.

- Ne relance pas le jeu si un contrôle échoue ou est oublié.
- Ne change aucun fichier ni réglage du mod pendant la session.
- Note simplement `PASS`, `FAIL` ou `NOT_REQUIRED` et ton observation.
- À la fin, ferme Victoria 3 et le launcher Paradox, puis préviens Codex.

Compteur au départ : `0 / 1`

## 1 — Chargement et menu principal

Lance le jeu une seule fois avec le fork actif.

- [y] `TRAFALGAR_LOADING_SCREEN = PASS` — le tableau et son cadrage restent corrects.
- [y] `DELAWARE_FRONTEND = PASS` — Washington reste dégagé du panneau.
- [y] `CANTUS_FIRMUS_STARTS = PASS` — Cantus Firmus démarre lorsque le menu apparaît.

Il n’est pas nécessaire d’attendre 150 secondes.

Observation :

`tous est en ordre`

## 2 — Contrôle obligatoire BEO

Ouvre `Nouvelle partie` → `Apprendre à jouer`.

- [y] Les recommandations sont exactement : Suède, Belgique, Đại Nam, Danemark–Norvège.
- [y] `BEO_BASE_FLAG_VISIBLE = yes`.
- [y] `BEO_BASE_FLAG_NOT_BLANK = yes`.
- [y] Le drapeau BEO montre une identité autrichienne/brabançonne cohérente avec les Pays-Bas autrichiens de 1776, et non le tricolore belge moderne.
- [y] `BEO_BASE_COA_RUNTIME = PASS`.

Observation BEO :

`le drapeau des belge autrichien est bien present`

## 3 — Non-régression du tutoriel

- [y] L’introduction enrichie est affichée en français.
- [y] Les quatre descriptions sont complètes et lisibles.
- [y] Le texte de BEO présente bien les Pays-Bas autrichiens.
- [y] `NO_RAW_KEYS = PASS`.
- [y] `NO_MAJOR_OVERFLOW = PASS`.

Observation :

`RAS`

## 4 — Non-régression rapide des objectifs

Ouvre brièvement les objectifs concernés.

- [y] `BIC_FLAG_REMAINS_PASS` — enseigne rayée de la Compagnie, sans étoile du Raj.
- [y] `VOC_FLAG_REMAINS_PASS` — drapeau portant les lettres VOC.
- [y] `FRA_BOURBON_FLAG_REMAINS_PASS` — étendard royal bourbonien.
- [y] Les quatre tableaux personnalisés restent présents : chasse au lion, bataille d’Ouessant, Bastille et Venise.

Observation :

`RAS`

## 5 — Entrée en jeu facultative

Si cela reste immédiat, sélectionne un pays et entre rapidement en partie. Sinon indique `NOT_REQUIRED`.

- [Pass] `GAME_ENTRY_SMOKE = PASS | NOT_REQUIRED | FAIL`.
- [y] Aucun crash.

Pays/date éventuels : `j'ai pris la bic en revanche son drapeau ne correspond pas à ce qui est montrer dans les objectif pareil pour les treize colonie (capture jointe)`

## 6 — Fermeture obligatoire

- [y] Quitter Victoria 3.
- [y] Fermer complètement le launcher Paradox.
- [y] Ne pas relancer le jeu.
- [y] Informer Codex que les deux sont fermés.

Compteur final obligatoire : `1 / 1`

## Bloc à transmettre à Codex

```text
PREP1E lancement humain : 1/1
Trafalgar : PASS/FAIL
Delaware : PASS/FAIL
Cantus Firmus démarre : PASS/FAIL
Tutoriel SWE/BEO/DAI/DENNOR : PASS/FAIL
Drapeau BEO visible : OUI/NON
Drapeau BEO non blanc : OUI/NON
Drapeau BEO approprié à 1776 : OUI/NON
Textes du tutoriel : PASS/FAIL
Clés brutes : OUI/NON
Débordement important : OUI/NON
BIC : PASS/FAIL
VOC : PASS/FAIL
France Bourbon : PASS/FAIL
Quatre tableaux : PASS/FAIL
Entrée en jeu : PASS/NOT_REQUIRED/FAIL
Crash : OUI/NON
Jeu fermé : OUI/NON
Launcher fermé : OUI/NON
Autres observations : ...
```
