# Wolgast — territoire suédois, sans inventer une ville native

La précision du joueur est confirmée : **Wolgast n'est pas représentée par un hub urbain natif** dans la région. La recherche exacte du nom dans les localisations effectives et l'inspection des instances de hubs ne trouvent aucun Wolgast. Dans `STATE_POMERANIA`, ID57, le hub `city` est Stettin, le `port` est Greifswald, le `mine` est Schwedt, le `farm` est Köslin et le `wood` est Schievelbein. Le CSV `PEENE_NATIVE_LOCATORS.csv` conserve les instances de la fenêtre locale ; l'inventaire des noms utilise aussi les clés `HUB_NAME_STATE_POMERANIA_*` du jeu.

Le point `(4410,735)` de R7/R8 n'était donc **pas un locator Wolgast prussien**. C'était la cellule contenant une estimation géographique provisoire. Aucun locator, nom de hub, bâtiment ou point de rendu n'est déplacé ou créé dans R9. Le joueur ne verra pas apparaître une nouvelle ville appelée Wolgast du seul fait de ce correctif.

## Correction réellement appliquée

R9 autorise une correction pratique du secteur de Wolgast, historiquement suédois, à l'échelle du jeu. La carte Mayer/Lotter1763 conservée a été relue ; elle distingue le territoire continental suédois et l'Usedom prussienne. Les quatre profils natifs figés R5 sont réutilisés comme diagnostics, sans optimisation supplémentaire ni revendication de précision cadastrale.

| Cellule | Avant | Après | Fonction |
| --- | --- | --- | --- |
| (4409,735) | xE1A03A / PRU | x567452 / SWE | raccord contigu au corridor R8 |
| (4410,735) | xE1A03A / PRU | x567452 / SWE | couvre le point géographique provisoire de Wolgast |

**Deux cellules**, pas une nouvelle province. Les quatre estimations centrales conservées de Wolgast tombent désormais dans SWE ; cela démontre l'effet de l'approximation sur ces diagnostics, **pas une validation géographique indépendante** de ces points. Le modèle sélectionné donne `(4410.1394,735.0490)` ; les sensibilités publiées R5 restent inchangées et ne deviennent pas un intervalle de confiance.

Les deux cellules sont de la terre dans le bitmap physique natif, sans eau ou nouveau canal recoloré. Leur rattachement ne déconnecte ni le RGB suédois ni son parent prussien. Il n'y a pas de dilation de toute une île, ni de transfert de tout `xE1A03A`.

### Limite explicite du nouveau tracé

La règle R8 exigeait que le bord droit de chaque cellule reste à l'ouest de toutes les rives modernes projetées à mi-ligne. **Cette règle plus conservatrice n'est pas satisfaite par tout le complément R9** : à Y735, le nouveau bord X4411 dépasse d'environ1.11pixel la variante occidentale de cette aide de dessin (X4409.8888). Ce n'est pas caché ni présenté comme un respect exact du Peenestrom historique. La courbe moderne, l'origine des cellules et le centre réel d'une ville ne sont pas la même chose.

Il s'agit d'une **approximation politique locale R9**, acceptée par la stratégie de résolution du jeu demandée, pour représenter le secteur suédois de Wolgast sans déplacer une ville inexistante. La souveraineté de l'Usedom historique n'est pas changée ; les autres cellules de l'approche orientale, notamment X≥4411 et les points de contrôle intérieurs des îles, restent PRU. Une restitution fine des deux rives demanderait une résolution et des homologues que le raster actuel ne garantit pas.

## Conservation et clôture pratique

- SWE : **398→400** cellules ; PRU parent : **292→290**.
- Les398 cellules suédoises antérieures et chacune des41 cellules R8 sont intactes.
- Stralsund, Greifswald et l'intérieur de Rügen donnent SWE dans les diagnostics conservés ; Anklam, Demmin, Usedom et Wollin donnent PRU. Le port natif Greifswald est réellement SWE. Les autres coordonnées restent des contrôles politiques grossiers, pas des homologues urbains certifiés.
- Toutes les lignes Y≥740 restent identiques, comme les approches orientales X≥4411. Pas de nouveau RGB, State_ID, membre du bloc ou droit impérial ajouté.
- **235 habitants** redistribués PRU→SWE par les plus forts restes existants, poids3586:2 sur3588cellules prussiennes régionales avant R9. Profils transférés :209north_german/default,21north_german/catholic,4polish/default,1ashkenazi/default. Ce n'est pas un recensement de Wolgast.
- Poméranie PRU421517, SWE47019, total468536 ; monde835804980. Bâtiments, PM, propriétés, infrastructures, unités et recrutements restent identiques.

Peendamm est **omis comme enclave distincte**, conformément à la décision explicite de résolution du joueur. Il n'est pas agrandi pour former un nouveau pays ou une province disproportionnée.

Statut : **PEENE_GAMEPLAY_COMPLETE**, au sens de représentation politique pratique et de conservation statique. Ce n'est ni une certification de toutes les limites historiques ni une validation moteur. Aucun test manuel R8/R9 n'a été communiqué.
