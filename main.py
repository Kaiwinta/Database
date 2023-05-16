from tkinter import *
from tkinter import  filedialog
import MoreFunctions , DataBasePart
from PIL import Image , ImageTk

import sqlite3

conn = sqlite3.connect('user.db')

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
    
    #On relie la fenètre au bouton "Echap" avec comme fonction de se détruire
    main.bind('<Escape>',lambda e: main.destroy())
    
    #ajout d'une image d'icone en haut et dans la barre de tache
    icon_image = Image.open('Images/gv3.png')
    icon_photo = ImageTk.PhotoImage(icon_image)
    main.iconphoto(True, icon_photo)
    
    #Ajout d'un cadre à la fenetre
    cadre(main)

    #Création d'une zone modifiable dans laquelle nous afficherons tous
    fr1 = Frame(main, bg ='#327EF1')
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
    liste_couleur = ["#c99b0e","#e1ad0f","#efbb1a","#f1c232","#f3c94a","#f4d062","#f6d77a"]
    

    for i in range(10):
        couleur = liste_couleur[i%7]
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

    framehaut = Frame(frame , bg = '#2864c0')
    framehaut.place(relx= 0.03 , rely=0.05 , relheight= 0.075 , relwidth= 0.94)

    framebutton = Frame(frame, bg = '#2864c0')
    framebutton.place(relx=0.20 , relwidth= 0.60, rely= 0.2 , relheight=0.7)

    text1 = Label(framehaut, text="Bienvenue dans l'outil de création de graphe d'un réseau social imaginaire", font=('Helvetica',14),bg = "#2864c0")
    text1.place(relx = 0.12, rely=0.05)

    button1 = Button(framehaut, activebackground='blue', background='purple',height=1 ,width = 1,command=gotopage2)
    button1.pack( side = "right")

    

def menu2(frame):
    """
    Objectif : Afficher la deucième page dans une frame

    Args:
        frame (Frame()): Est un espace dans lequel on va afficher ce que l'on veut
    """
    MoreFunctions.delete_frame(frame)

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
        img = Image.open("Images/image2test.png")
        width, height = img.size
        photo_img = ImageTk.PhotoImage(img)
        imgFrame.config( image=photo_img)
        imgFrame.pack(fill='none',expand=TRUE,)
        imgFrame.bind( "<Configure>",lambda event: resize_image(event, img,height,width))


    
    def actualiserNom(event):
        nom =entreeNom.get()
        if event.keysym != 'BackSpace' : 

            nom += event.char
        else: 
            nom = nom[:-1]

        listeNom.delete(0,END)
        if  nom != None:

            nom_possible = DataBasePart.recherche(nom,'Nom')
            for i in nom_possible:
                listeNom.insert(END , i)
                
    def actualiserPrenom(event):
        prenom =entreePrenom.get()
        if event.keysym != 'BackSpace':

            prenom += event.char
        else:
            prenom = prenom[:-1]
        
        listePrenom.delete(0, END)
        if prenom != None:

            prenom_possible = DataBasePart.recherche(prenom,'Prenom')
            for i in prenom_possible:
                listePrenom.insert(END , i)
        
        

    framehaut = Frame(frame , bg = '#2864c0')
    framehaut.place(relx= 0.03 , rely=0.05 , relheight= 0.075 , relwidth= 0.94)

    frameimg = Frame(frame ,bg='#2864c0')
    frameimg.place(relx=0.4, rely=0.15 , relheight= 0.80 , relwidth=0.57)

    framecrit = Frame(frame , bg = '#2864c0')
    framecrit.place(relx=0.03 , rely=0.15 , relheight=0.80 , relwidth=0.35)

    photo_img = ImageTk.PhotoImage(img)
    imgFrame = Label(frameimg, image=photo_img)
    imgFrame.pack(fill='none',expand=False,anchor=CENTER)
    imgFrame.bind( "<Configure>",lambda event: resize_image(event, img,height,width))

    
    button1 = Button(framehaut, activebackground='blue', background='purple',height=1 ,width = 1,command=gotopage3)
    button1.pack(side ='right')
    button1 = Button(framehaut, activebackground='blue', background='purple',height=1 ,width = 1,command=goback)
    button1.pack(side = "left")


    labelnom = Label(framecrit , text='Nom' )
    labelnom.place(rely=0.1 , relheight= 0.05 , relx = 0.05 , relwidth= 0.4)

    labelprenom = Label(framecrit, text='Prenom')
    labelprenom.place(rely=0.1 , relheight= 0.05 , relx = 0.55 , relwidth= 0.4)    

    entreeNom = Entry(framecrit, background='red')
    entreeNom.place(rely = 0.17 , relheight=0.05 , relwidth=0.4 , relx=0.05)
    entreeNom.bind('<FocusIn>', actualiserNom)
    entreeNom.bind('<Key>' , actualiserNom)

    entreePrenom = Entry(framecrit, background='blue')
    entreePrenom.place(rely = 0.17 , relheight=0.05 , relwidth=0.4 , relx=0.55)
    entreePrenom.bind('<FocusIn>', actualiserPrenom)
    entreePrenom.bind('<Key>' , actualiserPrenom)

    listeNom = Listbox(framecrit , bg='grey')
    listeNom.place(rely=0.3 , relheight= 0.3 , relx = 0.05 , relwidth= 0.4)

    listePrenom = Listbox(framecrit , bg='grey')
    listePrenom.place(rely=0.3 , relheight= 0.3 , relx = 0.55 , relwidth= 0.4)

    button1 = Button(framecrit, activebackground='blue', background='purple',height=1 ,width = 1,command=change)
    button1.place(rely = 0.8, relx=0.35, relheight= 0.05 , relwidth= 0.3)

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