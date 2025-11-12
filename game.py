import pygame
from board import Board
from assets import Assets
from Inventaire import Joueur


class Game:
    """"
    Cette class gère l'affichage et les évenements du jeu.
    On a deux mode : exploration et choix de pièces.
    C'est ici qu'on appelle les méthodes de board lier au évenement soit lorsqu'on appui
    sur uune touche.
    
    """
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
        pygame.display.set_caption("Blue Prince Prototype")
        self.clock = pygame.time.Clock()
        self.joueur = Joueur()
        self.board = Board(self.joueur)
        self.assets = Assets()
        self.direction_ui = None

        self.tirage_en_cours = []
        self.selection_tirage = 0
        
 


    def Partie_Salle(self):
        """
        Cette méthode crée la grille visuelle, affiche les pièces et la directions
        lors des appuis sur les touches.
        """
        depart_x =  0
        depart_y = 0
        taille_case = 80
        
        lignes = 9
        colonnes = 5
        
        for l in range(lignes):
            for c in range(colonnes):
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
        """
        Cette méthode affiche la partie inventaire, le tirage des pièces et la sélection visible
        des pièces lors du tirage.
        
        
        """
        depart_x = 400
        depart_y = 0
        
        largeur = 1520
        hauteur = 1080
        
        pygame.draw.rect(self.screen, (255,255,255),(depart_x,depart_y,largeur,hauteur))

        # ressources du joueur
        ressources = [
            ("Pas", self.joueur.get_quantite("Pas")),
            ("Gemmes", self.joueur.get_quantite("Gemmes")),
            ("Clés", self.joueur.get_quantite("Cle")),
            ("Dés", self.joueur.get_quantite("Des")),
            ("Pièces", self.joueur.get_quantite("Pieces")),
        ]

        font = pygame.font.Font(None, 36)
        for idx, (nom, valeur) in enumerate(ressources):
            text = font.render(f"{nom} : {valeur}", True, (0, 0, 0))
            self.screen.blit(text, (depart_x + 20, 40 + idx * 40))
        
        if self.board.message:
            info_font = pygame.font.Font(None, 28)
            message_surface = info_font.render(self.board.message, True, (30, 30, 30))
            self.screen.blit(message_surface, (depart_x + 20, 220))

        if self.board.magasin_actif:
            shop_font = pygame.font.Font(None, 28)
            title = shop_font.render(f"Magasin ({self.board.magasin_actif['piece']})", True, (0, 0, 120))
            self.screen.blit(title, (depart_x + 20, 260))
            for idx, option in enumerate(self.board.magasin_actif["options"]):
                text = shop_font.render(f"{idx+1}. {option['label']}", True, (0, 0, 0))
                self.screen.blit(text, (depart_x + 40, 300 + idx * 30))
            max_option = len(self.board.magasin_actif["options"])
            instr = shop_font.render(f"Appuyez sur 1-{max_option} pour acheter", True, (0, 0, 0))
            self.screen.blit(instr, (depart_x + 20, 390))
        
        
        # état de fin de partie
        if self.board.partie_terminee:
            status_font = pygame.font.Font(None, 48)
            if self.board.raison_fin == "victoire":
                message = "Victoire ! Vous avez atteint l'antichambre."
            else:
                message = "Défaite : vous n'avez plus de pas."
            status_text = status_font.render(message, True, (0, 120, 0) if self.board.raison_fin == "victoire" else (180, 0, 0))
            self.screen.blit(status_text, (depart_x + 20, 280))

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
        """"
        Cette méthode gere le lancement de la fenetre de eu et des évenements.
        C'est ici que l'on regarde dans quelle mode on est. 
        """
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN and self.board.magasin_actif:
                    index = None
                    if pygame.K_1 <= event.key <= pygame.K_9:
                        index = event.key - pygame.K_1
                    elif pygame.K_KP1 <= event.key <= pygame.K_KP9:
                        index = event.key - pygame.K_KP1
                    if index is not None:
                        self.board.acheter_objet_magasin(index)
                        continue
        
                
                if self.board.mode == "exploration":
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
        
                        # elif event.key == pygame.K_SPACE:
                        #     self.board.ouvrir_porte()
                            #en commentaire pour l'instant j'utilise pas se deplacer
                            #self.board.se_deplacer(self.joueur)
                        elif event.key == pygame.K_SPACE:
                            self.board.se_deplacer()
                            
        
                
                elif self.board.mode == "choix_piece":
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            self.board.changer_selection_tirage("gauche")
                        elif event.key == pygame.K_RIGHT:
                            self.board.changer_selection_tirage("droite")
                        elif event.key == pygame.K_r:
                            self.board.relancer_tirage()
                        elif event.key == pygame.K_RETURN:  
                            self.board.placer_piece_choisie()
                              
                    




            self.Partie_Salle()
            self.Partie_Inventaire()
            pygame.display.flip()
            self.clock.tick(30)

            if self.board.partie_terminee:
                pygame.time.wait(2000)
                running = False

        pygame.quit()
