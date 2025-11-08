import random
from Inventaire import cle, gemme, Nourriture, Joueur

def genere_obj():
    "tire aléatoirement les objets qui seront présents dans la pièce"
    obj_possibles = [
        (cle("Cle"), 0.3),
        (gemme("Gemmes"), 0.2),
        (Nourriture("pomme"), 0.15),
        (Nourriture("banane"), 0.1),
        (Nourriture("gateau"), 0.02),
        (Nourriture("sandwich"), 0.02),
        (Nourriture("repas"), 0.01),
        (None, 0.2)  # Rien dans la pièce
    ]

    obj_generes=[]
    for obj, proba in obj_possibles:
        if random.random() < proba:
            if obj != None: 
                obj_generes.append(obj)
    if None in obj_generes:
        return []
    else:
        return obj_generes