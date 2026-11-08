# Icônes navales corrigées — transfert bloqué

8 novembre 2026 — `GENERATED_CORRECTED_MASTERS_TRANSFER_BLOCKED_NOT_INSTALLED`.

Le joueur a rejeté le rendu métallique initial et demandé une couleur unie, un dégradé clair en haut/foncé en bas et un aspect papier en bas-relief. Les trois dessins corrigés ont été générés et montrés dans le chat. Ils sont conservés dans les fichiers natifs suivants :

| PM | Maître corrigé | Fichier attendu dans `masters/` |
| --- | --- | --- |
| Construction navale artisanale | `libfile_c534b3feb5a4819190dbf19710b4b964` — Coque de bateau et herminette.png | `artisanal_shipbuilding.png`, ou son nom français original |
| Doublage en cuivre | `libfile_c86c0896d3288191b8731200724646ad` — Icône de coque violette en relief.png | `copper_sheathing.png`, ou son nom français original |
| Coques non traitées | `libfile_de9bf3a72a0481919d61cafbe7d0d853` — Icône de coque violette barrée.png | `no_copper_sheathing.png`, ou son nom français original |

La variante barrée reprend le dessin du doublage avec un cercle d'interdiction de la même famille violette. La palette est tirée de `pm_palette_rules.json` : production ocre, secondaire violet. Les références vanilla effectivement décodées et montrées sont dans `../references/vanilla_reference_sheet.png`.

## Blocage observé

La matérialisation a résolu les trois fichiers avec leurs identifiants et tailles exactes, mais le téléchargement par le helper fourni échoue : résolution DNS impossible (`getaddrinfo failed`) vers l'hôte des images. Le navigateur a ensuite refusé une page locale de transfert, car le protocole `file:` est interdit par sa politique. Aucune tentative de contournement de ce refus n'est autorisée ni effectuée.

Les images corrigées n'ont donc pas pu être copiées dans le mod. Aucun DDS corrigé n'est installé, aucune référence vers un fichier manquant n'est activée, et les trois placeholders concernés restent présents. Les masters métalliques initiaux sont conservés comme preuves rejetées ; ils ne sont pas substitués aux images corrigées.

## Finalisation préparée

`tools/export_naval_pm_icons_20261108.cjs` est prêt pour les trois maîtres corrigés. Il vérifie les tailles exactes, l'alpha et les dimensions 1254 × 1254, prépare trois DDS natifs 208 × 208 BGRA8 à huit mipmaps, puis peut installer le lot et ses seules références de PM avec `--install-approved`. Il refuse un master manquant ou remplacé par un fichier différent. Le registre des sources est complété sans réécrire ses anciennes entrées.

Une copie manuelle des trois fichiers corrigés dans le sous-dossier `masters/` permet de reprendre sans génération supplémentaire. Le script reconnaît soit les noms courts du tableau, soit les noms français originaux. La conversion et l'intégration des trois DDS restent **non exécutées** tant que ces octets ne sont pas disponibles localement.
