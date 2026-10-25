# Révolution américaine R4 — secours, dette et appel des alliés

> **Rapport historique.** L’essai utilisateur a révélé un échec moteur lors de la ratification et des interventions trop larges. La correction courante est décrite dans [la synthèse R5](../AMERICAN_REVOLUTION_R5/SYNTHESIS.md). Les contrôles statiques R4 ci-dessous n’avaient pas détecté l’erreur de portée des options d’article.

18 octobre 2026. **Implémenté ; 201 contrôles statiques réussis. Essai moteur R4 non effectué.**
Les résultats sont dans [VALIDATION.json](VALIDATION.json). Les anciennes validations
R2/R3 décrivent leurs versions historiques, et ne constituent pas une validation
du fonctionnement courant. Aucun commit, staging ou changement de branche.

## Départ et pays joué

- Les **Compagnies de minutemen** sont activées dans l’historique américain,
  dès le premier jour. Le complément `zz_1776_usa_revolution_r2.txt` est chargé
  après le fichier américain d’origine qui active les levées paysannes.
- Avec un joueur américain, l’événement apparaît après trois jours écoulés
  — le 4 janvier depuis le départ du 1er janvier. Son bouton ouvre le journal ;
  le joueur demande ensuite le secours et choisit ses engagements.
- Avec une IA américaine, un événement caché ouvre le journal et envoie la
  demande au même moment. La France reçoit la lettre un jour après l’envoi,
  même lorsqu’elle est jouée par un humain. Le joueur français peut accepter,
  exiger 5 % d’intérêts, ou refuser. Le Congrès doit encore ratifier l’offre.
- Les décisions de récupération suivent aussi ces deux parcours. Les gardes
  communes empêchent deux demandes simultanées ou un deuxième prêt en cours.

## Traité de dix ans

L’accord final reste présenté par les événements de consentement, puis créé
comme **traité natif ratifié**, visible dans la diplomatie. Il n’est pas envoyé
comme brouillon par la fenêtre native de rédaction des traités.

| Article, dans l’ordre | Engagement |
|---|---|
| 1. Transfert d’argent au Congrès | France → États-Unis, **30 000 £ par semaine**, transfert monétaire natif |
| 2. Reconnaissance de dette | États-Unis → France, avec l’icône fournie par l’utilisateur |
| 3. Instructeurs | +10 % d’instruction et d’expérience américains ; coût militaire français conservé |
| 4. Armes légères | France → États-Unis, **15 unités** |
| 5. Artillerie | France → États-Unis, **1 unité** |

Une obligation diplomatique est consentie à la ratification. Les deux promesses
américaines donnent le même secours ; seuls les intérêts changent : aucun,
ou 5 % du capital ajoutés une seule fois lors du remboursement.

Le transfert utilise `is_money_transfer`, avec une quantité native de 30 000.
Les anciens versements de trésorerie périodiques sont désactivés : ils ne
doublent pas le paiement natif. Le financement dure dix ans après signature,
y compris après l’indépendance ou septembre 1783. Un défaut français gèle
le paiement selon la règle native ; les livraisons conservent leurs blocages
maritimes et commerciaux. Le déblocage de banque centrale n’est pas exigé.

La créance est le **capital contractuel prévu pour les dix ans**, calculé à
la signature : 30 000 × durée native d’engagement en jours ÷ 7. Pour 3 650 jours,
cela donne environ **15 642 857 £**, ou **16 425 000 £** avec 5 % d’intérêts.
La durée réellement lue dans le traité est prioritaire sur cette valeur de
repli. Ce calcul simple ne mesure pas les versements suspendus en cas de défaut
ou de rupture anticipée : ce n’est pas un registre des décaissements effectifs.
Les armes et les instructeurs ne sont pas capitalisés.

Le créancier ne peut réclamer le paiement avant la fin de l’engagement. Une
garde vérifie aussi les traités encore contraignants portant la reconnaissance
de dette, y compris après prolongation. Le débiteur peut payer, avec débit et
crédit de même montant, ou répudier : **+10 d’infamie et −40 de relations**.
Le règlement ferme la créance, afin de ne pas répéter les pénalités. L’accord
générique hors de cette convention reste un prêt accepté de 10 000 £, sans
intérêts, sur dix ans, avec un seul créancier par débiteur.

