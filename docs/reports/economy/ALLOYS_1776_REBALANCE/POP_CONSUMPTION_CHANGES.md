# Consommation courante : quincaillerie et faible demande d'alliages

Statut : `IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION`.

La quincaillerie est un bien distinct classé `staple`, comme les meubles ordinaires et vêtements. Elle rejoint uniquement `popneed_household_items`, dont les paniers commencent à richesse 10. Aucun besoin de luxe ni nouveau besoin général. Aucun panier modifié.

| Marchandise ajoutée | Poids | Plancher d'offre | Plafond d'offre |
|---|---:|---:|---:|
| Alliages, faible activité artisanale directe conservée | 0,02 | 0,01 | 0,05 |
| Quincaillerie, objets domestiques finis | 1 | 0,02 | 0,35 |

Meubles, verre et papier gardent leurs paramètres ; `furniture` reste le produit par défaut. La demande de quincaillerie est volontairement bien plus significative que celle des alliages achetés directement.

Les commentaires natifs décrivent un poids multiplié par une part d'offre bornée : il ne s'agit ni d'une dépense imposée de 2 % ni d'un plafond universel de 35 % des dépenses. Dans cette approximation, le coefficient de quincaillerie varie de 0,02 à 0,35 ; celui d'alliages de 0,0002 à 0,001. Le plancher existant des meubles est 0,10. Le maximum normalisé simplifié d'alliages reste sous 0,991 %, et l'ajout de quincaillerie réduit encore cette borne théorique.

Les prix, règles internes et volumes effectifs ne sont pas simulés par ce calcul. Une petite part relative peut représenter une quantité mondiale importante : relever commandes POP et industrielles après un mois puis dans une économie développée.

Les richesses inférieures à 10 n'ont pas ce besoin dans les paniers actuels. « Courant » désigne sa catégorie et son usage ; aucun nouveau panier n'est imposé aux ménages pauvres. Le bien est échangeable pour les pays sans production nationale, suivant les règles commerciales natives.
