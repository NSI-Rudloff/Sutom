#!/usr/bin/python3
from outils.common import *
from outils.graphique import *

from sys import argv

def jeu(mot : str = None) -> None:
    """
    Fonction principale du jeu du SUTOM
    """
    if not mot:
        mot = mot_au_hasard()
    longueur = len(mot) #on stocke la longueur du mot
    essai = 0
    max_essais = 6

    stat_lettres = initialiser_jeu(longueur,max_essais)

    continuer = True #variable pour la boucle principale
    while continuer:
        afficher_mot(mot, stat_lettres,essai)

        proposition = obtenir_proposition(longueur,essai)

        #triche !
        if proposition == "#"*longueur:
            triche(mot)
            essai -= 1

        # la liste stat_lettres contient autant de nombres que de lettres dans le mot
        # chaque nombre représente l'état de la lettre correspondante
        # le chiffre des dizaines représente l'état de la lettre pour l'ensemble de la manche
        # 1 <= lettre trouvée
        # 0 <= lettre non trouvée

        # le chiffre des unités représente l'état de la lettre pour la proposition en cours
        # 2 <= lettre trouvée
        # 1 <= lettre présente dans le mot mais pas à la bonne place
        # 0 <= lettre non trouvée

        stat_lettres = correction(proposition, mot, stat_lettres)
        afficher_correction(proposition,stat_lettres,essai)

        essai += 1
        continuer = fin_du_jeu(stat_lettres, mot, essai,max_essais)
    if rejouer():
        jeu()


jeu(argv[1].upper() if len(argv) > 1 else None) #si on a un argument (mot particulier à faire deviner), on le passe à la fonction jeu
