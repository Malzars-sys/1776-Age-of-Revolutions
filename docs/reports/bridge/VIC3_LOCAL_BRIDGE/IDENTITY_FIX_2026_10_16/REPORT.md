# Deuxième clic réel — nombres exportés, identité encore indisponible

Observation : 16 octobre 2026, après le clic annoncé par le joueur. Le dernier
bloc complet est horodaté **00:20:33**, date en jeu « janvier 1, 1776 ».
Le relevé original et sa provenance se trouvent dans `RUNTIME_BEFORE.json`.

## Ce qui a effectivement progressé

L'export 0.2.1 livre un bloc complet, avec **17 niveaux d'infrastructures**,
**0 témoin**, mode automatique, routes traditionnelles (`pm_traditional_road_network`),
sans canaux (`pm_no_canal_network`) ni rails (`pm_no_rail_network`). Ces nombres
proviennent désormais des prédicats sur les bâtiments, pas d'une évaluation sur
un état nul. Ils n'ont pas encore été comparés par le joueur à l'interface dans
cette session ; on ne déduit pas l'identité de l'État du seul nombre 17.

Le pays est encore vide et l'État vaut `NULL_STATE`. Les fonctions globales GUI
`GetPlayer` échouent donc aussi dans ce contexte de texte `debug_log`. Le lecteur
rejette correctement le bloc pour identité invalide. Ce n'est **pas un PASS**
du pont complet, ni une preuve de rails visibles.

Aucun nouveau dossier de crash n'a été trouvé depuis celui du premier essai.
Aucun processus victoria3 n'était présent lors du contrôle ; cela ne suffit pas
à certifier un test de stabilité ou à distinguer une fermeture normale d'un
arrêt sans rapport de crash. Les erreurs générales du jeu restent séparées.

## Correctif compagnon 0.2.2

Seuls les champs d'identification sont remplacés par des messages constants,
sélectionnés avec les prédicats natifs `this = c:TAG` sur le propriétaire et
`state_region = s:STATE_KEY` sur l'État. La table est générée depuis les fichiers
effectifs du jeu et du mod (le fichier homonyme du mod remplace celui du jeu),
sans inventer de TAG, State_ID ou RGB : **893 TAG et 781 clés de régions**.

Pour conserver la compatibilité avec le lecteur installé, les clés historiques
du protocole `country_name` et `state_name` restent, mais leurs valeurs sont
explicitement étiquetées : `TAG:FRA`, `REGION:STATE_ILE_DE_FRANCE`, par exemple.
Ces valeurs ne prétendent pas être des noms localisés. TAG + région identifient
la part nationale d'une région partagée ; ce n'est pas un ID numérique d'instance
d'État ni une couleur bitmap. Une entité absente de la table donne un champ absent
et donc un rejet, pas une identité inventée.

Tous les appels de texte GUI pour pays/État sont retirés. Seule la date globale,
déjà observée fonctionnelle, reste interpolée. Les PM et niveaux utilisent le
mécanisme de script déjà observé au deuxième essai. Aucun outil MCP, clé API,
configuration Codex ou mécanisme économique n'est modifié par ce correctif.

## Vérification et limite

La table générée est comparée à ses définitions sources et testée condition par
condition. Les niveaux, garde locale et absence d'effets économiques sont testés
statiquement. La compatibilité du lecteur est testée avec un exemple synthétique
explicitement distinct des relevés réels. Les empreintes du mod principal,
HEAD et index restent inchangées. Les fichiers 0.2.1 du compagnon sont sauvegardés
avant sa mise à jour, sans archive du dépôt.

L'identification corrigée **n'a pas encore été observée dans le moteur**.
Statut : **NUMERIC_EXPORT_OBSERVED_IDENTITY_FIX_AWAITING_RETEST**.
Une relance du compagnon 0.2.2 puis un seul clic d'export sont nécessaires.
Ne pas demander au joueur de changer des PM économiques pour ce test.
