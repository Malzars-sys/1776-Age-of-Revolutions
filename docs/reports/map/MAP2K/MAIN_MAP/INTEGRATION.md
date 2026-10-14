# Carte impériale intégrée au mod principal — 13 octobre 2026

Le joueur a confirmé « ça marche bien » et fourni une capture de Victoria 3
montrant les territoires de jure en jaune sur la carte principale. Cette preuve
valide le prototype en jeu, y compris son orientation géographique. Elle ne
valide pas une éventuelle évolution dynamique des limites impériales.

## Intégration

Le mod principal contient désormais les deux shaders, la définition du mode,
les deux textures de masque/signature et les traductions française et anglaise.
Les shaders, propriétés du mode et pixels sont ceux du prototype confirmé.
Le nom affiché est « Territoires de jure du Saint-Empire », sans « prototype ».
L'icône fournie est conservée.

Les noms internes de fichiers et le mode `mm_aor1776_hre_de_jure_prototype` sont
conservés volontairement : ils préservent l'identifiant testé et les sélections
existantes. Le compagnon ancien peut remplacer ces mêmes fichiers s'il reste
actif, mais ne crée pas un deuxième mode. Il n'est plus nécessaire : utiliser
le playset habituel avec le mod principal seul au prochain lancement. Le playset
de test n'est pas supprimé, et sa configuration n'est pas modifiée pendant que
le jeu peut être ouvert.

À la demande du joueur, le bouton bitmap du bas, son raccourci contextuel et
sa fenêtre autonome dans le HUD sont retirés. La carte bitmap **dans le journal**
est conservée. Le sélecteur, la barre des outils et le HUD retrouvent leur contenu
vanilla en dehors des autres changements du mod ; le compilateur n'ajoute plus
de raccourci d'atlas à sa sortie.

Les 16 contrôles propres au masque/rendu sont réussis pour les fichiers intégrés,
dont conservation exacte des 278 RGB et compilation Direct3D du code ajouté.
`VALIDATION.json` est un rapport hors jeu : son drapeau `runtime_verified=false`
ne nie pas la confirmation du joueur, il distingue celle-ci d'un nouveau test
automatisé de l'installation intégrée. Une relance avec le mod principal seul
reste nécessaire pour confirmer cette installation, pas son mécanisme déjà vu.

## Limites actuelles et évolution dynamique

Le jaune dépend actuellement d'un masque DDS construit à partir du registre
de jure. Il ne dépend pas du pays propriétaire : une conquête extérieure ne
retire pas les droits impériaux. Le shader ne lit pas directement un modificateur
d'État ou une variable scriptée arbitraire. Ajouter/retirer des États en cours
de partie ne modifiera donc **pas encore** cette coloration.

Pour la suite, les actions d'entrée/sortie devraient actualiser un registre
impérial partagé par la diplomatie, les marqueurs, les compteurs du journal et
la carte. Il faudra ensuite prototyper un moyen moteur de transmettre ce registre
actualisé au rendu. La possibilité de cette synchronisation sans relance n'est
pas encore vérifiée : ne pas promettre qu'un simple modificateur ou qu'une
régénération externe du DDS donnera un mode dynamique en jeu.

Il faudra aussi distinguer la sortie d'un **pays** du bloc et le retrait des
droits impériaux sur un **territoire** : ce ne sont pas automatiquement la même
action. Aucun changement aux règles d'entrée/sortie n'est implémenté ici.

## Reproduction

`tools/prototype_map2k_main_map.py --emit-integrated-patch` émet le patch des
sources intégrées. Après application, `--integrated-build-test` régénère les
DDS dans le mod principal et contrôle les résultats. Le script ne modifie ni
les sauvegardes ni les playsets.
