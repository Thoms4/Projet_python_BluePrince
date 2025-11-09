import pygame
from board import Board
from assets import Assets
from Inventaire import Joueur

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1200, 450))
        pygame.display.set_caption("Blue Prince Prototype")
        self.clock = pygame.time.Clock()
        self.board = Board()
        self.assets = Assets()
        self.direction_ui = None
        self.joueur=Joueur()  

    def Partie_Salle(self):
        depart_x = 0
        depart_y = 0
        taille_case = 50
        
        lignes = 9
        colonnes = 5
        
        for l in range(lignes):
            for c in range(colonnes):
                #if self.board.grille[l][c] is not None:
                    x = depart_x + c*taille_case
                    y = depart_y + l*taille_case
                    pygame.draw.rect(self.screen, (0,0,0),(x,y,taille_case,taille_case),1)
                    
                    #provisoire
                    room = self.board.grille[l][c]
                    if room is not None:
                        img = self.assets.rooms.get(room)
                        if img:
                            self.screen.blit(img, (x, y))
                
        x_joueur = self.board.colonne_joueur * taille_case
        y_joueur = self.board.ligne_joueur * taille_case
        pygame.draw.rect(self.screen, (255, 255, 255), (x_joueur, y_joueur, taille_case, taille_case), 3)
        

        if self.direction_ui is not None:
            marge = 4  
            epaisseur = 3
        
            if self.direction_ui == "haut":
                pygame.draw.line(self.screen, (255,255,255),
                                 (x_joueur + marge, y_joueur + marge),
                                 (x_joueur + taille_case - marge, y_joueur + marge),
                                 epaisseur)
            elif self.direction_ui == "bas":
                pygame.draw.line(self.screen, (255,255,255),
                                 (x_joueur + marge, y_joueur + taille_case - marge),
                                 (x_joueur + taille_case - marge, y_joueur + taille_case - marge),
                                 epaisseur)
            elif self.direction_ui == "gauche":
                pygame.draw.line(self.screen, (255,255,255),
                                 (x_joueur + marge, y_joueur + marge),
                                 (x_joueur + marge, y_joueur + taille_case - marge),
                                 epaisseur)
            elif self.direction_ui == "droite":
                pygame.draw.line(self.screen, (255,255,255),
                                 (x_joueur + taille_case - marge, y_joueur + marge),
                                 (x_joueur + taille_case - marge, y_joueur + taille_case - marge),
                                 epaisseur)


    
    def Partie_Inventaire(self):
        depart_x = 250
        depart_y = 0
        
        largeur = 950
        hauteur = 450
        
        pygame.draw.rect(self.screen, (255,255,255),(depart_x,depart_y,largeur,hauteur))
        
                
    

    def run(self):
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_z:
                        self.board.selectionner_direction("haut")
                        self.direction_ui = "haut"
                    elif event.key == pygame.K_s:
                        self.board.selectionner_direction("bas")
                        self.direction_ui = "bas"
                    elif event.key == pygame.K_q:
                        self.board.selectionner_direction("gauche")
                        self.direction_ui = "gauche"
                    elif event.key == pygame.K_d:
                        self.board.selectionner_direction("droite")
                        self.direction_ui = "droite"
                    elif event.key == pygame.K_SPACE:
                        self.board.se_deplacer(self.joueur)
                        self.direction_ui = None



            self.Partie_Inventaire()
            self.Partie_Salle()
            pygame.display.flip()
            self.clock.tick(30)

        pygame.quit()
