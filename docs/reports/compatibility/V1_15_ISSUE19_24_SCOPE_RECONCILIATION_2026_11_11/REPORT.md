# Missions 19 et 24 — clarification du suivi, 11 novembre 2026

Le mainteneur a demandé de reprendre les missions 19 et 24, dont les descriptions
paraissaient similaires. Cette passe clarifie le suivi et actualise les preuves
de carte ; elle n'installe aucun changement de gameplay.

| Mission | Rôle conservé |
| --- | --- |
| 19 | Coordination générale du hotfix, priorités, dépendances et clôture globale |
| 24 | Sous-chantier technique carte, États/pays initiaux, démarrage et DLC ; le catalogue de journaux reste délégué à 39 |
| 25 | Validation combinée, intégration et préparation de la distribution |

19 est le dossier parent de coordination ; 24 en couvre une partie concrète.
Les deux ne sont donc pas fermées comme doublons. Les titres et descriptions
des issues ont été modifiés et relus exactement après écriture. Les anciens
textes, installations, critères et preuves restent conservés dans les détails.
Aucune relation parent/enfant effective ni colonne Project n'est revendiquée
éditée : les outils actuels ne fournissent pas ces opérations.

## Listes remises à jour

Les états réels GitHub ont été consultés, plutôt que déduits d'anciens corps
d'issues : 20, 21, 22 et 23 sont fermées ; 24 et 25 restent ouvertes. Les
sous-lots 27, 35, 37, 40, 41, 50, 51 et 53 sont fermés ; 39 reste ouverte.
Les derniers suivis 48 à 53 sont également fermés, malgré des descriptions
conservant des formulations anciennes de revue en attente.

Ces états sont reproduits comme états GitHub. Ils ne créent pas une nouvelle
attestation de test de chaque branche, ni un build, une date simulée ou une
sauvegarde que le mainteneur n'aurait pas fournis. Aucune mission terminée n'est
rouverte et aucune acceptation explicite existante n'est retirée.

## Qualification courante de la carte

L'auditeur existant `issue24_residual_scope_audit.py --self-test` a produit une
nouvelle preuve :

- 13 provinces portent des instructions initiales inconditionnelles de
  propriétaires contradictoires. Aucun gagnant moteur ni propriétaire
  historique n'est choisi par ce lecteur.
- `xEF50C0`, dans Western Micronesia, reste une candidate de province praticable
  sans attribution initiale.
- 646 sélections de capitale sont cohérentes dans le modèle direct : 642
  capitales par défaut et quatre surcharges historiques explicites.
- Aucune erreur de parsing ; huit contrôles de classification réussis.
- Les 753 empreintes d'entrées ont été revérifiées après l'audit : aucune dérive.

Le statut reste **QUALIFIED_STATIC_ONLY**. Ces constats actualisent des
questions déjà connues ; ils ne reproduisent pas treize nouvelles pannes en
jeu et ne certifient pas l'exactitude historique ou l'acceptation globale.
L'arbitrage historique reste lié au chantier 18. Cette passe ne réaffecte
aucune province et ne reprend pas l'implémentation du catalogue 39.

## Suite distinguée

La mission 24 doit conserver une liste bornée des constats techniques,
qualifier les points territoriaux avec les preuves existantes de 18 et
consolider son acceptation, y compris le travail délégué à 39. La mission 25
effectue ensuite la validation combinée et l'intégration applicable. La mission
19 suit ces résultats sans redemander les mêmes corrections et reste ouverte
jusqu'à satisfaction des critères globaux. Aucun critère original n'est retiré
pour augmenter artificiellement la progression.

Les seules écritures de cette passe sont les deux titres/descriptions GitHub et
les preuves de ce dossier. Aucune opération Git d'écriture, aucun lancement
moteur, aucune publication, modification vanilla ou écriture de gameplay.

Preuves : `ISSUE_SNAPSHOTS.json`, `CURRENT_MAP_QUALIFICATION.json`,
`INPUT_HASH_GUARD.json` et `DELIVERY_RECEIPT.json`.
