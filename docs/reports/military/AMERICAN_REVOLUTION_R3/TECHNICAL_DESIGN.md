# Fonctionnement interne R3

## Déclenchement et consentements

`on_game_started_after_lobby` initialise une seule fois la version et programme
l'événement américain avec `days = 3`. L'historique ne crée pas le journal de
secours. L'option de l'événement le crée et pose son autorisation d'affichage.
La décision de récupération déclenche cet événement sans ratifier un accord.

Le bouton du journal et la décision américaine appellent le même effet de
demande : choix USA → réponse FRA à J+1 → offre USA → ratification. Les
marqueurs temporaires empêchent de lancer plusieurs demandes simultanées.
Le garde `can_create_treaty` reprend exactement les paramètres et entrées de
`create_treaty`. L'obligation n'est attribuée qu'après ce garde ; une obligation
déjà existante n'est pas réémise pour en prolonger artificiellement la durée.
Les anciens IDs d'événements R2 sont conservés comme événements cachés inertes
pour les sauvegardes qui les ont encore en attente.

## Pourquoi un pacte verse les avances

Les articles natifs `is_money_transfer` savent verser de l'argent, mais le
schéma fourni pour les articles n'offre pas de hook hebdomadaire pour constater
la somme effectivement prêtée. Ajouter un registre théorique à un transfert
potentiellement gelé produirait une dette fantôme. La priorité de R3 est de
faire correspondre chaque livre due à un versement effectivement effectué.

Le traité comporte donc une clause de crédit propre au mod, sans le drapeau
`is_money_transfer`, et ouvre un pacte diplomatique de dette. Son
`weekly_effect`, documenté et utilisé dans le vanilla, réalise ensemble :

1. les contrôles de guerre, date, créancier, pacte, défaut et réserves ;
2. le débit de la trésorerie du créancier ;
3. le crédit de la trésorerie du débiteur ;
4. l'augmentation égale du capital du débiteur ;
5. le verrou de sept jours contre les versements rapprochés.

Le premier versement emprunte le même effet après l'entrée en force de la
clause. La phase exacte du premier versement par rapport au jour hebdomadaire
du pacte doit être vérifiée en jeu. Le verrou peut reporter la deuxième
avance au prochain passage du pacte. Aucun deuxième transfert natif n'est
superposé à ces opérations.

Les versements de trésorerie ne changent pas le solde ordinaire comme un
revenu fiscal. Le capital stocké, les réserves des deux pays et le détail du
pacte sont les références de contrôle. Le principal est enregistré sur le
débiteur avec un créancier de type country ; aucun montant n'est déduit de
la seule présence d'un modificateur ou d'une promesse.

Les livraisons utilisent le drapeau natif `is_goods_transfer`, ses entrées
`goods` et `quantity`, ses capacités d'exportation et sa route maritime.
Leur disponibilité matérielle ne se confond pas avec le prêt d'argent. Les
instructeurs appliquent uniquement leurs modificateurs d'instruction et
d'expérience, avec un coût de biens militaires français.

Le marqueur du crédit révolutionnaire borne sa clause de reconnaissance au
3 septembre 1783. Le pacte de dette n'a pas cette limite : il continue à
porter le principal après disparition des clauses du traité.

## Prêt générique et règlement

L'acteur de `aor1776_deferred_debt` est le prêteur ; la cible est le débiteur.
L'action exige son consentement et verse un prêt unique symétrique de 10 000 £.
Le type de pacte sert aussi aux avances américaines ; sa pulsation n'accorde
du crédit récurrent que dans le cas USA/FRA explicitement autorisé.

La demande de remboursement vérifie le créancier enregistré, un principal
positif, l'absence d'une demande déjà en attente et la paix du débiteur.
Elle calcule le dû au moment de la demande : principal, ou principal × 1,05
pour le crédit renforcé. Le paiement inverse les deux trésoreries ; le refus
ne transfère rien, archive le dû et le créancier, applique les sanctions puis
retire la créance active. Ni paix ni fin du journal ne retirent le principal.

Un seul créancier actif par débiteur est la limite explicite de ce registre.
Le débiteur peut accepter une nouvelle créance après le règlement ou la
répudiation de l'ancienne ; cela nécessite un nouveau prêt réel et accepté.

## Intervention et IA

L'action intégrée, l'article `join_war` et les tirages de campagne appellent
`aor1776_intervene_effect`. Les participants sont enregistrés en scopes nommés
stables avant de parcourir les diplomatic plays en guerre. L'effet ne rejoint
que les guerres dont le pays soutenu est initiateur ou cible principal, et
seulement si l'intervenant n'en fait pas déjà partie.

Les tirages automatiques FRA/SPA sont exclus de l'IA générique de l'action et
de l'article, pour ne pas contourner les probabilités annuelles. Les événements
d'échéance sont programmés depuis le 1er janvier 1776 : 806 jours pour le
17 mars 1778 et 1267 jours pour le 21 juin 1779, différences calendaires
calculées avec années bissextiles. Le contrôleur mensuel recouvre les dates
passées ou une sauvegarde plus ancienne. La concordance du calendrier du
moteur reste une vérification runtime.

Les buts historiques ne sont ajoutés que dans le play USA initiateur / GBR
cible, une seule fois par intervenant. L'objectif métropolitain distinct
emploie le `kind = humiliation` natif avec
`contestion_type = control_target_country_capital`, documenté dans le schéma
des buts de guerre. Ce n'est pas une annexion ni une revendication historique
inventée sur l'Angleterre. Les stratégies utilisent `wargoal_weights` pour
les buts, et les désirs natifs `antagonize` / `protect` dans
`secret_goal_scores`. Ces deux familles ne sont pas interchangeables.

Les cibles d'armée et de marine s'ajoutent aux calculs vanilla ; les coefficients
de groupes de bâtiments les multiplient. La stratégie n'est plus éligible
après la paix. Aucun ordre scripté de débarquement non documenté n'est inventé.

## Vérifications et portée

Les nouvelles actions de dette reprennent, sans transformation, les icônes
vanilla `bankroll.dds` et `take_on_debt.dds` dans le dossier des icônes de
lentille, sous leurs identifiants d'action. L'icône d'intervention provient
du mod intégré et conserve son attribution distincte.

`tools/validate_american_revolution_r3.py` lit la base de travail antérieure
enregistrée sous `baseline/`, compare les paramètres des traités, la
conservation des fonds et la dette, et reprend les contrôles R2 non remplacés
sur les navires, Minutemen, ferveur, fondateurs et échos. Les scénarios de
trésorerie sont arithmétiques ; ils ne constituent pas un moteur de jeu.

Le fichier militaire européen est comparé intégralement après neutralisation
des deux seules valeurs HQ/hub demandées. Les autres armées partagées restent
identiques à la copie de travail pré-R3. Aucun script cartographique n'est
exécuté. HEAD et index sont seulement lus. Les résultats de cette passe sont
`READY_FOR_RUNTIME_VALIDATION`, jamais `PASS_RUNTIME_USER_VALIDATED`.
