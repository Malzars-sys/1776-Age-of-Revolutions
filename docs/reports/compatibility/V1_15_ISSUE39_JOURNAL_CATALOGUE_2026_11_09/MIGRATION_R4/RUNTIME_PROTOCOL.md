# #39 — Essais moteur groupés, version locale R4

Tous les résultats ci-dessous sont **à tester**. Utiliser une nouvelle partie de 1776, noter le build 1.15 réellement lancé, la configuration DLC et les autres mods. Le reçu `INSTALLATION.json` identifie le candidat local ; ce n'est pas le candidat de branche de #25.

## Première passe : affichage et continuité

1. **France**, journal des États généraux : ouvrir la fiche et vérifier des critères de réussite et d'échec visibles, les effets annoncés et l'échéance. Comparer le résultat aux conditions réelles ; l'affichage seul ne prouve pas que les effets s'exécutent.
2. **Maroc**, Terres d'anarchie : vérifier réussite, échec et invalidation cachée, les barres et les boutons. Observer la conservation du nettoyage des malus après une issue.
3. **Monténégro**, si l'entrée de raids est disponible : vérifier les aperçus d'événements dans les bonnes issues et la distinction entre réussite, échec et invalidation. Ne pas modifier la carte ou les lois de départ pour rendre le test possible.
4. **Témoin ottoman ou américain déjà accepté sous #27** : vérifier que les panneaux migrés précédemment et leurs continuations n'ont pas régressé. Ne pas conclure la nouvelle #39 à partir de l'ancien reçu #27.

## Deuxième passe : familles de conclusions

Sur des copies de sauvegarde dédiées ou des situations naturellement disponibles, relever au moins un cas de chaque famille. Une branche inaccessible dans la session reste non testée ; aucune réussite ne doit être déduite du seul audit statique.

- **Réussite puis sauvegarde/rechargement** : récompense et continuation une seule fois, effets persistants corrects, pulses de l'entrée conclue arrêtés.
- **Échec puis sauvegarde/rechargement** : effet d'échec et nettoyage une seule fois, aucune récompense de réussite simultanée.
- **Expiration** : durée et éventuelle extension calculée inchangées ; outcome d'expiration sans déclencheur ordinaire ; handler exécuté à l'échéance, pas à l'ouverture de la fiche.
- **Invalidation / retrait forcé** : issue cachée, nettoyage attendu et absence de conclusion visible ajoutée. Les handlers autrefois orphelins demandent un essai spécifique si une commande externe les atteint.
- **Conditions concurrentes** : préparer une copie où réussite et échec/invalidation deviennent vrais à la même évaluation ; relever l'issue et vérifier qu'aucun second effet ne suit après rechargement.
- **Situation sans pays racine** : une entrée telle que la Grande Crise orientale ou une situation internationale disponible doit exécuter les effets pour tous les pays impliqués dans leur contexte, sans les appliquer seulement au pays observateur.
- **Tutoriel / objectif** : vérifier condition, progression et conclusion d'un objectif simple. Une entrée permanente ou un dummy espagnol ne doit pas recevoir de conclusion nouvelle.

## Chaînes communistes et définitions restaurées

La famille communiste existante conserve ses conditions authored : l'ancien échec de `je_communism_1` poursuit sa chaîne, et son expiration mène à son autre événement. Vérifier les deux voies et leur présentation, sans supposer qu'un intitulé d'échec signifie la disparition de toute la chaîne.

Pour les anciens objectifs d'avant-garde, protection sociale et plan quinquennal : contrôler titre/raison FR ou EN, critères, progression et récompense. La définition native `je_five_year_plan` est distincte de l'ancien `je_5_year_plan` ; ne pas les confondre lors d'un déclenchement contrôlé. Si la branche native est testée, vérifier aussi les boutons, l'événement des chiffres falsifiés, la continuation et le rechargement des variables du plan.

Le mariage impérial japonais doit être ajouté par son événement prévu, puis présenter ses critères et les issues native de réussite, échec, expiration et invalidation. Aucun mariage n'est ajouté à l'histoire initiale par cette livraison.

« État et Révolution » retrouve sa définition native, mais les anciens choix de `communism.2` ne sont pas recâblés vers elle. Le portage complet des nouvelles familles DLC demeure un sujet distinct sous #24. Ne pas attester ce portage par un simple ajout manuel de l'entrée.

## Configuration et retour

Vérifier DLC activé puis désactivé lorsque la configuration le permet : pas d'exigence payante nouvelle pour le lancement de 1776. Les branches non disponibles sont enregistrées comme telles. Tester l'autre langue au moins sur les nouveaux noms et raisons ; relever les clés brutes ou textes coupés.

Conserver les sauvegardes utiles avant/après et les nouveaux logs ou rotations, avec leur configuration identifiée. Comparer à une référence vanilla ou au témoin moddé précis, sans présenter des erreurs anciennes comme nouvelles ou annoncer une baisse globale sans mesure. Ce protocole n'est ni un reçu de test exécuté ni une attestation humaine.
