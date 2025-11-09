import pygame
from board import Board
from assets import Assets


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
        pygame.display.set_caption("Blue Prince Prototype")
        self.clock = pygame.time.Clock()
        self.board = Board()
        self.assets = Assets()
        self.direction_ui = None
        self.tirage_en_cours = []
        self.selection_tirage = 0
        
    def Partie_Salle(self):
        depart_x =  0
        depart_y = 0
        taille_case = 80
        
        lignes = 9
        colonnes = 5
        
        for l in range(lignes):
            for c in range(colonnes):
                #if self.board.grille[l][c] is not None:
                    x = depart_x + c*taille_case
                    y = depart_y + l*taille_case
                    pygame.draw.rect(self.screen, (0,0,0),(x,y,taille_case,taille_case),1)
                    
                    
                    room = self.board.grille[l][c]
                    if room is not None:
                        img = self.assets.charger_image_piece(room,1)
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
        depart_x = 400
        depart_y = 0
        
        largeur = 1520
        hauteur = 1080
        
        pygame.draw.rect(self.screen, (255,255,255),(depart_x,depart_y,largeur,hauteur))
        
        
        #tirage du bas affichage
        if self.board.tirage_en_cours:
            y_img = 450
            for i, room in enumerate(self.board.tirage_en_cours):
                img = self.assets.charger_image_piece(room,2)
                if img:
                    #img_redim = pygame.transform.scale(img, (128, 128))
                    x_img = 500 + i * 150
                    #self.screen.blit(img_redim, (x_img, y_img))
                    self.screen.blit(img, (x_img, y_img))
        
                    # cadre autour de la pièce sélectionnée
                    if i == self.board.selection_tirage:
                        pygame.draw.rect(self.screen, (255, 255, 0), (x_img - 5, y_img - 5, 138, 138), 4)
        
                    # nom de la pièce en dessous
                    font = pygame.font.Font(None, 24)
                    text = font.render(room.nom, True, (0, 0, 0))
                    self.screen.blit(text, (x_img, y_img + 130))

        
                
    

    def run(self):
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
        
                
                if self.board.mode == "exploration":
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_z:
                            self.board.selectionner_direction("haut")
                        elif event.key == pygame.K_s:
                            self.board.selectionner_direction("bas")
                        elif event.key == pygame.K_q:
                            self.board.selectionner_direction("gauche")
                        elif event.key == pygame.K_d:
                            self.board.selectionner_direction("droite")
        
                        elif event.key == pygame.K_SPACE:
                            self.board.ouvrir_porte()
                            
        
                
                elif self.board.mode == "choix_piece":
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            self.board.changer_selection_tirage("gauche")
                        elif event.key == pygame.K_RIGHT:
                            self.board.changer_selection_tirage("droite")
                        elif event.key == pygame.K_RETURN:  
                            self.board.placer_piece_choisie()
                              



            self.Partie_Salle()
            self.Partie_Inventaire()
            pygame.display.flip()
            self.clock.tick(30)

        pygame.quit()
