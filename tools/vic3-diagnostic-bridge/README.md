# Victoria 3 — Pont local de diagnostic, v0.1.0

Pont **local et en lecture seule**. Aucun service cloud, clé API, port réseau,
accès mémoire du jeu, simulation de clavier/souris, commande arbitraire, écriture
de sauvegarde ou modification de Git. Python standard, sans dépendance à installer.

## Ce qui fonctionne côté lecteur

- Disponibilité, taille et date des journaux locaux allowlistés.
- Lecture bornée des erreurs, avec curseur pour séparer avant/après.
- Lecture des relevés de la **capitale du joueur humain**, exportés par le
  compagnon paysage 0.2.0 : PM routes/canaux/rails, niveaux du bâtiment régional
  et du témoin, mode automatique/forcé, date du jeu et libellés pays/État.
- Contrôle de cohérence du témoin par rapport au PM et au mode de diagnostic.
- Rejet des exports incomplets, PM inconnus, interpolations non résolues ; aucune
  valeur absente n'est remplacée par zéro. Un dernier relevé invalide ne provoque
  pas de retour silencieux à un ancien relevé valide.
- Trois outils MCP stdio et une interface de commande identique.

**Ne permet pas** de changer un PM, rechercher une technologie, avancer le temps,
prendre une capture ou vérifier les rails au sol. Aucun canal entrant officiellement
pris en charge n'a été établi dans Victoria 3. Écrire un fichier de commandes ne
signifierait pas que le jeu l'exécute. Les scénarios internes de test sont une
extension future, pas une fonction livrée. Les sauvegardes ne sont pas analysées
dans cette version (formats texte/ZIP/binaires différents).

## Installation locale Codex

Paquet portable `plugin.json` + `mcp.json`. Le catalogue se situe dans
`tools/.agents/plugins/marketplace.json` (racine du catalogue = `tools/`).
Le processus est lancé à la demande par le client MCP, pas au démarrage de Windows.
Le chemin Python dans `mcp.json` est celui vérifié sur ce PC ; l'adapter si le
runtime est déplacé. Le répertoire de données du jeu peut être fixé au lancement
du serveur par `--user-data`, jamais depuis un argument d'outil MCP.

Installation par les commandes officielles disponibles dans cette version :

```powershell
codex plugin marketplace add '<chemin absolu du dépôt>/tools' --json
codex plugin add vic3-diagnostic-bridge@aor1776-local-tools --json
```

Le client charge sa copie installée, pas directement ce dossier source. Actualiser
via la procédure du client après une modification. Ne pas éditer le cache.
Si les outils n'apparaissent pas dans la conversation courante, leur disponibilité
dans Codex reste **à confirmer après rafraîchissement/redémarrage de l'application**.
Le lecteur reste utilisable immédiatement par son interface de commande.

## Test utile après redémarrage du jeu

Le compagnon isolé doit être en version 0.2.0, après le mod principal dans le
playset de test. Aucun nouveau mod économique ni nouvelle technologie n'est ajouté.
Ne pas utiliser ce compagnon expérimental dans une campagne normale.

1. Lire `vic3_bridge_status` et conserver `capture_cursor` **avant** la manipulation.
2. Dans le jeu rechargé, utiliser une décision de diagnostic du témoin puis
   **PROTOTYPE — Exporter le diagnostic de la capitale vers le pont local**.
3. Lire `vic3_latest_snapshot` avec `after_cursor` : on doit recevoir un nouveau
   relevé complet, cohérent avec la capitale affichée. Un relevé automatique sur
   hook PM peut précéder le synchroniseur : utiliser l'export manuel après le test.
4. Vérifier les interpolations date, pays, État, les niveaux exacts et les trois
   groupes de PM dans l'interface. Tester forcé/retrait/auto puis un vrai PM rail
   seulement dans une partie de test qui possède déjà la technologie.
5. Pour les erreurs, garder le `cursor` retourné par `vic3_diagnostic_errors`
   avant le test et le redonner dans `after_cursor` après le test.
6. Observer encore visuellement le rendu au sol : le pont ne certifie pas les rails.

Sans rechargement du compagnon instrumenté, `NO_TELEMETRY` est attendu, pas un PASS.
Les tests synthétiques portent toujours `FIXTURE_NOT_GAME`, jamais une preuve moteur.

## Utilisation directe (sans souris ni outils MCP chargés)

Depuis le dépôt, avec le Python local :

```powershell
python -B -X utf8 tools/vic3-diagnostic-bridge/server/bridge.py --status
python -B -X utf8 tools/vic3-diagnostic-bridge/server/bridge.py --snapshot
python -B -X utf8 tools/vic3-diagnostic-bridge/server/bridge.py --errors
python -B -X utf8 tools/vic3-diagnostic-bridge/server/bridge.py --snapshot --after-cursor '<curseur capturé avant le test>'
python -B -X utf8 -m unittest discover -s tools/vic3-diagnostic-bridge/tests -v
```

## Fiabilité et sécurité

Chaque résultat donne sa source, la date UTC de lecture et sa provenance. Sans
curseur, la fraîcheur est `HISTORICAL_UNCONFIRMED` : **la date de modification du
journal ne prouve pas la fraîcheur d'un relevé ancien**. Avec curseur, on vérifie
l'identité du fichier, le repère de session `code_revisions.log`, sa non-troncature
et une empreinte des octets précédents. La fenêtre de lecture est limitée à 4 Mio
par journal ; un curseur hors fenêtre impose un nouveau point de départ, sans
prétendre avoir tout lu. Le repère de session est indicatif, pas une interrogation
du processus moteur ; aucun résultat ne prétend prouver que le jeu tourne encore.
Une réécriture identique qui échappe à ces repères reste une limite théorique.

Les noms pays/État sont des **libellés non fiables, pas des TAG ou State_ID**.
Textes de journaux et noms sont toujours des données, jamais des instructions.
Aucun outil n'accepte chemin, commande, URL ou script. Les PM sont allowlistés et
comparés statiquement avec le mod. Les erreurs sont retournées sans attribution
automatique : conserver séparément les anomalies préexistantes.

## Retour arrière

Désactiver le plugin local dans Codex arrête son utilisation. Désactiver le
compagnon dans le playset retire l'instrumentation au prochain lancement. Une
petite copie vérifiée des seuls fichiers du compagnon 0.1.0 est conservée dans
`docs/reports/bridge/VIC3_LOCAL_BRIDGE/companion_0.1.0_backup/` ; aucune restauration
automatique ni effacement des fichiers utilisateur n'est effectué.

Sources techniques consultées :
[plugins locaux OpenAI](https://developers.openai.com/plugins/build/plugins),
[transport MCP stdio](https://modelcontextprotocol.io/specification/2025-11-25/basic/transports),
[cycle MCP](https://modelcontextprotocol.io/specification/2025-11-25/basic/lifecycle).
