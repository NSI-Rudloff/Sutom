import pygame
from pygame.locals import *
from outils.common import verifier_mot
import time

pygame.init()

#import des audios
pygame.mixer.init()


class Case:
    """
    Classe modélisant une case du jeu SUTOM contenant une lettre
    """
    cote = 60 #attribut de classe : taille du coté de chaque case
    police = pygame.font.SysFont("Arial", cote//2, True)

    def __init__(self,lettre=None):
        self.lettre = lettre
        self.etat = 0 #0 <= bleu, 1 <= jaune, 2 <= rouge
        self.surface = self.get_surface()
        self.hitbox = self.surface.get_rect()

    def __repr__(self):
        return f"Case({self.lettre}, etat : {self.etat})"

    def blit(self,screen : pygame.Surface):
        """
        Affiche la case sur la surface spécifiée
        """
        screen.blit(self.surface, self.hitbox)

    def get_surface(self) -> pygame.Surface:
        """
        Renvoie l'objet pygame Surface qui représente la case
        """
        surface = pygame.Surface((self.__class__.cote, self.__class__.cote))
        if self.etat < 2:
            surface.fill((0,0,255))
        else:
            surface.fill((255,0,0))
        if self.etat == 1:
            # on dessine un cercle dans la case
            pygame.draw.circle(surface, (255,128,0), (self.__class__.cote//2, self.__class__.cote//2), self.__class__.cote//2, 0)

        if self.lettre:
            # on dessine la lettre dans la case
            texte = self.__class__.police.render(self.lettre, True, (255,255,255))
            surface.blit(texte, (self.__class__.cote//2 - texte.get_width()//2, self.__class__.cote//2 - texte.get_height()//2))

        #on rajoute un contour blanc
        pygame.draw.rect(surface, (255,255,255), (0,0,self.__class__.cote,self.__class__.cote), 1)
        return surface

    def update_surface(self):
        """
        Met à jour la surface de la case
        """
        self.surface = self.get_surface()


class Grille:
    """
    Classe modélisant la grille de jeu du SUTOM
    """
    def __init__(self,longueur : int, lignes : int):
        self.longueur = longueur
        self.lignes = lignes
        self.cases = [Case() for _ in range(longueur*lignes)]
        self.surface = self.get_surface()
        self.hitbox = self.surface.get_rect()

    def __repr__(self):
        #représenter les cases
        cases = ""
        for i in range(self.lignes):
            for j in range(self.longueur):
                cases += str(self[i,j]) + "\n"
        return f"Grille({self.longueur}, {self.lignes})\n" + cases

    def __getitem__(self, index) -> Case:
        """
        Renvoie la case à l'index spécifié
        Si l'index est un tuple de deux entiers, il est interprété comme (ligne, colonne)
        """
        if isinstance(index, tuple):
            return self.cases[index[0]*self.longueur + index[1]]
        else:
            return self.cases[index]

    def placer_mot(self, mot : str, ligne : int):
        """
        Place le mot spécifié sur la ligne spécifiée
        """
        len_mot = len(mot)
        for i in range(self.longueur):
            if i < len_mot:
                self[ligne,i].lettre = mot[i]
            else:
                self[ligne,i].lettre = "."

    def obtenir_mot(self,ligne : int):
        """
        Renvoie le mot contenu sur la ligne spécifiée
        """
        mot = ""
        for i in range(self.longueur):
            if self[ligne,i].lettre == ".":
                break
            mot += self[ligne,i].lettre
        return mot
        

    def get_surface(self) -> pygame.Surface:
        """
        Renvoie l'objet pygame Surface qui représente la grille
        """
        surface = pygame.Surface((self.longueur*Case.cote, self.lignes*Case.cote))
        surface.fill((0,0,0))
        for i in range(self.lignes):
            for j in range(self.longueur):
                self[i,j].hitbox.topleft = (j*Case.cote, i*Case.cote)
                self[i,j].update_surface()
                self[i,j].blit(surface)
        return surface

    def update_surface(self):
        """
        Met à jour la surface de la grille
        """
        self.surface = self.get_surface()

    def blit(self,screen : pygame.Surface):
        """
        Affiche la grille sur la surface spécifiée
        """
        screen.blit(self.surface, self.hitbox)

    

class Interface:
    """
    Classe modélisant l'interface graphique du jeu avec Pygame
    """
    def __init__(self, largeur : int, hauteur : int, titre : str) -> None:
        """
        Constructeur de la classe
        """
        self.largeur = largeur
        self.hauteur = hauteur
        self.titre = titre
        self.clock = pygame.time.Clock()
        self.FPS = 50
        self.police = pygame.font.SysFont("Arial", 25)

        self.grille = None

        self.message = [
            None, #message à afficher en haut de l'écran
            None #message à afficher en bas de l'écran
        ]

        self.screen = pygame.display.set_mode((self.largeur, self.hauteur))
        pygame.display.set_caption(self.titre)

        self.audios = {
            "bip" : [
                pygame.mixer.Sound("sons/motus_non.wav"),
                pygame.mixer.Sound("sons/motus_noui.wav"),
                pygame.mixer.Sound("sons/motus_oui.wav")
            ], 
            "applause" : pygame.mixer.Sound("sons/motus_applause.wav"),
            "lost" : pygame.mixer.Sound("sons/motus_lost.wav")
        }
    
    def affichage(self) -> None:
        """
        Affichage de l'interface
        """
        self.clock.tick(self.FPS)
        self.screen.fill((255, 255, 255))
        self.grille.hitbox.center = (self.largeur//2, self.hauteur//2)
        self.grille.blit(self.screen)

        if self.message[0]:
            for i in range(len(self.message[0])):
                self.screen.blit(self.message[0][i], (self.largeur//2 - self.message[0][i].get_width()//2, 10 + i*self.message[0][i].get_height()))
        
        if self.message[1]:
            for i in range(len(self.message[1])):
                self.screen.blit(self.message[1][i], (self.largeur//2 - self.message[1][i].get_width()//2, self.hauteur - 10 - (len(self.message[1]) - i)*self.message[1][i].get_height()))
        pygame.display.flip()

    def evenements(self,event : pygame.event.Event) -> None:
        """
        Gestion des évènements
        """
        if event.type == QUIT:
            pygame.quit()

    def afficher_message(self,texte : str=None, couleur : tuple=(0,0,0), position : bool = 0) -> None:
        """
        Configure l'affichage un message à l'attention du joueur
        Par défaut, le message est affiché en haut de l'écran
        Si position est à 0, le message est affiché en haut de l'écran
        Si position est à 1, le message est affiché en bas de l'écran
        """
        if texte:
            self.message[position] = []
            for ligne in texte.split("\n"):
                self.message[position].append(self.police.render(ligne, True, couleur))
            
        else:
            self.message[position] = None



interface = Interface(800, 600, "SUTOM")

def initialiser_jeu(longueur : int,max_essais : int) -> list:
    """
    Initialiser le jeu
    """
    interface.afficher_message(None, position=0)
    interface.afficher_message(None, position=1)

    stat_lettres = [12] + ([0] * (longueur-1))
    interface.grille = Grille(longueur,max_essais)
    interface.grille.update_surface()
    return stat_lettres

def triche(mot : str) -> None:
    """
    Tricher : affiche le mot à trouver
    """
    interface.afficher_message("Le mot à trouver est : " + mot,(255,0,0))

def afficher_mot(mot : str, stat_lettres : list, essais : int) -> None:
    """
    Prépare l'affichage du mot dans la grille
    """
    for i in range(len(mot)):
        if stat_lettres[i] // 10 == 1:
            interface.grille[essais,i].lettre = mot[i]
        else:
            interface.grille[essais,i].lettre = "."
    interface.grille.update_surface()

def afficher_correction(proposition : str,stat_lettres : list, essai : int) -> None:
    """
    Afficher la correction de la proposition dans la grille:
        Colore la case en rouge si la lettre est dans le mot et à la bonne place
        Colore la case en jaune si la lettre est dans le mot mais pas à la bonne place
        Colore la case en bleu si la lettre n'est pas dans le mot
    """
    for i in range(len(stat_lettres)):
        interface.grille[essai,i].lettre = proposition[i]
        etat = stat_lettres[i] % 10
        interface.grille[essai,i].etat = etat
        interface.audios["bip"][etat].play()
        time.sleep(0.2)
        interface.grille.update_surface()
        interface.affichage()

def obtenir_proposition(longueur : int, essai : int) -> str:
    """
    Obtenir une proposition de l'utilisateur
    Déclenche la gestion des événements clavier
    """
    proposition = interface.grille.obtenir_mot(essai)
    while True:
        interface.affichage()
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                elif event.key == K_RETURN:
                    if len(proposition) != longueur:
                        interface.audios["bip"][0].play()
                        interface.afficher_message("Le mot proposé doit faire " + str(longueur) + " lettres !",(255,0,0))
                    elif not verifier_mot(proposition):
                        interface.audios["bip"][0].play()
                        interface.afficher_message("Le mot proposé n'est pas dans le dictionnaire.",(255,0,0))

                    else:
                        interface.afficher_message()
                        return proposition
                elif event.key == K_BACKSPACE:
                    proposition = proposition[:-1]
                elif len(proposition) < longueur and event.unicode.upper() in "ABCDEFGHIJKLMNOPQRSTUVWXYZ#":
                    proposition += event.unicode.upper()
                interface.grille.placer_mot(proposition, essai)
                interface.grille.update_surface()
            interface.evenements(event)

def fin_du_jeu(stat_lettres : list, mot : str, essai : int, max_essais: int) -> bool:
    """
    Vérifie si le jeu peut continuer (true) ou s'il faut arrêter (false)
    """

    continuer_jeu = True

    if stat_lettres == [12] * len(mot):
        interface.audios["applause"].play()
        interface.afficher_message("Bravo !\nVous avez trouvé le mot " + mot)
        continuer_jeu = False
    elif essai >= max_essais:
        interface.audios["lost"].play()
        interface.afficher_message("Vous avez dépassé le nombre maximal d'essais.\nLe mot à trouver était " + mot)
        continuer_jeu = False

    if continuer_jeu:
        return True

def rejouer() -> bool:
    """
    Demande au joueur s'il veut rejouer
    """

    # affiche en bas de l'écran
    interface.afficher_message("Voulez-vous rejouer ?\nOui : appuyez sur Entrée\nNon : appuyez sur Echap", (0,0,0), True)
    while True:
        interface.affichage()
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return False
                elif event.key == K_RETURN:
                    return True
            interface.evenements(event)