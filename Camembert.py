import matplotlib.pyplot as plt  # Importer le module
import sqlite3 as sql  # Importer sqlite3
connection = sql.connect('C:/sqlite/student.db') # connexion avec la base
cursor = connection.cursor()
connection.commit() # Sauvgarder les modéfications

# !!!!! Pour etre simple on a sélectionner chaque catg seule !!!!:
cat1 = '''SELECT COUNT(nomE) FROM Etudiant
           INNER JOIN Resultat ON Resultat.num_etu = Etudiant.num_etu
           WHERE note >= 14'''
cursor.execute(cat1)
res1 = cursor.fetchone()
nb1 = res1[0]  # get the first result of the request

 #######The same for the others:##################
cat2 = '''SELECT COUNT(nomE) FROM Etudiant
           INNER JOIN Resultat ON Resultat.num_etu = Etudiant.num_etu
           WHERE note < 8'''
cursor.execute(cat2)
res2 = cursor.fetchone()
nb2 = res2[0]

cat3 = '''SELECT COUNT(nomE) FROM Etudiant
           INNER JOIN Resultat ON Resultat.num_etu = Etudiant.num_etu
           WHERE note < 10 AND note >= 8 '''
cursor.execute(cat3)
res3 = cursor.fetchone()
nb3 = res3[0]

cat4 = '''SELECT COUNT(nomE) FROM Etudiant
           INNER JOIN Resultat ON Resultat.num_etu = Etudiant.num_etu
           WHERE note < 14 AND note >= 12 '''
cursor.execute(cat4)
res4 = cursor.fetchone()
nb4 = res4[0]

cat5 = '''SELECT COUNT(nomE) FROM Etudiant
           INNER JOIN Resultat ON Resultat.num_etu = Etudiant.num_etu
           WHERE note < 12 AND note >= 10 '''
cursor.execute(cat5)
res5 = cursor.fetchone()
nb5 = res5[0]

cursor.close()
connection.close()

plt.title(" Nb d'étudiants par catégorie de notes ")  # Le titre de notre Camembert
explode = (0.1, 0, 0, 0, 0)
# donner des titres à chaque catégorie
labels = 'nb eleve note>=14','nb eleve note<8','nb eleve 8<=note<10','nb eleve 12<=note<14','nb eleve 10<=note<12',
x = [nb1, nb2, nb3, nb4, nb5]  #stocker les diff résultas dans la liste x
plt.pie(x,explode=explode, labels=labels, autopct='%1.1f%%', shadow=True)  # Appliquer la fct pie au objet plt
plt.show()  # Afficher le résultat (Camebert)