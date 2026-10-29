# Reproduire les contrôles

Python du runtime Codex, PYTHONIOENCODING=utf-8 :

`python tools/world1776_nordic01.py --validate`

Ne pas rejouer --survey, --apply ou --tracking. Les préimages sont celles du workspace courant au moment de la mutation, incluant DP-02. Le validateur exige les sorties exactes du manifeste DP-02 archivé ; si elles changent, lire les nouveaux reçus plutôt que désactiver la protection. --inspect est un outil de travail, pas une attestation de rendu moteur.

`world1776_nordic01_closeout.py --evidence --map --reports --final` actualise les preuves dérivées ; cette commande ne lance pas le jeu.
