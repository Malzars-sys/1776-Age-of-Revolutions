# Contradictions et arbitrages — instructions permanentes

25 octobre 2026. Ce document n’autorise aucune correction de gameplay ou de suivi. Les sources Sxx renvoient à l’[audit sourcé](PERMANENT_RULES_AUDIT.md) et à ses empreintes.

## C01 — Confirmation humaine brève et champs obligatoires du reçu

**Arbitrage ouvert, sans modification des reçus existants.**

- Le schéma SERG demande notamment une nouvelle partie datée et au moins un mois de simulation (S02, « Mises à jour additives » ; S18, `terminal_evidence` et `partial_runtime_evidence`).
- L’interdiction d’inventer des contrôles impose de limiter le reçu à ce que le joueur a confirmé (S02/S03). Certaines confirmations sont brèves : S19 cite « Ok, Ratisbonne passe. Tu peux passer à Ortenburg. », renseigne les champs du protocole et explique cette interprétation dans `protocol_confirmation_basis`.
- L’ambiguïté porte sur la portée d’une réponse globale au protocole fourni : vaut-elle confirmation de toutes ses étapes, ou faut-il une mention expresse de chacune des informations obligatoires ? Ce document ne déclare pas ce reçu faux et ne remet pas en cause l’acceptation du noyau.

**Décision à obtenir pour les futurs cas :** définir quand une confirmation globale vaut attestation du protocole complet et comment représenter les détails non répétés dans le schéma. La consolidation ne modifie ni validateur, ni reçu, ni progression. En attendant, V04 interdit d’affirmer un détail absent sans base explicite suffisante ; si le schéma impose ce détail, demander cette précision avant de le certifier.

## Écarts résolus par la portée ou un remplacement explicite

| Sujet | Sources et différence | Traitement retenu |
| --- | --- | --- |
| Conservation mondiale des populations | Anciennes passes MAP conservatrices ; S04 déclare explicitement remplacer la conservation absolue pour les découpages SERG ; S23 distingue transfert et correction historique dans WORLD | T02 distingue les opérations. Aucun transfert pur ne justifie de perdre des habitants ; une correction historique autorisée publie son delta, sans compensation artificielle. Aucun chiffre local n’est généralisé. |
| Transition WORLD malgré des obligations restantes | S23 permettait une transition après bilan technique ; S05 consigne le remplacement explicite du 24 octobre | La confirmation du test balkanique groupé est nécessaire avant de quitter les Balkans. Cela ne crée pas une barrière identique dans tous les chantiers. |
| Un lot ou plusieurs lots indépendants | Missions SERG bornées et latitude WORLD/TECH pour des ensembles cohérents (S02, S03, S23) | L’autorisation de la mission fixe la quantité et les dépendances. Le routage permanent ne lance pas la prochaine étape. |
| Sans changement fonctionnel : moteur ou décision documentaire | Profil SERG `no_functional_change` et critères de décision NA (S02) | Une conformité démontrée appelle la décision utilisateur et les contrôles adaptés, pas une validation moteur fictive. `NOT_APPLICABLE_VERIFIED` ne signifie pas tâche ignorée. |
| Git historique et Git actuel | Une ancienne passe décrit une création de branche (S20), tandis que les missions récentes interdisent les écritures (S03, S23 et présente mission) | Ancienne action contextualisée, aucune permission permanente. W02 conserve l’interdiction par défaut. |
| Archives à préserver et dérivés graphiques non versionnés | Préservation des rapports/reçus (S02/S03) ; cache des dérivés et sauvegardes temporaires d’images (S15) | Préserver les preuves et masters ; produire les nouveaux dérivés dans le cache. La consolidation ne supprime aucun fichier ancien. |
| Palette secondaire et quincaillerie rouge | Contrat général violet pour les productions secondaires (S16) ; demande particulière du joueur pour les dessins rouges de quincaillerie (S17) | Exception locale documentée, conservée dans son rapport ; aucun passage général des PM secondaires au rouge, aucune harmonisation automatique de ce lot depuis l’ancien contrat. |
| Lot graphique de trois et demandes spécifiques | S15/S16 imposent le cycle de trois pour les dessins individuels, tandis que S17 décrit quatre dessins demandés ; les flèches communes ont leur autorisation distincte | A02 conserve la règle et l’exception explicitement bornée. Une exception passée ne dispense pas de l’approbation des futurs dessins. |
| Ancienne baseline et préservation de concurrence | Anciennes captures de référence ; S03/S06 imposent le contenu courant | Comparer les écarts et adapter le patch, jamais restaurer l’intégralité d’un fichier ancien. Une différence légitime n’est pas une régression à annuler. |
| Recherche seulement ou corrections installées | S08 décrit un paquet préparatoire ; S02/S03/S23 autorisent des corrections dans certaines missions | Statut attaché au document ou à la mission ; aucune interdiction universelle d’implémenter, aucune autorisation d’installer une hypothèse non vérifiée. |

## Décisions expressément non prises

La consolidation ne tranche ni limites territoriales, ni cibles démographiques, ni recettes, ni parents particuliers de technologies, ni clôture d’une région. Les statuts actuels et les anciens résultats restent dans leurs dossiers. Aucun ancien rapport n’est réécrit pour faire disparaître une divergence.
