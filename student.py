import sqlite3

# Create database if not exist and get a connection to it

connection = sqlite3.connect('storage/database/student.db')  # .db represent the extension

# Get a cursor to execute sql statements

cursor = connection.cursor()

# -------------- !!!!Create tables:  c'est déja fait sur sqlite, juste pour connaitre qu'on peut les créer directement ici ---------------

# Auteur
# sql = '''CREATE TABLE IF NOT EXISTS Auteur
#                (Nauteur INTEGER, nomA VARCHAR(20), prenomA VARCHAR(20), nationaliteA VARCHAR(30),
#                 PRIMARY KEY(Nauteur))'''
# cursor.execute(sql)

# Livre

# sql = '''CREATE TABLE IF NOT EXISTS Livre
#                (Nlivre INTEGER, num_ISBN INTEGER, titre VARCHAR(25), nbPages INTEGER, anneeS DATE, prix FLOAT,
#                 PRIMARY KEY(Nlivre))'''
# cursor.execute(sql)

# Possede

# sql = '''CREATE TABLE IF NOT EXISTS Possede
#                (Nlivre INTEGER, Nauteur INTEGER, PRIMARY KEY(Nlivre, Nauteur),
#                FOREIGN KEY(Nlivre) REFERENCES Livre(Nlivre),
#                 FOREIGN KEY(NAuteur) REFERENCES Auteur(NAuteur))'''
# cursor.execute(sql)

# Pret

# sql = '''CREATE TABLE IF NOT EXISTS Pret
#                (Npret INTEGER, num_etu INTEGER, Nlivre INTEGER, datePret DATE, dateRetour DATE,
#                 DateRetourPrevue DATE, PRIMARY KEY(Npret), FOREIGN KEY(num_etu) REFERENCES Etudiant(num_etu),
#                 FOREIGN KEY(Nlivre) REFERENCES Livre(Nlivre))'''
# cursor.execute(sql)

# Etudiant

# sql = '''CREATE TABLE IF NOT EXISTS Etudiant
#                (num_etu INTEGER, nomE VARCHAR(20), prenomE VARCHAR(20), date_naissance DATE,
#                 ville VARCHAR(25), dateInscripBU DATE, dateAbs DATE, num_class INTEGER , PRIMARY KEY(num_etu),
#                 FOREIGN KEY(numClass) REFERENCES Class(numClass))'''
# cursor.execute(sql)

# Class

# sql = '''CREATE TABLE IF NOT EXISTS Class
#               (numClass INTEGER, nomClass VARCHAR(20), PRIMARY KEY(numClass))'''
# cursor.execute(sql)

# Cours

# sql = '''CREATE TABLE IF NOT EXISTS Cours
#               (num_cours INTEGER, nomC VARCHAR(25), nb_heures INTEGER, num_ens INTEGER, PRIMARY KEY(num_cours),
#               FOREIGN KEY(num_ens) REFERENCES Enseignant(num_ens))'''
# cursor.execute(sql)

# Enseignant

# sql = '''CREATE TABLE IF NOT EXISTS Enseignant
#               (num_ens INTEGER, nomP VARCHAR(20), prenomP VARCHAR(20), specialite VARCHAR(30), departement VARCHAR(30),
#               PRIMARY KEY(num_ens))'''
# cursor.execute(sql)

# Resultat

# sql = '''CREATE TABLE IF NOT EXISTS Resultat
#               (num_etu INTEGER, num_cours INTEGER,  note FLOAT, PRIMARY KEY(num_etu,num_cours),
#                FOREIGN KEY(num_etu) REFERENCES Etudiant(num_etu),
#                FOREIGN KEY(num_cours) REFERENCES Cours(num_cours))'''
# cursor.execute(sql)


# Charge

# sql = '''CREATE TABLE IF NOT EXISTS Charge
#               (num_ens INTEGER, num_cours INTEGER,  nbH TIME, PRIMARY KEY(num_ens,num_cours),
#               FOREIGN KEY(num_ens) REFERENCES Enseignant(num_etu),
#               FOREIGN KEY(num_cours) REFERENCES Cours(num_cours))'''
# cursor.execute(sql)

# Inscrit

