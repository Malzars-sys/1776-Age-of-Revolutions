# Substitution domestique des alliages

Statut : `IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION`.

Seul `popneed_household_items` dans `common/pop_needs/00_pop_needs.txt` est modifié. Les paniers du vanilla canonique commencent ce besoin à `wealth_10`, valeur 7, puis augmentent aux richesses suivantes. Aucun panier n'est édité.

L'entrée ajoutée est :

```text
entry = {
    goods = alloys
    weight = 0.02
    max_supply_share = 0.05
    min_supply_share = 0.01
}
```

L'offre d'alliages contribue donc à un poids très faible. Le plancher permet un petit signal de demande même sans offre initiale, suivant la convention décrite dans les commentaires natifs. Ce n'est ni une consommation obligatoire de 1 % ni un plafond de dépense de 5 %.

Interprétation statique des commentaires : coefficient d'alliages compris entre 0,02 × 0,01 = 0,0002 et 0,02 × 0,05 = 0,001. Les meubles gardent un poids minimal de 1 × 0,10 = 0,10. Même en ignorant tous les autres substituts, la normalisation donne au plus 0,001 / (0,10 + 0,001) = **0,9901 %**. Les prix, unités de valeur, accès et règles internes du moteur ne sont pas simulés ici : cette borne porte sur ce modèle de coefficients, pas sur des achats observés ou une limite universelle de dépenses.

Les entrées de meubles, verre et papier sont identiques à la baseline, ainsi que le produit par défaut `furniture`. Aucun autre besoin n'est changé. Aucune richesse plus faible n'est forcée à acheter du métal.

Le bien consommé directement représente une très petite activité domestique et artisanale non détaillée par des bâtiments : quincaillerie, chandeliers, petits objets et composants. L'usage industriel des manufactures est séparé et reste de 0,5 alliage dans le premier palier en consommant.

La part absolue des POPs dans la demande mondiale ne peut pas être garantie par un poids relatif seul : si beaucoup de ménages sont concernés et peu d'usines consomment le bien, même cette petite part peut dominer temporairement. Le protocole exige donc de relever les commandes d'achat POP et industrielles après un mois, puis dans un pays industrialisé. Si elle domine durablement à cette seconde étape, abaisser le poids/plancher lors de la validation plutôt que transformer tous les besoins.
