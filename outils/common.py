import random

def obtenir_liste_mots(fichier: str="sutom_wordlist.txt") -> list:
    """
    Obtenir la liste de mots depuis un fichier
    """
    with open(fichier, "r") as f:
        mots = f.read().strip().split("\n")
    return mots

def mot_au_hasard() -> None:
    """
    Obtenir un mot au hasard depuis la liste de mots
    """
    return random.choice(obtenir_liste_mots())

def verifier_mot(proposition : str) -> bool:
    """
    Vérifier si le mot proposé est dans le dictionnaire
    """
    return proposition in obtenir_liste_mots("dictionnaire.txt") or proposition == "#"*len(proposition)

def correction(proposition : str,mot: str, stat_lettres : list) -> list:
    """
    Corrige la proposition
    Retourne la liste stat_lettres modifiée
    """
    lettres_a_trouver = list(mot)

    for i in range(len(proposition)):
        if proposition[i] == mot[i]:
            lettres_a_trouver.remove(proposition[i])

    for i in range(len(proposition)):
        deja_trouve = (stat_lettres[i] // 10)*10
        if proposition[i] == mot[i]:
            stat_lettres[i] = 12
        elif proposition[i] in mot and proposition[i] in lettres_a_trouver:
            stat_lettres[i] = deja_trouve + 1
            lettres_a_trouver.remove(proposition[i])
        else:
            stat_lettres[i] = deja_trouve
    return stat_lettres
