import random

class Objets:                       
    def __init__(self,nom):
        """classe de base des objets du jeu, classe parente de ces mêmes objets"""
        self.nom = nom
    
class Nourriture(Objets): 
    """hérite de Objet, gère la régénération de pas avec la nourriture"""          
    def __init__( self, nom, nb_pas_recup):
        super().__init__(nom)
        self.nb_pas_recup=nb_pas_recup

    def utiliser(self, joueur):                     #ne pas confondre joueur et la classe Joueur en programmant 
        joueur.manger(self.nb_pas_recup)
        print(f"{joueur.nom} mange {self.nom} et récupère {self.nb_pas_recup} pas.")
        
class cle:

    def __init__( self, nom):
        super().__init__(nom)

    def utiliser(self, joueur):
        joueur.ouvrir_cle()


class Joueur:
    """Cette classe représente l'inventaire du joueur et ses actions """
    def __init__(self, nom):
        self.nom= nom
        self.pas= 70               # valeur du début de partie 
        self.inventaire= {}       # inventaire vide au démarrage
        if self.pas <=0:
            print("partie finie il reste pu de pas")     #à modifier j'ai pas encore implémenté la fin de partie 
        
    def manger(self, nb_pas_recup):
        self.pas += nb_pas_recup

    def ouvrir_cle(self):
        #implétemter l'ouverture de porte ici 
        print("ouvre la porte")

    def ouvrir_gemme(self):
        #implétemter l'ouverture de porte ici 
        print("ouvre la porte")

    def ramasser_objet(self, obj): 
        if obj.nom in self.inventaire:
            self.inventaire[obj.nom]["nombre"] += 1
            
        else:
            self.inventaire[obj.nom] = {"objet": obj, "nombre": 1}
        print(f"{obj.nom} ramassé")



    def utiliser_objet(self, nom_objet):
        if nom_objet in self.inventaire and self.inventaire[nom_objet]["nombre"] >0 :

            objet = self.inventaire[nom_objet]["objet"] 
            objet.utiliser(self)
            
            self.inventaire[nom_objet]["nombre"] -=1  
            if self.inventaire[nom_objet]["nombre"]==0:
                del self.inventaire[nom_objet]

            print(f"{self.nom} utilise {nom_objet}.")
        else:
            print(f"pas de {nom_objet} dans l'inventaire.")