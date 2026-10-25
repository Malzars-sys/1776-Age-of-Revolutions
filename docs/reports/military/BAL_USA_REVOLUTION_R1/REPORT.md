# BAL-USA-REVOLUTION-R1

Statut : **READY_FOR_RUNTIME_VALIDATION**. Aucun résultat de campagne moteur revendiqué.

## Audit et changement installé

Seul le bloc `modifier_usa_war_of_independence` de `common/static_modifiers/76mod_modifiers.txt` change. Le journal et les événements existants restent identiques.

| Effet exact | Avant | Après |
|---|---:|---:|
| unit_offense_mult | +0,20 | absent, contribution 0 |
| unit_defense_mult | +0,20 | absent, contribution 0 |
| building_training_rate_mult | +0,50 | +0,15 |
| unit_morale_recovery_mult | +0,50 | +0,15 |
| unit_morale_loss_mult | −0,35 | −0,10 |
| unit_morale_damage_mult | +0,25 | absent, contribution 0 |
| country_liberty_desire_add | +0,35 | +0,35, inchangé ; valeur additive, pas +35 % |
| country_tax_income_add | +60 000 | absent, contribution 0 |

Il ne reste aucun effet direct sur l'attaque, la défense, l'expérience, le plafond de conscription, la vitesse de déplacement ou la mobilisation. L'instruction accélère indirectement le remplissage des unités selon le fonctionnement des bâtiments recruteurs ; elle ne crée pas de bataillons, de qualifications ou d'armes. La récupération et la perte de moral ne sont pas l'organisation ni les renforts en hommes.

`je_usa_independence` applique le modificateur dans `immediate` lorsque USA est sujet de GBR, en guerre, et que GBR est son ennemi dans le jeu diplomatique. Il n'y a pas de durée calendaire. La réussite exige indépendance et absence de guerre ; l'échec exige la paix en restant sujet. Les deux issues retirent le bonus. L'indépendance pendant une autre guerre peut donc prolonger son maintien : comportement hérité à observer, sans réécrire les conditions dans R1.

Après victoire, `modifier_usa_freedom` donne +0,10 loyalistes issus des mouvements politiques et +0,30 attraction migratoire ; pas de bonus de combat. Après défaite, `modifier_usa_put_down` donne +0,10 radicaux issus des mouvements. Le journal modifie aussi l'idéologie des industrialistes, active quatre lois en cas d'échec et ouvre l'événement financier français .2 après réussite. Ces mécanismes ne changent pas ici.

## Justification et limites

Les difficultés d'engagement, d'instruction et de ravitaillement du début de 1776 sont documentées par le [National Park Service, Looking to Break the Siege](https://home.nps.gov/articles/000/looking-to-break-the-siege.htm) et la [correspondance de Washington du 31 décembre 1775](https://founders.archives.gov/documents/Washington/03-02-02-0579). Elles ne justifient ni une supériorité universelle des armes américaines ni une ressource budgétaire sans contrepartie. Les 15 % sont des valeurs d'essai de gameplay, pas une mesure historique de ferveur.

Le retrait de 60 000 de revenu fixe est majeur : à lecture hebdomadaire du budget, environ 3,12 millions sur 52 semaines. Aucun don français fictif ne le remplace. Mesurer le budget effectif, les importations d'artillerie et le crédit avant de conclure que le niveau proposé est viable. Si l'économie bloque toute guerre, corriger un coût ou un soutien traçable dans un lot suivant, sans rétablir automatiquement le revenu caché.

Illustration isolant ce modificateur : un mousquet de base 15/20 passait à 18/24 avant les autres effets ; il reste désormais à 15/20. Avec les seules levées paysannes (+0,10 perte de moral), le cumul du bonus de guerre passe de −0,25 à 0 ; le canon/mousquet à perte de base 10 passe donc de 7,5 à 10. Les commandants, expérience, prix, ravitaillement et autres effets doivent être comptés séparément. Le lot commandants est testé avec ce nouveau niveau et ne doit pas recréer le cumul supprimé.

Aucune force, technologie ou économie britannique n'est augmentée. L'équilibrage ne garantit ni victoire américaine ni victoire britannique.

## Dette héritée et tests

La France et l'Espagne figurent déjà parmi les soutiens de la guerre initiale ; l'alliance de 1778 n'est pas simulée chronologiquement par ce simple état de départ. Le système financier existant propose après victoire un refus assorti de 25 d'infamie ou un prélèvement sur 84 mois, sans registre attestant les prêts réellement reçus. Le lot de conception décrit son remplacement ultérieur. R1 ne crée aucune nouvelle obligation de remboursement et ne déclenche pas de révolution française supplémentaire.

Comparer trois campagnes USA et trois GBR avec même configuration et réglages, sans autre changement : pause initiale, semaine 1, mois 1/3/6/12, puis fin de guerre ou trois ans. Relever attaque/défense détaillées, moral maximum/perte/récupération, vitesse d'instruction, emploi militaire, régulier/conscript, prix et disponibilité des armes/artillerie, recettes, dépenses, dette, pertes et contrôle territorial. Tester séparément victoire et défaite, vérifier retrait du modificateur dans les deux branches et absence de revenu +60 000. Un résultat unique ne prouve pas l'équilibre ; conserver dates, sauvegardes et paramètres des campagnes.
