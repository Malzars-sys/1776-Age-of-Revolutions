# Test ciblé — deux options d'événements d'agitateurs

Version livrée : empreinte du fichier d'événements dans `INSTALLATION_RECEIPT.json`. Aucun résultat moteur n'est fourni ici.

1. Dans une nouvelle partie 1776, noter la version du jeu, la configuration DLC et le pays. Utiliser un pays remplissant les conditions du flux d'événements d'agitation/enactment ; une absence d'événement au départ n'est pas un échec du correctif.
2. Pour `agitator_legal_events.5`, obtenir l'option `.5.a` avec les portées `opposing_agitator` et `opposing_ig_leader` correctement créées. Vérifier que l'option prévoit le « Scandale de notoriété publique » sur le dirigeant opposant, puis que ce personnage reçoit la pénalité temporaire de popularité de 50 points avec la durée affichée. Le bonus du lanceur d'alerte et les effets de promulgation restent des témoins de conservation.
3. Pour `agitator_legal_events.12`, choisir `.12.b` avec la portée `da_boss` valide. Vérifier la même pénalité temporaire sur ce destinataire, ainsi que la conservation des autres effets de l'option.
4. Si la console ou le mode debug servent à préparer ces cas, préserver l'exécution du bloc de création des portées et leurs préconditions ; déclencher aveuglément un événement sans ses personnages ne constitue pas un test valable. Un cas difficile à préparer peut rester explicitement non testé.
5. Contrôler les nouveaux logs pour les anciens appels `add_modifier` à `scandalous`, puis sauvegarder/recharger et vérifier la persistance du modificateur temporaire et sa durée restante. Ne pas confondre le trait permanent homonyme avec le modificateur corrigé.

La disparition à échéance exige son propre témoin si elle est essayée ; ne pas déduire ce résultat d'un simple rechargement. Le rendu FR et EN peut être vérifié séparément. Consigner uniquement les cas réellement exécutés et les détails disponibles.

La référence manquante de l'ancien événement communiste reste hors lot. Ce protocole ne valide ni cet événement ni le parcours révolutionnaire/DLC global. L'issue reste ouverte jusqu'à l'acceptation correspondante.
