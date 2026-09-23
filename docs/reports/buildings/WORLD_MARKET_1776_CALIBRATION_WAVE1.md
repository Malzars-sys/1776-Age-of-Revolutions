# Marché mondial 1776 — première passe de calibration

État du travail : première passe statique appliquée, puis corrigée après confrontation avec les captures et la partie ouverte. **Les prix après ce correctif ne sont pas vérifiés** : les modifications des fichiers ne sont pas prises en compte par une partie déjà chargée. Les six captures du 1er janvier fournissent le point de départ, et l'inspection de la partie a permis de désambiguïser plusieurs icônes : le plant est l'engrais, le flacon gris le pétrole, les bouteilles la teinture et la plante avec flacons les produits chimiques industriels.

## Rectification des localisations et de l'engrais

- **Midlands, Grande-Bretagne :** une seule usine chimique préexistante dans l'historique. La capture du joueur montre bien son niveau 1 et son PM engrais inactif. Le correctif active `pm_artificial_fertilizers` tout en conservant `pm_lead_chamber_process` pour les produits chimiques. Il n'ajoute aucun niveau d'usine aux Midlands.
- **Lancashire, Grande-Bretagne :** les sept niveaux d'usine chimique inscrits par une passe antérieure ne sont pas sept usines aux Midlands. Ils sont retirés de l'historique de départ, conformément au retour du joueur. Les carrières ajoutées au Lancashire et aux Midlands restent pour l'instant ; leur effet sur le prix du calcaire doit être mesuré après rechargement.
- **Céréales britanniques :** six niveaux de champs de seigle retirés, sans supprimer de ferme : Yorkshire 21→19, Midlands 15→13, Home Counties 12→11, Est-Anglie 12→11. À PM inchangé, cela représente au maximum 180 céréales et 30 engrais de demande en moins par semaine avant emploi réel.
- **Normandie, France :** l'usine chimique ajoutée est en `STATE_NORMANDY` (niveau 1). La capture de Bretagne n'est donc pas son emplacement. La partie ouverte confirme l'usine en Normandie.
- **Sénégal :** les 24 niveaux de salines étaient *déjà présents* dans la portion `region_state:SIL` de `STATE_SENEGAL` ; la première passe n'y a ajouté que deux niveaux de centre commercial. La capture de la **Gambie britannique** montre un autre État, avec 0/2 salines potentielles : elle ne peut pas confirmer ni infirmer les salines de SIL. Aucun nouveau niveau de saline n'a été ajouté ici.
- **Sel métropolitain :** au correctif demandé ensuite, neuf niveaux de salines sont ajoutés sans nouveau potentiel de ressource : Est-Anglie (GBR) 0→3 sur 30 possibles, Bretagne (FRA) 0→4 sur 35, Languedoc (FRA) 0→2 sur 25. Le PM de base donne jusqu'à 10 sel/niveau, soit 90 unités théoriques au total, non garanties à prix réel faute de vérification de l'emploi et des échanges. Les 24 niveaux du Sénégal de SIL ne changent pas.

## Règle et mécanisme

Objectif : biens non luxueux dans la bande ±15 % du prix de base, sauf exception historique explicite ; les biens de luxe peuvent sortir de cette bande. Il ne suffit pas d'ajouter un bâtiment : le commerce autonome compare prix locaux et prix mondial, la quantité échangée varie selon le bien, et chaque centre commercial dispose d'une capacité dépendant de son personnel. Dans la partie ouverte, le centre des Home Counties employait déjà **29 points sur 28**. Les niveaux ci-dessous visent donc à corriger conjointement production et accès au commerce, sans présumer que tout le rendement nominal sera exporté.

## Changements appliqués

