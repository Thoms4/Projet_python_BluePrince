class Objets:                       
    def __init__(self,nom):
        """classe de base des objets du jeu, classe parente de ces mêmes objets"""
        self.nom = nom

    def utiliser(self, joueur):
        print(f"le joueur utilise {self.nom}")
    
class Nourriture(Objets): 
    """hérite de Objet, gère la régénération de pas avec la nourriture"""          
    def __init__( self, nom):
        super().__init__(nom)
        self.nb_pas_nourriture={"pomme":2,
                           "banane":3,
                           "gateau":10,
                           "sandwich":15,
                           "repas":25
                           }
        self.nb_pas_recup= self.nb_pas_nourriture.get(nom)

    def utiliser(self, joueur):                   
        joueur.add_inv(Objets("Pas"), self.nb_pas_recup)
        print(f"le joueur mange {self.nom} et récupère {self.nb_pas_recup} pas.")
        
class cle(Objets):                                  
    """hérite de Objet, gère l'utilisation des clés"""
    def __init__( self, nom):
        super().__init__(nom)

    def utiliser(self , joueur):
        #partie.ouvrir_porte                remplacer par la fonction qui ouvre une porte
        print(f"le joueur utilise une {self.nom} pour ouvrir la porte")

class gemme(Objets):                                
    """hérite de Objet, gère l'utilisation des gemmes"""
    def __init__( self, nom):
        super().__init__(nom)

    def utiliser(self, joueur):
        #partie.choisir_piece()             remplacer par la fonction qui choisit une pièce
        print(f"le joueur utilise une {self.nom} pour choisir une pièce")

class des(Objets):
    """hérite de Objet, gère l'utilisation des dés"""
    def __init__( self, nom):
        super().__init__(nom)

    def utiliser(self, joueur):
        #partie.tirer_piece()             remplacer par la fonction qui tire une pièce
        print(f"le joueur utilise un {self.nom} et tire de nouvelles pièces")



class Joueur:
    """Cette classe représente l'inventaire du joueur et ses actions """
    def __init__(self):
        #self.nom= nom 
        self.__inventaire= {"Pas": {"objet": Objets("Pas"), "nombre": 70},  
            "Gemmes": {"objet": gemme("Gemmes"), "nombre": 2},
            "Cle": {"objet": cle("Cle"), "nombre": 0},
            "Des": {"objet": des("Des"), "nombre": 0},
            "Pieces": {"objet": Objets("Pieces"), "nombre": 0}
            }       # inventaire de départ 
        self.objets_permanents = {
            "kit_crochetage": False,
            "detecteur_metaux": False,
            "patte_lapin": False
        }
                 
    @property   
    def inventaire(self):     
        """getter pour pouvoir consulter l'inventaire"""              
        return self.__inventaire

    def get_quantite(self, nom_objet):
        """Retourne la quantité d'un objet (0 si absent)."""
        if nom_objet in self.__inventaire:
            return self.__inventaire[nom_objet]["nombre"]
        return 0

    def possede_kit_crochetage(self):
        """Indique si le kit de crochetage a été obtenu."""
        return self.objets_permanents.get("kit_crochetage", False)

    def obtenir_kit_crochetage(self):
        """Active le kit de crochetage dans les objets permanents."""
        self.objets_permanents["kit_crochetage"] = True

    def possede_permanent(self, nom):
        return self.objets_permanents.get(nom, False)

    def obtenir_permanent(self, nom):
        if nom in self.objets_permanents:
            self.objets_permanents[nom] = True

    def possede_detecteur_metaux(self):
        return self.possede_permanent("detecteur_metaux")

    def possede_patte_lapin(self):
        return self.possede_permanent("patte_lapin")


    def add_inv(self, obj, quantite):
        """ajoute une quantite d'un objet à l'inventaire (retire si négatif)"""
        
        if obj.nom not in self.__inventaire:
            self.__inventaire[obj.nom]= {"objet": obj , "nombre": 0}

        if quantite<0 and self.__inventaire[obj.nom]["nombre"] - quantite < 0:
            print(f"pas assez de {obj.nom} dans l'inventaire")
        else:
            self.__inventaire[obj.nom]["nombre"]+= quantite  
            
    def retirer_objet(self, nom_objet, quantite):
        """retire une quantité spécifique si possible (True si succès)."""
        if nom_objet not in self.__inventaire:
            return False
        if self.__inventaire[nom_objet]["nombre"] < quantite:
            return False
        self.__inventaire[nom_objet]["nombre"] -= quantite
        if self.__inventaire[nom_objet]["nombre"] == 0:
            del self.__inventaire[nom_objet]
        return True


    def ramasser_objet(self, obj): 
        """permet d'ajouter un objet à l'inventaire quand on le ramasse"""
        if isinstance(obj, Nourriture):
            obj.utiliser(self)

        elif obj.nom in self.__inventaire:
            self.__inventaire[obj.nom]["nombre"] += 1
            print(f"{obj.nom} ramassé")
            
        else:
            self.__inventaire[obj.nom] = {"objet": obj, "nombre": 1}
            print(f"{obj.nom} ramassé")



    def utiliser_objet(self, nom_objet):
        if nom_objet in self.__inventaire and self.__inventaire[nom_objet]["nombre"] >0 :

            objet = self.__inventaire[nom_objet]["objet"]
            objet.utiliser(self)
            
            self.__inventaire[nom_objet]["nombre"] -=1  
            if self.__inventaire[nom_objet]["nombre"]==0:
                del self.__inventaire[nom_objet]

            #print(f"le joueur utilise {nom_objet}.")
        else:
            print(f"pas de {nom_objet} dans l'inventaire.")
