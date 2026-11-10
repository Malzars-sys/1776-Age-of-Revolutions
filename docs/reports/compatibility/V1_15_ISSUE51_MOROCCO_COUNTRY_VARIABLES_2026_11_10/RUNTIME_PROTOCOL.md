# #51 — Vérification moteur du Maroc

Révision : `CONTRACT.json`, six lectures corrigées dans le journal marocain. **Aucun test moteur n'est encore attesté pour ce correctif.**

1. Relancer complètement le jeu, puis commencer une nouvelle partie en 1776 avec le Maroc et la configuration DLC habituelle. Vérifier la présence des trois barres régionales et des modificateurs d'anarchie sur les portions marocaines du Rif, de Marrakech et du Maroc intérieur.
2. À l'activation, les valeurs initiales restent à 260. Vérifier que les pénalités sont numériques et cohérentes avec le multiplicateur 2,55, sans valeur vide ni effet calculé à partir d'une variable d'État absente.
3. Laisser passer au moins un changement de mois. Si une barre évolue, vérifier que sa pénalité régionale suit cette barre et que les autres régions conservent leur valeur propre. Les coefficients n'ont pas été rééquilibrés.
4. Examiner seulement les nouvelles lignes d'erreurs de ce lancement. Les erreurs « Value of wrong type » / type `none` issues des six multiplicateurs de `06_morocco_lands_of_anarchy.txt` ne doivent plus apparaître. Les neuf messages conservés dans les preuves sont antérieurs et ne doivent pas être présentés comme une nouvelle panne.
5. Sauvegarder, recharger puis passer un autre mois ; vérifier les barres et les pénalités régionales. Ne pas attribuer à ce test une validation des changements de propriétaire : le nettoyage territorial reste hors de cette passe.

Ce contrôle peut rejoindre la prochaine revue groupée. Ne pas effacer les journaux d'erreurs pour faire disparaître un constat, ni certifier les trois régions après n'en avoir inspecté qu'une. Le correctif ne change ni les frontières du Rif ni les conditions de reconquête du détroit.
