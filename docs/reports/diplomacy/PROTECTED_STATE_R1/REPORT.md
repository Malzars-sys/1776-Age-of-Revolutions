# États protégés — fusion des vassalités non reconnues

Statut : IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION. Référence de cette passe : demande utilisateur du 31 octobre 2026.

Un seul type générique remplace « Suzeraineté durranie sur Kalat » et « Allégeance traditionnelle » : **État protégé**. Les anciennes définitions sont supprimées par leurs propres fichiers d’override, pas conservées comme deux alias de types. Les anciens libellés sont des renvois de localisation uniquement.

Les quatre relations initiales DUR–KAL, DUR–BHW, DUR–D3S et KAL–LBL utilisent le même pacte. Aucune frontière, population, institution, armée ou recette n’est changée. Raguse, les protections kazakhes et le système impérial du SERG restent hors fusion.

Progression : **État protégé (autonomie 3, 0 % de tribut) → Tributaire (2, 20 % natifs) → Vassal (1, 30 % natifs) → Intégration**. Le retour Tributaire → État protégé est ajouté. Les actions normales gardent leurs exigences de désir de liberté et leurs délais. Le niveau numérique 3 n’a pas de plafond identifié dans les définitions locales ; sa présentation dans le moteur reste à contrôler. Les branches normales sont explicitement routées pour éviter un saut d’étape.

Le premier niveau conserve gouvernement, forces, diplomatie propre et absence d’entrée automatique en guerre ; aucun versement régulier ni ajustement fiscal n’y est autorisé. Le suzerain doit être non reconnu. Les pays décentralisés sont exclus. Les trois rangs non reconnus peuvent être suzerains ; les règles de rang supérieur des étapes tributaires/vassales restent appliquées. Une proposition volontaire générique permet de réutiliser ce lien hors des Durrani ; l’IA peut y répondre, sans nouvelle campagne automatique de propositions mondiales.

## Icône et affichage

La première génération a été rejetée par l’utilisateur et n’est pas installée. La deuxième utilise directement les PNG convertis des trois DDS vanilla : protectorate_15, tributary_15 et vassal_15. Génération intégrée image_gen, fond transparent. Aucun dessin, changement de couleur ou détourage algorithmique de l’œuvre : seulement suppression de marge transparente, redimensionnement et encodage DDS.

Maître : `workshop_assets/source/PROTECTED_STATE_R1/protected_state_v2.png`. Source générée : `C:\Users\simeo\.codex\generated_images\01a149d5-1620-7bf2-bf90-7fa9bf443072\exec-2ee5adc9-1054-48be-a488-1df6486e3c3b.png`. Les prompts exacts et le statut de chaque version sont conservés dans ASSET_PROMPTS.json. Ne pas confondre installation et approbation visuelle humaine de la deuxième version.

L’action diplomatique et le concept ont une texture explicite ; les variantes avec et sans icône de la localisation, les texticons et les résolutions 128/30/64 px sont installés. Le chemin principal dessert les consommateurs natifs DiplomaticPact.GetDiplomaticActionType.GetTexture et SubjectType.GetTexture ; les noms dérivés et boutons de loupe ont également un DDS. Les fichiers ont alpha, canaux BGRA et chaîne de mipmaps complète.

## Vérifications et limites

Contrôles statiques : 274/274. Aucun test moteur ou reçu joueur ajouté. Les préimages, empreintes et changements ciblés sont conservés dans BASELINE.json et preimages/. Les anciens rapports DP/SERG et leurs tests historiques ne sont pas réécrits pour faire passer la nouvelle attente. Les premières exécutions sont archivées : une comparaison liste/tuple après sérialisation a produit douze faux écarts de non-régression, corrigés sans changer les types concernés ; le contrôle des suffixes natifs a ensuite révélé neuf clés manquantes par langue, complétées. La validation finale conserve ces mêmes exigences.

Il faut redémarrer le jeu et lancer une nouvelle partie pour charger la suppression des anciens types. Aucune compatibilité des anciennes sauvegardes contenant ces types supprimés n’est revendiquée. Dans le tableau des sujets, vérifier une seule ligne État protégé avec un nom lisible, 0 %, la bonne icône et la transition vers Tributaire. Vérifier DUR–KAL/BHW/D3S et KAL–LBL, les fiches pays, infobulles, liste diplomatique et proposition reçue en français/anglais. Vérifier un aller-retour Protégé ↔ Tributaire puis une réduction vers Vassal, et sauvegarder/recharger. Contrôler aussi un sujet impérial et une protection kazakhe comme témoins inchangés.
