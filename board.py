import pygame

# class Board:
#     def __init__(self):

#         self.grille = [[None for _ in range(5)] for _ in range(9)]
#         self.ligne_joueur = 8  
#         self.colonne_joueur = 2  
#         self.ligne_antechambert = 0
#         self.colonne_antechambert = 2
#         self.grille[self.ligne_joueur][self.colonne_joueur] = "Entrancehall"
#         self.grille[self.ligne_antechambert][self.colonne_antechambert] = "Antechamber"



#         self.direction = None 

#     def selectionner_direction(self, direction):
#         """Met à jour la direction choisie par le joueur."""
#         self.direction = direction

#     def se_deplacer(self):
#         """Tente de déplacer le joueur s'il n'y a pas de mur."""
#         if self.direction is None:
#             return

#         nouvelle_ligne = self.ligne_joueur
#         nouvelle_colonne = self.colonne_joueur

#         if self.direction == "haut":
            
#             nouvelle_ligne -= 1
#         elif self.direction == "bas":
            
#             nouvelle_ligne += 1
#         elif self.direction == "gauche":
            
#             nouvelle_colonne -= 1
#         elif self.direction == "droite":
            
#             nouvelle_colonne += 1

#         if 0 <= nouvelle_ligne < 9 and 0 <= nouvelle_colonne < 5:
#             self.ligne_joueur = nouvelle_ligne
#             self.colonne_joueur = nouvelle_colonne

#         self.direction = None

class Board:
    def __init__(self):

        self.grille = [[None for _ in range(5)] for _ in range(9)]
        self.ligne_joueur = 8  
        self.colonne_joueur = 2  
        self.ligne_antechambert = 0
        self.colonne_antechambert = 2
        self.grille[self.ligne_joueur][self.colonne_joueur] = "Entrancehall"
        self.grille[self.ligne_antechambert][self.colonne_antechambert] = "Antechamber"
        self.choix = None 


        self.direction = None 

    def selectionner_direction(self, direction):
        """Met à jour la direction choisie par le joueur."""
        self.direction = direction

    def se_deplacer(self):
        """Tente de déplacer le joueur s'il n'y a pas de mur."""
        if self.direction is None:
            return

        nouvelle_ligne = self.ligne_joueur
        nouvelle_colonne = self.colonne_joueur

        if self.direction == "haut":
            
            nouvelle_ligne -= 1
        elif self.direction == "bas":
            
            nouvelle_ligne += 1
        elif self.direction == "gauche":
            
            nouvelle_colonne -= 1
        elif self.direction == "droite":
            
            nouvelle_colonne += 1
        
        if 0 <= nouvelle_ligne < 9 and 0 <= nouvelle_colonne < 5:
            self.ligne_joueur = nouvelle_ligne
            self.colonne_joueur = nouvelle_colonne

        self.direction = None
        
    def tirage_piece(self):
        
        if self.choix == "e":
            print("1")
        elif self.choix == "r":
            print("2")
        elif self.choix == "t":
            print("3")
            
        self.choix = None
        