| Bien ou goulet | Prix initial | Changement dans les fichiers | Motif / risque de suivi |
|---|---:|---|---|
| Bois, bois dur | +35 %, +20 % | +2 camps à Götaland, +4 en Norvège orientale, +5 à Arkhangelsk, +1 dans le Maine ; centres commerciaux +1 à Götaland, +1 en Norvège orientale, +1 à Arkhangelsk | Environ +305 bois et +70 bois dur **théoriques** avant emploi ; les nouvelles papeteries et menuiseries consommeront ~150 bois. Vérifier l'emploi et les flux après rechargement. |
| Papier, meubles | +23 %, +34 % | +1 papeterie à Londres, +1 à Paris, +1 en Hollande ; +1 manufacture de meubles à Paris, +1 en Hollande | Placements dans des centres de transformation préexistants, sans nouvelles ressources cartographiques. |
| Sel | +58 % | Centre commercial +2 dans le Sénégal de SIL ; puis +3 salines en Est-Anglie, +4 en Bretagne et +2 en Languedoc. Les 24 salines de SIL restent inchangées. | L'offre métropolitaine ajoutée peut atteindre 90 sel à plein emploi. Vérifier les emplois, l'accès au marché et le prix après rechargement. Ne pas confondre Sénégal de SIL et Gambie britannique. |
| Calcaire / engrais | +75 %, +75 % | +2 carrières au Lancashire, +3 aux Midlands, +2 en Wallonie ; centre commercial +1 aux Midlands et en Wallonie. **Correctif ultérieur :** sept niveaux d'usine chimique retirés au Lancashire, PM engrais activé dans l'unique usine des Midlands. | Les cinq carrières britanniques ajoutées produisent jusqu'à 150 calcaire théoriques. Le nouvel unique PM engrais des Midlands peut en utiliser 20 et produire jusqu'à 40 engrais, sous réserve d'emploi et d'intrants. Le prix du calcaire et la pénurie d'engrais doivent être remesurés ; risque de sur-correction ou de production insuffisante. |
| Charbon / fer | +39 %, +32 % | +1 charbon et +1 fer en Wallonie ; +1 fer au Svealand | Bassins déjà pourvus de ressources, avec accès commercial renforcé en Wallonie. |
| Produits chimiques industriels | +50 % | +1 usine chimique en Normandie, PM « chambres de plomb », sans fabrication d'engrais ; +2 mines de soufre en Sicile, +1 centre commercial sicilien | La production d'acide sulfurique par chambres de plomb est attestée près de Rouen dès 1768. Le soufre sicilien est attesté au XVIIIe siècle ; `shaft_mining` est accordé au propriétaire sicilien GR3 pour que la mine puisse exister au départ. Vérifier les intrants et l'emploi. |
| Soie | +55 % | +3 plantations à Suzhou, +3 au Zhejiang ; centre commercial +2 au Guangdong | Dans la partie ouverte, la soie chinoise était à −16 % localement tandis que le prix mondial était à +59 %, avec seulement 10 unités exportées par le marché chinois. Le débouché de Canton est donc aussi important que les plantations. |
| Teinture | −32 % au 1er janvier, −24 % au 19 janvier | Floride britannique : 2 → 1 plantation d'indigo | Réduction d'un niveau, en conservant la culture historiquement attestée ; environ −30 unités théoriques. |
| Home Counties | Capacité 29/28 | Centre commercial 4 → 6 | Débloquer les échanges londoniens ; les flux réels restent à confirmer. |

La somme de la **première passe**, avant les correctifs ci-dessus, est de **+12 niveaux de centres commerciaux**, **+12 camps de bûcherons**, **+7 carrières de calcaire**, **+3 papeteries**, **+2 manufactures de meubles**, **+2 mines de fer**, **+1 mine de charbon**, **+1 usine chimique en Normandie**, **+2 mines de soufre**, **+6 plantations de soie** et **−1 plantation de teinture**. Les correctifs ultérieurs retirent séparément **7 niveaux d'usine chimique au Lancashire** et **6 niveaux de seigle britannique**, changent le PM de l'usine des Midlands et ajoutent **9 niveaux de salines métropolitaines**. Aucun niveau d'armée ou de flotte, bâtiment militaire/naval protégé, ni potentiel de ressource britannique n'a été modifié dans ces passes.

## Hors bande à réévaluer après rechargement

