# Jeu du motus

## Règles du jeu
Le principe du jeu est le suivant :
 - Vous avez 6 essais pour trouver un mot entre 5 et 9 lettres.
 - Remplissez une ligne de la grille avec le clavier et appuyez sur `Entrée`. Le mot doit faire le nombre de lettres prévu et être dans le dictionnaire.
 - Les lettres du mot proposé se colorent :
    * en rouge si la lettre est à la bonne place
    * en orange si la lettre est dans le mot mais pas à la bonne place
    * en bleu (ne changent pas de couleur) si la lettre proposée n'est pas dans le mot

 - A la fin du jeu, faire `Entrée` pour rejouer et `ESC` pour quitter. A tout moment, on peut cliquer sur la croix de la fenêtre pour tuer le processus.

## Fonctionnalités
### Faire deviner un mot à un ami
Lancer le programme avec un argument permet de faire deviner le mot que l'on veut.

Par exemple, avec la commande `python3 sutom.py abricot` fais deviner le mot "abricot". Attention le mot donné doit être dans le dictionnaire !

### Tricher
Pour tricher, c'est-à-dire afficher le mot que l'on fait deviner, il suffit de donner un mot rempli de '\#'. La solution sera alors affichée, et il suffira de la recopier pour gagner.

### Jouer en console
Pour jouer sur des machines possédant des capacités trop basses pour faire tourner un SUTOM avec Pygame (Nokia 3310, GPS, calculatrice solaire, micro-ondes, grille-pain, lave-vaisselle, etc.), il est possible de jouer en mode console en remplaçant la ligne :
```python
from outils.graphique import *
```
par :
```python
from outils.console import *
```
dans `sutom.py`.