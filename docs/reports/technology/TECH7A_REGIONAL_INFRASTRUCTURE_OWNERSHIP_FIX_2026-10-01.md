# Infrastructures régionales : financement et propriété

Correction du 1er octobre 2026.

Le groupe `bg_land_transport_network` héritait de `bg_public_infrastructure`,
donc de `is_government_funded = yes`. Ce classement désignait un bâtiment
directement financé par l'État, au lieu d'un bâtiment économique subventionnable
dont les parts peuvent être transférées.

Le parent devient `bg_private_infrastructure`, comme pour le chemin de fer
vanilla installé. La déclaration `ownership_type = self`, manquante dans le
bâtiment régional, est également rétablie conformément à ce bâtiment vanilla.
Elle permet au bâtiment d'avoir des parts de propriété transférables.
Le groupe hérite du financement non gouvernemental, des
réserves de trésorerie de 25 000 par niveau et du démarrage subventionné des
nouvelles campagnes. `subsidized = yes` ne force pas les subventions dans une
campagne déjà commencée.

L'identifiant du bâtiment, son alias, les routes/canaux/rails, ses PM, l'absence
d'économie d'échelle et la consommation nulle d'infrastructure sont conservés.
Les lois économiques continuent à décider des restrictions sur la
privatisation et la nationalisation ; cette correction ne les contourne pas.

Validation : `tools/validate_regional_infrastructure_permissions.py` compare
la chaîne effective et le modèle de propriété aux définitions vanilla locales.
Test statique réussi ; aucun test des boutons dans le jeu ou de migration des
anciennes sauvegardes n'est revendiqué. Redémarrer le jeu pour recharger le
groupe puis vérifier les boutons dans une sauvegarde ou une nouvelle partie.
