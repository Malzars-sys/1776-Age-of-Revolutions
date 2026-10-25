# CONTENT-USA-R2 — Échos internationaux et Pères fondateurs

Statut des deux fonctionnalités : **IMPLEMENTED — READY_FOR_RUNTIME_VALIDATION**. Scripts et textes FR/EN installés ; aucune exécution nouvelle du moteur ni campagne simulée. Voir `CONTENT_R2_VALIDATION.json`, puis `FINAL_VALIDATION.json` pour les contrôles consolidés.

## Personnalités et fonctions installées

| Personnage | Naissance, âge exact au 1er janvier 1776 | Fonction de cette version |
|---|---|---|
| Benjamin Franklin | 17 janvier 1706, 69 ans | Politicien ; mission diplomatique volontaire à partir du 26 septembre 1776 |
| John Adams | 30 octobre 1735, 40 ans | Politicien ; choix d'une commission temporaire de contrôle des comptes après l'indépendance |
| Thomas Jefferson | 13 avril 1743, 32 ans | Politicien ; choix alternatif de garanties des assemblées après l'indépendance |

Les [National Archives donnent les dates de naissance](https://www.archives.gov/founding-docs/signers-factsheet). L'âge de leur tableau se rapporte à l'année de la Déclaration ; nos âges sont calculés au **1er janvier**. Franklin n'est donc pas déjà âgé de 70 ans au départ, ni Jefferson de 33 ans.

Créations uniquement dans l'historique d'une nouvelle partie, avec recherche préalable du modèle : aucun doublon volontaire, aucune recréation mensuelle, aucune résurrection. Chaque profil possède des traits natifs déterministes modestes : diplomate de base pour Franklin, homme de lettres pour Adams et Jefferson. Ils ne deviennent ni président ni chef de groupe d'intérêt par script ; Hancock et les sept profils militaires existants restent conservés. Ces trois politiciens rejoignent ici l'Intelligentsia avec une idéologie républicaine : c'est une simplification de représentation, particulièrement pour Jefferson, propriétaire esclavagiste, et non une attribution uniforme de convictions modernes.

La disponibilité exige un personnage vivant, adulte, appartenant aux États-Unis, politicien et libre d'une autre activité. Le contrôle est répété dans les options, pour éviter qu'un décès ou un départ intervenant pendant une fenêtre d'événement produise malgré tout un avantage. Les personnages restent soumis à la mortalité et aux évolutions politiques natives.

La mission de Franklin coûte 5 000 £ au choix de confirmation, accorde +10 de relations avec la France et impose un délai de 365 jours entre propositions. Elle exige une France existante et non ennemie et une Amérique indépendante ou encore engagée dans sa guerre d'indépendance. Aucun traité ni versement français ne découle automatiquement de cette dépense. La date ouvre la possibilité de confier le mandat ; elle ne signifie pas une arrivée instantanée de Franklin à Versailles. Le [Journal du Congrès du 26 septembre 1776](https://tile.loc.gov/storage-services/service/ll/llscd/lljc005/lljc005.pdf) enregistre la désignation des commissaires ; l'[Office of the Historian](https://history.state.gov/milestones/1776-1783/b-franklin) distingue la commission de 1776–1778 de la réception de Franklin comme ministre en 1779.

Après une issue indépendante, en paix et sous une république présidentielle, la commission du Congrès offre **un seul** choix de politique pour cette chaîne :

| Choix | Effets pendant au plus 24 mois | Compromis |
|---|---|---|
| Adams : comptes publics | salaires administratifs −5 % | autorité −25 |
| Jefferson : garanties des assemblées | approbation de l'Intelligentsia +1 | autorité −50 |
| Poursuivre les délibérations | aucun effet | possibilité de reprendre la décision |

Les effets cessent également au contrôle mensuel si le titulaire meurt, quitte le pays ou son rôle politique, ou si le gouvernement abandonne la république présidentielle. Une activité temporaire du titulaire après sa nomination ne lui retire pas automatiquement sa commission. Le drapeau de commission déjà constituée empêche d'enchaîner les deux récompenses ou de la renouveler à chaque expiration. Ces commissions et leurs chiffres sont une abstraction de gameplay, pas l'affirmation d'un office historique identique ou d'une économie de salaires historiquement mesurée.

Adams défend l'indépendance au Congrès et participe au Model Treaty ; voir [NPS, John Adams](https://www.nps.gov/adam/learn/historyculture/john-adams-1735-1826.htm). Jefferson est délégué en 1775–1776, auteur principal de la Déclaration, et poursuit des réformes en Virginie ; voir [NPS, Thomas Jefferson](https://www.nps.gov/thje/learn/publications.htm). Cette version ne leur attribue pas leurs présidences futures, ni le ministère français ultérieur de Jefferson. Madison et Hamilton restent des extensions ultérieures : la fonctionnalité livrée porte sur les trois profils et deux décisions décrits ici.

## Échos de la guerre

La résolution effective du journal américain déclenche une diffusion **unique**, sur réussite ou échec. Le résultat est copié dans une variable du destinataire avant l'événement : les textes ne dépendent pas d'un scope temporaire perdu. Aucun balayage mondial mensuel, aucune indépendance, révolution, loi ou guerre imposée.

| Destinataire | Conditions de transmission | Choix et effet maximal |
|---|---|---|
| France | a ratifié un accord d'aide ou signé le traité public | après victoire américaine, débat si Intelligentsia non marginale : approbation +1, autorité −25, 12 mois ; sinon réception narrative |
| Grande-Bretagne | existe à l'issue de la guerre | après défaite américaine, rassurer les défenseurs de l'ordre colonial : Propriétaires terriens +1, 12 mois ; sinon examiner le résultat sans bonus |
| Possessions britanniques ONT, QUE, NBS, NVS, HBC | encore sujets britanniques, droit de réunion ou relations USA ≥20 | choix local : après victoire, liberté +5 et Intelligentsia +1 si non marginale ; après défaite, liberté −3 et Propriétaires terriens +1 ; 12 mois |
| Colonies espagnoles SC1–SC4, CUB | encore sujets espagnols, même condition de relais | mêmes choix locaux, sans libération automatique |
| Brésil | encore sujet portugais, même condition de relais | mêmes choix locaux, sans imposer une révolte dès 1776 |
| Pays-Bas, Suède, Danemark | échanges scientifiques institutionnalisés, relations USA ≥20, Intelligentsia non marginale | après victoire américaine, réussite de promulgation +5 points de pourcentage et Propriétaires terriens −1, 12 mois ; discussion déclinable |

Chaque événement possède un choix sans modificateur et un verrou de réception. Les possessions asiatiques, les territoires impériaux et les autres pays ne reçoivent pas indistinctement les mêmes effets. Les valeurs de désir de liberté sont additives, pas des multiplicateurs. Les modificateurs expirent, même si le destinataire change ensuite de gouvernement. Ce premier périmètre ne prétend pas couvrir tous les pays touchés intellectuellement par la révolution américaine.

Le courrier de [José da Maia à Jefferson, 21 novembre 1786](https://founders.archives.gov/documents/Jefferson/01-10-02-0398), fournit un exemple concret de réception brésilienne ultérieure ; il ne justifie pas une révolte générale immédiate en 1776. La sélection de relais politiques et commerciaux est notre interprétation pour une histoire alternative, pas la reconstruction d'un réseau identique dans toutes les colonies. La [Library of Congress](https://blogs.loc.gov/international-collections/2021/07/the-franco-american-revolution-part-2/) documente la circulation franco-américaine des idées et les intérêts diplomatiques ; aucune chaîne inévitable vers 1789 n'en est déduite.

## Fichiers, contrôles et essai en jeu

Fichiers propres : `common/character_templates/1776_usa_founders.txt`, `common/history/characters/zz_1776_usa_founders.txt`, `common/scripted_triggers/1776_usa_founders.txt`, `common/decisions/1776_usa_founders.txt`, `events/1776_usa_founders.txt`, `common/scripted_effects/1776_usa_echoes.txt`, `events/1776_usa_echoes.txt`. Les effets partagent le nouveau fichier `common/static_modifiers/1776_usa_revolution_r2.txt` et les localisations R2 FR/EN. Seuls les deux résultats du journal d'indépendance existant reçoivent l'appel de diffusion ; l'action mensuelle américaine entretient les commissions.

Contrôles statiques : trois créations protégées, identifiants uniques, dates, traits disponibles, absence de changement imposé de chef d'État, deux issues de guerre raccordées, diffusion unique, destinataires limités, durées et choix neutres, références et localisations. Ils vérifient les données et les invariants, pas l'évaluation réelle des scopes par le moteur.

En nouvelle partie, vérifier les trois profils à côté de Hancock et des sept militaires, sans changement du dirigeant. Avant septembre, la mission de Franklin doit être absente ; après la date, tester acceptation, refus, manque d'argent et décès avant confirmation. Après victoire, tester les deux branches de commission dans des parties distinctes, puis décès, exil/départ et changement de régime. Vérifier l'expiration et l'impossibilité de reprendre une commission déjà choisie.

Pour les échos, provoquer séparément victoire et défaite ; comparer une colonie sans relais, une colonie avec droit de réunion, un pays européen sans relations et un destinataire éligible. Recharger avant/après résolution pour confirmer la réception unique et les choix neutres. Les nouvelles créations historiques nécessitent une **nouvelle partie** ; l'ancien enregistrement ne reçoit pas artificiellement des fondateurs ressuscités. L'annexion totale des États-Unis avant la résolution de leur journal peut supprimer son événement final : cette première version ne promet pas une diffusion internationale dans ce cas. Le financement, lui, devient invalide si un pays disparaît.

Textes joueurs FR/EN rédigés dans un registre immersif conformément à la mission R2 ; explications techniques conservées ici. Fonctionnement et rendu restent à valider humainement avant de qualifier la finition éditoriale de terminée.
