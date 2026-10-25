# USA-FRENCH-SUPPORT-1776

**IMPLEMENTED — READY_FOR_RUNTIME_VALIDATION.** Le moteur n'a pas été lancé par l'agent. Les calculs ci-dessous lisent une sauvegarde existante ; les projections d'aide sont arithmétiques, sans simulation de marché ou de campagne.

## Audit avant choix des montants

Source : autosave_exit.v3, version 1.13.11, date 1776.1.1, joueur FRA. Copie décodée en lecture seule par l'outil Rakaly déjà présent ; original inchangé. Empreinte, valeurs et inventaire dans ECONOMIC_AUDIT.json et STARTING_BUILDINGS.json. La date correspond au départ, mais cette sauvegarde française n'est pas nécessairement la partie exacte de la capture américaine. La localisation native `lesson_basics_treasury_show_more` précise que le solde supérieur est **hebdomadaire**.

| Poste hebdomadaire identifié | USA | FRA |
|---|---:|---:|
| Recettes totales | 3 714,24 £ | 106 533,00 £ |
| Dépenses totales | 31 181,00 £ | 74 774,44 £ |
| Solde | −27 466,77 £ | +31 758,56 £ |
| Salaires administratifs | 15 541,19 £ | 9 781,59 £ |
| Biens militaires des bâtiments logistiques | 1 466,70 £ | 12 968,98 £ |
| Salaires militaires | 1 838,82 £ | 16 691,40 £ |
| Subventions | 5 302,15 £ | 5 614,39 £ |
| Pertes de parts publiques identifiées | 591,94 £ | 4 923,21 £ |
| Trésorerie sauvegardée | 152 078,56 £ | 663 766,27 £ |
| Capacité de crédit sauvegardée, pas une dette | 7 390 785,57 £ | 30 672 662,68 £ |

L'origine principale **identifiée** du déséquilibre est structurelle : 53 niveaux scriptés d'administration américaine contre 34 français, avec des méthodes, emplois et salaires différents ; recettes américaines très faibles et 5 302 £ de subventions. Les coûts militaires identifiés ne suffisent pas à expliquer seuls le déficit. Le bâtiment interne building_railway représente les transports adaptés par le mod : ne pas assimiler ses 95 niveaux américains à 95 chemins de fer modernes, ni les retirer sans étude.

Le vecteur des dépenses comprend aussi 610,97 £ de dépenses diplomatiques et 5 829,24 £ dans deux positions dont la désignation exacte n'est pas établie par les champs nommés de la sauvegarde. Ils restent inclus dans le total vérifié ; ils ne sont pas rebaptisés « intérêts » ou « entretien de la marine » sans preuve. La trésorerie est positive. Le taux de prêt de base du mod est 20 % avant technologies, rang et autres modificateurs ; le taux effectif affiché n'est pas reconstruit ici. Aucun intérêt contractuel nouveau n'est appliqué par ce lot.

Les prix américains sauvegardés sont 57,64605 £ pour les armes légères et 17,5 £ pour l'artillerie ; les prix français 68,28765 £ et 17,5 £. Les indices sont rapprochés de l'ordre des définitions effectives des biens (ammunition, small_arms, artillery en tête). Ces prix ne démontrent pas une pénurie initiale d'armes. Les barrières commerciales et voies maritimes peuvent changer ensuite. Les 411,50 £ de droits américains attestent une activité commerciale ; l'audit ne reconstitue pas chaque voie commerciale de la sauvegarde. Le traité nouveau fournit son propre suivi natif des expéditions, limites de marché et interruptions.

Complément vérifié dans les gestionnaires natifs de traités, articles et voies maritimes de cette sauvegarde : aucun traité ni article de transfert monétaire ou de biens ne concerne USA. FRA possède cinq traités avec d'autres pays, sans transfert monétaire ou matériel vers USA. Les voies maritimes enregistrées comptent zéro liaison propre à USA et cinq connexions portuaires françaises, pour un coût de capacité de convois cumulé de 4,28106 (ce chiffre n'est pas une dépense en livres). Ces connexions ne reconstituent pas les ordres de commerce de chaque centre sur le marché mondial. L'absence de transfert bilatéral américain est établie dans `TRADE_AND_TREATY_AUDIT.json`, plutôt que déduite seulement des droits de douane. Le nouveau secours ne double donc pas un article d'aide franco-américaine déjà enregistré dans cette sauvegarde.

Les technologies, l'imposition et les lois de départ ne sont pas modifiées : USA, fiscalité foncière et levées paysannes ; FRA, fiscalité foncière et armée professionnelle. Aucun impôt américain de consommation n'est ajouté en compensation. Deux niveaux américains d'armurerie, aucune fonderie d'artillerie ; sept armureries et quatre fonderies françaises. Le potentiel de quinze conscrits reste non activé par nos scripts : à effectif complet, leur seule recette de type demande quinze unités supplémentaires d'armes, environ 864,69 £ aux prix de cet instant avant lois, mobilisation et logistique. Leurs salaires et l'effet des retraits de travailleurs ne sont pas simulés.

