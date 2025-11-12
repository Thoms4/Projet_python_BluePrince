# Projet Blue Prince – Journal d’avancement

Ce fichier décrit l’état du projet au fil du temps. À chaque nouvelle fonctionnalité, ajoutez une entrée dans la section « Historique des mises à jour » accompagné d’une description concise des changements. Gardez ce document synchronisé avec le dépôt pour faciliter la rédaction du rapport final et les présentations.

## État actuel (mise à jour : 2025-11-12)

- **Structure générale** : `main.py` lance `Game`, qui initialise la fenêtre Pygame, le `Board`, le cache `Assets` et un `Joueur`. Deux modes sont gérés : `exploration` (déplacements ZQSD + SPACE) et `choix_piece` (navigation ←/→, validation ENTER).
- **Plateau (`board.py`)** : grille 9×5 avec entrée (`EntranceHall`) et antichambre (`Antechamber`). Déplacement vérifie la disponibilité des Pas, consomme 1 Pas par mouvement, détecte victoire/défaite, gère les niveaux de portes et leurs coûts. À chaque découverte de salle, le butin (tirages aléatoires influencés par les permanents possédés) est généré, les magasins éventuels s’activent, et les objets interactifs (`coffre`, `casier`, `creuser`) sont stockés avec leur état. Les interactions consomment les ressources appropriées (clés, pelle, etc.) ou utilisent les permanents (marteau, kit) pour offrir un tirage spécifique (gemmes, pièces, permanents supplémentaires). Les pièces Attic/Walk-InCloset/Room8/Closet/StoreRoom distribuent désormais des permanents dédiés.
- **Catalogue et assets** : `room.Piece` définit portes, rareté, rotation et réinitialisation. `catalogue_des_pieces.py` liste les pièces disponibles et la pioche initiale. `assets.py` charge et met en cache les sprites (80×80 pour la grille, 128×128 pour l’inventaire) en tenant compte de l’angle.
- **Inventaire (`Inventaire.py`)** : classes d’objets (Pas, Gemmes, Clés, Nourriture, Dés). La classe `Joueur` stocke un inventaire dict, expose `retirer_objet`, et conserve l’état des objets permanents (kit, détecteur, patte de lapin, pelle, marteau) qui modifient les probabilités ou déverrouillent les interactions.
- **Interface** : le panneau de droite affiche les ressources principales (Pas, Gemmes, Clés, Dés, Pièces), les messages de statut, ainsi qu’un encart de magasin lorsqu’on entre dans une salle de type boutique (StoreRoom).
- **Flux utilisateur** : pendant un tirage, il est désormais possible d’annuler (`Échap`) pour revenir à l’exploration sans placer de pièce, ce qui reflète le comportement attendu lorsqu’on change d’avis sur une porte.
- **Aléatoire (`Aleatoire.py`)** : fonction `genere_obj` pour tirer des objets potentiels dans une salle. Pas encore branchée au plateau.

## Fonctionnalités restantes (d’après Projet_POO_2025.pdf)

- Gagner des pas via la nourriture, implémenter la détection de blocage (impossibilité de progresser) et étoffer les interactions liées aux Pas (objets permanents qui les modifient, etc.).
- Gestion avancée d’autres permanents/effects (pelle/marteau implémentés mais il reste la pelle contextuelle pour creuser, marteau sur coffres spéciaux, etc.) ainsi que des effets de pièces (chambres violettes qui rendent des pas, jardins qui boostent les probabilités, etc.).
- Système complet de ressources : acquisition contextuelle OK (clés, gemmes, dés, pièces, nourriture), magasins StoreRoom opérationnels, interactions avec coffres/casiers/creusement ajoutées. Il manque encore les autres boutiques/pièces jaunes et la dépense des pièces d’or dans d’autres contextes scénarisés.
- Apparition d’objets dans les salles (coffres, casiers, endroits à creuser), loot tables et objets permanents (pelle, marteau, etc.) avec effets associés.
- Effets spéciaux de pièces (gain/perte de ressources à l’entrée ou au tirage, modification des probabilités, ajout de nouvelles pièces au catalogue, dispersion de ressources).
- Renforcement de l’aléatoire (objets trouvés, pièces tirées, niveaux de portes) selon la section 2.8 du PDF.
- Interface graphique enrichie (HUD pour ressources, feedbacks, menus), documentation d’installation (`requirements.txt`, instructions de lancement) et UML/rapport exigés par l’énoncé.

## Historique des mises à jour

| Date       | Description |
|------------|-------------|
| 2025-11-12 | Création du journal d’avancement. Résumé de l’état initial (grille, tirage, inventaire théorique) et liste des fonctionnalités manquantes. |
| 2025-11-12 | Intégration du `Joueur` dans le loop de déplacement : consommation automatique des Pas, détection de victoire/défaite, affichage des ressources et messages d’état dans l’interface. |
| 2025-11-12 | Ajout des niveaux de porte: tirage aléatoire selon la rangée, consommation automatique de clés lors de l’ouverture, support du kit de crochetage (placeholder) et affichage des messages contextuels. Synchronisation du niveau entre les deux pièces reliées. |
| 2025-11-12 | Génération/ramassage des ressources dans les pièces (aléatoire + objets du catalogue), affichage des pièces d’or dans le HUD et paiement automatique des gemmes lors du placement des salles. |
| 2025-11-12 | Reroll du tirage (touche `R`) conforme au PDF: consommation d’un Dé, nouveau tirage garantissant une pièce à coût 0, feedback dans le HUD. |
| 2025-11-12 | Ajout d’un magasin fonctionnel pour `StoreRoom`: achats via 1/2/3, dépenses de pièces, obtention de clés/dés/kit de crochetage et affichage dédié dans l’interface. |
| 2025-11-12 | Gestion des objets permanents (détecteur, patte de lapin), probabilités de loot dynamiques, nouvelles options de boutique et intégration des pièces Attic / Walk-InCloset pour distribuer ces bonus. |
| 2025-11-12 | Ajout des interactions Coffre/Casier/Creuser avec clés/pelle/marteau, loot dédié, permanents supplémentaires (pelle/marteau) et interface de commandes contextuelles. |
| 2025-11-12 | Possibilité d’annuler un tirage (Échap) pour revenir à l’exploration, évitant de forcer le placement d’une pièce lorsqu’on explore plusieurs portes. |
| 2025-11-12 | Ajustement de l’UI du magasin pour éviter le chevauchement des options et clarification des actions restantes. |
