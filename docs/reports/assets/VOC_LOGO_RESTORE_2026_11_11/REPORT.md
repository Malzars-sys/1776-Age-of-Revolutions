# VOC — restauration du logo, 11 novembre 2026

À la demande du mainteneur, remplacement de la seule texture de la Compagnie néerlandaise des Indes orientales dans le dossier de travail. Le fichier courant, limité à 256 × 256 pixels et issu d'une image déjà dégradée, est remplacé par un DDS de 1 024 × 1 024 pixels avec onze niveaux de mipmaps.

Source retrouvée dans Téléchargements : `east india company logo - Google Search.jpg`, 630 × 630 pixels. Cet original est conservé dans `sources/`. Une restauration par l'outil intégré d'édition d'images retire le bleu et reprend le sceau en encre charbon sur papier ivoire, avec extérieur transparent. Le monogramme VOC, la date 1602, les inscriptions et les ornements du sceau servent de référence ; il s'agit d'une restauration graphique générée, pas d'une copie pixel à pixel. Le master final de 1 254 × 1 254 pixels est conservé dans `masters/`. Le prompt exact, la provenance et les empreintes figurent dans `ART_PROVENANCE.json`.

La texture installée reste `gfx/interface/icons/company_icons/historical_company_icons/nl_voc_medallion_1776.dds` : la définition de compagnie et ses références restent identiques. L'ancien DDS et le registre avant ajout sont conservés dans `before/`. Les 215 entrées préexistantes du registre des sources sont préservées ; une entrée reproductible est ajoutée pour ce seul logo. L'autorisation est la demande actuelle de remplacement ; aucune approbation humaine postérieure de l'aperçu n'est inventée. Le cycle par lots de PM ne concerne pas ce logo de compagnie.

Contrôles réalisés : reconstruction exacte avec l'exporteur existant, lecture du DDS, stockage BGRA natif, chaîne complète de mipmaps, transparence des coins et conservation de l'alpha. Aucun pixel opaque à dominante bleue selon le seuil consigné dans `CHECKS.json`. Le master et le DDS décodé ont été inspectés visuellement. Les règles de la compagnie sont inchangées.

Aucun lancement moteur, changement de version, écriture Git, mise à jour des copies Steam Build ou téléversement Steam dans cette passe. Le rendu final à la taille réelle de l'interface reste à observer en jeu.