- **Engrais et produits chimiques** : après retrait des sept niveaux du Lancashire, l'usine des Midlands cumule deux chaînes de production. Le rendement réel est conditionné aux intrants et aux travailleurs. Vérifier aussi si les carrières britanniques ajoutées ne sont pas trop nombreuses.
- **Tissu +20 % / vêtements −23 %** : ne pas supprimer au hasard les ateliers historiques de l'Inde, de la Suisse, de la Catalogne ou de Valence. Mesurer les marchés producteurs et les PM après ce premier rééquilibrage des matières premières.
- **Clippers −43 %** : ne pas toucher aux chantiers navals dans cette passe, afin de respecter la protection du dimensionnement naval. Décision spécifique nécessaire si la surproduction persiste.
- **Pétrole +75 %** : exception historique provisoire : pas de programme d'extraction pétrolière commercial en 1776 ; la demande provient de la logique du jeu et requiert une décision séparée plutôt qu'une création anachronique de puits.
- **Verre, acier et autres petits écarts** : les valeurs changent sensiblement entre le 1er et le 19 janvier ; attendre le nouveau démarrage avant une correction de 1–2 niveaux susceptible de surcompenser.
- **Biens de luxe** : la règle tolère explicitement plus de ±15 %, donc aucune production de luxe forcée dans cette passe.

## Vérifications statiques

- Les fichiers d'historique touchés gardent un équilibre d'accolades ; le parseur retrouve les trois nouvelles salines (3/4/2 niveaux) et les nouveaux niveaux sont inférieurs aux potentiels des régions (30/35/25).
- États `s:STATE_*` dupliqués : 0 ; couples `region_state:*` dupliqués : 0.
- Niveaux des nouveaux bâtiments retrouvés par le parseur de l'historique ; les limites de ressources des régions concernées ne sont pas dépassées par ces ajouts.
- Les 11 bâtiments orphelins signalés par l'audit global concernent d'autres états déjà présents avant cette passe ; aucun des nouveaux placements ne figure dans cette liste.
- `git diff --check` : aucune erreur d'espacement (les avertissements de conversion LF/CRLF sont émis par Git sur l'arbre préexistant).

## Vérification de jeu encore nécessaire

Relancer une **nouvelle partie 1776** avec les fichiers modifiés, attendre quelques cycles hebdomadaires puis relever en priorité les niveaux effectifs et les PM des Midlands et du Lancashire, le prix britannique et mondial de l'engrais, le prix du calcaire, les niveaux/employés des salines métropolitaines et de SIL, puis les prix/exportations/importations et la capacité des centres commerciaux. Ajuster ensuite les niveaux par petits pas ; les captures de l'ancienne partie ne garantissent pas la bande ±15 % après ces modifications. Ne pas écraser la partie ouverte sans accord.

## Sources historiques et mécaniques

- [Victoria 3, journal de développement sur le marché mondial](https://store.steampowered.com/news/app/529340/view/524212840420081889?l=english) ; les PM et les capacités réelles sont également vérifiés dans les fichiers locaux du jeu et du mod.
- [Historic England, extraction de calcaire autour de Dudley](https://historicengland.org.uk/listing/the-list/list-entry/1021381?section=official-list-entry) ; [Historic England, four à chaux de Worsley vers 1770](https://historicengland.org.uk/listing/the-list/list-entry/1427469).
- [Service géologique suédois, histoire des mines suédoises](https://www.sgu.se/mineralnaring/svensk-gruvnaring/historiska-gruvor/).
- [Académie des sciences, chimie parisienne et usine de Rouen à chambres de plomb](https://comptes-rendus.academie-sciences.fr/chimie/articles/10.1016/j.crci.2012.04.009/).
- [Ville de Caltanissetta, extraction du soufre sicilien depuis le XVIIIe siècle](https://www.comune.caltanissetta.it/it/vivere/745986).
- [Columbia University, commerce Qing et port de Canton](https://afe.easia.columbia.edu/qing/economy.html) ; [Hong Kong Museum of Art, exportations de soie à Canton](https://hk.art.museum/en/web/ma/exhibitions-and-events/a-tale-of-three-cities.html).
- [Library of Congress, exploitation d'indigo en Floride britannique](https://www.loc.gov/loc/lcib/0304/papers.html).
- [Historic England, salines de Southwold actives en 1776](https://historicengland.org.uk/research/results/reports/6966/HistoricSeascapeCharacterisationEastYorkshiretoNorfolk3) ; [département de Loire-Atlantique, salines de Guérande et de la baie de Bretagne](https://www.loire-atlantique.fr/44/culture-et-patrimoine/le-musee-des-marais-salants-a-batz-sur-mer/c_1272623) ; [ministère français de la Culture, concession des salins d'Aigues-Mortes vers 1775](https://pop.culture.gouv.fr/notice/merimee/IA00128147).
