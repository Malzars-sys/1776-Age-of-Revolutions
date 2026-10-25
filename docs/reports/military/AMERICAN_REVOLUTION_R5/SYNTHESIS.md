# Révolution américaine R5 — ratification et interventions

> L’ouverture de la chaîne commence désormais en France et la liste américaine des lois remplace la milice par les Minutemen : voir [R6](../AMERICAN_REVOLUTION_R6/SYNTHESIS.md). Les corrections financières, de ratification, de monument et d’intervention décrites ci-dessous sont conservées.

18 octobre 2026. **290 contrôles statiques et cas ciblés réussis. Essai moteur R5 non effectué.**
Le résultat complet est dans [VALIDATION.json](VALIDATION.json). R4 a été essayé
par l’utilisateur et **sa ratification échouait** ; ses 201 vérifications
structurelles n’avaient pas détecté cette incompatibilité de portée.

## Échec de ratification

Les journaux du jeu rapportent exactement :

```text
treaty trigger [ Wrong scope for trigger: treaty_article_options, expected treaty_article ]
common/treaty_articles/1776_usa_french_support.txt:21 / :77
```

Les preuves sont conservées dans [R4_RUNTIME_ERRORS.txt](R4_RUNTIME_ERRORS.txt),
avec les empreintes des journaux dans [RUNTIME_LOG_SOURCES.json](RUNTIME_LOG_SOURCES.json).
Pendant le contrôle préalable, l’article est encore un jeu d’options ; il ne
peut pas suivre le lien d’un article actif vers son traité. Ce lien a été
retiré des trois articles de secours et de la clause Join Ongoing Wars.

Les conditions de maintien admettent maintenant l’offre en cours **ou** le
financement actif. L’aide n’a donc plus besoin d’être activée artificiellement
avant sa ratification. Seule la solvabilité du payeur français est requise :
un défaut américain ne bloque pas la réception de l’argent.

Après la création native, une seconde vérification exige les cinq articles :
transfert, reconnaissance de dette, instructeurs et deux fournitures. La dette,
le verrou de dix ans et l’obligation ne sont enregistrés qu’après cette
vérification. Un échec ne crée pas de créance sans traité. L’événement d’échec
reste une vraie issue de secours ; il n’est plus annoncé dans l’infobulle de
ratification, qui présente les conditions du prêt.

## Offres sans intérêts et à 5 %

La sélection conditionnelle des textes suit maintenant intégralement la
structure native `first_valid` / `triggered_desc`, y compris la branche par
défaut. Les titres, descriptions, boutons de ratification et infobulles
distinguent les deux cas en français et en anglais.

Le taux approuvé par la France est conservé séparément jusqu’à la signature.
Les textes et la dette finale lisent cette même valeur, y compris après une
contre-proposition française. Un événement programmé par R4 peut récupérer
le taux depuis son ancien choix lorsqu’il s’ouvre avec les nouveaux scripts.

| Conditions | Sans intérêts | Intérêts à 5 % |
|---|---:|---:|
| Argent reçu par semaine | 30 000 £ | 30 000 £ |
| Armes légères / artillerie | 15 / 1 | 15 / 1 |
| Capital prévu sur 3 650 jours | ≈15 642 857 £ | ≈15 642 857 £ |
| Remboursement prévu à l’échéance | ≈15,6 millions £ | ≈16,4 millions £ |

Le secours reste identique ; **les intérêts augmentent le remboursement**.
Le calcul continue de lire la durée native du traité en jours. Le capital est
la valeur contractuelle des versements prévus, avec la limite R4 déjà documentée
sur les paiements gelés ou les ruptures. La demande de remboursement reste
bloquée pendant l’engagement ; les intérêts ne sont appliqués qu’une fois.

## Maison-Blanche

La définition native avait `buildable = no`. Le mod surcharge maintenant
`common/buildings/08_monuments.txt` pour mettre **seulement la Maison-Blanche**
à `buildable = yes`, avec `liberal_constitutionalism` (« Constitution libérale »)
comme technologie nécessaire. Sa région reste le district de Columbia, elle
reste unique, et son coût, ses effets, sa méthode de production et son modèle
sont conservés. Elle n’est pas offerte au départ.

Tous les autres monuments du fichier sont identiques au vanilla canonique.
La provenance et l’empreinte de cette copie sont dans [MONUMENT_SOURCE.json](MONUMENT_SOURCE.json).
Aucune donnée de carte ni aucun modèle n’a été modifié.

## Entrées dans la guerre américaine

L’intégration précédente considérait la présence d’une côte comme une portée
géographique suffisante pour rejoindre la guerre d’un allié. Pour une guerre
comprenant les États-Unis et la Grande-Bretagne, une nouvelle condition exige
au moins l’un des liens suivants :

- un intérêt actif dans la région stratégique **Côte atlantique** ;
- la France ou l’Espagne soutenant le camp opposé à la Grande-Bretagne ;
- le Portugal soutenant le camp britannique, avec une alliance britannique active ;
- une rivalité avec la Grande-Bretagne, pour combattre celle-ci.

Une simple alliance, un pacte défensif ou une côte ailleurs dans le monde ne
suffisent plus. La condition s’applique à l’éligibilité commune **et à chaque
guerre effectivement rejointe**, afin qu’un autre conflit admissible ne permette
pas de contourner la restriction américaine. Les autres guerres gardent les
règles générales précédentes. Un pays qui possède réellement l’intérêt régional
requis peut toujours intervenir, sans liste noire arbitraire de pays.

Les cas ciblés refusent Naples et les Ottomans sans cet intérêt ; ils acceptent
le Portugal allié, la France avec les insurgés et l’Espagne appelée par la
France. Les calendriers français, l’absence de tirages espagnols, l’approbation
espagnole et les autres gardes diplomatiques sont préservés.

## Vérification et essai attendu

L’outil courant est `tools/validate_american_revolution_r5.py`, accompagné de
cas ciblés dans `tools/validate_american_revolution_r5_cases.py`. Il vérifie
notamment les deux taux, les sélecteurs de texte réels, l’erreur de portée R4,
les postconditions du traité, douze situations d’intervention, la surcharge
du monument, les références, les localisations et les corrections américaines
antérieures. Le petit évaluateur de prédicats n’exécute ni la création de
traités native, ni l’IA du jeu. Aucun PASS_RUNTIME n’est attribué.

Les fichiers de carte, les populations, les États, les bâtiments de départ,
les formations militaires et la loi initiale des Minutemen sont inchangés
par cette passe. HEAD et l’index Git sont conservés. L’installation canonique
et les sauvegardes restent en lecture seule.

**Redémarrer complètement le jeu**, puis vérifier les deux offres sur une
nouvelle partie américaine : titre et bouton corrects, ratification, traité
à cinq articles, budget et dette. Faire aussi un essai français avec demande
de l’IA américaine, puis contrôler l’appel espagnol et l’entrée portugaise.
La nouvelle restriction ne retire pas des participants déjà entrés dans une
ancienne sauvegarde. Pour la Maison-Blanche, vérifier l’absence de construction
avant la technologie et sa disponibilité dans le district de Columbia après.

Les journaux conservent le statut technique à valider prévu par le guide du
dépôt. Leur seconde passe immersive attend la validation humaine du fonctionnement.
