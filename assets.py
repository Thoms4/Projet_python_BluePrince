import pygame

class Assets:
    def __init__(self):
        self.pieces = {}
    
    # def charger_image_piece(self, piece, taille):
    #     """
    #     Charge l'image correspondant à la pièce passée en paramètre.
    #     La met en cache pour éviter de recharger plusieurs fois la même image.
    #     """
    #     # On vérifie si l'image est déjà chargée
    #     if taille == 1 :
            
    #         if piece.image not in self.pieces:
    #                 img = pygame.image.load(piece.image).convert()
    #                 img = pygame.transform.smoothscale(img, (80, 80))
    #                 self.pieces[piece.image] = img
    
    #         # On retourne l'image déjà en cache
    #         return self.pieces[piece.image]
    #     elif taille == 2:
    #         if piece.image not in self.pieces:
    #                 img = pygame.image.load(piece.image).convert()
    #                 img = pygame.transform.smoothscale(img, (128, 128))
    #                 self.pieces[piece.image] = img
    
    #         # On retourne l'image déjà en cache
    #         return self.pieces[piece.image]
    
    def charger_image_piece(self, piece, taille):
        """
        Charge l'image d'une pièce et la redimensionne selon le contexte.
        - taille = 1 → affichage dans la grille (80x80)
        - taille = 2 → affichage du tirage (128x128)
        """
        tailles = {1: (80, 80), 2: (128, 128)}
        target_size = tailles[taille]
    
    
        self.pieces = {}
    
        cle = (piece.image, taille)
    
        if cle in self.pieces:
            return self.pieces[cle]
    
        img = pygame.image.load(piece.image).convert_alpha()
    
        if taille == 1:
            img = pygame.transform.smoothscale(img, target_size)
        else:

            pass
    
        self.pieces[cle] = img
        return img

            
