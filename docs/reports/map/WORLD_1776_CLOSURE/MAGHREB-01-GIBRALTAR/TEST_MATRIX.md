# Contrôles et protocole

Commandes exécutées avec le Python du workspace :

- `python tools/world1776_gibraltar.py --apply --validate` : installation unique effectuée ; première validation interrompue par un mauvais type d'argument dans l'outil de comparaison, corrigé sans nouvelle écriture fonctionnelle.
- `python tools/world1776_gibraltar.py --validate` : **36/36**, sortie 0. Détails dans `VALIDATION.json` ; aucune erreur moteur n'est déduite de l'incident du validateur.

Couverture : différence d'un seul champ par rapport au natif archivé ; douze définitions uniques ; onze autres détroits préservés ; propriétaire espagnol de Ceuta et britannique de Gibraltar ; existence des deux points maritimes ; terrain terrestre enregistré ; carte et toutes attributions politiques identiques ; population mondiale et index/identité Git inchangés ; 3 644 fichiers antérieurs protégés sans différence.

Lecture de compatibilité des missions : revendication marocaine conditionnée à la persistance d'un autre propriétaire dans AL_RIF ; conquête espagnole de la région entière distincte du simple contrôle de la rive. Cette lecture n'est pas une exécution des conditions en moteur. Scripts de missions conservés.

Test groupé ultérieur, statut **NOT_RUN** : nouvelle partie en 1776, vérifier Espagne à Ceuta/rive sud et Grande-Bretagne à Gibraltar/rive nord, aucun contrôle marocain initial sur la rive sud ; vérifier qu'une conquête effective de Ceuta peut transférer cette rive. Contrôler accès/fermeture selon les règles natives conservées, puis sauvegarde/rechargement et journaux Maroc/Espagne. Aucune validation humaine créée ni test intermédiaire demandé.
