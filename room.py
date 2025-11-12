import random

class Piece:
    def __init__(self, nom, image, portes, cout_gemmes=0, objets=None, effet=None, rarete=0, condition=None,
                 niveaux_portes=None):
        """
        Représente une pièce du manoir et défini toute ces caractéristique.
        C'est a partir de cette class qu'on récupere les informations des pièces.

        :param nom: Nom de la pièce (ex: "Hall d'entrée")
        :param image: chemin ou surface pygame représentant l'image de la pièce
        :param portes: dict des portes, ex: {"haut": 0, "droite": None, "bas": 1, "gauche": None}
        :param cout_gemmes: coût en gemmes pour tirer cette pièce (0 par défaut)
        :param objets: liste d'objets présents dans la pièce
        :param effet: effet spécial éventuel (fonction ou string)
        :param rarete: 0 = commune, 1 = rare, 2 = épique, 3 = légendaire
        :param condition: règle de placement (ex: "bordure", "centre", etc.)
        """
        self.nom = nom
        self.image = image
        self.portes = dict(portes)
        self.cout_gemmes = cout_gemmes
        self.objets = list(objets) if objets else []
        self.effet = effet
        self.rarete = rarete
        self.condition = condition
        self.niveaux_portes = dict(niveaux_portes) if niveaux_portes else {"haut": None,"droite": None,"bas": None,"gauche": None}
        self.angle = 0  
        self.portes_original = portes.copy()
        self.niveaux_portes_original = self.niveaux_portes.copy()
        self.angle_original = 0

    def tirer_niveaux_portes(self, rangee):
        """ 
        Cette méthode tire le niveau des portes en fonction de l'avancement dans le manoir.
     
        """
        
        for direction in ["haut", "droite", "bas", "gauche"]:
            if self.niveaux_portes[direction] is None:

                if rangee == 8:
                    niveau = 0
                elif  5 <= rangee <= 7:
                    niveau = random.choice([0, 1])
                elif  1 <= rangee <= 4:
                    niveau = random.choice([1, 2])
                else:
                    niveau = 2

                self.niveaux_portes[direction] = niveau
                
    def tourner_la_piece(self, sens="horaire"):
        """ 
        Cette méthodes tourne la pièce pour son placement sur la grille.
        Elle est appeller dans l'oriention des pièces dans board
        
        """

        if sens == "horaire":
            self.angle = (self.angle - 90) % 360
            nouvelles_portes = {
                "haut": self.portes["gauche"],
                "droite": self.portes["haut"],
                "bas": self.portes["droite"],
                "gauche": self.portes["bas"],
            }
            nouveaux_niveaux = {
                "haut": self.niveaux_portes["gauche"],
                "droite": self.niveaux_portes["haut"],
                "bas": self.niveaux_portes["droite"],
                "gauche": self.niveaux_portes["bas"],
            }
            
        elif sens == "antihoraire":
            self.angle = (self.angle + 90) % 360
            nouvelles_portes = {
                "haut": self.portes["droite"],
                "droite": self.portes["bas"],
                "bas": self.portes["gauche"],
                "gauche": self.portes["haut"],
            }
            nouveaux_niveaux = {
                "haut": self.niveaux_portes["droite"],
                "droite": self.niveaux_portes["bas"],
                "bas": self.niveaux_portes["gauche"],
                "gauche": self.niveaux_portes["haut"],
            }
        else:
            nouveaux_niveaux = self.niveaux_portes
            
        self.portes = nouvelles_portes
        self.niveaux_portes = nouveaux_niveaux

    def reinitialiser_rotation(self):
        """
        Remet la pièce dans son orientation d'origine.
        """
        self.portes = self.portes_original.copy()
        self.niveaux_portes = self.niveaux_portes_original.copy()
        self.angle = self.angle_original
