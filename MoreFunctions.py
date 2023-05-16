from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image

def loading(frame , callback):
    """
    Objectif :
        Afficher une Barre de chargement sur une frame
        Faire en sorte que l'on envoie un signal quand chargée

    Args:
        frame (tk.Frame()): Une frame d'un fenetre qui sera dans main
        callback (function): Cet argument permet aux fichier principal de savoir si c'est finis ou non
    """
    style = ttk.Style()
    style.theme_use('default')
    style.configure("Custom.Horizontal.TProgressbar", thickness=20, troughcolor='#4f4f4f', background='#ffa500', darkcolor='#ffa500', lightcolor='#ffa500')

    frameLogo = Frame(frame, bg= 'red')
    frameLogo.place(relheight = 0.3 , relx = 0.4 , rely = 0.3 , relwidth = 0.2)

    img = Image.open('Images/Kai (2).gif')
    

    photo_img = ImageTk.PhotoImage(img)
    imgFrame = Label(frameLogo, image=photo_img)
    imgFrame.pack()

    labelTitre = Label(frame, bg= 'red')
    labelTitre.place(relheight = 0.05 , relx = 0.4 , rely = 0.2 , relwidth = 0.2)


    Progress_Bar = ttk.Progressbar(frame,length=300 , orient='horizontal' , mode='determinate', style ="Custom.Horizontal.TProgressbar")

    def Slide():
        """
            Slide permet de faire progresser la barre en 10 seconde gràce à la librairie time
            Puis d'envoyer le signal à main que c'est finis
        """
        from time import sleep

        for i in range(6):
            Progress_Bar['value']+=100/5
            #Met instantanément à jour la frame
            frame.update_idletasks()
            sleep(1)

        #CallBack est appelé et corespond à une fonction dans main qui permet d'executer la suite sans import
        #Le fait de mettre callback la fonction en paramètre permt d'éviter les imports à tous va
        callback()    

    #Affichage de la barre de Chargement sur la frame
    Progress_Bar.place(relheight=0.05 , relwidth=0.5 , rely=0.8 , relx=0.25)

    #Relie la barre à un event
    #L'orsque que la barra s'affiche  ("<Expose>" == Quand ça apparait) la fonction Slide est lancéé
    Progress_Bar.bind("<Expose>",lambda event: Slide())


def delete_frame(frame):
    """
    Sert à vider une frame totalement et sera appelé par des autres fonction (gotopage())
    
    Args:
        frame (frame): frame que l'on souhaite vider de ses éléments
    """
    for widget in frame.winfo_children():
        widget.destroy() 

