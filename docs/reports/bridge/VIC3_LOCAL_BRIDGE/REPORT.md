# Pont local Victoria 3 — livraison v0.1.0

> **Validation visuelle manuelle reçue le 16 octobre** : le joueur confirme
> l'apparition des rails puis fournit une capture après retrait où les tronçons
> inspectés ont disparu. Reçu séparé dans le prototype :
> `RUNTIME_USER_VISUAL_VALIDATION_2026_10_16.json`. Cette preuve humaine complète
> les diagnostics 0 → 1 → 0 ; le pont n'a pas analysé le rendu automatiquement.

> Séquence complète observée : **témoin 0 → 1 → 0**, retour au mode automatique,
> 17 niveaux régionaux et PM inchangés. Voir `RUNTIME_AUTO_RETURN_2026_10_16`.
> Onze nouveaux blocs complets le montrent ; un bloc ultérieur reste partiel.
> Ce résultat constate la transition, pas un état live ni le rendu des rails.

> Test suivant : le forçage annoncé par le joueur produit un **nouveau relevé
> après curseur dans la même session**, témoin **0 → 1**, infrastructures toujours
> à 17 et PM inchangés. Voir `RUNTIME_FORCED_PROBE_2026_10_16`.
> La réaction du témoin est observée ; le rendu des rails reste non vérifié.

> Dernier essai : **PASS_RUNTIME_EXPORT_OBSERVED**. Le compagnon 0.2.2 exporte un
> relevé lisible et identifiable pour FRA / STATE_ILE_DE_FRANCE : 17 niveaux,
> 0 témoin, routes traditionnelles sans canal ni rail. Voir le reçu et le rapport
> `RUNTIME_EXPORT_OBSERVED_2026_10_16`. Cela ne valide ni le rendu, ni les commandes
> entrantes, ni la causalité de ce clic précis sans curseur avant/après.

> Deuxième essai réel : le relevé 0.2.1 est complet et contient 17 niveaux
> d'infrastructures et 0 témoin, mais `GetPlayer` ne fournit toujours pas l'identité.
> Voir `IDENTITY_FIX_2026_10_16/REPORT.md`. Le compagnon 0.2.2 passe à des identifiants
> émis par prédicats de scripts ; nouvel essai moteur requis.

> Suivi du premier essai réel : l'export 0.2.0 s'exécute mais perd ses références
> pays/État, et un crash d'accès mémoire a été retrouvé à l'heure de l'essai.
> Voir `EXPORT_SCOPE_FIX_2026_10_16/REPORT.md`. Correctif compagnon 0.2.1 préparé,
> à retester ; aucun PASS moteur ne découle des contrôles statiques ci-dessous.

Date : 15 octobre 2026. Statut :
**READER_AND_LOCAL_INSTALL_PASS_ENGINE_EXPORT_PENDING**.

## Résultat concret

Serveur MCP local de lecture livré dans `tools/vic3-diagnostic-bridge/`, installé
et activé par le client Codex sous
`vic3-diagnostic-bridge@aor1776-local-tools`. Aucun téléversement ni appel à une
API de modèle. Un test stdio réel a démarré **la copie effectivement installée**,
négocié le protocole, découvert les trois outils et appelé chacun sur les journaux
actuels du jeu. Empreintes source/copie installée identiques.

Ces appels sont des tests de protocole lancés localement, **pas des invocations
des nouveaux outils depuis cette conversation Codex** : ils ne sont pas encore
exposés dans la liste des outils de ce tour après deux contrôles espacés.
Le plugin est présent et activé dans la liste du client ; son exposition à la
conversation reste à confirmer après rafraîchissement/redémarrage de Codex.
L'interface de commande du lecteur est utilisable dès maintenant.

Le compagnon isolé existant a été mis à jour de 0.1.0 à 0.2.0 : nouveaux scripts
d'export, une décision d'export en français/anglais, hooks de démarrage/mensuels/PM.
Le bâtiment économique et tous les PM restent inchangés. Les anciens fichiers
non concernés sont identiques. Seuls deux fichiers existants de décisions/hooks
ont reçu le BOM UTF-8 manquant, sans changer leurs trois actions de diagnostic.
Les avertissements d'encodage constatés au test précédent seront à revérifier au
prochain lancement ; ils ne sont pas déclarés résolus dans le moteur par ce rapport.

## Informations disponibles et limites

