#Importation des élements
import sqlite3
from graphviz import Digraph
from os import remove

#Créer un dot
dot = Digraph(comment = "Un simple dot", engine = 'circo')

#Relier Le python avec la base de donnée
conn = sqlite3.connect('user.db')



def afficher_graphe_perso(nom, prenom):
    """
        Objectif  :     Créer un dot Des liens d'une personne
        Variables : 
            nom     :   Le nom de la personne recherchée
            prenom  :   Le prenom de cette même personne
        
        Renvoie :
            Une affichage des liens de cette personne sous forme de dot
            Les liens auront 3 couleurs différentes 
    """
    dot = Digraph(comment = "Un simple dot", engine = 'circo')
    
    c = conn.cursor()
    requete = "SELECT * FROM Utilisateur WHERE Nom = '%s' And Prenom = '%s' "%(nom, prenom)
    User =  c.execute(requete).fetchall()[0]       #Fetchall() Permet d'avoir les résultat et [0][à] est la parti qui nous intérrese
    
    if User:
        dot.node(str(User[0]),str(User[1:]))

        Liste_Follow = []
        Liste_Follower = []
        Liste_Proche = []

        requete = "SELECT idFollowed FROM Follow WHERE IdFollower = %i"%User[0]
        for row in c.execute(requete):
            Liste_Follow.append(row[0])

        requete = "SELECT idFollower FROM Follow WHERE IdFollowed = %i"%User[0]
        for row in c.execute(requete):
            Liste_Follower.append(row[0])

        for i in Liste_Follow:
            if i in Liste_Follower:
                Liste_Proche.append(i)
                Liste_Follow.remove(i)
                Liste_Follower.remove(i)

        for i in range(len(Liste_Follow)) : 
            Liste_Follow[i]=c.execute("SELECT * FROM Utilisateur WHERE IdUser = %i "%Liste_Follow[i]).fetchall()
            dot.node(str(Liste_Follow[i][0][0]),str(Liste_Follow[i][0][1:]))
            dot.edge(str(User[0]),str(Liste_Follow[i][0][0]), color = 'red')

        for i in range(len(Liste_Follower)) : 
            Liste_Follower[i]=c.execute("SELECT * FROM Utilisateur WHERE IdUser = %i "%Liste_Follower[i]).fetchall()
            dot.node(str(Liste_Follower[i][0][0]),str(Liste_Follower[i][0][1:]))
            dot.edge(str(Liste_Follower[i][0][0]),str(User[0]), color = 'blue')

        for i in range(len(Liste_Proche)) : 
            Liste_Proche[i]=c.execute("SELECT * FROM Utilisateur WHERE IdUser = %i "%Liste_Proche[i]).fetchall()
            dot.node(str(Liste_Proche[i][0][0]),str(Liste_Proche[i][0][1:]))
            dot.edge(str(Liste_Proche[i][0][0]),str(User[0]), color = 'orange')
            dot.edge(str(User[0]),str(Liste_Proche[i][0]), color = 'orange')
        dot.format="png"
        dot.render("Images/Result",view=False,cleanup=False)
        
    else:
        return 0
        
    
def recherche(Entree,categorie,secondecate,secondeentree):
    """
    Objectif effectuer une requete Sql Dans tout type de situation et renvoyer une liste des résultats

    Args:
        Entree (str): Entree principale de la requete SQL
        categorie (str): La categorie de la Première entree( Nom/ Prenom)
        secondecate (str): Facultatif ==> Permet d'avoir une deuxième catégorie àa chercher et faire une requete imbriquer
        secondeentree (str): Aussi Facultatif si la deuxième catégorie != None ==> La valeur de la deuxieme catégorie de rechercher

    Returns:
        Liste_possible(type : liste): La liste de tout les résultats de la requète SQL
    """
    c = conn.cursor()
    Liste_possible = []

    if secondecate !='':
        #Verifie si l'on doit faire une requete imbriquer ou une simple
        requete = "SELECT DISTINCT "+categorie+" FROM Utilisateur WHERE "+categorie+" LIKE '"+Entree+"%' AND "+secondecate+" LIKE '"+secondeentree+"%'"
    else:
        requete = "SELECT DISTINCT "+categorie+" FROM Utilisateur WHERE "+categorie+" LIKE '"+Entree+"%'"
    
    #Ajout des résultat sous une meilleure forme dans la liste que l'on renvoie

    for row in c.execute(requete):
        Liste_possible.append(row[0])
    
    return Liste_possible




