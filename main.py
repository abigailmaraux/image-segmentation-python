import menu
from image import Image_analysis
import numpy as np
from PIL import Image, ImageFilter, ImageDraw
import matplotlib.pyplot as mpt
from scipy.ndimage import gaussian_filter,label,find_objects
import time

print("\n")
print("\n")
print("Démarrage du programme ...")
print("\n")
whatamIdoing=None

#DEMANDER LE NOM DU FICHIER
while whatamIdoing is None:
    try:
        chemin=input("Quel est le chemin de votre fichier : ?")
        print("\n")
        whatamIdoing=Image_analysis(chemin)
        print("Image chargée en mémoire !")
        print("\n")
    except FileNotFoundError:
        print("Fichier introuvable, veuillez ressayer")
        print("\n")
        whatamIdoing=None

whatamIdoing.affichage()

#AFFICHAGE DE L'HISTOGRAMME
if whatamIdoing is not None:
    print("Affichons l'histogramme associé ... \n")
    whatamIdoing.histogramme()

#EFFECTUER LE FLOU GAUSSIEN
if whatamIdoing is not None:
    choix2=int(input("Le rayon va determiner la taille du viseur. Quel est votre rayon choisi : ? \n"))
    choix222=int(input("Le sigma va determiner l'intensité du flou. Quelle valeur pour votre sigma : ? \n"))
    whatamIdoing.flou_gaussien(rayon=choix2,sigma=choix222)

#AFFICHAGE DE L'IMAGE
if whatamIdoing is not None:
    whatamIdoing.affichage()

#AFFICHAGE DE L'HISTOGRAMME
if whatamIdoing is not None:
    print("Affichons l'histogramme associé ...")
    print("\n")
    whatamIdoing.histogramme()

#DEMANDE POUR FAIRE UNE BINARISATION AVEC SEUIL
action=False
while action==False:
    choix1=input("Voulez-vous faire une binarisation : ? (réponse :  oui/non) \n\n")
    if choix1.lower()=="oui":
        valeur=int(input("Quel est votre seuil : ?"))
        print("Et non j'ai choisi un seuil pour toi (de rien)")
        vraie_valeur=int(whatamIdoing.trouver_seuil())
        whatamIdoing.binarisation(seuil=vraie_valeur)
        action=True
    elif choix1.lower()=="non":
        action=True


 # SI BINARISATION FAITE, AFFICHAGE DE L'IMAGE ET DU MASQUE       
if choix1.lower()=="oui":   
    if whatamIdoing is not None:
        print("Affichons l'image associée ... et le masque")
        print("\n")
        whatamIdoing.affichage()
        whatamIdoing.affiche_masque()

#DEMANDER SI L'UTILISATEUR VEUT UNE OUVERTURE, FERMETURE OU PASSER
choice22=menu.choix()
if choice22=="1":
    if whatamIdoing is not None:
            whatamIdoing.erosion()
            whatamIdoing.dilatation()
            print("Affichons l'image associée ... et le masque")
            print("\n")
            whatamIdoing.affichage()
            whatamIdoing.affiche_masque()
    
elif choice22=="2":
    if whatamIdoing is not None:
            whatamIdoing.dilatation()
            whatamIdoing.erosion()
            print("Affichons l'image associée ... et le masque")
            print("\n")
            whatamIdoing.affichage()
            whatamIdoing.affiche_masque()
elif choice22=="3":
    None


#APPLIQUER LE MASQUE SUR L'IMAGE

time.sleep(3)
print("On applique le masque sur l'image ...")

whatamIdoing.appliquer_masque()
whatamIdoing.affichage()


#APPLIQUER LE CONTOUR

reponse1=False
while reponse1==False:
    reponse=input("Voulez-vous voir votre segmentation finale ? (reponse : oui/non) ")
    if reponse.lower()=="oui":
        if whatamIdoing is not None:
            whatamIdoing.affichage_final()
            reponse1=True
    else:
        print("Il faut répondre oui")
        reponse1=False

while 1:
    choice=menu.afficher_options()
    if choice=="1":
        if whatamIdoing is not None:
            whatamIdoing.affichage_final()
        

    elif choice=="2":
        if whatamIdoing is not None:
            whatamIdoing.erosion()
    
    elif choice=="3":
        if whatamIdoing is not None:
            whatamIdoing.dilatation()


    elif choice=="4":
        if whatamIdoing is not None:
            whatamIdoing.trivia()

    elif choice=="5":
        if whatamIdoing is not None:
            for i in range(9):
                whatamIdoing.erosion()
                whatamIdoing.dilatation()
            print("Affichons l'image associée ... et le masque")
            print("\n")
            whatamIdoing.affichage()
            whatamIdoing.affiche_masque()
    
    elif choice=="6":
        if whatamIdoing is not None:
            for i in range(9):
                whatamIdoing.dilatation()
                whatamIdoing.erosion()
            print("Affichons l'image associée ... et le masque")
            print("\n")
            whatamIdoing.affichage()
            whatamIdoing.affiche_masque()

    elif choice=="7":
        print("Bye bye")
        break      
    else:
        print("Seules réponses possibles : 1, 2, 3, 4, 5, 6 ou 7")
        

    
