import random
import catalogue_des_pieces
from Aleatoire import genere_obj, objets_depuis_tags
import copy

class Board:
    """" 
    Gere la grille du jeu soit tout ce qui est en lien avec le joueur son déplacement,
    l'ouverture d'une porte, le tirage des pièces, la séléctions des pièces, la rotation
    des pièces et le placement des pieces.
    
    
    """
    def __init__(self, joueur):

        self.joueur = joueur
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
        self.partie_terminee = False
        self.raison_fin = None
        self.message = ""
        self.pieces_fouillees = {(self.ligne_joueur, self.colonne_joueur)}
        self.grille[self.ligne_joueur][self.colonne_joueur].tirer_niveaux_portes(self.ligne_joueur)
        self.grille[self.ligne_antechambert][self.colonne_antechambert].tirer_niveaux_portes(self.ligne_antechambert)
        
        

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
        if self.partie_terminee:
            return

        piece_actuelle = self.grille[self.ligne_joueur][self.colonne_joueur]
        if self.direction is None:
            return

        if self.joueur.get_quantite("Pas") <= 0:
            self._terminer_partie("plus_de_pas")
            print("Vous n'avez plus de pas, la partie est terminée.")
            self.message = "Défaite : plus de pas."
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
            self.message = "Pas de porte dans cette direction."
            return

        niveau_porte = self._obtenir_niveau_porte(piece_actuelle, self.direction, self.ligne_joueur)

        if self.grille[ligne][colonne] is not None:
            self.ligne_joueur = ligne
            self.colonne_joueur = colonne
            print(f"Le joueur s’est déplacé en ({ligne}, {colonne})")
            self.message = ""
            self._apres_deplacement()

        else:
            if not self._essayer_ouvrir_porte(niveau_porte):
                return
            print("Aucune salle ici, ouverture d’une nouvelle porte.")
            self.direction_pour_placement = self.direction
            self.tirer_pieces_possibles()
            self.case_cible = (ligne, colonne)
            self.message = "Choisissez une pièce à placer."
        
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
        essais = 0
        while len(pieces_tirees) < 3:
            tirage = random.choices(self.pioche_initial, weights=poids, k=1)[0]
            if tirage not in pieces_tirees:
                pieces_tirees.append(tirage)
            essais += 1
            if essais > 200:
                break
        if not any(piece.cout_gemmes == 0 for piece in pieces_tirees):
            zero_cost = [p for p in self.pioche_initial if p.cout_gemmes == 0]
            if zero_cost:
                pieces_tirees[-1] = random.choice(zero_cost)
                
        for piece in pieces_tirees:
            self.orienter_piece_selon_direction(piece)
                
    
        # Sauvegarde le tirage actuel           
        self.tirage_en_cours = pieces_tirees
        self.selection_tirage = 0  # index du choix par défaut
        self.mode = "choix_piece"
    
        #print("Tirage :", [piece.nom for piece in pieces_tirees])
        return pieces_tirees

    def relancer_tirage(self):
        """Permet de relancer le tirage en dépensant un dé."""
        if self.mode != "choix_piece":
            self.message = "Impossible de relancer hors tirage."
            return False
        if self.joueur.get_quantite("Des") <= 0:
            self.message = "Pas de dé disponible pour relancer."
            return False

        self.joueur.utiliser_objet("Des")
        for piece in self.tirage_en_cours:
            piece.reinitialiser_rotation()
        self.tirer_pieces_possibles()
        self.message = "Nouveau tirage (1 dé utilisé)."
        return True

        

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
        piece_source = self.grille[self.ligne_joueur][self.colonne_joueur]
        cout = piece_choisie.cout_gemmes
        if cout > 0:
            if self.joueur.get_quantite("Gemmes") < cout:
                self.message = f"Besoin de {cout} gemme(s) pour placer {piece_choisie.nom}."
                print("Pas assez de gemmes pour cette pièce.")
                return
            for _ in range(cout):
                self.joueur.utiliser_objet("Gemmes")
        
        #on eleve d'abord de la pioche la piece
        if piece_choisie in self.pioche_initial:
            self.pioche_initial.remove(piece_choisie)
        #puis on cree une copie qu'on va placer
        piece_choisie_a_placer = copy.deepcopy(piece_choisie)
        piece_choisie_a_placer.tirer_niveaux_portes(ligne)
        self._synchroniser_porte_ouverte(piece_source, piece_choisie_a_placer)
            
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
        self.message = "Pièce placée."
    
        # Retour au mode exploration
        self.mode = "exploration"

    def _apres_deplacement(self):
        """Consomme un pas et vérifie les conditions de fin de partie."""
        self.joueur.utiliser_objet("Pas")
        self._traiter_entree_piece()

        if (self.ligne_joueur == self.ligne_antechambert and
                self.colonne_joueur == self.colonne_antechambert):
            self._terminer_partie("victoire")
            print("Vous avez atteint l'antichambre !")
            return

        if self.joueur.get_quantite("Pas") <= 0:
            self._terminer_partie("plus_de_pas")
            print("Vous n'avez plus de pas, la partie est terminée.")

    def _terminer_partie(self, raison):
        """Enregistre la fin de partie avec la raison indiquée."""
        self.partie_terminee = True
        self.raison_fin = raison
        if raison == "victoire":
            self.message = "Victoire !"
        elif raison == "plus_de_pas":
            self.message = "Défaite : plus de pas."

    def _obtenir_niveau_porte(self, piece, direction, ligne):
        """S'assure que la pièce a un niveau pour la porte donnée et le retourne."""
        piece.tirer_niveaux_portes(ligne)
        return piece.niveaux_portes.get(direction, 0)

    def _essayer_ouvrir_porte(self, niveau):
        """Tente d'ouvrir la porte en consommant les ressources nécessaires."""
        if niveau == 0:
            self.message = "Porte déverrouillée."
            return True

        if niveau == 1:
            if self.joueur.possede_kit_crochetage():
                self.message = "Kit de crochetage utilisé pour la porte niveau 1."
                return True
            if self.joueur.get_quantite("Cle") > 0:
                self.joueur.utiliser_objet("Cle")
                self.message = "1 clé dépensée pour la porte niveau 1."
                return True
            self.message = "Porte niveau 1 : une clé est nécessaire."
            print("Impossible d'ouvrir la porte niveau 1 sans clé.")
            return False

        if niveau == 2:
            if self.joueur.get_quantite("Cle") > 0:
                self.joueur.utiliser_objet("Cle")
                self.message = "1 clé dépensée pour la porte niveau 2."
                return True
            self.message = "Porte niveau 2 : une clé est nécessaire."
            print("Impossible d'ouvrir la porte niveau 2 sans clé.")
            return False

        return True

    def _synchroniser_porte_ouverte(self, piece_source, piece_nouvelle):
        """Copie le niveau de verrouillage de la porte déjà ouverte vers la nouvelle pièce."""
        if self.direction_pour_placement is None:
            return
        opposites = {"haut": "bas", "bas": "haut", "gauche": "droite", "droite": "gauche"}
        direction_opposite = opposites.get(self.direction_pour_placement)
        if direction_opposite is None:
            return
        piece_source.tirer_niveaux_portes(self.ligne_joueur)
        niveau = piece_source.niveaux_portes.get(self.direction_pour_placement, 0)
        piece_nouvelle.niveaux_portes[direction_opposite] = niveau

    def _traiter_entree_piece(self):
        """Génère les objets de la pièce lors de la première visite."""
        coord = (self.ligne_joueur, self.colonne_joueur)
        if coord in self.pieces_fouillees:
            return

        piece = self.grille[self.ligne_joueur][self.colonne_joueur]
        butin = []

        if piece.objets:
            tags_specifiques = [tag for tag in piece.objets if tag != "aleatoire"]
            butin.extend(objets_depuis_tags(tags_specifiques))
            tirages = piece.objets.count("aleatoire")
            for _ in range(tirages):
                butin.extend(genere_obj())
        else:
            butin.extend(genere_obj())

        noms = []
        for obj in butin:
            self.joueur.ramasser_objet(obj)
            noms.append(obj.nom)

        if noms:
            self.message = "Objets ramassés : " + ", ".join(noms)
        else:
            self.message = "La pièce semble vide."

        self.pieces_fouillees.add(coord)

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
            
        
                
            
                
