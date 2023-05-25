#Importation des élements
import sqlite3
from graphviz import Digraph

#Créer un Graphe
dot = Digraph(comment = "Un simple graphe", engine = 'circo')

#Relier Le python avec la base de donnée
conn = sqlite3.connect('user.db')


def afficher_graphe_perso(graphe, db, nom, prenom):
    """
        Objectif  :     Créer un graphe Des liens d'une personne
        Variables : 
            graphe  :   Le graphe sur lequel on va travailler
            db      :   La Base de données des Utilisateurs et Liens
            nom     :   Le nom de la personne recherchée
            prenom  :   Le prenom de cette même personne
        
        Renvoie :
            Une affichage des liens de cette personne sous forme de graphe
            Les liens auront 3 couleurs différentes 
    """
    c = db.cursor()
    requete = "SELECT * FROM Utilisateur WHERE Nom = '%s' And Prenom = '%s' "%(nom, prenom)
    User =  c.execute(requete).fetchall()[0]       #Fetchall() Permet d'avoir les résultat et [0][à] est la parti qui nous intérrese

    graphe.node(str(User[0]),str(User[1:]))

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
        graphe.node(str(Liste_Follow[i][0][0]),str(Liste_Follow[i][0][1:]))
        graphe.edge(str(User[0]),str(Liste_Follow[i][0][0]), color = 'red')

    for i in range(len(Liste_Follower)) : 
        Liste_Follower[i]=c.execute("SELECT * FROM Utilisateur WHERE IdUser = %i "%Liste_Follower[i]).fetchall()
        graphe.node(str(Liste_Follower[i][0][0]),str(Liste_Follower[i][0][1:]))
        graphe.edge(str(Liste_Follower[i][0][0]),str(User[0]), color = 'blue')

    for i in range(len(Liste_Proche)) : 
        Liste_Proche[i]=c.execute("SELECT * FROM Utilisateur WHERE IdUser = %i "%Liste_Proche[i]).fetchall()
        graphe.node(str(Liste_Proche[i][0][0]),str(Liste_Proche[i][0][1:]))
        graphe.edge(str(Liste_Proche[i][0][0]),str(User[0]), color = 'orange')
        graphe.edge(str(User[0]),str(Liste_Proche[i][0]), color = 'orange')

    print(Liste_Follow)

    
    
def recherche(Entree,categorie,secondecate,secondeentree):
    c = conn.cursor()

    mot = ''
    for i in Entree :
        mot+=i
    
    Liste_possible = []
    if secondecate:
        requete = "SELECT DISTINCT "+categorie+" FROM Utilisateur WHERE "+categorie+" LIKE '"+mot+"%' AND "+secondecate+" LIKE '"+secondeentree+"'%"
    else:
        requete = "SELECT DISTINCT "+categorie+" FROM Utilisateur WHERE "+categorie+" LIKE '"+mot+"%'"

    for row in c.execute(requete):
        Liste_possible.append(row[0])

    return Liste_possible


 