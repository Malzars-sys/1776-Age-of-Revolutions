# EUROPE-LAWS-R1 — vérification historique et corrections de départ

11 novembre 2026 — référence historique : **1er janvier 1776**. Installation : **IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION**, avec cas de conception réservés et exception technologique ottomane documentée. Ce statut concerne les demandes de lois écrites dans les fichiers, pas une observation des lois effectivement actives en jeu.

## Résultat installé

Un seul fichier de données ajouté : `common/history/countries/zzzz_1776_europe_starting_laws_r1.txt`.

- **68 demandes explicites de sujétion** pour des monarchies ou théocraties ; parmi elles, **60 TAGs allemands**, dont 34 avaient une dernière demande de suprématie nationale et 26 n'avaient aucune citoyenneté explicitement demandée. Pour ces 26, l'ancien choix effectif du moteur demeure inconnu.
- Les huit autres pays corrigés sont **Grande-Bretagne, France, Portugal, Pays-Bas autrichiens, États pontificaux, Suède, Danemark-Norvège et Monténégro**.
- **Suisse : suffrage censitaire → oligarchie**, approximation du régime agrégé de la Confédération ; les différences cantonales restent documentées.
- **Empire ottoman : demande de censure explicitée**. Le fichier de TUR ne demandait aucune loi de cette catégorie ; l'ancien choix par défaut du moteur n'est pas affirmé à partir de cette absence. Le signalement joueur d'Opposition interdite reste une observation à confronter au prochain lancement.

**70 demandes de lois au total**, sans nouveau pays, technologie, amendement, loi, groupe de lois ou changement de recette. Les 13 TAGs allemands déjà sous sujétion explicite restent intacts. Les 13 républiques/villes à conseils allemandes restent réservées : les traiter comme des monarchies serait une nouvelle approximation non justifiée.

Les données économiques et les gouvernances complexes sont conservées en attendant le choix décrit dans [OPTIONS.md](OPTIONS.md). L'Espagne n'est pas changée silencieusement : la discussion complémentaire a conduit à documenter une variante bourbonienne plutôt qu'à imposer un nom russe.

## Comment les signalements ont été vérifiés

Le relevé porte sur **106 pays actifs**, dont **86 TAGs de culture primaire nord- ou sud-allemande**, avec les effets de démarrage développés dans l'ordre. La présence d'un nom dans une liste de commandes ne suffit pas : une commande suivante ou un effet peut remplacer une première demande. Les branches conditionnelles sont séparées ; aucun défaut moteur n'est inventé.

Exemple : AUS contient une demande d'interventionnisme, mais un effet ultérieur redemande l'agrarianisme. La première lecture simplifiée a été rectifiée avant la décision. De même, les variantes marchandes de GEN/VEN sont de vraies lois existantes, et non du simple texte d'interface.

**Sujétion** appartient à **Citoyenneté** ; **Agrarianisme** et **Interventionnisme** appartiennent au **Système économique**. L'une ne remplace pas l'autre. La sujétion ici décrit les habitants liés au souverain, pas le statut diplomatique d'un pays vassal.

Un gate absent signale un problème d'adoption/re-promulgation ou d'alignement du profil. Il ne démontre ni l'absence historique de l'institution, ni le refus d'une commande initiale `activate_law` par le moteur. Les grants artificiels de romantisme, nationalisme ou économie politique classique sont donc écartés de cette passe.

Les affirmations « la plupart n'ont que le niveau 3 » et « tous les Allemands ont la suprématie nationale » ne décrivent pas exactement les fichiers actuels. Des profils nommés ont des technologies allant jusqu'à l'ère 5 ; plusieurs principautés allemandes ont déjà la sujétion ou n'ont pas de demande explicite de citoyenneté. Les chiffres exhaustifs se trouvent dans `COUNTRY_MATRIX.csv` et les deux instantanés.

## Décision par pays du premier lot

Sources historiques détaillées et limites : [SOURCES.md](SOURCES.md). « Conservé » ne signifie pas validation historique exhaustive de toutes les lois du pays.

