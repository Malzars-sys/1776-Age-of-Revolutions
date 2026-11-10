# Mission #46 — Protocole moteur

Version livrée : manifeste R4, six nouveaux fichiers, statut **IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION**. Aucun test moteur n'est encore attesté. Les tests avancés demandant un contexte du XIXe siècle peuvent être regroupés avec les missions #39 et #45 ; une courte partie en 1776 ne les valide pas.

## 1. Chargement et témoins

1. Relancer complètement le jeu avec le mod à jour et sa configuration habituelle. Lancer une nouvelle partie en 1776 au Japon.
2. Vérifier le chargement, les premières semaines, un passage annuel puis sauvegarder et recharger. Contrôler aussi le témoin annuel japonais de #45 selon son propre protocole.
3. Examiner les nouvelles lignes du journal d'erreurs : aucune définition absente pour `marx_events.3/.4`, `japan_events.32/.33/.34/.35`, `ideology_state_socialist`, `ideology_communist_leader`, `ideology_communist_leader_valid_trigger` ou `law_labour_suffrage` ; aucun doublon introduit par les six fichiers #46.
4. Comparer les lois et technologies de départ avec le témoin habituel : la restauration n'accorde ni socialisme, ni république des conseils, ni suffrage ouvrier à un pays en 1776.
5. Le problème préexistant `on_memento_mori`, s'il apparaît, reste distinct et n'est pas un résultat nouveau de #46.

## 2. Japon — disponibilité, effets et présentation

Pour les quatre événements, utiliser une sauvegarde de test où leurs prérequis sont réellement remplis. Un déclenchement forcé dans un pays arbitraire ne prouve ni la sélection annuelle ni la validité des scopes. Les conditions détaillées figurent dans `REPORT.md` et dans le fichier installé `events/zz_1776_v115_event46_japan.txt`.

| Événement | Contexte à préparer | Vérifications |
| --- | --- | --- |
| `.32` | Japon non isolationniste avec académie d'art traditionnel admissible | État choisi cohérent, deux choix et bonus correspondants ; textes et image visibles. |
| `.33` | Souverain/empereur adulte Meiji ou Showa, culture japonaise et mouvement culturel admissible | Bon personnage et mouvement, options cohérentes, effets annoncés appliqués ; l'immortalité temporaire est correctement nettoyée après la résolution. |
| `.34` | Famine dans un État japonais incorporé avec au moins deux niveaux de pêche à la baleine | Bonne région sélectionnée et effets locaux conformes aux options. |
| `.35` | Japon sous hiérarchie Edo et lois compatibles, conditions de cherté du grain et d'agitation du Kanto satisfaites | État ciblé, choix et conséquences cohérents ; aucun scope vide. |

Tester le DLC `ep2_content` activé puis désactivé si la configuration le permet. Sans ce contenu, aucun des quatre événements ne doit devenir admissible. Dans les deux cas, vérifier le chargement ; avec le contenu actif, vérifier les médias réels et leur éventuel repli. Le contrôle statique d'un chemin d'icône ne certifie pas une vidéo DLC montée.

Vérifier aussi qu'un événement résolu ne revient pas malgré `fire_only_once`, puis sauvegarder/recharger une partie concernée. Noter les branches réellement essayées, sans généraliser une seule option à toute la famille.

## 3. Marx — distinguer sécurité et intégration complète

**Limite conservée :** le Marx.1 écrit pour le mod ne fournit pas le global d'auteur attendu par le Marx.3 natif. Cette mission n'ajoute pas ce raccordement. La simple absence de Marx.3 dans une partie ordinaire ne constitue donc pas une preuve d'échec de chargement ; inversement, elle ne certifie pas la nouvelle histoire complète.

1. Dans une partie où `big_communism_builder` est absent, vérifier que Marx.3 n'apparaît pas avec un portrait ou un auteur manquant, y compris si les autres drapeaux historiques sont présents. Aucun acteur ne doit être fabriqué pour contourner le blocage.
2. Pour tester positivement Marx.3/.4, préparer une sauvegarde de qualification contenant un véritable personnage adéquat référencé par ce global et les autres prérequis. Ne pas lancer l'événement sans son contexte. La création d'un tel scénario de qualification reste à organiser si aucune sauvegarde ne le fournit.
3. Dans ce contexte seulement, vérifier le portrait, l'auteur/pays ou l'exil, les conditions des trois options, les branches de 16 et 8 ans, le financement et l'état occupé/immortel.
4. Vérifier la résolution différée Marx.4, ses deux descriptions selon la présence de l'auteur, les effets sur le mouvement choisi et le nettoyage des noms générés. Une sauvegarde proche de l'échéance sera nécessaire pour tester raisonnablement les longues durées ; ne pas certifier ces délais après quelques jours de simulation.
5. Vérifier que le texte français, les infobulles et les effets ne montrent aucun nom vide. Répéter une résolution pertinente après sauvegarde/rechargement.

## 4. Dépendances politiques tardives

Dans une sauvegarde avancée, vérifier le suffrage ouvrier : indisponible sans socialisme ou sans république des conseils, accessible avec les deux prérequis lorsque les autres règles du jeu l'autorisent. Vérifier les opinions du socialisme d'État dans ce contexte. Les deux poids aléatoires du nouvel identifiant communiste doivent rester nuls ; les personnages existants conservent leurs identifiants historiques du mod.

## Compte rendu attendu

Indiquer la version/manifeste, la configuration DLC, les pays et sauvegardes utilisés, les sections/options réellement vérifiées et toute nouvelle erreur. Un résultat partiel reste partiel, notamment si les scénarios Meiji/Showa ou Marx n'ont pas été préparés. Ne pas certifier la chaîne complète de Marx avec le seul test de démarrage.