# sql = '''CREATE TABLE IF NOT EXISTS Inscrit
#               (num_etu INTEGER, num_cours INTEGER,  dateInsC DATE, PRIMARY KEY(num_etu,num_cours),
#               FOREIGN KEY(num_etu) REFERENCES Etudiant(num_etu),
#               FOREIGN KEY(num_cours) REFERENCES Cours(num_cours))'''
# cursor.execute(sql)


# -----------------------------------------------------------------------------------------------------------------------

# insert data into table

# sql = "INSERT INTO Auteur (Nauteur, nomA, prenomA, nationaliteA) VALUES (300, 'SOW', 'Joj', 'Canada')"
# cursor.execute(sql)

# sql = "INSERT INTO Enseignant (num_ens, nomP, prenomP, specialite, departement) VALUES (11, 'Ouassou', 'Idir', 'Algebre','Math')"
# cursor.execute(sql)


# Persist data in file test.db
connection.commit()  # to commit any change to our db /!\ not cursor.commit()

# close the connection

connection.close()

# %%%%%%%%%%%%%%%%%%%%%%% Our Functions %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# 1

def insBU(etud_name):
    query = "SELECT dateInscripBU FROM Etudiant WHERE nomE=?;"  # the request: select dateIns

    connect = sqlite3.connect('storage/database/student.db') #connect to data
    curs1 = connect.cursor() #our cursor
    curs1.execute(query, [etud_name]) #execution with etu_name as parameter
    results = curs1.fetchall() #get all results of the request
    curs1.close()
    connect.close()

    if not results: #Error message
        return 'Error ' + 'Could not find any etudiant with name: ' + str(etud_name)
        # return None
    else:
        return results[0][0] #return the first results


# TESTING :

print('-----------------------------------------------------------1------------------------------------------\n')
print("Date d'inscription de l'étudiant 'BACHAR' :", insBU('Bachar'))
print("Date d'inscription de l'étudiant 'DAHBI' :", insBU('Dahbi'))
print("Date d'inscription de l'étudiant 'ANFAR' :", insBU('Anfar'))


# 2

def insCour(numcours):
    connt = sqlite3.connect('storage/database/student.db')
    curs2 = connt.cursor()
    sql2 = "SELECT nomE, prenomE FROM Etudiant INNER JOIN Inscrit ON Inscrit.num_etu=Etudiant.num_etu INNER JOIN Cours ON Cours.num_cours=Inscrit.num_cours WHERE Cours.num_cours=?;"

    curs2.execute(sql2, [numcours])

    all_rows = curs2.fetchall()
    curs2.close()
    connt.close()

    if not all_rows:
        return " !  Il n'y a pas d'étudaint inscrit dans le cours N° : " + str(numcours)
    else:
        return all_rows


#   TESTING:

print("-----------------------------------------2---------------------------------------------\n")

print("Les noms des étudiants inscrit dans le cours n° 7 :", insCour(7))
print("Les noms des étudiants inscrit dans le cours n° 13 :", insCour(18))
print("Les noms des étudiants inscrit dans le cours n° 9:", insCour(9))




# 3

def ResuEtu(numetu,numcr):
    connnt = sqlite3.connect('storage/database/student.db')
    curs3 = connnt.cursor()
    sql3 = '''
        SELECT nomC, AVG(note), MAX(note), MIN(note)
        FROM Etudiant
        INNER JOIN Resultat ON Resultat.num_etu = Etudiant.num_etu
        INNER JOIN Cours ON Cours.num_cours = Resultat.num_cours
        WHERE Cours.num_cours = ?'''
    #request  with the inner join between Resultat , Etu & Cours Tables

    curs3.execute(sql3, [numcr])
    all_rows = curs3.fetchall()

    curs33 = connnt.cursor()      # Requete Pour la moyenne général de l'etu
    sql33 = ''' SELECT nomE, prenomE, AVG(note) FROM Etudiant  
                INNER JOIN Resultat ON Resultat.num_etu=Etudiant.num_etu
                WHERE Etudiant.num_etu = ?
                                       '''
    curs33.execute(sql33, [numetu])
    moy = curs33.fetchall()

    curs333 = connnt.cursor()
    sql333 = '''SELECT note FROM Resultat
                INNER JOIN Etudiant ON Resultat.num_etu = Etudiant.num_etu
                INNER JOIN Cours ON Cours.num_cours = Resultat.num_cours
                WHERE Cours.num_cours = ? AND Etudiant.num_etu = ?
    '''
    curs333.execute(sql333, [numcr, numetu])
    Note = curs333.fetchone()
    connnt.commit()
    curs3.close()
    curs33.close()
    curs333.close()
    connnt.close()

    return ("Nom complet d'etu  :" + str(moy[0][0]) + ' ' + str(moy[0][1])  #JUST TO SIMPLIFY THE PRINT
            + '\n' 'Nom Module : ' + str(all_rows[0][0])
            + '\n' 'Note : ' + str(Note[0])
            + '\n' 'Note Moyenne dans le module : ' + str(all_rows[0][1])
            + '\n' 'Note supérieure  : ' + str(all_rows[0][2]) + '\n' 'Note inférieure : ' + str(all_rows[0][3])

            + '\n' "Moyenne Général d'etu : " + str(moy[0][2]))
