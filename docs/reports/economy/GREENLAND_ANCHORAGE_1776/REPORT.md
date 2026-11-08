# Mouillage du Groenland dano-norvégien

31 octobre 2026 — IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION.

Ajout demandé par le joueur : un niveau de building_port dans STATE_GREENLAND, portion DENNOR, avec pm_anchorage et le PM par défaut sans collecte de données. Aucun prérequis technologique supplémentaire. Reprend la syntaxe du mouillage groenlandais du vanilla canonique, adaptée au propriétaire actuel DENNOR ; le mod remplaçait le fichier natif et ne conservait aucun port dans cette portion.

Avant : zéro port. Après : un port de niveau 1. À plein emploi, le PM d’ancrage prévoit 70 ouvriers, 20 employés et 10 bureaucrates ; son fonctionnement et son emploi réel ne sont pas observés en moteur. Les recettes ne sont pas modifiées.

Neuf contrôles statiques exécutés et réussis : port unique, niveau total 1, sélection des deux PM, compatibilité technologique des PM et du bâtiment, propriétaire actuel valide, analyse syntaxique, conservation des empreintes de tous les fichiers préexistants des bâtiments/États/régions et état Git en lecture seule inchangé. La première assertion comparait des tokens entre guillemets à des identifiants nus : sa normalisation a été corrigée, sans changement nécessaire du script de jeu.

Aucun changement de carte, POP, recette, technologie ou suivi territorial. BASELINE.json et DELIVERY_MANIFEST.json consignent les entrées et la version livrée. Le hub portuaire régional natif x5B326C est dans la portion groenlandaise autonome, pas DENNOR : aucun hub n'est déplacé dans cette petite demande de bâtiment ; placement du marqueur et fonctionnement du port à confirmer en moteur.

Contrôle moteur restant : nouvelle partie 1776, ouvrir le Groenland dano-norvégien et vérifier le port niveau 1 avec Mouillage ; sauvegarde/rechargement si nécessaire. Aucun test moteur déclaré.
