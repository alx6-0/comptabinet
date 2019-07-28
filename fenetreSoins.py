#! /usr/bin/python
# -*- coding:-utf8 -*-
import tkinter as tk
from tkinter import scrolledtext
import lesDonnees

def listbox_update():
    extrait = lesDonnees.lesSoins()
    # delete previous data
    laListe.delete(0, 'end')
    leSoinCourt.delete(0, leSoinCourt.index("end"))
    for laLigne in extrait:
        laListe.insert('end',str(laLigne[0]))

def on_select(event):
    temp = event.widget.curselection()
    if temp:
        affiche(laListe.get(temp[0]))
        laListe.selection_clear(("active"))

def setLabel(leLabel, leTexte):
    leLabel.delete(0, leLabel.index("end"))
    leLabel.insert(0, leTexte)

def ajouter():
    lesDonnees.ajouterSoin(("nouveau","Texte imprimé", 150))
    listbox_update()
    affiche("nouveau")

def supprimer():
    lesDonnees.supprimerSoin(leSoinCourt.get())
    listbox_update()

def modifier():
    if len(leSoinInit.get()):
        temp=(leSoinCourt.get(),leSoinLong.get(),leSoinPrix.get(),leSoinInit.get())
        lesDonnees.modifierSoin(temp)
        listbox_update()
        affiche(temp[0])

def affiche(unSoin):
    leSoinInit.set(unSoin)
    setLabel(leSoinCourt, unSoin)
    setLabel(leSoinPrix, (lesDonnees.detailSoin(unSoin)[1]))
    setLabel(leSoinLong, (lesDonnees.detailSoin(unSoin)[0]))

def ferme():
    try:
        fenetreSoins.destroy()
    except:
        fenetreSoins=None

def initialisation():
    global fenetreSoins
    global leSoinCourt
    global leSoinInit
    global leSoinLong
    global leSoinPrix
    global laListe



    #leSoinDropDown.destroy()

    ferme()

    fenetreSoins = tk.Tk()
    fenetreSoins.title("liste des Soins")

    laListe= tk.Listbox(fenetreSoins, width=30, height=21)
    laListe.grid(rowspan=15, row=0, column=0, padx=15, pady=0)
    laListe.bind('<Double-Button-1>', on_select) #double click
    laListe.bind('<<ListboxSelect>>', on_select) #simple cick

    leSoinInit=tk.StringVar(fenetreSoins)
    leSoinInit.set("Aucun soin sélectionné")
    tk.Label(fenetreSoins, textvariable=leSoinInit).grid(row=0, column=2)

    tk.Label(fenetreSoins, text="Titre du Soin").grid(row=1, column=1)
    leSoinCourt=tk.Entry(fenetreSoins)
    leSoinCourt.grid(row=1, column=2)
    leSoinCourt.config(width=15)

    tk.Label(fenetreSoins, text="Prix du Soin").grid(row=1, column=3)
    leSoinPrix=tk.Entry(fenetreSoins)
    leSoinPrix.grid(row=1, column=4)
    leSoinPrix.config(width=10)

    tk.Label(fenetreSoins, text="Texte long").grid(row=2, column=1)
    leSoinLong = tk.Entry(fenetreSoins)
    leSoinLong.grid(columnspan=3, row=2, column=2)
    leSoinLong.config(width=35)

    tk.Label(fenetreSoins, text="Aucun soin ne doit avoir le même nom").grid(columnspan=4, row=4, column=1)
    tk.Label(fenetreSoins, text="changements pris en compte au prochain lancement").grid(columnspan=4, row=5, column=1)

    ajoute =tk.Button(fenetreSoins, text=" Nouveau ", command=ajouter).grid(row=16, column=1)
    supprime = tk.Button(fenetreSoins, text="Supprimer", command=supprimer).grid(row=16, column=2)
    modifie = tk.Button(fenetreSoins, text="Enregistrer", command=modifier).grid(row=16, column=4)

    listbox_update()
