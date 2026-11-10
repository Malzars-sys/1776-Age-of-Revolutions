# Correctif de compatibilité Victoria 3 1.15 — notes préparatoires

**Brouillon du 9 novembre 2026. Non publié.** Ces notes décrivent le workspace local examiné ; la branche de PR n'en est pas encore une copie intégrée et validée. Aucun numéro de nouvelle version du mod n'est arrêté ici.

## Changements préparés

- Adaptation des scripts concernés au soutien de guerre de la 1.15, avec conservation des paramètres propres au départ de 1776.
- Actualisation des calculs d'infamie et des objectifs territoriaux, de leur application pendant la guerre et des contre-objectifs de reprise. Conquête et annexion ont été acceptées par le mainteneur ; l'unification reste à tester.
- Correction des articles de traité portant sur les péages des détroits et des contributions à la projection navale des lois et principes concernés.
- Migration des lots de journaux livrés vers les conclusions de la 1.15 ; rétablissement des conditions et effets manquants dans les entrées américaines et polonaises concernées, et correction des titres canadiens.
- Paramètres standards du cuivre alignés sur le vanilla, avec **conservation de la distribution des gisements du mod** ; icônes du bien, de la mine et des méthodes concernées corrigées.
- Rétablissement des données climatiques manquantes dans les régions concernées, sans modification des frontières ou des ressources lors de cette passe climatique.
- Ajout du cuivre aux améliorations concernées des coques de frégates et de vaisseaux de ligne. La cogue conserve ses améliorations de transport et reçoit aussi une progression de sa capacité de marines ; ce dernier correctif demande encore son contrôle en jeu après redémarrage.
- Correction déjà acceptée du crash naval à la reprise du temps, de l'affichage de la sélection des objectifs et du défaut local de passabilité du nord de la Norvège.

## Validation actuellement disponible

Le mainteneur a accepté les sept points du résumé de test groupé, **sauf l'unification**, et a signalé le défaut de marines de la cogue corrigé ensuite. Les missions 21, 27, 29, 30 et 33 sont Done. Cette confirmation ne fournit pas une mesure distincte pour chaque scénario avancé ni un contrôle du dernier correctif de cogue.

Le premier recontrôle statique confirme les 485 assertions de l'audit API. Des travaux concurrents font ensuite passer ce recontrôle à 484/485 : l'assertion de conservation de `technology_events.txt` signale une modification hors de l'ancien lot, sans nouvel appel d'API retirée détecté. Le contrôle cuivre garde son résultat 154/155 : l'unique différence constatée dans son assertion de conservation correspond aux deux nouvelles textures de coque, sans changement de recette. Ces résultats sont conservés tels quels. Les sept ambiguïtés de définitions économiques restent documentées et demandent une vérification moteur.

## Limites à publier avec le candidat si elles subsistent

- Commencer une **nouvelle partie** pour le candidat intégrant le changement d'identifiant du transport précoce ; la compatibilité automatique avec les anciennes sauvegardes contenant l'ancien identifiant de cogue n'est pas certifiée.
- L'unification reste non testée. Le dernier correctif de marines de la cogue et les nouvelles proses de statut ottomanes n'ont pas encore de contrôle visuel après modification.
- Des journaux hérités non inclus dans les lots acceptés conservent des champs de conclusion rejetés. La présence d'un titre dans le journal ne garantit pas le fonctionnement d'une chaîne non migrée.
- Des erreurs de scopes/références restent à isoler dans l'IA et les contextes de culture, religion et contenu communiste/DLC. Leur gravité et leur attribution ne doivent pas être généralisées à partir du nombre de messages répétés.
- Les chaînes espagnoles différées et les anciens partages forcés polonais ne sont pas réactivés par ce hotfix.
- Le comportement avec DLC désactivés, la couverture de tous les scénarios avancés et la comparaison exhaustive avec une référence vanilla équivalente restent à compléter.

## État de publication

La PR 34 est encore en brouillon et signalée en conflit ; main et la branche hotfix ont divergé. Ces notes ne constituent ni une annonce de sortie, ni une autorisation de fusion, ni une certification de compatibilité générale. La déclaration de version du lanceur reste inchangée dans le mod actif ; son correctif 1.15 est préparé séparément comme candidat.
