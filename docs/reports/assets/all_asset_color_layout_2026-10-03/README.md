# Couleurs des assets : correction étendue

3 octobre 2026. La première passe était trop limitée : la capture suivante montre le bien **calcaire** encore bleu alors que sa carrière est corrigée. Le prochain lot reste suspendu ; aucun nouveau dessin n'est généré.

## Cause et portée

Nos exports non compressés utilisaient des octets RGBA. Les références vanilla installées pour **les cinq familles** utilisent des octets BGRA avec les masques A8R8G8B8. Un décodeur respectant les anciens masques pouvait retrouver le PNG original, mais cette vérification ne détectait pas l'incompatibilité de stockage observée en jeu. Lire l'ancien stockage comme le natif reproduit précisément le calcaire bleu de la capture. Le détail interne du moteur reste une déduction, pas une inspection du moteur.

L'inventaire intégral des en-têtes DDS de `gfx` retrouve **38 exports RGBA restants**, tous identifiés dans les manifestes des créations approuvées : six biens, quatre technologies, treize méthodes de production et quinze illustrations militaires. Les quatre bâtiments déjà corrigés sont également revérifiés, mais pas reconvertis. Les autres textures déjà natives, les assets externes compressés et les textures 3D restent intacts.

## Correction sans retouche

Échange des octets de stockage rouge/bleu ET de leurs masques, pour toutes les versions réduites de chaque texture. **Les couleurs logiques de la peinture, tous les pixels alpha, les dimensions et les mipmaps restent strictement identiques.** Un objet bleu dans son PNG approuvé demeure bleu ; il ne s'agit pas d'appliquer un filtre chaud à tous les dessins.

Les PNG approuvés restent inchangés. Les 38 DDS originaux sont conservés dans `backups/`, avec leur empreinte dans le nom. Les anciens rapports d'export et leurs empreintes sont conservés comme preuves historiques ; le contrôle retrouve exactement l'ancienne empreinte en inversant uniquement cette conversion de format.

Les six outils d'export concernés utilisent désormais une convention native commune pour toutes ces familles. Les contrôles de stockage natif ne sont plus limités aux bâtiments.

## Preuves et contrôles

- [Diagnostic préalable](diagnosis.json) : 42 sources approuvées vérifiées pixel par pixel à la taille cible ; références vanilla par famille ; inventaire des anciens masques.
- [Validation de conversion](validation.json) : **38 conversions supplémentaires**, quatre bâtiments préservés et **1 644 autres fichiers de jeu inchangés** par rapport à l'état juste avant la conversion. Cet état comprend `common`, `gfx`, `events`, `gui`, `localization` et `map` ; aucune référence, recette, caractéristique ou frontière n'est modifiée.
- [Second contrôle indépendant](independent_validation.json) : **42 assets et 380 mipmaps** ; Pillow décode séparément les originaux et les sorties, puis confirme la lecture BGRA explicite et les empreintes des sources.
- [Comparaison des couleurs](COMPARAISON_COULEURS.png) : PNG approuvé à gauche, simulation de l'ancien stockage lu comme le natif au centre, fichier DDS corrigé à droite. **La colonne centrale n'est pas une capture du jeu.**
- [Tous les fichiers corrigés, décodés suivant la convention native](TOUS_LES_DDS_CORRIGES.png).

Les vérifications ASSET4 (icônes et unités) et ASSET5–6 (sources, raccordements et DDS courants) réussissent après conversion. Pour ASSET5–6, le mode `--assets-only` conserve les anciens rapports globaux : il vérifie les assets actuels, pas une réintégration de l'ancien lot. L'absence de changement de gameplay dans cette correction est vérifiée séparément par l'état de référence actuel.

Le validateur global historique du laboratoire signale quatre différences de bâtiments par rapport à son ancien état de référence : carrière, mine de phosphate, raffinerie et infrastructure privée. Aucune erreur de stockage DDS n'est signalée. Ces fichiers étaient déjà dans cet état avant cette passe ; ils restent strictement inchangés. Ce résultat n'est donc pas présenté comme un succès du contrôle global historique, et ses garde-fous ne sont pas assouplis.

## Limite et vérification en jeu

**Le rendu moteur de cette passe reste à confirmer par le joueur.** Aucun lancement ni rechargement du jeu n'est revendiqué. Redémarrer complètement Victoria 3 pour éviter les anciennes textures en mémoire ; une nouvelle partie n'est pas nécessaire pour une correction de textures.

Reproduction sans modifier les fichiers du jeu : `node tools/fix_asset_color_layout.cjs --verify`, puis `python tools/validate_asset_color_layout.py`. L'audit initial refuse d'écraser le diagnostic ; la conversion refuse de poursuivre si les fichiers du jeu ou les sources ont changé depuis l'audit. Ne pas réexécuter les anciens exports pour remplacer leurs preuves historiques.
