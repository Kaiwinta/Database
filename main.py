from tkinter import *
from tkinter import  filedialog
import MoreFunctions , DataBasePart
from PIL import Image , ImageTk

import sqlite3

conn = sqlite3.connect('user.db')
colorpalette = ["#8e94f2","#9fa0ff","#ada7ff"]


def main():
    """
        Lance la boucle Principale

        Créer une fenetre main
    """
    #Création de la fenetre
    main = Tk()
    main.geometry("1024x574")
    main.title('Outils Graphe Db')
    main.iconbitmap('Images/grv2.ico')
    main.resizable(False,False)
    #On relie la fenètre au bouton "Echap" avec comme fonction de se détruire
    main.bind('<Escape>',lambda e: main.destroy())
    
    #ajout d'une image d'icone en haut et dans la barre de tache
    icon_image = Image.open('Images/gv3.png')
    icon_photo = ImageTk.PhotoImage(icon_image)
    main.iconphoto(True, icon_photo)
    
    #Ajout d'un cadre à la fenetre
    cadre(main)

    #Création d'une zone modifiable dans laquelle nous afficherons tous
    fr1 = Frame(main, bg =colorpalette[0])
    fr1.pack(fill= 'both', expand= True)

    
    def my_callback():
        """
            Cette fonction permet d'attendre le message de la pars de loading avant d'éxécuter le reste
        """
        menu1(fr1)

    #Appel la fonction loading d'un autre fichier en lui ajoutant comme paramètre la fonction my_callback
    #pour qu'il puisse renvoyer un signal
    MoreFunctions.loading(fr1,my_callback)


    #Lancement de La fenètre
    main.mainloop()
 



def cadre(root):
    """
    Affiche un cadre de contour d'une fenetre 
    Le Cadre est composé de 3 rectangle par coté et 2 par hauteur formant un gradiant de couleur

    Args:
        root (Tk()): une fenetre
    """
    liste_cote = ["left","right" , "top" , "bottom"]
    liste_couleur = ["#bbadff","#cbb2fe","#dab6fc","#ddbdfc","#e0c3fc"]
    

    for i in range(10):
        couleur = liste_couleur[i%5]
        cote = liste_cote[i%4] 

        fill='x'
        if i%4 <2:
            fill ='y'
        rect= Canvas(root, bg=couleur,height=25, highlightthickness=0 , width=25)
        rect.pack(side=cote, fill=fill)
    


def menu1(frame):
    """
    Objectif : Afficher la première page dans une frame

    Args:
        frame (Frame()): Est un espace dans lequel on va afficher ce que l'on veut
    """
    MoreFunctions.delete_frame(frame)
    def gotopage2():
        """
            Cette fonction permet d'utiliser la fonction delete_frame en appuyant sur un bouton
        """
        menu2(frame)

    framehaut = Frame(frame , bg = colorpalette[1])
    framehaut.place(relx= 0.03 , rely=0.05 , relheight= 0.075 , relwidth= 0.94)

    framebutton = Frame(frame, bg = colorpalette[1])
    framebutton.place(relx=0.20 , relwidth= 0.60, rely= 0.2 , relheight=0.7)

    titrePage1 = Label(framehaut, text="Bienvenue dans l'outil de création de graphe d'un réseau social imaginaire", font=('Helvetica',14),bg = colorpalette[1])
    titrePage1.place(relx = 0.12, rely=0.05)

    button1 = Button(framehaut, activebackground=colorpalette[2], background='purple',height=1 ,width = 1,command=gotopage2)
    button1.pack( side = "right")

    

