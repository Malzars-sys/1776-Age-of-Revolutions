# TECH6A-3F — Prompt de restylisation des icônes PM Fine Food

Utiliser ce prompt en mode **image-to-image**, séparément sur chacune des trois icônes problématiques. L’image fournie est une référence structurelle obligatoire : son sujet et sa fonction doivent rester immédiatement reconnaissables.

## Prompt

Restylise l’icône source pour qu’elle s’intègre naturellement parmi les icônes vanilla des méthodes de production de Victoria 3. Modifie uniquement le traitement visuel ; conserve le sujet, la composition générale, les objets, leur orientation et le sens fonctionnel de l’icône source.

Adopte le langage visuel des icônes vanilla de méthodes de production : illustration 2D peinte et légèrement gravée, formes simples et massives, silhouette immédiatement lisible à très petite taille, contours épais brun-noir, ombres courtes et mates, volumes suggérés par deux ou trois niveaux de valeur, détails fortement simplifiés. Le rendu doit ressembler à un pictogramme industriel du XIXe siècle peint à la main, et non à une illustration réaliste ou à un objet 3D.

Utilise une palette limitée, chaude, mate et désaturée, proche des icônes vanilla alimentaires : brun charbon `#181613`, brun sombre `#554834`, ocre brun `#755F42`, taupe `#937F5F`, beige patiné `#AF9D7D` et lumière parchemin `#BBA686`. Les accents doivent rester rares et assourdis. Remplace l’or vif, les reflets métalliques brillants, les blancs purs et les couleurs fortement saturées par ces tons patinés.

Optimise toute la composition pour une taille finale de **104 × 104 px** : un seul groupe visuel centré, grandes masses compactes, marges transparentes régulières, aucun petit détail indispensable à la lecture. L’icône doit rester claire lorsqu’elle est affichée à environ 56 px dans l’interface. Conserve un fond entièrement transparent et une ombre de contact discrète. N’ajoute ni cadre carré, ni cercle de fond, ni texte, ni lettre, ni chiffre.

Contraintes propres à la variante :

- **Nourriture épicée** : conserver les épices et le verre comme sujet principal, mais les réduire à une silhouette compacte en aplats ocre, taupe et beige ; aucun éclat doré.
- **Nourriture raffinée épicée** : conserver exactement le même langage visuel que la variante précédente et garder les deux étoiles comme seul signe d’amélioration ; étoiles petites, simples et couleur parchemin mate, sans glow.
- **Aucune préparation raffinée** : conserver le même sujet barré et le symbole d’interdiction, mais simplifier fortement l’ensemble ; cercle et barre épais en beige patiné avec contour brun-noir, sans métal brillant.

Négatif : photoréalisme, rendu 3D, matériau métallique poli, or vif, glow, bloom, néon, forte saturation, micro-détails, texture photographique, longues ombres, perspective complexe, décor, assiette, cadre ajouté, texte, watermark, modification du sujet, nouvel objet.

Sortie : PNG carré avec transparence alpha, composition centrée, sans marge excessive. Générer les trois résultats comme une série cohérente partageant exactement la même palette, le même contour, le même contraste et le même niveau de simplification. Ne pas convertir en DDS durant la génération ; la conversion finale vers DDS sera effectuée après validation visuelle.

## Fichiers cibles après validation

- `spiced_food_preparations.dds`
- `refined_spiced_food_preparations.dds`
- `no_fine_food_preparations.dds`
