def afficher_options():
    print("\n")
    
    print("Quelle action souhaitez-vous effectuer ? ")
    print("\n")
    
    print("1. Affichage de la segmentation")
# permet de fixer un seuil et puis en fonction de ce seuil,créer un masque a partir de l'image binarisée, avec 1 si c'est au dessus du seuil et 0 sinon
    print("2. Erosion") 
# permet de rogner en quelques sortes si les pixels autour d'un pixel 1 sont pas tous à 1
    print("3. Dilatation")
# permet d'aggrandir la superficie de pixels autour de chaque pixel
    
    
   
    print("4. Question trivia")
    print("5. Ouverture x10")
    print("6. Fermeture x10")
    print("7. Quitter")
    print("\n")
    choix=input("Quel est votre choix : ? ")
    print("\n")
    print("\n")
    return choix

def choix():
    print("Choisissez une des options suivantes : \n")
    print("1. Ouverture (enlever les poussieres)")
    print("2. Fermeture (boucher les trous)")
    print("3. Passer")  
    print("\n")
    choix2=input("Quel est votre choix ? : ")
    print("\n")
    return choix2