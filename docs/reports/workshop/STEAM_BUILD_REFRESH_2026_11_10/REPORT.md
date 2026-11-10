# Steam Build local 2.6.0 — livraison du 11 novembre 2026

À la demande du mainteneur, la copie allégée est reconstruite depuis le dossier de travail testé, avec le correctif du libellé français des céréales. La version passe de **2.5.0 à 2.6.0** dans le travail local et les deux copies de publication. La compatibilité est **1.15.0** dans les métadonnées et **1.15.\*** dans les descripteurs concernés.

Copies synchronisées :

- Dossier utilisé par l'entrée Steam Build du lanceur et destiné à la publication : `C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/workshop_build/Age_of_Revolution_Fork`.
- Copie nommée Steam Build dans les mods locaux : `C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/Age of revolution Fork [Steam Build]`.

Chaque copie contient **2 984 fichiers**, environ **404 Mo** : scripts, interface, localisations, carte, textures, modèles, musique, miniature et métadonnées nécessaires. Les outils, rapports, recherches, documentation, caches, Git, sorties de travail et sources d'illustration non utilisées sont exclus. Quatre documents Markdown présents à l'intérieur de `common/` sont également exclus. Les fichiers runtime copiés restent identiques aux sources ; seul le nom d'affichage propre à la copie secondaire est conservé dans ses métadonnées.

Les deux inscriptions locales du lanceur gardent leurs noms et chemins : seule leur compatibilité déclarée passe de 1.13 à 1.15. Les identifiants et les paramètres de remplacement sont préservés. La seule modification dans les données du dossier de développement est la valeur de version de `.metadata/metadata.json` ; ses outils et sa documentation sont conservés.

## Contrôles exécutés

- Préparation par liste explicite des dix entrées runtime du manifeste de livraison existant ; son ancien commentaire « 1.13 » n'est pas utilisé comme contrainte de compatibilité.
- Le constructeur historique `build_steam_package.ps1`, qui impose encore 1.13, n'est pas exécuté. Un candidat 1.15 est préparé et contrôlé avant toute installation.
- Métadonnées 2.6.0/1.15.0, descripteur 1.15, miniature PNG 600 × 600, absence de fichiers de développement et présence du correctif des céréales : vérifiés.
- Empreintes SHA-256 de la préparation, des sources courantes et des deux copies installées : **zéro écart**, hors différence intentionnelle du nom d'affichage secondaire. Aucun changement concurrent des sources runtime pendant cette opération.
- Ensemble des chemins installé identique au manifeste préparé : aucun fichier ancien résiduel. Deux inscriptions du lanceur vérifiées après leur modification bornée.

L'installation utilise le script existant `tools/workshop/refresh_local_steam_build.ps1`, inspecté puis vérifié par empreinte. Il contrôle les chemins absolus et l'absence de liens/jonctions, prépare et vérifie les deux nouvelles copies, puis déplace les anciennes dans une sauvegarde récupérable avant remplacement. Aucune suppression récursive du dossier de travail n'est effectuée.

Sauvegarde des anciennes copies et inventaires :

`C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/workshop_build/backups/steam-refresh-20261111-000243-06908460`

Les anciennes métadonnées de travail et inscriptions du lanceur sont conservées dans ce dossier de rapport. `PREPARED_PLAN.json`, `INSTALLER_RECEIPT.json` et `DELIVERY_VERIFICATION.json` consignent les chemins, versions, manifestes, empreintes et résultats. La préparation ayant commencé le 10 novembre, le dossier de preuve conserve cette date ; installation et contrôle final ont eu lieu le 11 novembre, heure de Paris.

Aucun nouveau lancement moteur, opération Git d'écriture ou téléversement Steam n'a été effectué. Il s'agit de la mise à jour des copies locales prêtes à publier, à partir du contenu accepté par le mainteneur et de la correction mineure de localisation qu'il a autorisé à intégrer directement.
