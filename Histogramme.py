from matplotlib import pyplot as plt
import sqlite3

connection = sqlite3.connect('storage/database/student.db')
cursor = connection.cursor()

# we select all notes from Resultat table:
note = "SELECT note From Resultat INNER JOIN Etudiant ON Etudiant.num_etu=Resultat.num_etu GROUP BY note "
cursor.execute(note)
y = [item[0] for item in cursor.fetchall()]  #to change the result to a list

#We select nbr of students by notes:
nbEtu = "SELECT COUNT(E.num_etu) FROM Etudiant AS E INNER JOIN Resultat ON Resultat.num_etu = E.num_etu GROUP BY note"
cursor.execute(nbEtu)
x = [item[0] for item in cursor.fetchall()] #to change the result to a list

plt.xlabel("Note")
plt.ylabel("Nombre d'Etu")
plt.bar(y, x, 0.07)
plt.show()

