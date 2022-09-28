from outils.common import verifier_mot

def rejouer() -> bool:
    """
    Renvoie si l'utilisateur veut rejouer
    """
    rejouer = input("Voulez-vous rejouer ? (O/N) ").upper()
    while rejouer.upper() not in ["O","N"]:
        rejouer = input("Voulez-vous rejouer ? (O/N) ").upper()
    return rejouer == "O"

def initialiser_jeu(longueur : int, essais_max: int) -> list:
    """
    Initialiser le jeu
    """
    stat_lettres = [12] + ([0] * (longueur-1))
    print("Bienvenue dans le SUTOM en console.\nLe mot à trouver contient", longueur, "lettres.\nVous avez",essais_max,"essais pour le trouver.")
    return stat_lettres

def fin_du_jeu(stat_lettres : list, mot : str, essai : int, max_essais: int) -> bool:
    """
    Vérifie si le jeu peut continuer (true) ou s'il faut arrêter (false)
    """
    if stat_lettres == [12] * len(mot):
        print("Bravo ! Vous avez trouvé le mot", mot)
        return False
    elif essai >= max_essais:
        print("Vous avez dépassé le nombre maximal d'essais. Le mot à trouver était",mot)
        return False
    return True

def triche(mot : str) -> None:
    """
    Affiche le mot à trouver
    """
    print("[DEBUG/TRICHE] Le mot à trouver est",mot)

def obtenir_proposition(longueur : int, essai : int) -> str:
    """
    Obtenir une proposition de l'utilisateur
    """
    proposition = input(f"Donnez votre proposition n°{essai+1} : ").upper()
    ok = False #on initialise une variable qui indique si la proposition est valide

    while not ok:
        if len(proposition) != longueur:
            proposition = input("Le mot proposé doit contenir {} lettres. Réessayez : ".format(longueur)).upper()
        elif not verifier_mot(proposition):
            proposition = input("Le mot proposé n'est pas dans le dictionnaire. Réessayez : ").upper()
        else:
            ok = True
    return proposition


def afficher_mot(mot : str, stat_lettres : list, essais : int) -> None:
    """
    Afficher le mot avec les lettres trouvées
    """
    mot_affiche = ""
    for i in range(len(mot)):
        if stat_lettres[i] // 10 == 1:
            mot_affiche += mot[i]
        else:
            mot_affiche += "."

    print(mot_affiche,f"Essai n°{essais+1}",sep="\n")


def afficher_correction(proposition : str,stat_lettres : list, essai : int) -> None:
    """
    Afficher la correction de la proposition dans la console:
        Affiche un + si la lettre est dans le mot et à la bonne place
        Affiche un ~ si la lettre est dans le mot mais pas à la bonne place
        Affiche un - si la lettre n'est pas dans le mot
    """
    
    chaine_correction = ""
    for stat in stat_lettres:
        if stat % 10 == 2:
            chaine_correction += "+"
        elif stat % 10 == 1:
            chaine_correction += "~"
        else:
            chaine_correction += "-"
    print(f"Résultat pour l'essai n°{essai+1} :",proposition,chaine_correction,sep="\n")