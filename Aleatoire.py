import random
from Inventaire import cle, gemme, Nourriture, des, PieceOr, Objets

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
        (des("Des"), 0.05),
        (PieceOr("Pieces"), 0.25),
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

def objets_depuis_tags(tags):
    """Transforme les tags définis dans catalogue_des_pieces en objets concrets."""
    objets = []
    for tag in tags:
        tag_normalise = tag.lower()
        if tag_normalise == "cle":
            objets.append(cle("Cle"))
        elif tag_normalise == "gemme":
            objets.append(gemme("Gemmes"))
        elif tag_normalise == "or":
            objets.append(PieceOr("Pieces"))
        elif tag_normalise == "des":
            objets.append(des("Des"))
        elif tag_normalise == "puzzle":
            objets.append(Objets("Puzzle"))
        else:
            # inconnu -> ignorer (peut être étendu plus tard)
            pass
    return objets

def tirer_pieces(grille,ligne,colonne):
    """temporaire pour tester la génération de pièce"""
    pieces=["Pantry","SpareRoom"]
    i=random.randint(0,1)
    grille[ligne][colonne] = pieces[i]
    return grille
    
