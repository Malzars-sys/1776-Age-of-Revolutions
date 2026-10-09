# 1776 — Événements d’ouverture des journaux ottomans

## Résultat

Deux événements ottomans sont programmés à la sortie du lobby, au lancement d’une nouvelle campagne. Les journaux ne deviennent disponibles qu’après le choix de leur événement respectif. Les titres, descriptions et extraits littéraires sont immersifs ; les règles de jeu restent dans les infobulles des choix.

| Événement | Titre français | Unique choix du sultan | Journal activé |
|---|---|---|---|
| `ottoman_1776.10` | Une bureaucratie désuète | Nous devons rétablir les comptes et faire respecter nos ordres. | Le fardeau de la Sublime Porte |
| `ottoman_1776.11` | Un trône, mille maîtres | Nous devons rallier les provinces et affermir notre autorité. | Un empire aux multiples maîtres |

### Une bureaucratie désuète

Les registres de la Porte recensent les droits du sultan, mais les recettes passent par une multitude d’intermédiaires. Les fermes fiscales, parfois concédées à vie, avancent au Trésor des sommes dont il a besoin ; elles donnent aussi aux détenteurs des revenus provinciaux une influence que les bureaux de Constantinople peinent à contrôler. Entre exemptions, créances anciennes et comptes tardifs, la somme promise n’est pas toujours la somme reçue. Pourvoir les offices, vérifier les recettes et faire appliquer les décisions impériales devient une nécessité : le sceau du sultan ne peut tenir lieu de comptes rendus.

*Le vieux commis tira du coffre un registre dont le cuir s’effritait. Une quittance, pliée entre deux feuillets, portait trois sceaux et pas une date. « Le village a payé, dit-il. Le fermier aussi, à ce qu’il assure. » Son apprenti regarda la colonne vide. Au-dehors, les portefaix déchargeaient les sacs du Trésor ; dans le bureau, l’argent n’était encore qu’une promesse.*

*— Les Registres de la Corne d’Or*

Infobulle : activation du journal administratif ; allégement temporaire des malus selon les objectifs satisfaits ; résolution après maintien de toutes les conditions pendant 12 mois consécutifs.

### Un trône, mille maîtres

Des Balkans aux provinces arabes, les firmans proclament une seule souveraineté. Leur exécution dépend pourtant des gouverneurs, des notables provinciaux et des maisons qui disposent des revenus et des hommes du pays. En Égypte, les beys mamelouks possèdent leurs propres forces ; ailleurs, les puissants négocient ce qu’ils doivent au centre et ce qu’ils entendent conserver. Leur fidélité n’a pas disparu, mais elle ne se commande plus par un sceau seul. La Porte doit donner à ces autorités une place dans un ordre commun, avant que leurs rivalités et les ambitions étrangères ne déchirent l’édifice impérial.

*Le messager avait traversé trois provinces sous la protection du même firman. À chaque porte, on lui avait demandé un autre nom. « Celui du sultan ne vous suffit donc pas ? » Le garde écarta le rideau : dans la cour, les hommes du bey attendaient leur solde. « Ici, répondit-il, nous savons qui la verse. »*

*— Les Portes du Sultan*

Infobulle : activation du journal politique ; échéance au **1er janvier 1836**, soit 60 ans depuis le départ de 1776 ; déchéance anticipée possible sous une pression grave et une instabilité prolongée ; passage à L’homme malade de l’Europe en cas d’échec ; rappel des effets sur les sujets et le soutien étranger au séparatisme.

Les deux extraits et les deux titres de romans sont des créations originales fictives, pas des citations historiques. Ils utilisent le champ natif `flavor` et le balisage italique du jeu. Localisation française et anglaise ajoutée.

## Fonctionnement et conservation

- Le démarrage initialise les variables, puis programme les deux fenêtres après la sélection du pays. Chaque événement possède exactement une option par défaut.
- Chaque choix déverrouille seulement son journal. L’ordre de validation des deux choix est indifférent.
- Les marqueurs de programmation et d’ouverture empêchent les répétitions.
- Activation par éligibilité des entrées précréées par le moteur : pas de nouvel `add_journal_entry` susceptible de rencontrer une entrée inactive déjà existante.
- Les sauvegardes des versions précédentes conservent leurs journaux et leurs compteurs ; le rapprochement mensuel ajoute les nouveaux marqueurs sans rejouer les introductions.
- Objectifs, échéances, méthodes de calcul, modificateurs, armées et niveaux des bâtiments inchangés par ce lot. L’homme malade de l’Europe ne récupère pas de malus administratif parallèle pour le scénario ottoman 1776.
- Les illustrations des journaux déjà intégrées sont réutilisées, avec deux vidéos d’événement présentes dans l’installation du jeu.

## Tests réalisés

`tools/validate_diplomacy_ottoman_1776.py` : **tous les contrôles passent**.

- Programmation unique des deux événements ; aucun journal ouvert avant son choix.
- Exécution des effets des options réellement définies dans les événements ; ouverture correcte dans les deux ordres.
- Répétition des appels sans doublon ; déclencheurs invalidés après ouverture.
- Conservation de la progression d’une ancienne sauvegarde dans le modèle de test.
- Contrôle du branchement après lobby, des textes FR/EN et des champs d’événement ; vidéos et icônes existantes.
- Non-régression : 1 024 combinaisons d’objectifs administratifs, 96 combinaisons de conditions politiques, consolidation, échéance de 1836, déchéance anticipée et retrait des anciens malus.
- Contrôles précédents conservés : administrations ottomanes 64 → 54, armée permanente 72, Égypte et autres propriétaires préservés, diplomatie et pompe diesel.
- `git diff --check` : aucune erreur de whitespace.

Ces tests statiques et de simulation ne remplacent pas un lancement du jeu. À vérifier dans une **nouvelle partie ottomane** : les deux fenêtres apparaissent au démarrage, leurs extraits sont en italique, chaque choix affiche son infobulle et active le bon journal. Le délai exact de rafraîchissement du panneau du journal reste à observer dans le moteur.

Aucun push, merge ou commit effectué.

## Repères historiques utilisés

Les textes évoquent les fermes fiscales à vie, les intermédiaires des recettes et le pouvoir des notables provinciaux ; il ne s’agit pas de déclarer toute l’administration ottomane uniformément inefficace.

- Deniz Karaman, [The Ankara Damga Mukataası (Stamp Tax) in the 18th Century](https://dergipark.org.tr/en/pub/bilig/article/267805), Bilig, 2005 : étude des registres et de l’administration des revenus affermés.
- Nihal Metin, [étude sur le malikâne et Eğinli İshak Paşa](https://dergipark.org.tr/tr/pub/ijsi/article/1017831), 2022 : relations entre fermes fiscales, pouvoir provincial et interventions du centre.
