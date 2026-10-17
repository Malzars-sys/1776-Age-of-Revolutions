# Premier relevé réel complet et identifiable

Statut : **PASS_RUNTIME_EXPORT_OBSERVED**, limité à la lecture d'un export réel.
Ce n'est ni `PASS_RUNTIME_USER_VALIDATED` du paysage, ni un test moteur automatisé.

Après le clic annoncé par le joueur, le lecteur local accepte un bloc complet
du journal, horodaté **00:37:45** le 16 octobre, date du jeu **1 janvier 1776** :

- Propriétaire : **FRA** (France).
- Région : **STATE_ILE_DE_FRANCE** (Île-de-France).
- Infrastructures régionales : **17** niveaux.
- Témoin ferroviaire : **0** niveau, suivi **automatique**.
- PM actifs : `pm_traditional_road_network`, `pm_no_canal_network`,
  `pm_no_rail_network`.
- Aucune erreur de structure ou d'identité dans ce bloc. Témoin absent cohérent
  avec le PM sans rails. Identifiants vérifiés dans les définitions effectives.

Les valeurs proviennent bien du journal réel, pas d'une fixture. L'accès est
effectué par l'interface de commande du lecteur installé dans le projet : les
outils MCP natifs n'ont toujours pas été exposés à ce tour de conversation.

## Limites maintenues

Il n'y avait pas de curseur capturé **avant ce clic dans la même session**.
Le lecteur marque donc honnêtement la fraîcheur `HISTORICAL_UNCONFIRMED` : le
bloc est réel et appartient au nouveau fichier de session, mais son déclenchement
par ce clic précis plutôt que par un hook automatique n'est pas démontré.
Un curseur a maintenant été conservé dans le reçu pour un prochain test A/B.

Les valeurs n'ont pas encore été comparées par le joueur avec l'interface lors
de cet essai. Le relevé ne prouve pas l'apparence des rails, la stabilité prolongée,
le changement de PM ferroviaire réel ou le fonctionnement de commandes entrantes.
Aucun nouveau dossier de crash n'a été trouvé au contrôle ; cela ne prouve pas
l'absence de tout crash ni que le jeu tourne encore.

Les recherches ciblées dans `error.log` n'ont trouvé aucune référence aux scripts
`aor1776_bridge`. Des avertissements d'interface `PRODUCTION_METHOD_OPTIONS_BULK`
et des succès Steam invalides figurent dans les journaux ; ils ne sont pas
attribués automatiquement au pont et ne sont pas masqués ou corrigés dans ce test.

Le mod principal et HEAD/index restent inchangés. Aucun redémarrage supplémentaire
n'est demandé pour cette observation. Le prochain test éventuel peut se faire dans
la même partie de test : forcer/retirer le témoin puis exporter, et lire le résultat
après le curseur conservé. L'observation visuelle du sol reste distincte.
