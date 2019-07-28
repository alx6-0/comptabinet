#! /usr/bin/python
# -*- coding:-utf8 -*-
import sqlite3
from sqlite3.dbapi2 import Cursor
import os
import csv

#les Patients
def nouveau(laLigne):
    leCurseur.execute(
        "INSERT INTO Patients(patientID, titre, prenom, nom, telephone, cellulaire, email, adresse1, adresse2, adresse3, notes) values(?,?,?,?,?,?,?,?,?,?,?)",laLigne)
    laConnex.commit()

def change(laLigne):
    liste = []
    i = 1
    while i < len(laLigne):
        liste.append(laLigne[i])
        i+=1
    liste.append(laLigne[0])
    leCurseur.execute(
        "UPDATE Patients set titre = ?, prenom = ?, nom = ?, telephone = ?, cellulaire = ?, email = ?, adresse1 = ?, adresse2 = ?, adresse3 = ?, notes = ? WHERE patientID = ?",liste)
    laConnex.commit()

def chercheNom(lePatient):
    temp = ("%" + lePatient + "%", "%" + lePatient + "%",)
    leCurseur.execute("Select patientID, nom, prenom FROM Patients WHERE prenom like ? OR nom like ?", ("%" + lePatient + "%", "%" + lePatient + "%",))
    return (leCurseur.fetchall())

def lePatient(numPatient):
    leCurseur.execute("Select * FROM Patients WHERE patientID like ?",(numPatient,))
    return (leCurseur.fetchone())

def leComptePatients():
    leCurseur.execute("SELECT COUNT(*) FROM Patients;")
    return leCurseur.fetchone()

#leJournal
def ajouter(lEntree):
    lEntreeMod = []
    lEntreeMod.append(leCompteJournal()[0])
    i = 0
    while i < len(lEntree):
        lEntreeMod.append(lEntree[i])
        i += 1
    leCurseur.execute(
        "INSERT INTO Journal (LigneID, patientID, PatientNom, laDate, soin, commentaireSoin, prix, creance, paiement, commentaire) values(?,?,?,?,?,?,?,?,?,?)",lEntreeMod)
    laConnex.commit()

def modifierLibelle(ligneID, nouvLibelle,nouvComment):
    leCurseur.execute("UPDATE Journal set commentaire = ?, commentaireSoin = ? WHERE LigneID = ?",(nouvLibelle,nouvComment,ligneID))
    laConnex.commit()

def lesEntrees(numPatient):
    leCurseur.execute("Select LigneID, laDate, soin, commentaireSoin, prix, creance, paiement, commentaire FROM Journal WHERE patientID like ? ORDER BY laDate DESC LIMIT 5", (numPatient,))
    return (leCurseur.fetchall())

def totalCreance(numPatient):
    leCurseur.execute("Select SUM(creance) FROM Journal WHERE patientID like ?",(numPatient,))
    return (leCurseur.fetchone())

def leCompteJournal():
    leCurseur.execute("SELECT COUNT(*) FROM Journal;")
    return (leCurseur.fetchone())

#lesSoins
def lesSoins():
    leCurseur.execute("Select soinMenu FROM Soins ORDER BY soinMenu ASC")
    return (leCurseur.fetchall())

def detailSoin(leSoin):
    leCurseur.execute("Select soinImprime, prix, commentaire FROM Soins WHERE soinMenu like ?",(leSoin,))
    return (leCurseur.fetchone())

def ajouterSoin(laLigne):
    leCurseur.execute(
        "INSERT INTO Soins(soinMenu, soinImprime, prix) values(?,?,?)",laLigne)
    laConnex.commit()

def supprimerSoin(leSoin):
    leCurseur.execute("DELETE FROM Soins WHERE soinMenu like ?", (leSoin,))
    laConnex.commit()

def modifierSoin(laLigne):
    leCurseur.execute("UPDATE Soins SET soinMenu = ?, soinImprime = ?, prix = ? WHERE soinMenu like ?", (laLigne))


def ferme():
    laConnex.commit()
    laConnex.close()


def exporterCompta(debut, fin):
    leCurseur.execute(
        "Select DATE(laDate), PatientNom, soin, prix, creance, paiement, commentaire FROM Journal WHERE laDate > ? AND laDate < ? ORDER BY laDate ASC",
        (debut,fin))
    titres = [("date", "nom Patient", "Type Soin", "Montant Payé", "Montant Dû", "Mode Paiement", "Libellé")]
    csvData = titres + leCurseur.fetchall()
    with open(os.path.join(os.path.dirname(__file__),'export' + debut + " - " + fin + '.csv'), 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(csvData)
        csvFile.close()


lechemin = os.path.join(os.path.dirname(__file__),'BDD.sqlite')
laConnex = sqlite3.connect(lechemin)
leCurseur = laConnex.cursor()

leCurseur.execute(
    """CREATE TABLE if not exists Patients (patientID int PRIMARY KEY, titre text, prenom text, 
nom text, telephone text, cellulaire text, email text, adresse1 text, adresse2 text, adresse3 text, notes text)""")
if leComptePatients()[0] == 0:
    nouveau((1,"M. / Mme","Générique","Patient","--","--","--","--","--","--","--"))

leCurseur.execute(
    """CREATE TABLE if not exists Journal (LigneID int PRIMARY KEY, patientID int, PatientNom text, 
laDate datetime, soin text, commentaireSoin text, prix smallmoney, creance smallmoney, paiement text, commentaire text)""")

leCurseur.execute(
    """CREATE TABLE if not exists Soins (soinMenu text PRIMARY KEY, soinImprime text, prix smallmoney, commentaire text)""")
if len(lesSoins()) == 0:
    leCurseur.execute("""INSERT INTO Soins(soinMenu, soinImprime, prix) values(?,?,?)""",('Semelles','Semelles de confort', 150))
    laConnex.commit()

leCurseur.execute("Select * FROM Patients WHERE prenom like '%And%' OR patientID like '%4%'")
lesLignes = leCurseur.fetchall()

