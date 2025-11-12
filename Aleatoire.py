import random
from Inventaire import cle, gemme, Nourriture, des, Objets

def _cree_objet(tag):
    if tag == "cle":
        return cle("Cle")
    if tag == "gemme":
        return gemme("Gemmes")
    if tag == "piece":
        return Objets("Pieces")
    if tag == "de":
        return des("Des")
    if tag.startswith("nourriture:"):
        return Nourriture(tag.split(":", 1)[1])
    return None

def genere_obj(joueur=None):
    "tire aléatoirement les objets qui seront présents dans la pièce"
    detecteur = joueur.possede_detecteur_metaux() if joueur else False
    patte = joueur.possede_patte_lapin() if joueur else False

    base_possibles = [
        ("cle", 0.25),
        ("gemme", 0.18),
        ("piece", 0.25),
        ("de", 0.05),
        ("nourriture:pomme", 0.12),
        ("nourriture:banane", 0.08),
        ("nourriture:gateau", 0.02),
        ("nourriture:sandwich", 0.02),
        ("nourriture:repas", 0.01),
        (None, 0.2)
    ]

    obj_generes = []
    for tag, proba in base_possibles:
        proba_effective = proba
        if detecteur and tag in ("cle", "gemme", "piece"):
            proba_effective = min(proba_effective * 1.5, 0.95)
        if patte and tag is not None:
            proba_effective = min(proba_effective * 1.2, 0.95)

        if random.random() < proba_effective:
            if tag is None:
                return []  # pièce vide
            obj = _cree_objet(tag)
            if obj:
                obj_generes.append(obj)

    return obj_generes

def objets_depuis_tags(tags):
    """Transforme les tags définis dans catalogue_des_pieces en objets concrets."""
    objets = []
    for tag in tags:
        tag_normalise = tag.lower()
        if tag_normalise in {"permanent_detecteur", "permanent_patte_lapin"}:
            continue
        if tag_normalise == "cle":
            objets.append(cle("Cle"))
        elif tag_normalise == "gemme":
            objets.append(gemme("Gemmes"))
        elif tag_normalise == "or":
            objets.append(Objets("Pieces"))
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
    
