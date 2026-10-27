# Images et exports

Lire ce document uniquement pour le périmètre indiqué dans `AGENTS.md`. Il ne lance aucune mission.

- **A01.** Conserver les masters finaux approuvés, leur provenance et les DDS utilisés ; le nom `previews/` ne rend pas un master jetable. Placer les nouveaux dérivés temporaires de contrôle dans `.asset-cache/`, sans les versionner. Consulter le registre des sources ; ne pas effacer les archives probantes ni déplacer les sources historiques pour normaliser les chemins.
- **A02.** Préserver alpha, proportions, dimensions et stockage attendus par la référence native ; contrôler les mipmaps et références. Réutiliser les variantes communes existantes des flèches de groupes, sans redessiner chaque groupe. Pour les dessins individuels de PM, appliquer le cycle existant preview/approbation/intégration par lots de trois, sauf instruction explicite délimitant un autre lot. Une exception locale de palette ne remplace pas le contrat général.
- **A03.** Distinguer vérification et installation : `tools/rebuild_asset_icons.cjs --verify` contrôle les exports ; `--install-approved --asset=nom_exact` écrit un DDS et exige le périmètre autorisé. Une nouvelle génération depuis un ancien prompt est une proposition, pas une reproduction garantie du master approuvé.

Traçabilité de chaque règle : [inventaire et sources](../docs/reports/agents/PERMANENT_RULES_AUDIT.md).
