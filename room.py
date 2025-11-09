import random

class Piece:
    def __init__(self, nom, image, portes, cout_gemmes=0, objets=None, effet=None, rarete=0, condition=None,
                 niveaux_portes=None):
        """
        Représente une pièce du manoir.

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
        self.portes = portes
        self.cout_gemmes = cout_gemmes
        self.objets = objets if objets else []
        self.effet = effet
        self.rarete = rarete
        self.condition = condition
        self.niveaux_portes = niveaux_portes if niveaux_portes else {"haut": None,"droite": None,"bas": None,"gauche": None}


    def tirer_niveaux_portes(self, rangee):
        
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