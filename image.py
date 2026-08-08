import numpy as np
from PIL import Image, ImageFilter, ImageDraw
import matplotlib.pyplot as mpt
from scipy.ndimage import gaussian_filter,label,find_objects, binary_erosion
import random
import math
import time

class Image_analysis():

    def __init__(self, image1):
        img = Image.open(image1)
        if img.mode in ("RGB","RGBA"):
            img=img.convert("L")
        matrice_1 = np.array(img, dtype=float)#je créer une matrice pour pouvoir ensuite convertir les pixels pour 8 bit
        matrice_gray = (matrice_1/ np.max(matrice_1)) * 255.0 #petite conversion hehe
        image_propre = Image.fromarray(matrice_gray.astype(np.uint8)) #on remets ca en vraie image de 8 bits
        self.image = image_propre
        self.image_og = self.image.copy()
        self.masque = None
    

    def affichage_og(self):
        self.image_og.show()
        

    def affichage(self):
        self.image.show()

    #trouver le seuil
    def trouver_seuil(self): #methode otsu
        pixels=np.array(self.image).flatten() #une grande liste plate 
        nbr_pixels=len(pixels)
        meilleur_seuil=0
        score_max=0
        for t in range(256): #de 0 à 255 tout tester
            g1=pixels[pixels<t]#noir
            g2=pixels[pixels>=t]#pixels lumineux
            if len(g1)==0 or len(g2)==0: #verifier que les groupes ne soient pas vide
                continue
            w1=len(g1)/nbr_pixels#nombre pixels noir divisé par nombre de pixel (proportion)
            w2=len(g2)/nbr_pixels#nombre pixels lumineux divisé par nombre de pixel
            moyenne1=np.mean(g1)#calcul moyenne couleur pixel du groupe 1
            moyenne2=np.mean(g2)#calcul moyenne couleur pixel du groupe 2
            score=(w1*w2)*((moyenne1-moyenne2)**2)
            if score>score_max:
                score_max=score
                meilleur_seuil=t
        return meilleur_seuil

    #BINARISATION AVEC CHOIX DU SEUIL
    def binarisation(self,seuil):
        lignes=self.image.size[1]
        colonnes=self.image.size[0]
        self.masque=np.zeros((lignes,colonnes))
        for i in range(lignes):
            for j in range(colonnes):
                valeur= self.image.getpixel((j, i))
                if valeur>=seuil:
                    self.masque[i,j]=1
                else:
                    self.masque[i,j]=0

        print("Binarisation terminée")



    #EROSION
    def erosion(self):
        lignes=self.image.size[1]
        colonnes=self.image.size[0]
        nouveau_masque=np.copy(self.masque)
        for i in range(lignes):
            for j in range(colonnes):
                if self.masque[i,j]==1:
                    doit_blanc=True
                    if i>0 and self.masque[i-1,j]==0:
                            doit_blanc=False
                    if i<lignes-1 and self.masque[i+1,j]==0:
                            doit_blanc=False
                    if j<colonnes-1 and self.masque[i,j+1]==0:
                            doit_blanc=False
                    if j>0 and self.masque[i,j-1]==0:
                           doit_blanc=False
                    if not doit_blanc:
                        nouveau_masque[i,j]=0
        self.masque=nouveau_masque
        print("Erosion terminée")

    #DILATATION AU VOISIN DIRECT
    def dilatation(self):
        lignes=self.image.size[1]
        colonnes=self.image.size[0]
        nouveau_masque=np.copy(self.masque)
        for i in range(lignes):
            for j in range(colonnes):
                if self.masque[i,j]==1:
                    if i<lignes-1:
                        nouveau_masque[i+1,j]=1
                    if i>0:
                        nouveau_masque[i-1,j]=1
                    if j<colonnes-1:
                        nouveau_masque[i,j+1]=1
                    if j>0:
                        nouveau_masque[i,j-1]=1
        self.masque=nouveau_masque
        print("Dilatation terminée")

    #AFFICHAGE HISTOGRAMME  
    def histogramme(self):
        lignes=self.image.size[1]
        colonnes=self.image.size[0]
        mpt.xlabel("Niveau de gris")
        mpt.ylabel("Nombre de pixel")
        Liste=[]
        for i in range(lignes):
            for j in range(colonnes):
                valeur=self.image.getpixel((j,i))
        
                Liste.append(valeur)
        mpt.hist(Liste,bins=260,range=(0,259))
        mpt.show()
   
    #AFFICHAGE DU MASQUE EN NOIR ET BLANC
    def affiche_masque(self):
        if self.masque is None:
            print("Ton masque est vide")
            return
        mpt.axis("off")
        mpt.imshow(self.masque, cmap='gray') #pour afficher en noir et blanc
        mpt.title("Regarde")
        mpt.show()

    #FLOU GAUSSIEN MERCI SCIPY, AVEC CHOIX DU "FLOU" 
    def flou_gaussien(self, rayon, sigma):
        #CREATION DU NOYAU
        taille=2*rayon + 1 #rayon definir la taille en soit
        noyau=np.zeros((taille,taille))#création de matrice avec 0 pour le noyau
        somme=0
        for ky in range(-rayon, rayon+1):
            for kx in range(-rayon,rayon+1):
                e=math.exp(-(kx**2+ky**2)/(2*sigma**2)) #calculateur de poids qui dépend aussi de la valeur de sigma
                noyau[ky+rayon][kx+rayon]=e #je donne la valeur du "poids" au noyau a la bonne position le +rayon est pour rester dans les valeurs positives
                somme=somme + e
        noyau=noyau/somme #on divise chaque case par la somme des poids (pour rester dans une tranche calculable par la suite)
        #noyau fait
        image_grise=self.image #conversion en image grise
        matrice_image=np.array(image_grise,dtype=float) #je créer une matrice
        ligne,colonne=matrice_image.shape #je recupere nombre ligne colonne
        matrice_finale=np.copy(matrice_image) #je fais une copie pour définir nouvelle matrice avec le flou du coup
        for y in range(rayon,ligne - rayon): #allez de rayon a ligne moins rayon car le curseur est placé au centre taille noyau et non pas aux extremités
            for x in range(rayon, colonne - rayon): #idem
                somme_pixel=0.0
                for ky in range(-rayon, rayon+1):
                    for kx in range(-rayon,rayon+1):
                        poids=noyau[ky+rayon][kx+rayon]
                        somme_pixel=somme_pixel+(poids*(matrice_image[y+ky][x+kx]))
                matrice_finale[y][x]=somme_pixel
        matrice_finale=np.clip(matrice_finale,0,255).astype(np.uint8)
        self.image=Image.fromarray(matrice_finale)
        print("flou terminé")


    #APPLIQUER LE MASQUE (POUR ENSUITE FAIRE LE CONTOUR)
    def appliquer_masque(self):
        mat_image=np.array(self.image)
        image_superposee=(self.masque * mat_image).astype(mat_image.dtype)
        self.image=Image.fromarray(image_superposee)
        print("Masque appliqué")

    
    #AFFICHAGE L'IMAGE D'ORIGINE + LE CONTOUR (GRACE A MATPLOTLIB)
    def affichage_final(self):
        mpt.imshow(self.image_og, cmap="gray")
        mpt.contour(self.masque, levels=[0.4], colors='red', linewidths=3)
        mpt.axis("off")
        mpt.show()

    #A NE PAS PRENDRE EN COMPTE (JE NE M'EN SERT PAS AU FINAL)
    def contour(self):
        
        width=5
        erosion_masque=binary_erosion(self.masque, iterations=width)
        nouveau_contour=self.masque-erosion_masque
        nouveau_contour=np.array(nouveau_contour)
        self.image=self.image.convert("RGB")
        mat_image=np.array(self.image)
        mat_image[nouveau_contour==1]=[255,0,0]
        
        self.image=Image.fromarray(mat_image)

    def trivia(self):
        jouer = input("\nVeux-tu jouer au mini-jeu Trivia pour décompresser ? (oui/non) : \n")
        if jouer.lower() == "oui":
            print("\n")
            print("BIENVENUE DANS LE TRIVIA DE L'IMAGE")
            print("\n")
    
            questions = questions =  {
    "Quel animal fait des crottes carrées comme s'il jouait à Minecraft ?": "wombat",
    "Quel pays a déclaré la guerre à des oiseaux... et a perdu ?": "australie",
    "Quel animal peut se saouler en mangeant des fruits fermentés ?": "elephant",
    "Quel est le seul aliment qui ne périme pratiquement jamais, même oublié par tes arrière-petits-enfants ?": "miel",
    "Quel animal peut survivre plusieurs jours après avoir perdu sa tête ?": "cafard",
    "Quelle planète sent l'œuf pourri à cause de son atmosphère ?": "uranus",
    "Quel animal applaudit ses potes avec ses pinces sous l'eau ?": "crevette_pistolet",
    "Quel pays possède une île remplie uniquement de lapins ?": "japon",
    "Quel animal a inventé le jet d'urine à longue distance avant les karchers ?": "lama",
    "Quel poisson devient littéralement un blob avec une sale tête quand il remonte à la surface ?": "blobfish",
    "Quel animal peut retenir son caca pendant plusieurs mois ?": "paresseux",
    "Quel mammifère pond des œufs et ressemble à un Pokémon buggué ?": "ornithorynque",
    "Quel pays possède un distributeur automatique presque tous les 25 mètres ?": "japon",
    "Quel animal peut dormir 22 heures par jour sans culpabiliser ?": "koala",
    "Quel insecte peut survivre à une explosion nucléaire mieux que toi ?": "cafard",
    "Quel fruit est techniquement une baie alors qu'il n'en a pas l'air ?": "banane",
    "Quel animal peut changer de sexe au cours de sa vie ?": "poisson-clown",
    "Quel pays a une ville qui s'appelle Batman ?": "turquie",
    "Quel animal produit le bruit le plus fort du monde par rapport à sa taille ?": "crevette_pistolet",
    "Quel animal a des empreintes digitales tellement proches des nôtres qu'il pourrait presque commettre un crime parfait ?": "koala",
    "Quel oiseau peut imiter une tronçonneuse mieux que certains youtubeurs bricolage ?": "lyrebird",
    "Quel animal transpire du sang quand il est stressé ?": "hippopotame",
    "Quel pays consomme plus de nouilles instantanées que le reste de l'univers semble raisonnable ?": "chine",
    "Quel animal peut voir avec ses fesses ?": "papillon",
    "Quel animal possède le plus gros cerveau du monde ?": "cachalot",
    "Quel animal peut rester coincé dans un bocal et quand même dominer l'océan ?": "pieuvre",
    "Quel pays possède un musée entièrement dédié aux échecs amoureux ?": "croatie",
    "Quel animal est capable de se cloner lui-même ?": "meduse",
    "Quel animal peut survivre dans l'espace alors que toi tu meurs sans wifi ?": "tardigrade",
    "Quel animal a été filmé en train de voler des caméras pour prendre des selfies ?": "singe"
}
    
            question_choisie = random.choice(list(questions.keys()))
            bonne_reponse = questions[question_choisie]
    
            print(f"\n❓ Question : {question_choisie}")
            reponse_utilisateur = input("Ta réponse : (en majuscule) ").strip().lower()
            print("\n Mhhhh 🧐 ")
            time.sleep(2)
            if reponse_utilisateur == bonne_reponse:
                print("Ouais okay, c'est une bonne réponse 🙄 bravo tres contente pour toi")
            else:
                print(f"AIE AIE AIE, tellement pas! La bonne réponse était : {bonne_reponse.upper()}")
                print("C'est okay d'etre nul")
                print("\n")