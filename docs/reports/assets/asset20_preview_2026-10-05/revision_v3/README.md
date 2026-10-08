# Lot 17 — calcul à la craie sur le tableau noir

**Trois icônes approuvées et intégrées. Couleurs et alpha des DDS vérifiés ; gameplay inchangé. Aucun essai moteur revendiqué.**

La demande de l'utilisateur remplace les inscriptions aléatoires par « 2 + 2 », puis « = 4 » sur la ligne suivante, légèrement décalé à droite. Cette écriture explicite est l'exception demandée à la règle générale d'absence de texte lisible.

Le tableau conserve visuellement son cadre en bois, sa surface sombre, ses pieds et sa craie. La génération le réinterprète légèrement : ses pixels ne sont pas identiques à ceux de la révision v2. Le registre de population et le télégraphe optique sont conservés exactement.

- [Aperçu du lot](LOT_17_APERCU.png)
- [Transparence](LOT_17_ALPHA_DAMIER.png)
- [Comparaison Vanilla et tailles de lecture](LOT_17_COMPARAISON_VANILLA.png)
- [Source sélectionnée du tableau](previews/organized_elementary_schooling_padded.png)
- [Prompt exact — générateur intégré](PROMPT_CALCUL.md)
- [Provenance](source_provenance.json)
- [Contrôles techniques](preview_validation.json)
- [Revue visuelle](visual_review.json)

Le contrôle d'aperçu conservé décrit l'état avant intégration. Le [contrôle d'intégration](integration_static_validation.json) confirme maintenant trois DDS 256 px avec neuf mipmaps en BGRA8 natif, une seule définition touchée (trois lignes de texture), 1 249 autres fichiers protégés inchangés, couleurs et alpha identiques aux PNG sélectionnés. Aucun test en jeu. Les marges transparentes ajoutées à la source v3 ne modifient pas ses pixels RGBA.

La révision v2 et la première proposition restent disponibles comme historique.
