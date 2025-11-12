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

INTERACTION_TABLES = {
    "coffre": [
        ("piece", 0.7),
        ("gemme", 0.5),
        ("cle", 0.4),
        ("de", 0.2),
        ("permanent:marteau", 0.07),
    ],
    "casier": [
        ("piece", 0.6),
        ("nourriture:banane", 0.25),
        ("nourriture:gateau", 0.1),
        ("cle", 0.2),
    ],
    "creuser": [
        ("piece", 0.4),
        ("gemme", 0.3),
        ("permanent:pelle", 0.15),
        ("permanent:patte_lapin", 0.1),
    ],
}

def objets_depuis_tags(tags):
    """Transforme les tags définis dans catalogue_des_pieces en objets concrets."""
    objets = []
    for tag in tags:
        tag_normalise = tag.lower()
        if tag_normalise in {
            "permanent_detecteur",
            "permanent_patte_lapin",
            "permanent_pelle",
            "permanent_marteau",
            "coffre",
            "casier",
            "creuser",
        }:
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

def generer_butin_interaction(source, joueur=None):
    table = INTERACTION_TABLES.get(source, [])
    if not table:
        return [], []
    patte = joueur.possede_patte_lapin() if joueur else False
    butin = []
    permanents = []
    for tag, proba in table:
        proba_effective = proba
        if patte and tag and not tag.startswith("permanent:"):
            proba_effective = min(proba_effective * 1.15, 0.95)
        if random.random() < proba_effective:
            if tag is None:
                continue
            if tag.startswith("permanent:"):
                permanents.append(tag.split(":", 1)[1])
            else:
                obj = _cree_objet(tag)
                if obj:
                    butin.append(obj)
    return butin, permanents

def tirer_pieces(grille,ligne,colonne):
    """temporaire pour tester la génération de pièce"""
    pieces=["Pantry","SpareRoom"]
    i=random.randint(0,1)
    grille[ligne][colonne] = pieces[i]
    return grille
    
