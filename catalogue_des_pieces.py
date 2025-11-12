from room import Piece
N_A = 100
COMMONPLACE = 0
STANDART = 1
UNUSUAL = 2
RARE = 3

EntranceHall = Piece(
    nom = "EntranceHall",
    image="assets/rooms/Entrancehall.png",  
    portes={
        "haut": True,       
        "droite": True,   
        "bas": False,
        "gauche": True},
    cout_gemmes = 0,
    objets=[],
    effet = None,
    rarete = N_A,
    niveaux_portes = {"haut": 0,"droite": 0,"bas": None,"gauche": 0}
)

Antechamber = Piece(
    nom = "Antechamber",
    image = "assets/rooms/Antechamber.png",  
    portes={
        "haut": False,       
        "droite": True,   
        "bas": True,
        "gauche": True},
    cout_gemmes = 0,
    objets = [],
    effet = None,
    rarete = N_A,
    niveaux_portes = {"haut": None,"droite": 2,"bas": 2,"gauche": 2}
)

TheFondation = Piece(
    nom = "TheFondation",
    image = "assets/rooms/The_Foundation.png",  
    portes={
        "haut": False,       
        "droite": True,   
        "bas": True,
        "gauche": True},
    cout_gemmes = 0,
    objets = [],
    effet = None,
    rarete = RARE,
    condition = "impossible_dans_les_coins"
)

SpareRoom = Piece(
    nom = "SpareRoom",
    image = "assets/rooms/SpareRoom.png",  
    portes={
        "haut": True,       
        "droite": False,   
        "bas": True,
        "gauche": False},
    cout_gemmes = 0,
    effet = None,
    rarete = N_A,
)

Rotunda = Piece(
    nom = "Rotunda",
    image = "assets/rooms/Rotunda.png",  
    portes={
        "haut": False,       
        "droite": False,   
        "bas": True,
        "gauche": True},
    cout_gemmes = 3,
    objets = [],
    effet = None,
    rarete = RARE,
)

Parlor = Piece(
    nom = "Parlor",
    image = "assets/rooms/Parlor.png",  
    portes={
        "haut": False,       
        "droite": False,   
        "bas": True,
        "gauche": True},
    cout_gemmes = 0,
    objets = ["puzzle"],
    effet = None,
    rarete = COMMONPLACE,
)

BilliardRoom = Piece(
    nom = "BilliardRoom",
    image = "assets/rooms/Billiard_Room.png",  
    portes={
        "haut": False,       
        "droite": False,   
        "bas": True,
        "gauche": True},
    cout_gemmes = 0,
    objets = ["puzzle"],
    effet = None,
    rarete = COMMONPLACE,
)

Gallery = Piece(
    nom = "allery",
    image = "assets/rooms/Gallery.png",  
    portes={"haut": True,"droite": False,"bas": True,"gauche": False},
    cout_gemmes = 0,
    objets = ["puzzle"],
    effet = None,
    rarete = RARE,
    condition = "debloquer_la_room_46"
)

Room8= Piece(
    nom = "Room8",
    image = "assets/rooms/Room_8.png",  
    portes={"haut": False,"droite": False,"bas": True,"gauche": True},
    cout_gemmes = 0,
    objets = ["aleatoire","creuser","permanent_pelle"],
    effet = None,
    rarete = RARE,
)

Closet = Piece(
    nom = "Closet",
    image = "assets/rooms/Closet.png",  
    portes={"haut": False,"droite": False,"bas": True,"gauche": False},
    cout_gemmes = 0,
    objets = ["aleatoire","aleatoire","coffre","permanent_marteau"],
    effet = None,
    rarete = COMMONPLACE,
)

WalkInCloset = Piece(
    nom = "Walk-InCloset",
    image = "assets/rooms/Walk-in_Closet.png",  
    portes={"haut": False,"droite": False,"bas": True,"gauche": False},
    cout_gemmes = 1,
    objets = ["aleatoire","aleatoire","aleatoire","aleatoire","permanent_patte_lapin"],
    effet = None,
    rarete = STANDART,
)

Attic = Piece(
    nom = "Attic",
    image = "assets/rooms/Attic.png",  
    portes={"haut": False,"droite": False,"bas": True,"gauche": False},
    cout_gemmes = 1,
    objets = ["aleatoire","aleatoire","aleatoire","aleatoire","permanent_detecteur"],
    effet = None,
    rarete = RARE,
)

StoreRoom = Piece(
    nom = "StoreRoom",
    image = "assets/rooms/StoreRoom.png",  
    portes={"haut": False,"droite": False,"bas": True,"gauche": False},
    cout_gemmes = 0,
    objets = ["cle","gemme","or","casier"],
    effet = None,
    rarete = COMMONPLACE,
)

catalogue = [
    EntranceHall, Antechamber, TheFondation, SpareRoom, Rotunda,
    Parlor, BilliardRoom, Gallery, Room8, Closet,
    WalkInCloset, Attic, StoreRoom
]

pioche = [
    TheFondation, SpareRoom, Rotunda,
    Parlor, BilliardRoom, Gallery, Room8, Closet,
    WalkInCloset, Attic, StoreRoom
]
