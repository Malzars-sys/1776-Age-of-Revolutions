# American Revolution Rework R2 — livraison

> **Historique.** Le financement et le déclenchement décrits ici sont remplacés par [R3](../AMERICAN_REVOLUTION_R3/SYNTHESIS.md) : demande américaine, traité de crédit, remboursement différé et interventions FRA/SPA. Le contenu américain non remplacé est conservé et vérifié par le validateur R3.

**Suivi du test joueur :** l'offre initiale ne s'ouvrait pas et le journal exposait une variable. Le [correctif de déclenchement et d'interface](RUNTIME_FIX_01/REPORT.md) est installé ; sa confirmation en jeu reste à obtenir. L'ancienne réussite des seuls contrôles de fichiers ne confirmait pas le déclenchement du pacte.

Les mécanismes franco-américains, les marchands armés, les Minutemen, la ferveur, les échos internationaux et trois Pères fondateurs sont installés. **Leur validation dans Victoria 3 reste à effectuer sur une nouvelle partie.** La cavalerie mondiale possède un patch de comparaison isolé, livré sans activation.

## État de chaque fonctionnalité

| Fonctionnalité | État | Résultat |
|---|---|---|
| USA-FRENCH-SUPPORT-1776 | **IMPLEMENTED — READY_FOR_RUNTIME_VALIDATION** | offre française et consentement américain ; deux niveaux de subsides et fournitures ; obligation native ; traité public ultérieur conditionnel ; anciens prélèvements incohérents neutralisés |
| MIL-NAV-USA-1776 | **IMPLEMENTED — READY_FOR_RUNTIME_VALIDATION** | cinq marchands armés, coque et cinq équipements disponibles sans don de technologie ; statistiques et coûts conservés |
| CONTENT-USA-R1 : Minutemen | **IMPLEMENTED — READY_FOR_RUNTIME_VALIDATION** | variante américaine volontaire du modèle d'armée ; préparation rapide, instruction et coût matériel ; réforme ultérieure possible |
| CONTENT-USA-R1 : ferveur | **IMPLEMENTED — READY_FOR_RUNTIME_VALIDATION** | score 0–100, trois états exclusifs ; réactions bornées aux batailles et aux décisions, sans décroissance calendaire |
| CONTENT-USA-R2 : échos | **IMPLEMENTED — READY_FOR_RUNTIME_VALIDATION** | quatre familles d'événements après la résolution ; destinataires et choix conditionnels, effets de douze mois |
| CONTENT-USA-R2 : fondateurs | **IMPLEMENTED — READY_FOR_RUNTIME_VALIDATION** | Franklin, Adams, Jefferson ; mission diplomatique et commission politique alternative, existence/vie/disponibilité contrôlées |
| MIL-CAVALRY-1776 | **DESIGN_ONLY — patch isolé non installé** | diagnostic réexécuté, candidat P1 applicable à un fichier ; aucune statistique mondiale active modifiée |
| MIL-START-AUDIT, BAL-USA-REVOLUTION-R1, USA-COMMANDERS-1776 | **PRESERVED — attestation limitée du joueur** | corrections antérieures conservées ; aucune durée ou campagne exhaustive inventée |

## Budget et accord

L'autosave retrouvée est `autosave_exit.v3`, datée du 1er janvier 1776 et jouée en France, version 1.13.11. Lecture et décodage d'une copie seulement, sans modification de l'original. Elle ne constitue pas la reproduction exacte de la capture américaine, ni une campagne exécutée par l'agent.

Le déficit américain sauvegardé est **hebdomadaire : −27 466,77 £**, contre un surplus français de **+31 758,56 £**. Les 15 541 £ de salaires administratifs et 5 302 £ de subventions identifiés pèsent davantage que les seuls 1 839 £ de salaires militaires et 1 467 £ de biens militaires identifiés. Le problème est donc principalement structurel parmi les postes identifiés ; retirer l'ancien revenu gratuit de 60 000 £ l'a révélé. Le relevé conserve séparément 5 829 £ de dépenses non attribuées avec certitude, et ne prétend pas reconstruire le taux de prêt effectif ou tous les ordres commerciaux du marché mondial.

| Scénario arithmétique, hors réactions de marché et fret | USA | FRA |
|---|---:|---:|
| Sans nouveau soutien | −27 466,77 £/semaine | +31 758,56 £/semaine |
| 14 000 £ + six armes et un canon | −13 466,77 £/semaine | +17 758,56 £/semaine avant fournitures |
| 21 000 £ + douze armes et un canon | −6 466,77 £/semaine | +10 758,56 £/semaine avant fournitures |

Les subsides sont de véritables articles natifs de transfert FRA → USA ; les fournitures utilisent l'expédition native de biens, à la charge de la France. Les résultats du tableau sont des projections comptables à partir du même instant, **pas des mesures de campagne**. La guerre peut encore épuiser les finances américaines ou françaises.

Chaque tranche dure au plus 182 jours, avec délai de 196 jours entre signatures, six tranches au maximum, refus des deux côtés et conditions d'arrêt. Une seule obligation diplomatique initiale est consentie, sans prêt, remboursement automatique ou souveraineté française. Les privilèges commerciaux réciproques et l'alliance appartiennent à une négociation publique distincte, possible à partir d'octobre 1777 et soumise aux conditions natives ; le statut de sujet peut notamment empêcher une alliance avant l'indépendance. Aucun effet ne force la France à entrer en guerre en janvier 1776.

## Rapports et contrôle

- [USA_FRENCH_SUPPORT_1776.md](USA_FRENCH_SUPPORT_1776.md) : comptes, anciennes aides/dettes, montants, matériel, obligation, commerce, interruptions et protocole.
- [MIL_NAV_USA_1776.md](MIL_NAV_USA_1776.md) : types, équipements, technologies, coûts et limites navales.
- [CONTENT_USA_R1.md](CONTENT_USA_R1.md) : loi, score de ferveur, modificateurs, hooks et bornes.
- [CONTENT_USA_R2.md](CONTENT_USA_R2.md) : personnages, dates, fonctions, événements et destinataires.
- [MIL_CAVALRY_1776.md](MIL_CAVALRY_1776.md) : exposition à 117 pays / 505 bataillons, proposition et essais requis.
- [PLAYER_ATTESTATION.md](PLAYER_ATTESTATION.md) : portée exacte de la confirmation antérieure du joueur.
- [MANIFEST.json](MANIFEST.json) : fichiers R2 actifs et empreintes ; fichiers protégés comparés à la base.

**159 contrôles R2 et 22 contrôles du candidat de cavalerie passent : 181 au total.** `FINAL_VALIDATION.json` remplace les instantanés intermédiaires de validation pour l'état livré. Syntaxe structurelle, références, assets, localisations FR/EN, plafonds et exclusivité, durées, consentements, dette héritée, invariants comptables, armées et commandants protégés ont été vérifiés. Le correctif ajoute des contrôles de la guerre réelle, du rattrapage de l'offre, des boutons et des conditions lisibles. Le patch de cavalerie passe un contrôle d'applicabilité sans être appliqué ; son candidat conserve les coûts, technologies, mobilités, lanciers et unités non montées. Le contrôle des espaces du diff des six fichiers existants modifiés par R2 passe également.

Ces contrôles ne prouvent pas la création effective d'un traité, la traversée d'un convoi, les capacités de recrutement ou le comportement de l'IA dans le moteur. Aucun nouveau résultat de simulation, de bataille, de sauvegarde/rechargement ou de rendu d'interface n'est revendiqué. Le validateur R1 compare certains fichiers à leur état antérieur à R2 et ne doit plus servir seul à juger les changements intentionnels de navire, diplomatie et chaîne financière ; le validateur R2 contrôle maintenant leur nouvelle base et les corrections militaires conservées.

Les textes français et anglais ont une première rédaction immersive conforme à la demande R2, et leurs paramètres techniques sont conservés dans les rapports. Leur finition reste à confirmer après vérification humaine du fonctionnement et du rendu. Pas de traduction espagnole dans cette passe.

## Limites à vérifier en priorité

1. Nouvelle partie USA/FRA, J+2 : offre, deux consentements, premier débit/crédit identique dans les budgets, puis coûts et arrivée des biens. Tester refus, défaut, routes coupées, paix et rechargement avant de prolonger une campagne.
2. Après 1777 : ratification native du traité public, privilèges réciproques, absence d'entrée en guerre scriptée. La convention de 1776 reste visible comme couverture commerciale ; le moteur ne lui procure pas une véritable invisibilité diplomatique.
3. Marine : équipages, entretien et remplacement des coques ; l'expansion de l'administration navale conserve sa technologie propre, absente au départ. Le poids IA du nouveau navire est nul ; son renouvellement par l'IA n'est pas garanti par ce correctif.
4. Loi Minutemen : vérifier les effets et prérequis effectivement hérités du parent dans l'interface. Ferveur : seuils, délais, paix, gain unique de l'accord français.
5. Fondateurs : présence en nouvelle partie, décès/départ pendant une fenêtre de choix, commission unique et retrait après changement de régime. Échos : destinataires éligibles et inéligibles, deux issues et réception unique. L'annexion complète de USA avant son journal peut supprimer la diffusion finale ; aucun destin révolutionnaire n'est forcé.

## Coordination et Git

Les fichiers de carte, les populations et les systèmes impériaux du chantier concurrent n'ont pas été édités par R2. Les définitions initiales françaises et américaines sont préservées ; les changements au fichier de guerre, au journal et aux premiers événements financiers sont limités aux besoins décrits. Les trois clés françaises/anglaises du journal hérité sont corrigées sans réécrire le reste de leurs fichiers.

HEAD vérifié : `9b1764e3f43a7e9bd6ef4bee7eef9f9182d069b6`, identique à la base enregistrée de R2 ; empreinte de l'index inchangée. Aucun staging, commit, push, changement de branche ou opération d'intégration effectué par cet agent. L'installation canonique et les sauvegardes sont restées en lecture seule. Les autres fichiers déjà modifiés dans le workspace appartiennent notamment aux chantiers antérieurs ou concurrents ; le manifeste R2 ne se confond pas avec un état Git global.
