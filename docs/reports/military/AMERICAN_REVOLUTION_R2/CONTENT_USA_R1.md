# CONTENT-USA-R1 — Minutemen et ferveur

**IMPLEMENTED — READY_FOR_RUNTIME_VALIDATION.** Les tests sont statiques et arithmétiques ; aucun recalcul militaire moteur exécuté par l'agent.

## Compagnies de minutemen

Nouvelle variante `law_aor1776_minutemen`, parent natif law_national_militia, groupe army_model. Elle est visible seulement aux USA et ne peut pas être imposée à un autre pays. Son déblocage propre est light_infantry_tactics, déjà possédé. La décision « Organiser les compagnies locales » permet de l'adopter pendant la guerre depuis les levées paysannes. Elle n'est pas activée automatiquement et ne donne aucune technologie.

| Effet de la variante | Valeur |
|---|---:|
| Taux de conscription | 4 % |
| Plafond de casernes par état | 25 |
| Plafond de centres de conscription par état | 25 |
| Vitesse de mobilisation des formations | +20 % |
| Vitesse d'instruction | +10 % |
| Coût des biens militaires | +5 % |

Les plafonds et le taux conservent ceux des levées paysannes ; copier le plafond de cinq casernes de la milice nationale aurait menacé les neuf réguliers du Massachusetts. La restriction aux seuls paysans et le malus d'expérience des levées ne sont pas repris. Aucun bataillon n'est créé par la décision. La variante doit supporter une réforme ultérieure par les lois ordinaires ; permanent_engineer_services n'est pas accordé pour débloquer l'armée professionnelle.

En cas de défaite et de retour sous suzeraineté, la variante revient aux levées paysannes. En cas d'indépendance, elle peut être conservée ou réformée. Aucun bonus de sécurité intérieure, de coup d'État, de sécession, d'opposition ou de résistance au bloc n'est copié de National Guard. L'héritage des prérequis et des effets du parent doit être contrôlé dans l'interface de la version locale, en plus du fichier explicite.

Source historique : [NPS — The Militia and Minute Men of 1775](https://home.nps.gov/mima/learn/historyculture/the-militia-and-minute-men-of-1775.htm), qui distingue obligation milicienne, volontariat et instruction fréquente de compagnies spécialisées. Les valeurs de loi sont des abstractions du mod, pas des pourcentages historiques d'efficacité.

## Ferveur

Score interne initial 50, borné 0–100. Trois états exclusifs apparaissent dans les modificateurs du pays et sont expliqués par un journal : engagement ébranlé (<35), tenu (35–65), raffermi (>65). L'état tenu n'ajoute aucun effet.

| Cause | Variation et limite |
|---|---|
| Victoire non vide contre GBR pendant cette guerre | +5 ; délai 90 jours entre gains de ce type |
| Défaite non vide contre GBR | −5 ; délai 90 jours entre pertes de ce type |
| Premier accord de soutien français accepté | +5 une seule fois, au contrôle mensuel ; signal politique d'un engagement valide, pas preuve de chaque paiement |
| Primes de réengagement financées | coût 7 500 £ ; +10 ; décision limitée à une fois tous les 180 jours |
| Primes différées | −5, sans suppression de bataillons |

Les primes représentent environ quatre semaines des salaires militaires identifiés dans la sauvegarde (1 838,82 £ × 4, arrondi). Elles ne recrutent pas gratuitement quinze bataillons supplémentaires.

Effets exclusifs : faible, récupération de moral −5 % et perte de moral +5 % ; élevé, récupération +5 % et perte −5 %. Avec le seul Liberty Or Death R1, l'enveloppe nationale devient +10 à +20 % de récupération et −5 à −15 % de perte de moral. Lois, chefs et expérience restent des contributions séparées. Aucun bonus général d'attaque/défense, dégâts de moral ou expérience ajouté.

Les hooks natifs on_battle_won/on_battle_lost fournissent le pays et enemy_country ; les hooks de bataille vide ne sont pas utilisés. Les combats contre d'autres alliés britanniques ne comptent pas dans cette première version. Aucune mesure de pertes ou pénurie précise non démontrée n'est inventée. Un petit combat non vide peut compter : le délai de 90 jours limite ce biais mais ne mesure pas à lui seul l'importance stratégique d'une victoire.

Le contrôle mensuel répare seulement l'état et enregistre une fois le signal de l'accord français ; il ne fait pas décroître le score avec le temps. Les modificateurs sont retirés avant chaque remplacement. Les deux branches du journal d'indépendance et le contrôle mensuel nettoient les effets à la fin de la guerre. Aucun parcours mondial, de provinces ou d'unités n'est effectué à chaque bataille.

Correctif après test joueur : le filtre partagé utilise désormais la guerre réelle USA–GBR et les suppressions sont précédées d'une vérification de présence du modificateur. La condition de fin du journal possède une infobulle traduite. Voir `RUNTIME_FIX_01/REPORT.md` pour l'échec observé avant correction et les contrôles supplémentaires ; les bornes de score et les valeurs de moral restent identiques.

Sources : [Washington Papers — problèmes de ravitaillement](https://washingtonpapers.org/resources/articles/supply-problems-plagued-the-continental-army-from-the-start/) et [NPS — Valley Forge](https://home.nps.gov/vafo/learn/historyculture/valley-forge-history-and-significance.htm). Ces expériences motivent le lien entre confiance, engagements et moyens matériels, sans imposer à une partie alternative les événements de 1777–1778.

## Validation en jeu

Nouvelle partie USA : noter les 13 réguliers et 15 conscrits potentiels avant adoption, adopter la variante, puis relever capacités, effectifs, coûts et méthodes à J+1/J+7/M+1. Vérifier le Massachusetts, les plafonds 25, l'absence de technologie ajoutée et la réforme ultérieure. Contrôler que la variante est indisponible en FRA/GBR/BRZ/SC2. Tester victoire et défaite américaines sans perte anormale d'unités.

Contrôler le journal de l'engagement et le modificateur visible. Tester victoire/défaite non vide, combat vide, autre guerre, répétition avant 90 jours, seuils 34/35/65/66, primes avec/sans 7 500 £, répétition avant 180 jours, accord français accepté puis renouvelé et sauvegarde/rechargement. Le renouvellement du soutien ne doit pas répéter son gain de ferveur. Après la paix, aucun des trois modificateurs ne doit rester. Les sept profils militaires et leurs formations sont comparés à la base R2.

Les textes FR/EN sont une première rédaction immersive, accompagnée ici des paramètres techniques ; validation fonctionnelle et contrôle de rendu restent distincts.
