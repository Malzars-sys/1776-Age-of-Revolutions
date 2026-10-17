# Livraison du compagnon 0.1.0

> **Mise à jour 16 octobre : apparition et retrait des rails au sol validés
> manuellement sur les tronçons inspectés**, avec captures conservées.
> Voir `RUNTIME_USER_VISUAL_VALIDATION_2026_10_16.md` et son reçu JSON.
> Le compagnon courant reste isolé (0.2.2). Les PM ferroviaires réels, autres
> États et effets indirects restent à tester ; aucune intégration principale.

> Historique de livraison 0.1.0. La version installée est maintenant 0.2.0 avec
> télémétrie en lecture seule ; voir `docs/reports/bridge/VIC3_LOCAL_BRIDGE/REPORT.md`.
> La passe 0.2.0 passe 153 contrôles statiques, mais son export moteur attend
> encore une relance du jeu. Les résultats visuels 0.1.0 ci-dessous restent partiels.

Statique : **PROTOTYPE_READY_FOR_RUNTIME_TEST**. Essai en jeu ultérieur : **PROTOTYPE_RUNTIME_PARTIAL_INCONCLUSIVE_VISUAL**, voir RUNTIME_TEST_2026_10_15.md. Aucun PASS_RUNTIME_USER_VALIDATED complet pour ce compagnon.

- Compagnon installé dans le nouveau dossier `../aor1776_landscape_prototype`
  à côté du mod principal, avec son descripteur `.mod` externe et ses métadonnées.
- Tous les fichiers installés sont identiques au paquet source par SHA-256.
  `INSTALLED_VALIDATION.json` contient les empreintes.
- **146/146 contrôles statiques** : syntaxe, chaîne building/group/PMG/PM,
  garde des sept PM ferroviaires, table de vérité des forçages, idempotence,
  retrait après changement de PM, conservation des données économiques simulées,
  hooks additifs et localisations français/anglais.
- Empreintes de tous les fichiers d'exécution du mod principal inchangées par
  cette passe. HEAD/index conservés ; aucun commit, merge ou push. Aucun playset
  ou réglage du launcher n'a été changé, aucun jeu lancé/fermé par l'assistant.
- MAP2N : attestation manuelle enregistrée séparément et **44/44 tests de
  non-régression** repassés. Un ancien test supposait qu'aucun retour manuel
  n'avait encore été reçu : il exige maintenant l'attestation correspondante
  avant d'accepter ce drapeau, sans confondre cela avec un test moteur.

## Non démontré, à tester

Le compagnon peut-il réellement piloter les rails au sol sans emplois ou sorties
ferroviaires ? Les connexions militaires/IA restent-elles cohérentes avec ce
changement de désignation ? Les hooks se rafraîchissent-ils sans recharge ?
Ce sont les questions de l'essai, pas des résultats déjà acquis.

Le témoin est un interrupteur d'un niveau ; ni une synchronisation de densité ni
un système complet de routes/canaux. Aucun ancien tracé n'est modifié. Le guide
README décrit le test court dans la capitale et le retour au mode automatique.

ColGrep-Agent : un appel utile a été tenté, puis relancé avec l'accès nécessaire
à son index local après un refus de verrouillage. Les pistes d'on_actions ont été
vérifiées ; les pistes de consolidation économique/carte ne résolvaient pas le
rendu et ont été écartées. Les exemples précis déjà connus ont été réutilisés.
Aucun changement d'intégration ni reconstruction globale de l'index.