| Pays / TAG | Vérification du signalement | Décision et limite |
|---|---|---|
| Grande-Bretagne / GBR | Agrarianisme sans romantisme ; suprématie nationale sans nationalisme. | Citoyenneté → sujétion, base juridique d'allégeance [S01]. Économie réservée, OPTIONS B. |
| France / FRA | Même paire de gates absents. | Citoyenneté → sujétion [S02]. Économie et réformes physiocratiques à distinguer, OPTIONS B [S06]. |
| Espagne / SPA | Suprématie nationale sans nationalisme confirmée. | Réservée : uniformisation bourbonienne réelle, mais non homogénéité accomplie [S03–S04]. Variante recommandée, OPTIONS A. |
| Portugal / POR | Suprématie nationale confirmée. | → Sujétion comme base dynastique ; ne nie pas centralisation pombaline ni exclusions coloniales [S22]. Les autres lois restent inchangées. |
| Pays-Bas autrichiens / BEO | Exclusion culturelle sans droits humains ; BEO est le TAG actif, pas BEL. | → Sujétion, dans une monarchie à droits provinciaux [S09–S10]. Les institutions de terre de la Couronne sont préservées. |
| Prusse / PRU | Suprématie nationale et, en dernière demande, agrarianisme. | Citoyenneté → sujétion, sans proclamer une égalité des populations [S21]. Économie caméraliste réservée, OPTIONS C. |
| Autriche / AUS | Agrarianisme en dernière demande ; citoyenneté déjà sujétion. | Pas de réécriture économique. OPTIONS C [S08]. Sujétion existante préservée. |
| Pologne-Lituanie / PLC | Suprématie nationale et république présidentielle confirmées, mais amendement électif déjà présent. | Préserver le montage de monarchie élective et le liberum veto [S11] ; variantes liées à examiner, OPTIONS E. |
| Pays-Bas / NET | République présidentielle + oligarchie, ainsi que suprématie nationale, sont les dernières demandes. | Pas de conversion en monarchie héréditaire générique ; stathoudérat républicain à représenter [S12], OPTIONS F. |
| Empire ottoman / TUR | Aucune loi de liberté d'expression explicitée dans l'historique. | Censure demandée explicitement [S18] ; absence du gate de périodiques consignée ci-dessous. |
| États pontificaux / PAP | Suprématie nationale confirmée. | → Sujétion ; théocratie et religion d'État conservées [S23]. |
| Suède / SWE | Suprématie nationale confirmée. | → Sujétion ; le lot ne certifie pas les autres lois après la réforme politique de 1772 [S19]. |
| Danemark-Norvège / DENNOR | Suprématie nationale confirmée ; DEN n'est pas le TAG actif de cet ensemble. | → Sujétion [S19]. Pas de refonte de toutes les lois de la monarchie absolue. |
| Suisse / SWI | Suprématie nationale, suffrage censitaire et république parlementaire confirmés. | Distribution → oligarchie [S13]. Gouvernance et citoyenneté restent à traiter, OPTIONS G. |
| Venise / VEN | Suprématie nationale et présidentielle confirmées, mais République marchande et Banques marchandes sont déjà présentes. | Pas de recul vers une monarchie ni d'effacement des variantes ; dogat/conseils à préciser [S14], OPTIONS F. |
| Toscane / TUS | Sujétion déjà demandée ; interventionnisme sans économie politique classique. | Pas de grant collectif ; réformes documentées avant 1776 [S16], OPTIONS D. |
| Parme / PAR | Sujétion déjà demandée ; interventionnisme sans gate. | Réservée : rupture de 1771, pas de copie de la Toscane [S17], OPTIONS D. |
| Lucques / LUC | Sujétion déjà demandée sous une gouvernance républicaine ; interventionnisme sans gate. | Exception de compatibilité et régime patricien à traiter ensemble [S15], OPTIONS D/F. |
| Gênes / GEN | Suprématie nationale et présidentielle ; Banques marchandes déjà présente. | Préserver les variantes et le dogat existants ; OPTIONS F [S14]. |
| Modène / MOD | Sujétion déjà demandée ; interventionnisme sans gate. | Économie réservée, recherche complémentaire nécessaire avant une variante ; OPTIONS D. |
| Massa-Carrara / MCA | Interventionnisme via effet initial ; sujétion déjà demandée. | Économie réservée ; aucune assimilation de MCA au TAG MAS/Mascara ; OPTIONS D. |
| Monténégro / MON | Suprématie nationale confirmée, sous théocratie + oligarchie. | → Sujétion ; souverain, clans, guvernadur et frontières conservés [S20]. |

