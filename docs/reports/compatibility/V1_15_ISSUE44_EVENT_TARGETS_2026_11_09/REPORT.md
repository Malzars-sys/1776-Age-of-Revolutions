# Mission 44 — Trois événements vanilla masqués

9 novembre 2026. **IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION**. Référence canonique locale : Victoria 3 **1.15.0**. Aucun résultat moteur ni acceptation humaine nouvelle.

## Résultat installé

Quatre appels `trigger_event` conservés dans les scripts ne trouvaient plus leur définition : les anciens fichiers homonymes du mod masquaient trois événements désormais présents en vanilla. Trois fichiers isolés rétablissent exactement ces définitions actuelles, avec leurs namespaces, sans réécrire les événements existants ou leurs appelants.

| Cible rétablie | Appelant existant | Fichier neuf |
| --- | --- | --- |
| `russia_monarchy.12` | `character_russia_ruler_succession_chain_effect`, branche de succession générique russe | `events/zz_1776_v115_event44_russian_accession.txt` |
| `ip4_coup.11` | `create_coup_event_from_character`, coup soutenu par une puissance étrangère | `events/zz_1776_v115_event44_foreign_coup.txt` |
| `set_hierarchy_event.3` | bouton `je_end_edo_system_button` et décision du mod `jap_abolish_edo_system` | `events/zz_1776_v115_event44_edo_hierarchy.txt` |

La source du coup se trouve dans un dossier nommé `iberia_events`, mais son événement est générique : ce lot ne lance aucun chantier espagnol ou colonial. Aucun appel automatique, pays, dirigeant, condition de disponibilité, loi initiale, technologie ou histoire nationale n'est ajouté.

## Identité native et dépendances

Les trois blocs correspondent entièrement aux définitions canoniques capturées dans `native/`, provenant de `events/russia_events.txt:839`, `events/iberia_events/ip4_coup_events.txt:194` et `events/india_events/set_hierarchy_events.txt:60`. Les fichiers homonymes du mod restent byte-identiques ; aucune autre définition de ces fichiers natifs n'est réintroduite.

Les journaux directement nommés (`je_tsarpoints_master`, `je_ip4_coup`), modificateurs du coup, types de lobby, hiérarchie par défaut et notification Edo ont des fournisseurs effectifs uniques. Les helpers directement appelés correspondent aux payloads actuels natifs, y compris les deux helpers d'immortalité temporaire déjà rétablis par le travail 39. Leurs sources restent inchangées.

Les fenêtres, icônes, textes FR/EN et alias utilisés par ces événements sont résolus. Les textes et l'icône de la notification Edo sont également vérifiés. **Aucune clé de localisation nouvelle n'est nécessaire.** Les références dynamiques aux personnages, au pays commanditaire et au lobby restent celles du vanilla ; leur disponibilité réelle exige les essais appropriés.

Ce contrôle porte sur les dépendances directement examinées. Il ne simule ni toutes les branches internes des helpers, ni leurs effets, ni la sélection des événements ou l'ensemble du parcours DLC. Il ne valide pas le fonctionnement des journaux 39 par simple présence de leur identifiant.

## Vérifications exécutées et résultats conservés

- Avant : **2 506 événements effectifs**, **747 appels littéraux**, quatre appels sans cible et six appels dynamiques non développés.
- Contrôle vanilla distinct : **2 400 événements**, **630 appels littéraux**, aucune cible manquante ; deux appels dynamiques conservés.
- Candidat initial : **60/64**, résultat conservé dans `CANDIDATE_VALIDATION.json`. Le lecteur cherchait les lobbies dans `political_lobby_types` au lieu du dossier réel `political_lobbies` ; il ignorait aussi le texte d'ambiance russe suivi d'un commentaire de source. Aucun faux fournisseur ni nouvelle traduction n'a été créé pour compenser ces défauts du lecteur.
- Après correction du lecteur : **64/64** dans R2. Ajout de la vérification explicite des textes/icône de notification : **69/69** dans R3, puis **69/69** sur l'installation réelle.
- **7/7 contrôles négatifs** détectent la disparition de chacun des trois événements, un payload russe altéré, une notification Edo absente, un alias français absent et un type de lobby manquant. Les témoins restent en mémoire.
- Après : **2 509 événements**, les **mêmes 747 appels littéraux** tous résolus et les **mêmes six appels dynamiques**. Zéro erreur de parsing dans ce périmètre.
- Conservation : **2 965 fichiers de fonctionnement préexistants inchangés** ; seuls les trois fichiers neufs annoncés sont ajoutés. Les entrées effectives, références natives et ressources de présentation sont revérifiées dans `SOURCE_PROTECTION.json`. HEAD et index sont inchangés ; aucun Git write, changement du vanilla ou publication.

L'inventaire couvre les appels explicites `trigger_event` des événements, on_actions, effets scriptés, boutons et décisions. Les listes d'événements des on_actions, les expansions dynamiques, les outcomes de journaux et l'accessibilité moteur ne sont pas inclus dans les 747 appels. Les résultats ne constituent pas un certificat global de compatibilité.

## Lecture et reproduction

Consulter `CHANGES.patch`, les snapshots avant/candidat/natif, `BASELINE.json`, les trois validations candidates, `LIVE_VALIDATION.json`, les reçus et la garde de conservation. Les échecs initiaux ne sont pas effacés.

```text
python -B tools/compatibility/issue44_event_targets_audit.py --controls --output docs/reports/compatibility/V1_15_ISSUE44_EVENT_TARGETS_2026_11_09/RECHECK_NEW.json
```

Utiliser un nom de sortie neuf. L'outil ne comporte aucun installateur et n'écrit ni fichier de fonctionnement ni métadonnée Git. Le protocole moteur est dans `RUNTIME_PROTOCOL.md`.

La fiche **44** est mise à jour avec une livraison prête pour revue. La colonne Project est seulement demandée **In review**, sans prétendre l'avoir modifiée depuis la session navigateur précédemment déconnectée. Aucun parent ou lot en attente de test n'est clôturé.