#TESTING :
print('---------------------------------------3------------------------------------------------\n')
print(ResuEtu(5, 5))
print('-------------------------------------------')
print(ResuEtu(10, 1))
print('-------------------------------------------')
print(ResuEtu(52, 3))

print('-------------------------------------------')
print(ResuEtu(13, 7))




# 4 : la liste des étudiants (nom, prenom, note ; la moyene d classe) ayant une note inferieur à 10 et groupés par nom module

def resultEchec():
    conn = sqlite3.connect('storage/database/student.db')
    curs4 = conn.cursor()
    sql4 = '''
           SELECT nomE,prenomE,note, nomC
           FROM Etudiant
           INNER JOIN Resultat ON Resultat.num_etu=Etudiant.num_etu
           INNER JOIN Cours ON Cours.num_cours=Resultat.num_cours
           WHERE Resultat.note < 10 GROUP BY nomC
           
       '''
    curs4.execute(sql4)
    data = curs4.fetchall()
    conn.commit() #Applay changes
    conn.close()
    #return data
    for row in data:
        print(row)
    return 'Selected Successfully !'
#TESTING :
print('----------------------------------4--------------------------------\n')
print("Les étudiants ayant une note inferieur à 10 et groupés par nom module :")
print(resultEchec())

#5 list of students inscrit in every cours
def insr():
    connnn = sqlite3.connect('storage/database/student.db')
    curs5 = connnn.cursor()
    sql5 = '''
               SELECT DISTINCT nomE, prenomE
               FROM Etudiant
               INNER JOIN Inscrit ON Etudiant.num_etu=Inscrit.num_etu 
               INNER JOIN Cours ON Cours.num_cours=Inscrit.num_cours
               WHERE NOT EXISTS( SELECT * FROM Cours
               WHERE NOT EXISTS( SELECT * FROM Inscrit))

           '''
    curs5.execute(sql5)
    all_rows = curs5.fetchall()
    connnn.commit()
    connnn.close()
    #return all_rows
    for row in all_rows:
        print(row)
    return 'Selected Successfully !'
#TESTING :
print("----------------------------------------5-----------------------------------------------")
print("les noms des étudiants inscrits dans tous les modules :")
print(insr())

#6
def empLiv(nlivre):
    connnect = sqlite3.connect('storage/database/student.db')
    curs6 = connnect.cursor()
    query = "SELECT nomE, dateRetour FROM Etudiant INNER JOIN Pret ON Pret.num_etu=Etudiant.num_etu INNER JOIN Livre ON Livre.Nlivre=Pret.Nlivre WHERE Livre.Nlivre=?;"
    curs6.execute(query, [nlivre])
    results = curs6.fetchall()
    curs6.close()
    connnect.close()
    if not results:
        return 'Error ' + 'Could not find any etudiant emprunt the book N°: ' + str(nlivre)
    # return None
    else:
         return ("les Noms des étudiants avec date retour , qui ont empruntés le livre pour code Nlivre ={} sont:".format(nlivre) + '\n' + str(results))

