# Corps du génie — contre des fortifications terrestres

19 octobre 2026 — **ENGINEER_CORPS_READY_FOR_RUNTIME_VALIDATION**.

L’unité **Corps du génie** se débloque avec la technologie existante du même nom (`permanent_engineer_services`). Elle appartient à un groupe de spécialistes distinct de l’infanterie. Les autres unités et leurs améliorations restent inchangées.

**2 073 contrôles statiques réussis.** Les 1 982 fichiers protégés sont identiques au début de cette passe ; le vanilla canonique, HEAD et l’index Git sont inchangés. Aucun essai dans Victoria 3 n’a été effectué. Les résultats sont des projections des scripts réels, pas une simulation du moteur. Voir [VALIDATION.json](VALIDATION.json) et [RUNTIME_VALIDATION.md](RUNTIME_VALIDATION.md).

## Réduction locale de la protection

Chaque **bataillon à plein effectif de 1 000 hommes**, présent dans la bataille du côté adverse, retire **un point de pourcentage** aux trois bonus du fort terrestre : réduction des provinces perdues, réduction des pertes subies et défense terrestre.

| Cinq niveaux de fort, garnison complète | Protection sans génie adverse | Bataillons du génie pour annuler les trois bonus |
|---|---:|---:|
| PM1 — simples | 25 % | 25 |
| PM2 — renforcées | 50 % | 50 |
| PM3 — avancées | 75 % | 75 |

Un fort avancé à cinq niveaux conserve 50 points de protection face à 25 bataillons du génie et 25 points face à 50 bataillons. À 75 bataillons, son supplément est nul. Les sapeurs supplémentaires ne transforment jamais cette protection en pénalité.

Le calcul utilise les unités de **cette bataille**, filtrées par leur type et l’état de guerre de leur propriétaire avec le défenseur. Les alliés attaquants présents peuvent donc contribuer. Les sapeurs du défenseur ou de ses alliés ne réduisent pas leur propre fort. Des unités ailleurs dans le pays, dans une autre bataille ou dans une réserve absente du combat ne sont pas parcourues par cette liste.

Les bataillons incomplets contribuent selon leur effectif : 24 bataillons de 500 hommes valent 12 bataillons complets et laissent 13 points à cinq niveaux simples. Les bataillons vides ne contribuent pas. Les données d’effectif du moteur restent à vérifier au cours d’un véritable combat.

La puissance des forts conserve les quinze paliers antérieurs et l’arrondi au point de puissance le plus proche. Après soustraction des équivalents-bataillons du génie, le reliquat est arrondi au point de pourcentage le plus proche puis borné entre 0 et 75. L’arrondi final peut représenter un demi-point d’écart avec un effectif intermédiaire. Les seuils à effectif complet sont exacts.

La portée des forts reste celle de la passe précédente : défense dans une province possédée et contrôlée par le pays du côté concerné, État intérieur appartenant au même pays, bâtiment et garnison présents. Le génie n’annule aucun modificateur national, aucun effet de Liberty Or Death et aucun bonus naval. Il retire seulement le supplément fourni par les fortifications terrestres.

## Batailles et compatibilité

Le générateur conserve les 21 conditions natives et tous les identifiants des conditions fortifiées antérieures. Les 75 valeurs possibles du reliquat disposent de positions normales et de variantes de poursuite, déroute et retraite contrôlée : 300 conditions fortifiées et une condition de sortie.

Chaque variante conserve les modificateurs et le poids de sa condition d’urgence native. Le supplément du fort est ajouté au reliquat effectif. Lors d’une annulation complète, le parcours retrouve les conditions natives ; une condition déjà fortifiée perd son supplément au prochain contrôle de transition natif. Une reprise de la protection peut sélectionner de nouveau une position fortifiée.

Il n’y a aucun ajout de modificateur au pays ou au commandant, aucune impulsion quotidienne, aucune création d’unités de départ et aucun changement de carte ou d’armées historiques. Le fichier natif adapté `00_battle_conditions.txt` reste byte pour byte identique à celui de la passe R3. Les définitions générées et leurs références restent à fusionner explicitement avec un autre mod qui modifie les mêmes conditions.

Les formules de script parcourent les unités de bataille à chaque évaluation native ; le coût réel en présence de nombreux combats reste à mesurer. Le cache de l’outil de projection sert uniquement à accélérer ses scénarios immuables et ne constitue pas une affirmation sur un cache du moteur.

## Recrutement et entretien

