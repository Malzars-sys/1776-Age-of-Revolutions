# Organisation scientifique du travail — extension urbaine

Patch du 23 octobre 2026 : **21 industries couvertes**, soit les vingt manufactures du catalogue et les centrales électriques. Sept manufactures possédaient déjà le groupe ; les treize autres et les centrales le reçoivent désormais.

## Périmètre et fonctionnement

Le groupe générique `pmg_scientific_management` est ajouté à : alimentation, textile, meubles, verrerie, papier, chimie, explosifs, produits synthétiques, acier, chantiers navals, ciment, raffinage, métaux non ferreux et centrales électriques.

Les groupes déjà présents sont conservés, y compris les variantes automobile et électrique. Aucune industrie n’a deux groupes d’organisation scientifique du travail.

Le PM et son icône sont réutilisés sans modification. Déblocage : `corporate_management`. La première option reste « Sans organisation scientifique du travail » ; aucune activation forcée n’est ajoutée.

Les effets existants restent les mêmes : par niveau à pleine capacité, 5 papiers, 10 services et 1 donnée de recherche organisée en intrants ; −500 ouvriers, −250 machinistes, +500 employés et +250 ingénieurs ; coefficient de débit `building_throughput_add = 0.005` multiplié par le niveau. Les qualifications requises et les cumuls avec d’autres automatisations demeurent à observer en jeu.

Aucun ajout aux centres urbains de services, exploitations agricoles, ports ou bâtiments gouvernementaux. L’extension du transport agricole et les productions routières 5/10/15 de la passe précédente sont conservées.

## Modifications et vérification

Cinq fichiers de bâtiments sont modifiés, exclusivement par quatorze lignes de référence au groupe existant. Toutes les autres données de ces fichiers sont conservées octet pour octet après retrait des lignes ajoutées.

**178/178 contrôles statiques réussis** : couverture des 21 industries, conservation des sept variantes existantes, absence de doublons, option inactive par défaut, technologie et recettes conservées, exclusions et conservation des données.

Les **2 420 fichiers hors périmètre** sont identiques à l’instantané de début de passe : carte/populations, sociétés Anzin et Saint-Gobain, icônes, technologies, fortifications/génie, États-Unis/Minutemen et accords sont préservés. Aucune écriture vanilla ni opération Git d’écriture ; HEAD, branche et index inchangés.

Le moteur n’a pas été exécuté. Après redémarrage, vérifier le groupe et ses deux choix dans une industrie nouvellement équipée puis dans une centrale, le verrou technologique et la conservation d’une variante déjà présente. Après activation dans une partie de test disposant de la technologie, vérifier les intrants, emplois par profession et débit, puis sauvegarder/recharger. Aucun résultat économique ou d’interface en jeu n’est revendiqué.

`BASELINE.json`, les copies initiales des cinq fichiers, `VALIDATION.json` et `MANIFEST.json` consignent le périmètre et les empreintes.