# TESTING :
print('--------------------------------------------6-------------------------------------------------------------------------\n')
print(empLiv(7))
print('-------------------------------------------------------------------------------------------------')
print(empLiv(5))
print('--------------------------------------------------------------------------------------------------')
print(empLiv(10))



#7

def retard():
    connt = sqlite3.connect('storage/database/student.db')
    curs7 = connt.cursor()
    seven = '''SELECT nomE, prenomE FROM Etudiant 
               INNER JOIN Pret ON Pret.num_etu=Etudiant.num_etu
               INNER JOIN Livre ON Livre.Nlivre=Pret.Nlivre
               WHERE Livre.Nlivre = (SELECT Nlivre FROM Pret WHERE( SELECT date("now") >= DateRetourPrevue))'''

    curs7.execute(seven)

    heislate = curs7.fetchall()

    curs7.close()
    connt.close()

    if not heislate:
        return "Il n y a pas de livre retourner en retard"
    else:
        return heislate
#test
print('------------------------------------------------7-----------------------------------------------------------------\n')
print("Les étudiants n'ayant pas encore rendus au moins un livre sont :  ",retard())

#8
def noEmp():
    con8 = sqlite3.connect('storage/database/student.db')
    curs8 = con8.cursor()
    eight = " SELECT  titre FROM Livre WHERE NOT exists (SELECT * FROM Pret WHERE Pret.Nlivre = Livre.Nlivre);"
    curs8.execute(eight)
    noemprunt = [item[0] for item in curs8.fetchall()] #Pour changer l'affichage un petit peu
    curs8.close()
    con8.close()
    if not noemprunt:
        return "Tout les livre ont déjà ete emprunter"
    else:
        for row in noemprunt:
            print(row)
    return 'Selected Successfully !'

#Test :
print('-------------------------------------------------8----------------------------------------------------\n')
print('les livres qui ne sont pas encore empruntés :')
print(noEmp())

#9
def ResultTot():
    con9 = sqlite3.connect('storage/database/student.db')
    curs9 = con9.cursor()
    sql9 = '''SELECT nomClass, nomC,  AVG(note) 
              FROM Class
              INNER JOIN Etudiant ON Etudiant.numClass = Class.numClass
              INNER JOIN Resultat ON Resultat.num_etu = Etudiant.num_etu
              INNER JOIN Cours ON Cours.num_cours = Resultat.num_cours
              GROUP BY nomClass,nomC   
    '''
    curs9.execute(sql9)
    results = curs9.fetchall()
    return results

# TEST :
print('------------------------------------------------------9----------------------------------------------------\n')
print(ResultTot())



############################Fonctions To moodificate Tables !===!!!!!!!!!

# 1 : To add new Student
def add_etudiant(database_file, new_etud):
    connectio = sqlite3.connect(database_file)
    cur = connectio.cursor()
    query = "INSERT INTO Etudiant (num_etu, nomE, prenomE, date_naissance, ville, dateInscripBU, dateAbs, numClass, email) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);"
    cur.execute(query, list(new_etud))
    cur.close()
    connectio.commit()
    connectio.close()
    print('One Student added !')

# Change the name of cours :
def changeCoursname(nvname, numcours):
    con = sqlite3.connect('storage/database/student.db')
    curs = con.cursor()
    sql = '''UPDATE Cours
             SET nomC = ?
            WHERE num_cours = ?'''
    curs.execute(sql, [nvname, numcours])
    curs.close()
    con.commit()
    con.close()
    return "Name Changed Successfully !"


#Testing :
print('----------------------------------------------10---------------------------------------------------\n')

print(changeCoursname('Base de données', 9))


#3 Delete Cours
def deletCours(numcour):
    con2 = sqlite3.connect('storage/database/student.db')
    cur2 = con2.cursor()
    sql2 = '''DELETE FROM Cours
              WHERE num_cours = ?'''
    cur2.execute(sql2, [numcour])
    records = cur2.fetchall()
    con2.commit()
    try:
        if not records:
                return "\nRecord Deleted successfully "

    except sqlite3.Error as e:
        print("Failed to delete record from table: {}".format(e))

    cur2.close()
    con2.close()

 # TEST :
print('------------------------------------------------11-----------------------------------------------------------\n')
print(deletCours(9))