| Paramètre par bataillon | Valeur |
|---|---:|
| Effectif maximal | 1 000 |
| Capacité de ravitaillement | 30 |
| Attaque / défense de base | 15 / 20 |
| Perte de moral | 10 |
| Pénalité de débarquement | −25 % |
| Entretien : armes légères / outils / bois | 1 / 1 / 0,5 |

Les statistiques ordinaires suivent le niveau d’infanterie à mousquet du mod ; l’outillage et le bois représentent les travaux de siège. Aucun bonus de siège national n’est porté par cette unité. Le groupe ne remplace pas l’infanterie par défaut et aucune chaîne d’amélioration existante ne conduit automatiquement au génie. Le drapeau permettant la conscription sous levées paysannes est désactivé.

L’IA dispose d’un poids de recrutement de 15 pour ce groupe après la technologie, et de zéro avant. Les autres poids de sa stratégie ont été comparés intégralement à l’état initial. Ce poids donne une cible de composition ; les recrutements réels et le budget demandent un essai moteur.

## Illustrations selon la culture

Le choix se fait sur la **culture de l’unité**, selon le contrat natif des illustrations, sans condition sur le pays joueur.

| Variante | Illustration fournie | Routage |
|---|---|---|
| Générique | Uniformes kaki, nouvelle image `a42ef6f7…` | Repli final, sans condition |
| Européenne | Uniformes bleus, image `f3ed7f48…` | Graphismes européens, français et balkaniques, hors cultures américaines |
| Amériques et Caraïbes | Scène tropicale, image `c7df8ec0…` | Graphismes américains/brésiliens et héritages des cultures de colons nord-américains, latino-américains et de la diaspora africaine |
| Asie orientale | Image `577907c5…` | Graphismes est-asiatiques |
| Asie du Sud | Image `8b046f8b…` | Graphismes sud-asiatiques |
| Afrique | Image `cfbe8a7c…` | Graphismes africains, hors branche américaine |
| Monde arabe | Image `00c8ed82…` | Graphismes arabes |

La branche américaine est prioritaire : les cultures yankee, canadiennes, mexicaine, caribéenne, brésilienne et afro-américaine ne reçoivent pas l’image européenne ou africaine du fait de graphismes partagés. Les cultures espagnole et portugaise restent dans la branche européenne. La variante européenne n’est pas limitée à la France. Les cultures sans branche dédiée, par exemple polynésiennes, utilisent le générique.

Les sept PNG originaux sont conservés. Les exports utilisent un recadrage carré centré et un redimensionnement au format natif des unités : DDS BGRA8, 512 × 512, dix mipmaps. Aucune image générée ni retouche picturale. Les aperçus ont été contrôlés visuellement. [Planche des variantes](CULTURAL_PREVIEW.png), [empreintes et sources](ART.json).

Les noms, descriptions et explications du contre sont livrés en français et en anglais, UTF-8 avec BOM et sans doublons ajoutés.

## Sources et preuves

- Vanilla canonique local : `common/combat_unit_types/00_land_combat_unit_types.txt`, `common/combat_unit_groups/00_combat_unit_groups.txt`, `common/battle_conditions/battle_condition.md`, `common/cultures/00_cultures.txt`, `common/culture_graphics/00_culture_graphics.txt`, `gui/texticons.gui`, `gui/military_formation_panel.gui` et les exemples de valeurs scriptées.
- Le déblocage et les statistiques de mousquet proviennent des définitions présentes dans ce dépôt au début du lot ; la technologie garde son contenu existant.
- Documentation générée du moteur 1.13, conservée dans `sources/` : [triggers.log](https://github.com/Victoria-3-Modding-Co-op/Modding-Digests/blob/main/1.13.0/docs/triggers.log) et [event_targets.log](https://github.com/Victoria-3-Modding-Co-op/Modding-Digests/blob/main/1.13.0/docs/event_targets.log). Elle confirme les listes d’unités en portée bataille, le type d’unité, les propriétaires, l’effectif, l’état de guerre et les comparaisons culturelles utilisés. Le script local reste l’autorité pour la version installée ; la compatibilité moteur effective n’est pas certifiée par cette seule documentation.
- [État initial du lot](BASELINE.json), copies avant modification dans `baseline/`, résultats précédents des forts dans `fortifications_R3/`, [manifeste final](MANIFEST.json).

Les contrôles couvrent les seuils exacts, la réduction partielle, l’effectif, le propriétaire, les alliés, les unités ordinaires, les 75 valeurs du reliquat, les transitions et les statistiques d’urgence, la reprise du parcours natif, les cultures réelles, les sept assets et la préservation des travaux concurrents. L’essai moteur reste requis pour le recrutement, les achats de biens, l’affichage, le contenu exact de la liste de bataille, les transitions, la sauvegarde et les performances.