La v1 exporte la capitale du joueur humain : noms pays/État (pas TAG/State_ID),
date du jeu, niveaux infrastructure/témoin, mode de forçage et PM actifs routes,
canaux et rails. Le lecteur vérifie la cohérence logique du témoin, **pas le rendu**.
Un hook de PM peut précéder la synchronisation : après la manipulation, utiliser
la décision d'export pour lire le résultat final.

Le résultat réel actuel est **NO_TELEMETRY**. Le jeu en cours n'a pas chargé les
nouveaux scripts. Aucun relevé synthétique n'a été écrit dans ses journaux. Aucun
zéro ou PASS n'est substitué à cette absence. Les interpolations, hooks et valeurs
exportées restent à comparer dans une nouvelle session avec l'interface du jeu.

Pas de commande entrante, accès mémoire, clavier/souris, technologie accordée,
modification de PM, parsing de sauvegarde ou prétendue API de rendu dans cette
livraison. Aucun scénario automatisé dans le moteur n'est déclaré validé.

## Vérifications

- **27/27 tests du lecteur** : données synthétiques explicitement étiquetées,
  négociation MCP, découverte et appels, bornes/arguments, erreurs, fraîcheur par
  curseur, réécriture/troncature, session, fenêtre de 4 Mio, frame incomplète,
  interpolation non résolue et données de journal non fiables.
- **153/153 contrôles statiques du compagnon**, dont tests de vérité du témoin,
  idempotence et préservation du bâtiment économique ; ce n'est pas un test moteur.
- Contrôles supplémentaires : PM exportés = PM réels des trois PMG du mod,
  références de scripts, absence d'effets économiques dans l'exporteur, encodages.
- Copie du compagnon installé = source par SHA-256 ; copie 0.1.0 de retour arrière
  vérifiée avant les seuls écrasements autorisés. Environ quelques Ko de textes,
  pas d'archive volumineuse du dépôt.
- Tous les fichiers runtime du mod principal inchangés depuis le début de cette
  passe, HEAD et index inchangés ; allocations MAP2N et attestation manuelle préservées.
- **26/26 tests MAP2N** repassés, ainsi que **46/46 contrôles** du garde PM des
  véhicules ferroviaires. Ces nombres correspondent aux suites réellement
  découvertes et exécutées dans cette passe, sans ajouter les anciens décomptes.
- Premier lancement des tests : problème d'accès au Temp du sandbox, pas un échec
  moteur. Les fixtures ont été déplacées dans un dossier temporaire du workspace
  et la suite entière a repassé. Aucun fichier du jeu n'a servi de fixture.

Les erreurs lues dans `error.log` appartiennent à la session préexistante, sans
télémétrie du nouveau pont. Elles restent **non attribuées** : pas de nettoyage,
masquage ni résolution présumée. Les défauts antérieurs (événements, scopes
diplomatiques, variantes de lois, etc.) restent séparés du diagnostic du pont.

## Installation et protection

Catalogue local ajouté avec le client officiel, puis plugin installé avec ce
même client. Pas d'édition de cache, pas de seconde intégration MCP parallèle.
Le serveur n'ouvre aucun port et ne démarre qu'à la demande du client. Aucun
réglage de launcher, playset ou sauvegarde modifié. Jeu laissé tel quel, sans
fermeture ni relance automatique. Aucun commit, merge ou push.

Le guide du paquet détaille la désactivation du plugin/compagnon et le petit
backup de retour arrière. La compétence de création de plugin a conduit au
paquet local stdio et à son installation par le client ; OpenAI Docs a servi à
vérifier cette procédure. Aucun service cloud n'a été créé.

## Prochaine vérification nécessaire

1. Redémarrer Victoria 3 avec le même compagnon (désormais 0.2.0) dans le playset de test.
2. Capturer un curseur du lecteur avant le test.
3. Déclencher **PROTOTYPE — Exporter le diagnostic de la capitale vers le pont local**.
4. Lire le nouveau relevé après curseur et comparer pays, État, niveaux et PM à l'interface.
5. Lire seulement les nouvelles erreurs après un curseur d'erreurs initial.
6. Observer les rails au sol pour le volet visuel, qui n'est toujours pas automatisé.

ColGrep-Agent-2B : un appel de localisation, résultats contrôlés dans
`tools/audit_1776_runtime_logs.py`. Son lecteur de sauvegardes texte a été écarté
de cette v1 pour ne pas prétendre prendre en charge les formats compressés/binaires.
Les recherches exactes suivantes ont réutilisé les fichiers connus. Aucune économie
chiffrée de quota n'est déduite de cet unique essai.
