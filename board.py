import pygame

import random
import catalogue_des_pieces
#fusion
from Inventaire import Joueur,Objets
from Aleatoire import genere_obj, tirer_pieces
import copy

class Board:
    """" 
    Gere la grille du jeu soit tout ce qui est en lien avec le joueur son déplacement,
    l'ouverture d'une porte, le tirage des pièces, la séléctions des pièces, la rotation
    des pièces et le placement des pieces.
    
    
    """
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
        self.pioche_initial = copy.deepcopy(catalogue_des_pieces.pioche)
        self.mode = "exploration"
        self.direction_pour_placement = None
        
        

    def selectionner_direction(self, direction):
        """Met à jour la direction choisie par le joueur via ZQSD."""
        self.direction = direction
        
        
        

    # def se_deplacer(self,joueur):

    #     """Tente de déplacer le joueur s'il n'y a pas de mur."""
    #     if self.direction is None:
    #         return

    #     nouvelle_ligne = self.ligne_joueur
    #     nouvelle_colonne = self.colonne_joueur

    #     if self.direction == "haut":
            
    #         nouvelle_ligne -= 1
    #     elif self.direction == "bas":
            
    #         nouvelle_ligne += 1
    #     elif self.direction == "gauche":
            
    #         nouvelle_colonne -= 1
    #     elif self.direction == "droite":
            
    #         nouvelle_colonne += 1

    #     if 0 <= nouvelle_ligne < 9 and 0 <= nouvelle_colonne < 5:
    #         self.ligne_joueur = nouvelle_ligne
    #         self.colonne_joueur = nouvelle_colonne

        
    #     if self.grille[nouvelle_ligne][nouvelle_colonne] is None:
    #         self.grille=tirer_pieces(self.grille,nouvelle_ligne,nouvelle_colonne)
    #         obj_genere= genere_obj()
    #         for obj in obj_genere:
    #             joueur.ramasser_objet(obj)
    #     joueur.utiliser_objet("Pas")
    #     self.direction = None
    
    def se_deplacer(self):
        """Déplace le joueur si la salle en face existe déjà.
        Gere les cas d'un mur, d'une porte fermer, d'une porte bloquer.
        Appelle la methode du tirage des pièces dans le cas ou on veut se déplacer dans
        une case vide.
        C'est la méthodes qui va appeller les autres indirectement pour l'avancer dans le jeu.
        Cette méthode est appeller dans le fichier game lors d'un évenement (appui sur espace).
        """
        piece_actuelle = self.grille[self.ligne_joueur][self.colonne_joueur]
        if self.direction is None:
            return
    
        ligne = self.ligne_joueur
        colonne = self.colonne_joueur
    
        if self.direction == "haut":
            ligne -= 1
        elif self.direction == "bas":
            ligne += 1
        elif self.direction == "gauche":
            colonne -= 1
        elif self.direction == "droite":
            colonne += 1
    
        # Vérification des bornes de la grille
        if not (0 <= ligne < 9 and 0 <= colonne < 5):
            print("Mur du manoir, impossible de bouger.")
            return
        
        if piece_actuelle.portes[self.direction] == False:
            print("Pas de porte ici!")
            return
       

        if self.grille[ligne][colonne] is not None:
            self.ligne_joueur = ligne
            self.colonne_joueur = colonne
            print(f"Le joueur s’est déplacé en ({ligne}, {colonne})")

        else:
            print("Aucune salle ici, ouverture d’une nouvelle porte.")
            self.direction_pour_placement = self.direction
            self.tirer_pieces_possibles()
            self.case_cible = (ligne, colonne)
            

        
    def tirer_pieces_possibles(self):
        """
        Effectue le tirage aléatoire des pieces selon leur rareté et gere la rotation lors
        du tirage.

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
    
        
        pieces_tirees = []
        while len(pieces_tirees) < 3:
            tirage = random.choices(self.pioche_initial, weights=poids, k=1)[0]
            if tirage not in pieces_tirees:
                pieces_tirees.append(tirage)
                
        for piece in pieces_tirees:
            self.orienter_piece_selon_direction(piece)
                
    
        # Sauvegarde le tirage actuel           
        self.tirage_en_cours = pieces_tirees
        self.selection_tirage = 0  # index du choix par défaut
        self.mode = "choix_piece"
    
        #print("Tirage :", [piece.nom for piece in pieces_tirees])
        return pieces_tirees

        

    def changer_selection_tirage(self, direction):
        """Permet de changer le choix dans les 3 propositions avec les flèches directionelles."""
        if not self.tirage_en_cours:
            return
        if direction == "gauche":
            self.selection_tirage = (self.selection_tirage - 1) % len(self.tirage_en_cours)
        elif direction == "droite":
            self.selection_tirage = (self.selection_tirage + 1) % len(self.tirage_en_cours)
            
            
            
    def placer_piece_choisie(self):
        """Place la pièce choisie sur la case cible et ré-initialise le tirage au moment
        du placement.
        Appeller dans game au moment de l'appui sur entrée.
         
        """

        # Récupération de la pièce choisie
        piece_choisie = self.tirage_en_cours[self.selection_tirage]
        ligne, colonne = self.case_cible
        
        #on eleve d'abord de la pioche la piece
        if piece_choisie in self.pioche_initial:
            self.pioche_initial.remove(piece_choisie)
        #puis on cree une copie qu'on va placer
        piece_choisie_a_placer = copy.deepcopy(piece_choisie)
            
        # Placement dans la grille
        self.grille[ligne][colonne] = piece_choisie_a_placer
    
        # ré-initialistion du tirage de toute les pieces, utile plus tard quand la pioche
        #aura plusieur meme piece de base
        for piece in self.tirage_en_cours:
            piece.reinitialiser_rotation()
            
        self.tirage_en_cours = []
        self.selection_tirage = 0
        self.case_cible = None
        self.direction_pour_placement = None
        print(f" Pièce '{piece_choisie.nom}' placée en ({ligne}, {colonne})")
    
        # Retour au mode exploration
        self.mode = "exploration"

    def orienter_piece_selon_direction(self, piece):
        """
        Oriente les pièces de sorte a pouvoir continuer a progresser dans le manoir.
        Tout les cas possibles.
        Appeler dans le placement des pièces.
        Appelle la méthode de la class Pièce pour éffectuer la rotation.
        
        """
        
        portes = piece.portes
        #print(f"{piece.nom} | Portes : {piece.portes} | Direction placement : {self.direction_pour_placement}")
        if portes["bas"] and not (portes["haut"] or portes["gauche"] or portes["droite"] ):
            
            if self.direction_pour_placement == "haut":
                pass
                
            elif self.direction_pour_placement == "droite":
                piece.tourner_la_piece("horaire")
                
            elif self.direction_pour_placement == "gauche":
                piece.tourner_la_piece("antihoraire")
                
            elif self.direction_pour_placement == "bas":
                piece.tourner_la_piece("horaire")
                piece.tourner_la_piece("horaire")
                
        if portes["bas"] and portes["gauche"] and not (portes["haut"]  or portes["droite"] ):
            
            if self.direction_pour_placement == "haut":
                pass
                
            elif self.direction_pour_placement == "droite":
                piece.tourner_la_piece("horaire")
                
            elif self.direction_pour_placement == "gauche":
                piece.tourner_la_piece("horaire")
                piece.tourner_la_piece("horaire")
                
            elif self.direction_pour_placement == "bas":
                if self.grille[self.ligne_joueur-1][self.colonne_joueur -1] == None:
                    piece.tourner_la_piece("horaire")
                else: 
                    piece.tourner_la_piece("horaire")
            
        if portes["bas"] and portes["haut"] and not (portes["gauche"]  or portes["droite"] ):
            
            if self.direction_pour_placement == "haut":
                pass
                
            elif self.direction_pour_placement == "droite":
                piece.tourner_la_piece("horaire")
                
            elif self.direction_pour_placement == "gauche":
                piece.tourner_la_piece("antihoraire")
                
            elif self.direction_pour_placement == "bas":
                piece.tourner_la_piece("horaire")
                piece.tourner_la_piece("horaire")
            
        
                
            
                



