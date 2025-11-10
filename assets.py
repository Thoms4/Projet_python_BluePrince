import pygame

class Assets:
    """
    Cette class gère les le chargement des images pour l'affichage.
    
    """
    def __init__(self):
        self.pieces = {}
    
    def charger_image_piece(self, piece, taille):
        """
        Charge l'image d'une pièce, la redimensionne selon le contexte,
        et applique la rotation actuelle de la pièce si nécessaire.
        - taille = 1 → affichage dans la grille (80x80)
        - taille = 2 → affichage du tirage (128x128)
        """
        tailles = {1: (80, 80), 2: (128, 128)}
        target_size = tailles[taille]
    
        if not hasattr(self, "pieces"):
            self.pieces = {}
    
        angle = getattr(piece, "angle", 0)
        cle = (piece.image, taille, angle)
    
        if cle in self.pieces:
            return self.pieces[cle]
    
        img = pygame.image.load(piece.image).convert_alpha()
        img = pygame.transform.smoothscale(img, target_size)
    
        if angle !=  0:
            img = pygame.transform.rotate(img, angle)
    
        # Mise en cache
        self.pieces[cle] = img
        return img


            