### États allemands

La sujétion est retenue comme abstraction des liens princiers/ecclésiastiques. Cette décision ne nie pas les patriotismes ni les débats allemands antérieurs à 1789 [S21]. Les groupes d'intérêt, cultures primaires, droits d'ordre, dirigeants, autonomies et sujets impériaux sont inchangés.

Les 86 lignes allemandes et les lois avant/après figurent dans `COUNTRY_MATRIX.csv`. Les 13 républiques/villes réservées sont listées dans OPTIONS F, avec les solutions possibles pour le droit de bourgeoisie. Aucun territoire ou suivi SERG n'a été modifié.

## Exception ottomane et défauts conservés

La demande de censure est historiquement défendable, mais TUR ne possède pas `periodical_print_networks`. Le nouvel écart est **explicite**, conservé dans `VALIDATION.json` et OPTIONS H ; il n'est pas transformé en technologie gratuite. Une activité d'imprimerie autorisée depuis le premier XVIIIe siècle ne prouve pas ce réseau de périodiques. Le chargement effectif initial de cette loi doit être observé en moteur ; le contrôle statique ne le garantit pas.

Les gates économiques manquants, les gates de gouvernance républicaine et les restrictions de sujétion sous une république restent recensés. Les défauts précédents ne sont ni supprimés des résultats ni assimilés à des erreurs corrigées. OPTIONS.md donne les quatre degrés de solution demandés.

## Contrôles et concurrence

Commandes exécutées avec le Python local, option `-B` :

```text
tools/audit_europe_starting_laws_1776.py --output docs/reports/politics/EUROPE_STARTING_LAWS_R1_2026_11_11/BEFORE.json
tools/audit_europe_starting_laws_1776.py --output docs/reports/politics/EUROPE_STARTING_LAWS_R1_2026_11_11/AFTER.json
tools/validate_europe_starting_laws_1776.py
```

Le collecteur réutilise `collect_snapshot()` du validateur existant de technologies ; cela ne constitue pas une exécution de toutes les validations historiques ni une certification de tous les profils.

Résultats : **17/17 contrôles de contrat réussis**, **4/4 contre-exemples rejetés**. Les 70 dernières demandes correspondent au plan ; les profils technologiques des **106 pays** sont identiques. **43 constats de gate de loi disparaissent**, un constat ottoman documenté est ajouté. Ce n'est pas un comptage de technologies nouvellement recherchées.

Les **2 548 fichiers** runtime préexistants inventoriés dans common/events/gui/map_data/localization restent identiques. Le seul ajout runtime est l'historique ciblé. Aucune modification concurrente de ces entrées n'est observée entre les instantanés ; les autres changements antérieurs du workspace sont conservés. Les graphes TECH-R1/R2/R3, lois russes, recettes ECON-ALLOYS/quincaillerie, banques marchandes, amendement prussien et données territoriales sont préservés.

**Aucun test moteur, validation humaine, opération Git d'écriture, modification du vanilla, versionnement du mod ou mise à jour Steam Build dans ce lot.**

## Suite

Lire [OPTIONS.md](OPTIONS.md) pour choisir le traitement de l'Espagne et des autres cas réservés. La proposition prioritaire est une **variante de sujétion bourbonienne**, sans copier la nationalité officielle russe. Un nouveau groupe de lois ne semble pas nécessaire pour le premier correctif.

Le protocole [TESTS_MOTEUR.md](TESTS_MOTEUR.md) est prêt pour une vérification groupée ultérieure. Aucun test intermédiaire n'est demandé à chaque pays et aucune nouvelle région n'est engagée automatiquement.
