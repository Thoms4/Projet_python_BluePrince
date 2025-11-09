import pygame

import random
import catalogue_des_pieces
#fusion
from Inventaire import Joueur,Objets
from Aleatoire import genere_obj, tirer_pieces


# class Board:
#     def __init__(self):

#         self.grille = [[None for _ in range(5)] for _ in range(9)]
#         self.ligne_joueur = 8  
#         self.colonne_joueur = 2  
#         self.ligne_antechambert = 0
#         self.colonne_antechambert = 2
#         self.grille[self.ligne_joueur][self.colonne_joueur] = "Entrancehall"
#         self.grille[self.ligne_antechambert][self.colonne_antechambert] = "Antechamber"
#         self.tirage_en_cours = []
#         self.selection_tirage = 0



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
        
#     def tirer_salles_possibles(self):
#         """Tire 3 salles aléatoires (pour l’instant sans condition spéciale)."""
#         toutes_les_salles = list(donnee_room.info_pieces.values())
#         self.tirage_en_cours = random.sample(toutes_les_salles, 3)
#         print("Tirage :", [r.nom for r in self.tirage_en_cours])
#         self.selection_tirage = 0
        

#     def changer_selection_tirage(self, direction):
#         """Permet de changer le choix dans les 3 propositions."""
#         if not self.tirage_en_cours:
#             return
#         if direction == "gauche":
#             self.selection_tirage = (self.selection_tirage - 1) % len(self.tirage_en_cours)
#         elif direction == "droite":
#             self.selection_tirage = (self.selection_tirage + 1) % len(self.tirage_en_cours)


class Board:
    def __init__(self):

        self.grille = [[None for _ in range(5)] for _ in range(9)]
        self.ligne_joueur = 8  
        self.colonne_joueur = 2  
        self.ligne_antechambert = 0
        self.colonne_antechambert = 2
        self.grille[self.ligne_joueur][self.colonne_joueur] = catalogue_des_pieces.EntranceHall
        self.grille[self.ligne_antechambert][self.colonne_antechambert] = catalogue_des_pieces.Antechamber
        self.direction = None 
        self.tirage_en_cours = []
        self.case_cible = None
        self.pioche_initial = list(catalogue_des_pieces.pioche)
        #self.ligne_cible = None
        #self.colonne_cible = None
        self.mode = "exploration"
        
        

    def selectionner_direction(self, direction):
        """Met à jour la direction choisie par le joueur."""
        self.direction = direction
        
    def ouvrir_porte(self):
        
        if self.direction is None:
            return
        
        piece_actuelle = self.grille[self.ligne_joueur][self.colonne_joueur]
        
        ligne_cible = self.ligne_joueur
        colonne_cible = self.colonne_joueur


        if self.direction == "haut":
            
            ligne_cible -= 1
        elif self.direction == "bas":
            
            ligne_cible += 1
        elif self.direction == "gauche":
            
            colonne_cible -= 1
        elif self.direction == "droite":
            
            colonne_cible += 1  
        
        if not (0 <= ligne_cible < 9 and 0 <= colonne_cible < 5):
            print("Impossible, il y a un mur.")
            return
            
            
        if piece_actuelle.portes[self.direction] == False:
            print("Pas de porte ici!")
            return
        
        if self.grille[ligne_cible][colonne_cible] == None:
            self.tirer_pieces_possibles()
            #recuperer la salle choisie / provisoire
            piece_choisie = self.tirage_en_cours[self.selection_tirage]
            
            piece_choisie.tirer_niveaux_portes(ligne_cible)
            
            self.case_cible = (ligne_cible,colonne_cible)
        else: 
            return
        
        

    def se_deplacer(self,joueur):

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

        
        if self.grille[nouvelle_ligne][nouvelle_colonne] is None:
            self.grille=tirer_pieces(self.grille,nouvelle_ligne,nouvelle_colonne)
            obj_genere= genere_obj()
            for obj in obj_genere:
                joueur.ramasser_objet(obj)
        joueur.utiliser_objet("Pas")
        self.direction = None
        
    def tirer_pieces_possibles(self):
        """

        """
        poids_par_rarete = {
            catalogue_des_pieces.COMMONPLACE: 100,
            catalogue_des_pieces.STANDART: 100/3,
            catalogue_des_pieces.UNUSUAL: (100/3)/3,
            catalogue_des_pieces.RARE: ((100/3)/3)/3
            }
    
        
        poids = []  

        for piece in self.pioche_initial:  
            rarete = piece.rarete          
            if rarete in poids_par_rarete: 
                valeur = poids_par_rarete[rarete]  
            else:
                valeur = 0  
            poids.append(valeur)  
    
        
        pieces_tirees = random.choices(self.pioche_initial, weights=poids, k=3)
    
        # Sauvegarde le tirage actuel
        self.tirage_en_cours = pieces_tirees
        self.selection_tirage = 0  # index du choix par défaut
        self.mode = "choix_piece"
    
        print("Tirage :", [piece.nom for piece in pieces_tirees])
        return pieces_tirees

        

    def changer_selection_tirage(self, direction):
        """Permet de changer le choix dans les 3 propositions."""
        if not self.tirage_en_cours:
            return
        if direction == "gauche":
            self.selection_tirage = (self.selection_tirage - 1) % len(self.tirage_en_cours)
        elif direction == "droite":
            self.selection_tirage = (self.selection_tirage + 1) % len(self.tirage_en_cours)
            
    def placer_piece_choisie(self):
        """Place la pièce choisie sur la case cible et nettoie le tirage."""
        # if not self.tirage_en_cours or not hasattr(self, "case_cible"):
        #     print("Aucune pièce à placer.")
        #     return
        
        # Récupération de la pièce choisie
        piece_choisie = self.tirage_en_cours[self.selection_tirage]
        ligne, colonne = self.case_cible
    
        # Placement dans la grille
        self.grille[ligne][colonne] = piece_choisie
    
        # Retirer la pièce de la pioche pour éviter de la revoir
        if piece_choisie in self.pioche_initial:
            self.pioche_initial.remove(piece_choisie)
    
        # Nettoyage
        self.tirage_en_cours = []
        self.selection_tirage = 0
        self.case_cible = None
    
        print(f" Pièce '{piece_choisie.nom}' placée en ({ligne}, {colonne})")
    
        # Retour au mode exploration
        self.mode = "exploration"

        
