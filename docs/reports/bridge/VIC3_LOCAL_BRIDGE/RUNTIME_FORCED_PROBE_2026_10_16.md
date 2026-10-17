# Forçage du témoin — nouveau relevé vérifié après curseur

Statut limité : **PASS_RUNTIME_FORCED_PROBE_EXPORT_OBSERVED**.
Action annoncée par le joueur : forcer le témoin puis exporter le diagnostic.

Le lecteur trouve un bloc réel complet horodaté **00:44:17 le 16 octobre 2026**,
nouveau depuis le curseur conservé au contrôle précédent :
`freshness = NEW_SINCE_CURSOR`. Même identité de fichier, même repère de session,
empreinte avant curseur intacte ; aucun repli vers une ancienne session.

| Donnée | Avant | Après |
| --- | --- | --- |
| Pays / région | FRA / STATE_ILE_DE_FRANCE | Identiques |
| Témoin ferroviaire | 0 | **1** |
| Mode du témoin | auto | **force_on** |
| Infrastructures régionales | 17 | 17 |
| PM routes | routes traditionnelles | Identique |
| PM canaux | sans canaux | Identique |
| PM rails | sans réseau ferroviaire | Identique |

Le témoin correspond au forçage attendu et le relevé ne comporte aucune erreur
de structure ou d'identité. La réaction du témoin et sa lecture après action sont
donc observées dans cette session. Accès effectué par le lecteur local en ligne
de commande, pas par un nouvel outil MCP natif exposé dans cette conversation.

Cela ne certifie pas les rails au sol, l'ensemble des données économiques ou un
pilotage entrant du jeu. Ce n'est pas une validation manuelle complète du paysage
ni un test moteur automatisé. Le prochain contrôle peut être un retour au suivi
automatique puis un export, sans relance : sans vrai PM rail, le témoin devrait
revenir à zéro. Le nouveau curseur est conservé dans le reçu JSON associé.
