# BALKANS-04 — Contrôles exécutés

Résultat propre : 107/107, détails dans VALIDATION.json. Pas de moteur.

| Domaine | Vérification | Limite |
| --- | --- | --- |
| Mutations ciblées | Six fichiers fonctionnels reconstruits exactement ; extérieur des régions ciblées identique | Le parseur n'est pas le chargeur natif |
| Géométrie | 41 pixels autorisés, cinq RGB uniques, terrains hérités, deux pixels connexes par poste et île entière de 33 pixels | Huit pixels sont des noyaux politiques, pas un cadastre |
| Mer et arrière-pays | Tous les pixels anciens hors masques identiques, accès côtier vérifié, continent de Cérigo conservé | Navigation et rendu à tester |
| POPs | Totaux locaux/mondial et profils culture/religion/profession conservés, 13 700 réaffectés | Calibrations historiques signalées |
| Institutions | Aucun changement de loi, souverain, armée ou pacte ; VEN existant seulement | Titulaires locaux et autonomie fine non simulés |
| Économie et technologies | Quatre mouillages, un fort ; PM et gates résolus ; 27 technologies à prérequis fermés | Qualifications, marché, budget et hubs minoritaires non testés |
| Non-régression | Cyclades, pixels RAG/Neum/Sutorina, reçus B03 et archives précédentes ; 2521 fichiers protégés | Les autres mécaniques ne sont pas réauditées |
| SERG | 922 preuves identiques et 5 mises à jour externes documentées ; ni écriture réservée ni suivi écrit par B04 | Aucun reçu joueur WORLD ajouté |

Commande de lecture reproductible : `python tools/world1776_balkans04.py --validate`. `--apply` et `--extend-kythera` sont des installations uniques et refusent un second passage. Le contrôle ne réécrit aucun ancien reçu B01/B02/B03.