def menu2(frame):
    """
    Objectif : Afficher la deucième page dans une frame

    Args:
        frame (Frame()): Est un espace dans lequel on va afficher ce que l'on veut
    """
    MoreFunctions.delete_frame(frame)
    Nom = ''
    Prenom = ''

    def goback():
        menu1(frame)

    def gotopage3():
       
        menu3(frame)

    img = Image.open("Images/no_image.png")
    width, height = img.size

    def resize_image(event,img,height,width):
        
        frame_width = event.width
        frame_height = event.height

        if width > height:
            new_width = frame_width
            new_height = int(height * frame_width / width)
        else:
            new_height = frame_height
            new_width = int(width * frame_height / height)

        # Resize the image to the desired size
        img = img.resize((new_width, new_height), Image.LANCZOS)

        # Convert the resized image to a PhotoImage
        photo_img = ImageTk.PhotoImage(img)

        # Update the label with the new image
        imgFrame.config(image=photo_img)
        imgFrame.image = photo_img  # Keep a reference to the PhotoImage to prevent garbage collection
    
    def change():
        
        print(Nom,Prenom)
        if Nom != '' and Prenom !='':
            print('bouhh')
            DataBasePart.afficher_graphe_perso(Nom,Prenom)

            img = Image.open("Images/Result.png")
            width, height = img.size
            photo_img = ImageTk.PhotoImage(img)
            imgFrame.config( image=photo_img)
            imgFrame.pack(fill='none',expand=TRUE,)
            imgFrame.bind( "<Configure>",lambda event: resize_image(event, img,height,width))

    def actualiser(event, zone):
        """
        Objectif: Actualise la partie voulue et aussi l'autre à chaque événement rentré

        Args:
            event (Event): L'événement de la clé pressée ou du focus in dans une des deux zones
            zone (str): Soit "Nom" ou "Prenom" pour mieux gérer les collisions
        """

        #L'on défini les variable en fonciton du cas dans lequel l'on est 
        if zone == "Prenom":
            entree = entreePrenom
            entree2 = entreeNom
            liste = listePrenom
            liste2 = listeNom
            seconde = "Nom"

        else:
            entree = entreeNom
            entree2 = entreePrenom
            liste = listeNom
            liste2 = listePrenom
            seconde = "Prenom"

        valeur = entree.get()
        valeur2 = entree2.get()

        if event.keysym != "BackSpace" and event.keysym != "Tab" and event.keysym != 'Return':
            valeur += event.char

        if event.keysym == "BackSpace":
            valeur = valeur[:-1]

        liste.delete(0, END)
        liste2.delete(0,END)

        if len(valeur) > 0 or len(valeur2)>0:
            if len(entree2.get()) > 0:
                possibilite = DataBasePart.recherche(valeur, zone, seconde, valeur2)
                possibiliteseconde = DataBasePart.recherche(valeur2 ,seconde, zone, valeur)
                
            else:
                possibilite = DataBasePart.recherche(valeur, zone, '', '')
                possibiliteseconde = DataBasePart.recherche('', seconde, zone, valeur)
                
            for i in possibilite:
                liste.insert(END, i)
            
            for y in possibiliteseconde:
                liste2.insert(END, y)
    
    def validationNom():
        Nom = listeNom.get(ANCHOR)
        return Nom

    def validationPrenom():
        Prenom = listePrenom.get(ANCHOR)
        return Prenom
    #Divising our page in Frame
    framehaut = Frame(frame , bg = colorpalette[1])
    frameimg = Frame(frame ,bg=colorpalette[1])
    framecrit = Frame(frame , bg = colorpalette[1])

    #Placing our frames
    framehaut.place(relx= 0.03 , rely=0.05 , relheight= 0.075 , relwidth= 0.94)
    frameimg.place(relx=0.4, rely=0.15 , relheight= 0.80 , relwidth=0.57)
    framecrit.place(relx=0.03 , rely=0.15 , relheight=0.80 , relwidth=0.35)

    #Placing the Image
    photo_img = ImageTk.PhotoImage(img)
    imgFrame = Label(frameimg, image=photo_img)
    imgFrame.pack(fill='none',expand=False,anchor=CENTER)
    
    
    #A changer
    button1 = Button(framehaut, activebackground='blue', background='purple',height=1 ,width = 1,command=gotopage3)
    button1.pack(side ='right')
    labelTitre = Label(framehaut, text="Recherche de personne",font=('Helvetica',14),bg = colorpalette[1])
    labelTitre.place(relx = 0.4, rely=0.05)

    button1 = Button(framehaut, activebackground='blue', background='purple',height=1 ,width = 1,command=goback)
    button1.pack(side = "left")

    #We define all the object of the frame : framecrit
    labelnom = Label(framecrit , text='Nom' )
    labelprenom = Label(framecrit, text='Prenom')

    entreeNom = Entry(framecrit, background=colorpalette[2])
    entreePrenom = Entry(framecrit, background=colorpalette[2])

    listeNom = Listbox(framecrit , bg=colorpalette[2])
    listePrenom = Listbox(framecrit , bg=colorpalette[2])

    buttonValiderNom = Button(framecrit,text="Valider Nom", activebackground='blue', background='purple',height=1 ,width = 1,command=validationNom)
    buttonValiderPrenom = Button(framecrit,text="Valider Prenom", activebackground='blue', background='purple',height=1 ,width = 1,command=validationPrenom)    
    buttonGraphe = Button(framecrit, text="Afficher les Liens",activebackground='blue', background='purple',height=1 ,width = 1,command=change)

    #We place all the object on the frame
    labelnom.place(rely=0.1 , relheight= 0.05 , relx = 0.05 , relwidth= 0.4)
    labelprenom.place(rely=0.1 , relheight= 0.05 , relx = 0.55 , relwidth= 0.4)    

    entreeNom.place(rely = 0.17 , relheight=0.05 , relwidth=0.4 , relx=0.05)
    entreePrenom.place(rely = 0.17 , relheight=0.05 , relwidth=0.4 , relx=0.55)
    
    listeNom.place(rely=0.3 , relheight= 0.3 , relx = 0.05 , relwidth= 0.4)
    listePrenom.place(rely=0.3 , relheight= 0.3 , relx = 0.55 , relwidth= 0.4)

    buttonValiderNom.place(rely = 0.62, relx=0.05, relheight= 0.05 , relwidth= 0.4)
    buttonValiderPrenom.place(rely = 0.62, relx=0.55, relheight= 0.05 , relwidth= 0.4)
    buttonGraphe.place(rely = 0.85, relx=0.35, relheight= 0.05 , relwidth= 0.3)


    #Binding all our event
    imgFrame.bind( "<Configure>",lambda event: resize_image(event, img,height,width))
    entreeNom.bind('<Key>', lambda event: actualiser(event, "Nom"))
    entreePrenom.bind('<Key>', lambda event: actualiser(event, "Prenom"))

    frame.mainloop()

def menu3(frame):
    """
    Objectif : Afficher la deucième page dans une frame

    Args:
        frame (Frame()): Est un espace dans lequel on va afficher ce que l'on veut
    """
    MoreFunctions.delete_frame(frame)

    def goback():
        menu2(frame)

        
    button1=Label(frame,width=12, height = 6,text=  'page3')
    button1.pack(side="left",expand=False , fill="x")
    button1 = Button(frame, activebackground='blue', background='purple',height=1 ,width = 1,command=goback)
    button1.pack(fill ='x',expand = False, side = "bottom")



#Lancement du programme principal
if __name__ == '__main__':
    main()