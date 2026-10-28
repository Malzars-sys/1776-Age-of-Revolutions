# Reproduction en lecture seule

Depuis le dépôt avec Python configuré :

`python tools/world1776_interior01.py --tech --validate`

`python tools/world1776_interior01_closeout.py --final`

Ne pas relancer --apply, --tracking ni le survey initial. Les entrées et reçus archivés ne sont pas une baseline à réinstaller. Un changement concurrent doit être rapproché de sa preuve, jamais annulé pour satisfaire un test. --evidence régénère uniquement cartes, correspondances et bilans dans le dossier du lot ; --reports écrit ses rapports. Ces commandes ne lancent pas le moteur. Les reçus historiques des autres lots restent des preuves de leur version passée.