## France et Espagne

L’entrée française de janvier 1776 venait du tirage R3 à 10 %. Le contrôleur
automatique est maintenant bloqué avant 1777 : 45 % au premier tirage de 1777,
75 % en 1778, puis intervention certaine à partir du 17 mars 1778 si la guerre
et les conditions diplomatiques permettent toujours l’entrée. Le délai annuel
ne bloque pas cette échéance. Un joueur français garde son choix.

L’Espagne n’effectue **plus aucun tirage annuel**. L’IA française peut utiliser
« Appeler l’allié du Pacte de famille » après son entrée dans la guerre
américaine. Cette action exige l’alliance franco-espagnole existante, puis
l’accord espagnol. L’acceptation ratifie une clause Join Ongoing Wars, avec
l’Espagne comme intervenant et la France comme camp soutenu. Ce chemin accepte
que la France soit un allié participant plutôt que le chef américain.

L’appel concerne uniquement la guerre comprenant les États-Unis et la
Grande-Bretagne. Il ne fait pas entrer l’Espagne dans les autres guerres
françaises. La situation financière, le défaut, les autres guerres et les
relations peuvent conduire l’IA espagnole à refuser. L’intervention générique
ne contourne pas ce parcours pour l’IA espagnole dans cette campagne.

Les objectifs de guerre français et espagnols, les stratégies militaires R3,
la garnison britannique au Guatemala et le recul américain réduit de 30 %
sont préservés. Les investissements et débarquements dépendent du moteur ;
aucune invasion réussie de la Grande-Bretagne n’a été observée en R4.

## Compatibilité, illustrations et conservation

Les événements visibles utilisent la vidéo Great Wave `ep2_intellectual_writer`,
présente dans l’installation et utilisée par les événements japonais vanilla.
L’icône de reconnaissance de dette et sa provenance sont détaillées dans
[ASSETS.md](ASSETS.md), avec la consigne exacte et le mode de l’outil.

Les journaux et la rédaction associés restent au statut **technique à valider**.
La validation humaine de leur fonctionnement déclenchera la seconde passe
immersive prévue par le guide du dépôt ; les identifiants internes restent
dans cette documentation, hors des textes joueurs.

L’ancien essai du 30 janvier a révélé des erreurs réelles que les contrôles
statiques R3 n’avaient pas détectées : déclencheur de participation inconnu,
getter de relations sans portée, entrée `goods` refusée par `can_create_treaty`,
champ `base` invalide dans les décisions et quatre notifications non localisées.
Les scripts ont été corrigés contre les exemples de l’installation locale.
Le contrôle natif préalable valide les trois premiers articles ; la portée
commerciale est vérifiée séparément pour les fournitures, car le parseur de
ce contrôle refusait leurs entrées. La création conserve les cinq articles.

Les scripts du lot utilisent UTF-8 BOM et les nouvelles localisations existent
en français et en anglais. La base de travail R4 est archivée dans
[BASELINE.json](BASELINE.json), les erreurs observées dans
[R3_RUNTIME_ERRORS.txt](R3_RUNTIME_ERRORS.txt). La carte, les populations,
les scripts impériaux et les ressources Saint-Gobain n’ont pas été modifiés
par ce lot. Les corrections militaires R1/R2 et le contenu américain restent
couverts par les contrôles de non-régression applicables.

**Redémarrer complètement le jeu et lancer une nouvelle partie.** Les clauses
d’un ancien traité signé, les lois déjà initialisées et une entrée en guerre
déjà réalisée ne sont pas remplacées rétroactivement. La migration désactive
les anciennes avances périodiques sans transformer les anciens prêts en une
nouvelle créance de quinze millions. Aucune sauvegarde n’a été modifiée.

Les essais attendus figurent dans [RUNTIME_CHECKLIST.md](RUNTIME_CHECKLIST.md).