L'ancien bonus +60 000 était une recette fixe hebdomadaire ; le rétablir aurait porté arithmétiquement ce solde à +32 533,23 £, sans financement français. Il reste supprimé. La sauvegarde ne contient pas les anciens modificateurs de dette chez USA/FRA ; leur disparition ne sert donc pas à produire artificiellement l'amélioration du scénario.

## Accord installé

Offre française programmée pour le 3 janvier d'une nouvelle partie, deux jours après la sortie du lobby, ou demande manuelle depuis le journal et les décisions. Le journal américain réessaie chaque semaine si une offre initiale a été empêchée et que les conditions sont rétablies. La France choisit un montant ou refuse ; les États-Unis acceptent ou refusent ensuite. Un refus français est notifié au Congrès. Les fonds ne sont pas crédités tant que l'accord natif ne peut pas être créé. Un refus, une offre expirée ou un échec commercial ne crée ni versement ni obligation. Voir [le correctif de déclenchement et d'interface](RUNTIME_FIX_01/REPORT.md) et le résultat du test joueur antérieur.

| Scénario | Versement natif FRA → USA par semaine | Biens natifs FRA → USA par semaine | Solde USA projeté hors marchés | Solde FRA projeté hors biens/fret |
|---|---:|---|---:|---:|
| Sans aide | 0 | 0 | −27 466,77 £ | +31 758,56 £ |
| Modéré | 14 000 £ | 6 armes légères + 1 artillerie | −13 466,77 £ | +17 758,56 £ |
| Important | 21 000 £ | 12 armes légères + 1 artillerie | −6 466,77 £ | +10 758,56 £ |

Ces montants arrondissent environ la moitié et les trois quarts du déficit observé, sans l'annuler, et restent inférieurs au surplus français de la sauvegarde. Une réserve française d'au moins 84 000 £ (quatre semaines du niveau élevé) et un solde non déficitaire sont exigés pour accepter ; le niveau élevé exige aussi 22 000 £ de solde à l'offre. Le coût indicatif des biens au prix français de cet instant est 427,23 / 836,95 £ par semaine, **pas une facture moteur garantie** : s'y ajoutent les conséquences réelles de marché et de transport. La France paie le transfert monétaire et les fournitures séparément ; aucun rabais militaire ni bien créé par modificateur ne recompte ces livraisons.

Chaque tranche dure 182 jours, soit 26 semaines : maximum monétaire 364 000 / 546 000 £ avant arrêt anticipé. Renouvellement possible, avec choix d'augmenter le niveau, jusqu'à six tranches. Un délai de 196 jours entre signatures laisse quatorze jours après expiration pour éviter le chevauchement d'anciens articles. Six tranches ne constituent pas une promesse : chaque offre requiert à nouveau le consentement, la guerre et la capacité financière. Une longue guerre ou l'arrêt du secours laisse donc une crise possible.

Les articles propres au mod utilisent les comportements natifs **is_money_transfer** et **is_goods_transfer**. La comptabilité bilatérale et les expéditions sont assurées par le moteur ; aucun événement mensuel n'ajoute de trésorerie. Les mêmes entrées littérales sont utilisées par can_create_treaty et create_treaty, via paramètres de scripted effect. Les marchandises alimentent les marchés ; aucun stock national fictif n'est inventé. Les 6/12 armes représentent la moitié/la totalité de la recette de type des douze mousquets réguliers ; le canon couvre la recette du bataillon d'artillerie, sans donner de technologie ni garantir son emploi ou son ravitaillement.

Le contrat commercial reste visible dans l'interface des traités : c'est une **couverture de négociants**, pas un mécanisme de secret diplomatique natif. Il n'a aucun drapeau de reconnaissance, alliance, accès militaire ou entrée en guerre. Il est suivi par un journal et deux consentements. Les interactions diplomatiques ordinaires du moteur continuent de s'appliquer ; ne pas promettre une invisibilité aux autres joueurs.

## Contreparties et chronologie

À la première signature valide, USA consent une obligation diplomatique envers FRA, durée native 120 mois. Le renouvellement ne crée pas une nouvelle obligation ni ne prolonge une obligation existante. Elle peut être utilisée ou répudiée selon les règles natives ; elle ne donne ni territoire ni souveraineté et ne constitue pas un prêt.

À partir du 17 octobre 1777, une décision permet une négociation publique distincte : alliance et deux privilèges commerciaux réciproques, si les règles natives de ratification le permettent et si la France accepte. Le traité lie ses parties pour cinq ans ; aucun monopole ni cession, aucune abolition mondiale des tarifs. Le privilège natif est un avantage de relation commerciale et de levier, pas une reproduction intégrale de toutes les clauses historiques de nation la plus favorisée. Si le statut de sujet, les relations ou les engagements existants bloquent l'alliance, l'option ne force pas la ratification. La signature ne lance aucun effet d'entrée en guerre : la coopération militaire suit ensuite les possibilités diplomatiques natives.

La participation française forcée à la guerre initiale et ses deux objectifs contre GBR sont retirés. Sans cela, parler de soutien indirect de janvier 1776 aurait été trompeur. Les soutiens espagnols et coloniaux hérités restent inchangés et constituent une autre simplification chronologique, signalée sans élargir ce lot à la diplomatie espagnole.

Sources : [Office of the Historian — alliance et aide](https://history.state.gov/milestones/1776-1783/french-alliance), [Model Treaty](https://history.state.gov/milestones/1776-1783/model-treaty), [National Archives — traité de 1778](https://www.archives.gov/milestone-documents/treaty-of-alliance-with-france). Les circuits clandestins précèdent les traités du 6 février 1778 ; les clauses commerciales et l'alliance sont distinctes. Les chiffres du mod sont une calibration de budget, sans conversion prétendue de livres tournois en monnaie de jeu.

Pour le matériel : [US Army CMH — Supply of Ordnance](https://webdoc.sub.gwdg.de/ebook/p/2005/CMH_2/www.army.mil/cmh-pg/books/revwar/risch/chpt-12.htm) situe l'autorisation royale à Beaumarchais en mai 1776 ; la [correspondance de Beaumarchais de septembre 1776](https://beaumarchais.huma-num.fr/Inventaire/Correspondance?ID=582) explique l'usage commercial des excédents d'arsenaux. L'offre de janvier reste celle d'intermédiaires génériques : elle ne prétend pas qu'Hortalez était déjà pleinement constitué à cette date.

## Dons, dettes et sauvegardes

Cette première version finance **des subsides et fournitures non remboursables**. Aucun prêt ou livraison à crédit nouveau n'est consenti. La variable de principal est initialisée à zéro et ne reçoit pas les aides ; une future offre de prêt doit être un contrat distinct. L'obligation diplomatique n'est pas une créance financière.

Ancien système examiné : je_usa_independence déclenchait french_revolution_mod_events.2 à la réussite ; son refus infligeait 25 d'infamie et ouvrait .4 en France. L'acceptation appliquait debt_usa_big_money, dépenses +57 700 pendant 84 mois, puis .3 donnait à FRA +57 700 pendant 84 mois. .1 après échec et .4 pouvaient aussi appliquer des dépenses et ouvrir les États généraux. Il n'existait pas de registre de principal cohérent.

Les identifiants .1–.4 sont conservés pour les événements en attente, mais deviennent des notices de clôture sans prélèvement, revenu, infamie ou révolution imposée. Les événements français .5 et suivants restent identiques. Le journal américain ne lance plus l'ancien remboursement après victoire. La migration mensuelle USA supprime les deux modificateurs anciens des deux pays et ne convertit pas les aides passées en dette. Les prélèvements historiques déjà exécutés ne sont pas remboursés arbitrairement faute de registre ; le présent lot ne reconstruit pas les finances d'une ancienne sauvegarde.

Les trois clés du journal français hérité (titre, raison et présentation du lobby) sont corrigées en français et en anglais dans `mod_v2content_l_french.yml` / `mod_v2content_l_english.yml` : son ancien texte annonçait une crise française certaine après non-remboursement. Il décrit désormais l'engagement atlantique sans transformer les subsides en prêts ni imposer de crise. Toutes les autres clés de ces deux fichiers sont conservées.

Le problème des dettes et des aides de statut ambigu est documenté par l'[Office of the Historian — U.S. Debt and Foreign Loans](https://history.state.gov/milestones/1784-1800/loans). Il ne justifie pas de traiter tous les subsides comme des prêts.

## Arrêts et tests moteur

Les articles deviennent invalides si la guerre USA–GBR cesse, si USA/FRA disparaît, si les deux pays deviennent ennemis, si leurs relations tombent sous −25, si FRA fait défaut, si la tranche expire ou si l'un met fin au secours par décision. Un solde français négatif entraîne également la clôture au contrôle mensuel. Le blocage maritime peut suspendre les marchandises tout en laissant le versement financier distinct ; ne pas le confondre avec l'arrivée physique d'un convoi. Aucune dette envers un tag disparu n'est créée.

Vérifier une nouvelle partie USA puis FRA : pause, J+2, acceptation/refus, premier calcul hebdomadaire, un mois, six mois, sauvegarde/rechargement. Comparer dans le budget le même montant transféré des deux côtés, puis les coûts et volumes de biens dans le traité et les voies d'expédition. Contrôler qu'aucun fonds ne provient d'un modificateur caché. Tester voie bloquée, défaut français, paix américaine victorieuse, paix sous tutelle, relations hostiles, disparition d'un pays et renouvellement après le délai. Le total ne doit pas croître en rechargeant au même instant.

Pour le traité public, tester les conditions natives après 1777, les privilèges réciproques, le refus et l'absence d'entrée en guerre scriptée. Vérifier que l'ancien événement .2 ne prélève plus 57 700 et n'inflige plus 25 d'infamie, y compris lorsqu'il était en attente dans une sauvegarde. Tester au moins douze mois de guerre pour observer les prix et les finances françaises ; les projections de ce rapport ne remplacent pas ces résultats.

Les textes FR/EN ont une première rédaction immersive à la demande expresse de la mission R2 ; les calculs restent dans ce rapport. Leur exactitude fonctionnelle et leur rendu restent à vérifier avant de qualifier la finition éditoriale de validée.
