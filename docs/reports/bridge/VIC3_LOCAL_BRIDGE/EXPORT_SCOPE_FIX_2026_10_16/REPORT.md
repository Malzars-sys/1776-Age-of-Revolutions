# Premier export réel : défaut détecté, correctif compagnon à retester

Le clic annoncé par le joueur a été suivi de lectures locales du journal. Ce
n'est pas un test moteur automatisé, ni un PASS du pont complet.

## Observations réelles

- Le jeu a exécuté l'export : plusieurs blocs `AOR1776_BRIDGE_V1` complets à
  23:59:35–36, date du jeu « janvier 1, 1776 ».
- Les branches de script signalent les PM routes traditionnelles, sans canaux,
  sans réseau ferroviaire. Ces identifiants sont lus, mais leur comparaison à
  l'interface et leur rattachement au bon État restent non validés.
- Les références nommées dans `debug_log` donnent un pays vide et `NULL_STATE`.
  Les niveaux zéro provenant de ces références sont **non fiables**.
- Le dernier bloc est incomplet. Le lecteur le rejette correctement, sans
  substituer un ancien bloc ou prétendre que les niveaux sont nuls.
- Aucun processus Victoria 3 n'était retrouvé au contrôle ultérieur. Un rapport
  de crash existe à `crashes/victoria3_01260915_215937/exception.txt` :
  **Victoria 3 1.13.11, 2026-10-15 21:59:38, C0000005 / ACCESS_VIOLATION**.
  La pile n'est pas symbolisée : la cause exacte n'est pas prouvée. Le journal
  tronqué ne doit donc pas être attribué seulement à une écriture tamponnée.

## Correctif 0.2.1 du seul compagnon

- Suppression des scopes sauvegardés dans les textes exportés ; noms obtenus via
  le joueur local et sa capitale, protégés par `owner.is_local_player`.
- Suppression de toutes les interpolations `MakeScope.ScriptValue` de l'export.
  Elles associaient une référence invalide à une évaluation de script ; leur
  implication dans le crash est plausible mais non démontrée.
- Niveaux lus par prédicats sur les bâtiments existants et messages constants :
  0–256 niveaux régionaux, 0–4 témoins. Une valeur hors plage produit
  `UNSUPPORTED_LEVEL`, que le lecteur rejette ; aucune valeur n'est plafonnée.
- Pas de changement de PM, technologie, bâtiment économique, population ou carte.
  Les anciennes définitions script_values restent présentes mais ne sont plus
  invoquées par l'export. Schéma de lecture inchangé, plugin Codex non modifié.
- Aucun remplissage de journal ni « API de flush » hypothétique n'est livré.

Les fonctions globales sont présentes dans les données UI natives ; leur emploi
dans cet export corrigé **attend un nouvel essai dans le moteur**. Un contrôle
statique ne peut pas garantir la disparition du crash d'accès mémoire.

## Contrôles et reprise

153 contrôles statiques du compagnon passent. Six tests spécifiques couvrent
tous les niveaux pris en charge, le dépassement de plage, la garde locale, le
rejet des données réellement défectueuses et l'absence d'effets économiques.
Les 27 tests du lecteur passent aussi. Empreintes du principal et HEAD/index
contrôlés inchangés. Petite sauvegarde vérifiée du compagnon 0.2.0 avant copie.

**Statut : correctif statique installé, relance et nouvel export nécessaires.**
Ni le nouveau lecteur ni les nouveaux textes n'ont été déclarés validés dans
le moteur. Garder la partie dans le playset de test et reprendre le clic d'export
après relance ; ne pas continuer une campagne normale avec ce prototype.
