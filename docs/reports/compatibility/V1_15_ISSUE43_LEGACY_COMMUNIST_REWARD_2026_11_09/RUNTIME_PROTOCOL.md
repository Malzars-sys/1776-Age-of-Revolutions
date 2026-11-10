# Test ciblé — Institutions socialistes

Livraison exacte : les trois empreintes dans `INSTALLATION_RECEIPT.json`. Aucun résultat moteur n'est attesté ici.

1. Dans une nouvelle partie de test en 1776, noter la version du jeu, la configuration DLC et le pays sélectionné. Relever son panneau de bureaucratie à l'arrêt.
2. Tester la récompense de l'ancien événement `communism.6`, soit par sa chaîne normale, soit par l'outil debug habituel en conservant une portée de pays valide. Un déclenchement isolé ne valide pas les conditions du journal ni la progression révolutionnaire.
3. Choisir `communism.6.a`. Vérifier le nom **Institutions socialistes** (ou **Institutions of Socialism**), l'icône de document positif et le bonus de **20 % de bureaucratie** pour **3 650 jours**. Contrôler le modificateur dans les détails de la bureaucratie : le solde net dépend aussi des autres bonus et des dépenses, il n'est pas nécessairement multiplié par 1,20.
4. Contrôler les nouveaux logs pour l'identifiant de récompense, puis sauvegarder/recharger. Vérifier la persistance du bonus et la durée restante. L'expiration complète à échéance est un cas distinct, à noter comme non testé si elle n'est pas observée.
5. La chaîne moderne restaurée sous `aor1776_v115_ai_progression.1` conserve son propre modificateur et son nettoyage. L'observer séparément si elle est exercée ; ne pas assimiler un test isolé de l'ancien bonus à la validation des deux parcours ou de tout le DLC.

Consigner uniquement les cas réellement exécutés. Ce lot n'ajoute aucune activation automatique et n'accorde pas de loi ou technologie pour faciliter les tests. La validation humaine de fonctionnement reste nécessaire avant une clôture.
