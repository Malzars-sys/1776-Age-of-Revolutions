# Vérification moteur — événements rétablis de 44

Version exacte : trois fichiers et empreintes dans `INSTALLATION_RECEIPT.json`. Les cases ci-dessous ne sont pas attestées par la validation statique.

1. Démarrer une nouvelle partie 1776, noter version, configuration DLC et pays. Capturer les nouveaux logs après les cas réellement exercés.
2. **Russie :** observer la branche générique d'une succession existante. Vérifier l'affichage de l'avènement, le bon souverain et la portée `tsar_scope`, puis l'absence d'immortalité temporaire résiduelle après fermeture. Un événement isolé peut vérifier le panneau ; il ne valide pas une succession complète ni les missions de l'Autocrate, qui restent conditionnelles à leur journal.
3. **Coup étranger :** utiliser le parcours diplomatique de soutien d'un coup avec général, pays commanditaire et lobby valides. Vérifier les textes, noms générés, options de soutien/résistance et l'ouverture du journal de coup déjà présent. Ne pas déclencher l'événement à vide : sa cancellation et ses textes dépendent des scopes fournis par le helper. Une préparation lourde ou une configuration DLC indisponible laisse ce cas explicitement non testé.
4. **Japon :** lorsque les conditions existantes du bouton ou de `jap_abolish_edo_system` sont remplies, vérifier que le changement de hiérarchie et la notification de disparition du système Edo visent le bon pays. Ne pas modifier les lois/technologies initiales du mod pour rendre le test artificiellement immédiat. Un essai debug isolé doit conserver une portée de pays valide et être distingué du parcours normal.
5. Faire la sauvegarde/reprise adaptée aux cas exécutés : notification/hiérarchie persistante, état du coup et absence d'effet temporaire russe oublié. Relever tout nouveau diagnostic avec sa chaîne d'appel exacte.

Ces événements ne créent aucun déclenchement nouveau au lancement. Leur absence au premier jour n'est pas un échec du correctif. Ne certifier que les cas observés : la restauration de fournisseurs ne prouve ni toutes les conditions des journaux ni la parité complète du DLC.
