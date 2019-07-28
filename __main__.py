#! /usr/bin/python
# -*- coding:-utf8 -*-

import tkinter as tk
from tkinter import scrolledtext
from tkinter import simpledialog
import datetime as dt
import os

import lesDonnees
import fenetreSoins

def suivant():
    if int(laFiche.get()) == int(lesDonnees.leComptePatients()[0]):
        setVars(lesDonnees.lePatient(1))
    else:
        setVars(lesDonnees.lePatient(int(laFiche.get())+1))

def precedent():
    if int(laFiche.get()) == 1:
        setVars(lesDonnees.lePatient(int(lesDonnees.leComptePatients()[0])))
    else:
        setVars(lesDonnees.lePatient(int(laFiche.get()) - 1))

def annuler():
    if int(laFiche.get()) > int(lesDonnees.leComptePatients()[0]):
        setVars(lesDonnees.lePatient(int(lesDonnees.leComptePatients()[0])))
    else:
        setVars(lesDonnees.lePatient(int(laFiche.get())))

def nouveau():
    temp = (lesDonnees.leComptePatients()[0]) + 1
    lesVars = (temp, "M. / mme", "Nouveau", "Patient", "", "", "", "", "", "", "")
    setVars(lesVars)

def enregistrer():
    if int(laFiche.get()) > int(lesDonnees.leComptePatients()[0]):
        lesDonnees.nouveau(getVars())
    else:
        lesDonnees.change(getVars())
    setVars(lesDonnees.lePatient(int(laFiche.get())))
    listbox_update(entry.get())

def getVars():
    lesVars = (laFiche.get(), leTitre.get(), lePreNom.get(), leNom.get(), telephone.get(), cellulaire.get(), email.get(), adresse1.get(), adresse2.get(),
               adresse3.get(), notes.get(1.0, notes.index("end")),)
    return lesVars

def setVars(lesVars):
    laFiche.set(lesVars[0])
    setLabel(leTitre, lesVars[1])
    setLabel(lePreNom, lesVars[2])
    setLabel(leNom, lesVars[3])
    setLabel(telephone, lesVars[4])
    setLabel(cellulaire, lesVars[5])
    setLabel(email, lesVars[6])
    setLabel(adresse1, lesVars[7])
    setLabel(adresse2, lesVars[8])
    setLabel(adresse3, lesVars[9])
    notes.delete(1.0, notes.index("end"))
    notes.insert(1.0, lesVars[10])
    setEntrees()

def setLabel(leLabel, leTexte):
    leLabel.delete(0, leLabel.index("end"))
    leLabel.insert(0, leTexte)

def on_keyrelease(event):
    # get text from entry
    value = event.widget.get()
    value = value.strip().lower()
    listbox_update(value)

def listbox_update(mot):
    extrait = lesDonnees.chercheNom(mot)
    # delete previous data
    listbox.delete(0, 'end')
    lesID.clear()
    lesNoms.clear()
    for laLigne in extrait:
        lesID.append(laLigne[0])
        tempStr = str(laLigne[0]).zfill(4) + " -- " + laLigne[1] + " " + laLigne[2]
        lesNoms.append(tempStr)
        listbox.insert('end',tempStr)

def on_select(event):
    # display element selected on list
    #print('(event) previous:', event.widget.get('active'))
    #print('(event)  current:', event.widget.get(event.widget.curselection()))
    temp = event.widget.curselection()
    if temp:
        setVars(lesDonnees.lePatient(lesID[temp[0]]))
        listbox.selection_clear(("active"))

#le Journal
def tick():
    # l'horloge de l'ordi
    maintenant = dt.datetime.now()
    maintenant = maintenant.strftime('%Y-%m-%d %H:%M:%S')
    lHeure.config(text=maintenant)
    fenetre.after(1000,tick)

def leSoinUpdate(event):
    if leSoin.get().startswith(">R"):
        lePrix.set(lesDonnees.totalCreance(laFiche.get())[0])
    elif leSoin.get().startswith("+M"):
        fenetreSoins.initialisation()
    else:
        lePrix.set(lesDonnees.detailSoin(leSoin.get())[1])

def ajouter():
    #patientID, PatientNom, laDate, soin, prix, paiement, commentaire
    differ=0
    px=float(lePrix.get())
    if lePaiement.get().startswith(">"):
        differ=px
        px=0
    if leSoin.get().startswith(">R"):
        differ=-px
    lEntree=(int(laFiche.get()), lePreNom.get() + " " + leNom.get(), lHeure.cget("text"), leSoin.get(),
             leCommentaireSoin.get(1.0, leCommentaireSoin.index("end")), px, differ, lePaiement.get(), leCommentaire.get())
    lesDonnees.ajouter(lEntree)
    leCommentaireSoin.delete(1.0, leCommentaireSoin.index("end"))
    leSoinUpdate(1)
    setLabel(leCommentaire,"")
    setEntrees()

def completerLibelle():
    if histNum[4] > -1:
        nouvLibelle = histComment[4].cget("text")
        if len(leCommentaire.get()) > 0:
            nouvLibelle = nouvLibelle + " " + leCommentaire.get()
        nouvComment = histCommentSoin[4].get(0.0,histCommentSoin[4].index("end")).rstrip()
        print (nouvComment)
        #print(leCommentaireSoin.get(1.0,leCommentaireSoin.index("end")))
        if len(leCommentaireSoin.get(1.0,leCommentaireSoin.index("end"))) > 0:
            nouvComment = nouvComment + " " + leCommentaireSoin.get(0.0,leCommentaireSoin.index("end")).rstrip()
        lesDonnees.modifierLibelle(histNum[4], nouvLibelle, nouvComment)
    setLabel(leCommentaire, "")
    leCommentaireSoin.delete(1.0, leCommentaireSoin.index("end"))
    setEntrees()


def setEntrees():
    lesEntrees=lesDonnees.lesEntrees(int(laFiche.get()))
    maxi = len(lesEntrees)-1
    i=0
    while i < 5:
        histNum[(4 - i)]=-1 #id ligne journal non affiché
        histCommentSoin[(4 - i)].config(state='normal')
        histDate[(4-i)].config(text="-")
        histSoin[(4 - i)].config(text="-")
        histCommentSoin[(4 - i)].delete(1.0, histCommentSoin[(4 - i)].index("end"))
        histPrix[(4 - i)].config(text="-", fg='black')
        histMode[(4 - i)].config(text="-")
        histComment[(4 - i)].config(text="-")
        if i <= maxi:
            histNum[(4 - i)] = (lesEntrees[i][0]) #id ligne journal non affiché
            histDate[(4-i)].config(text=(lesEntrees[i][1]))
            histSoin[(4-i)].config(text=(lesEntrees[i][2]))
            histCommentSoin[(4-i)].insert(1.0,(lesEntrees[i][3]))
            histPrix[(4-i)].config(text=(lesEntrees[i][4]))
            if (lesEntrees[i][5]) > 0:
                histPrix[(4 - i)].config(text="("+str(lesEntrees[i][5])+")",fg='red')
            histMode[(4-i)].config(text=(lesEntrees[i][6]))
            histComment[(4-i)].config(text=(lesEntrees[i][7]))
        histCommentSoin[(4 - i)].config(state='disabled')
        i+=1

def imprimer():
    f=open(os.path.join(os.path.dirname(__file__),'modeleFacture.ps'))
    leTexte=f.read().replace("<numFact>", str(lesDonnees.leCompteJournal()[0]).zfill(4))
    leTexte=leTexte.replace("<NomPatient>", (leTitre.get() + " " + lePreNom.get() + " " + leNom.get()))
    leTexte = leTexte.replace("<adresse1>", adresse1.get())
    leTexte=leTexte.replace("<adresse2>", adresse2.get())
    leTexte=leTexte.replace("<laDate>", dt.datetime.now().strftime('%d/%m/%Y'))
    leTexte = leTexte.replace("<detailSoin>", lesDonnees.detailSoin(leSoin.get())[0])
    leTexte = leTexte.replace("<prixSoin>", str(lesDonnees.detailSoin(leSoin.get())[1]))

    charAremplacer=(('é','è','ê','à','ç', 'ô'))
    charRemplacement=(("\\351","\\350","\\352", "\\340", "\\347", "\\364"))
    i=0
    while i<len(charAremplacer):
        leTexte = leTexte.replace(charAremplacer[i],charRemplacement[i])
        i+=1

    tmp=open(os.path.join(os.path.dirname(__file__),'z-facture.ps'),'w+')
    tmp.write(leTexte)
    os.popen("lpr " + "'" + os.path.join(os.path.dirname(__file__),'z-facture.ps')+"'")
    tmp.close()
    #os.remove(os.path.join(os.path.dirname(__file__),'tmp.ps'))

def export():
    debut=simpledialog.askstring("Date début", "AAAA-MM-JJ",parent=fenetre, initialvalue= dt.datetime.now().strftime('%Y-%m-' + '01'))
    fin=simpledialog.askstring("Date fin", "AAAA-MM-JJ",parent=fenetre, initialvalue= dt.datetime.now().strftime('%Y-%m-%d'))
    if len(debut) and len(fin) :
        lesDonnees.exporterCompta(debut, fin)

fenetre = tk.Tk(className="PodoLib")
fenetre.title("Podo Lib")

laLigne = 0
laFiche = tk.StringVar(fenetre)
tk.Label(fenetre, textvariable=laFiche).grid(row=laLigne, column=2, pady=10)
tk.Button(fenetre, text="<--", command=precedent).grid(row=laLigne, column=3, pady=10)
tk.Button(fenetre, text="-->", command=suivant).grid(row=laLigne, column=4, pady=10)
tk.Button(fenetre, text="enregistrer", command=enregistrer, bg='IndianRed1').grid(row=0, column=7, padx=2, pady=5)
tk.Button(fenetre, text="  nouveau  ", command=nouveau).grid(row=0, column=8, padx=2, pady=5)
tk.Button(fenetre, text="  annuler  ", command=annuler).grid(row=0, column=6, padx=2, pady=5)

laLigne += 1
tk.Label(fenetre, text="Titre").grid(row=laLigne, column=2)
leTitre = tk.Entry(fenetre)
leTitre.grid(row=laLigne, column=3, columnspan=2)
leTitre.config(width=30)

laLigne += 1
tk.Label(fenetre, text="Nom").grid(row=laLigne, column=2)
leNom = tk.Entry(fenetre)
leNom.grid(row=laLigne, column=3, columnspan=2)
leNom.config(width=30)

laLigne += 1
tk.Label(fenetre, text="Premon").grid(row=laLigne, column=2)
lePreNom = tk.Entry(fenetre)
lePreNom.grid(row=laLigne, column=3, columnspan=2)
lePreNom.config(width=30)

laLigne += 1
#tk.Label(fenetre, text="").grid(row=laLigne, column=2)  # spacer

laLigne += 1
tk.Label(fenetre, text="Téléphone").grid(row=laLigne, column=2)
telephone = tk.Entry(fenetre)
telephone.grid(row=laLigne, column=3, columnspan=2)
telephone.config(width=30)

laLigne += 1
tk.Label(fenetre, text="Cellulaire").grid(row=laLigne, column=2)
cellulaire = tk.Entry(fenetre)
cellulaire.grid(row=laLigne, column=3, columnspan=2)
cellulaire.config(width=30)

laLigne += 1
tk.Label(fenetre, text="email").grid(row=laLigne, column=2)
email = tk.Entry(fenetre)
email.grid(row=laLigne, column=3, columnspan=2)
email.config(width=30)

laLigne += 1
#tk.Label(fenetre, text="").grid(row=laLigne, column=2)  # spacer

laLigne += 1
tk.Label(fenetre, text="Adresse - rue").grid(row=laLigne, column=2)
adresse1 = tk.Entry(fenetre)
adresse1.grid(row=laLigne, column=3, columnspan=2)
adresse1.config(width=30)

laLigne += 1
tk.Label(fenetre, text="Adresse - ville / CP").grid(row=laLigne, column=2)
adresse2 = tk.Entry(fenetre)
adresse2.grid(row=laLigne, column=3, columnspan=2)
adresse2.config(width=30)

laLigne += 1
tk.Label(fenetre, text="Adresse - remarques").grid(row=laLigne, column=2)
adresse3 = tk.Entry(fenetre)
adresse3.grid(row=laLigne, column=3, columnspan=2)
adresse3.config(width=30)

tk.Label(fenetre, text="notes").grid(row=1,columnspan=6, column=5, pady=0)
notes = tk.scrolledtext.ScrolledText(fenetre, wrap=tk.WORD, width=60, height=laLigne+1)
notes.grid(rowspan=laLigne, columnspan=5, row=2, column=5, padx=5)

laLigne += 1

#tk.Frame(fenetre, width=700, height=2, bd=2,bg='white', relief='sunken').grid(columnspan=9, row=laLigne, column=2, padx=0, pady=25)
tk.Frame(fenetre, width=10, height=670, bd=4,bg='lightgrey', relief='sunken').grid(rowspan=34, row=0, column=1, padx=0, pady=0)

#la zone de recherche
lesID = []
lesNoms = []

entry = tk.Entry(fenetre, width=30)
entry.grid(row=0, column=0)
entry.bind('<KeyRelease>', on_keyrelease)

listbox = tk.Listbox(fenetre, width=30, height=21)
listbox.grid(rowspan=17, row=1, column=0, padx=15, pady=0)
listbox.bind('<Double-Button-1>', on_select) #double click
listbox.bind('<<ListboxSelect>>', on_select) #simple cick

leScroll=tk.Scrollbar(fenetre, orient="vertical")
leScroll.config(command=listbox.yview)
leScroll.grid(rowspan=17, row=1, column=0,sticky='nse')

listbox.config(yscrollcommand=leScroll.set)

listbox_update("")

#le journal des ventes
lesSoins=[]
temp = (lesDonnees.lesSoins())
i = 0
while i < len(temp):
    lesSoins.append(temp[i][0])
    i = i + 1
lesSoins.append(">Régularisation")
lesSoins.append("+Modifier")
#lesPrix =(150,70,40,0)
lesPaiements=("Espèces", "Chèque", "Carte Bleue", "Hors compta",">Différé")

histNum=[]
histDate=[]
histSoin=[]
histCommentSoin=[]
histPrix=[]
histMode=[]
histComment=[]

laLigne += 1
i=0
while i<5:
    histNum.append(-1) #id ligne journal non affiché
    histDate.append(tk.Label(fenetre, text="date", borderwidth=2, relief="groove"))
    histDate[i].grid(columnspan=1,row=laLigne, column=2)
    histDate[i].config(width=20)
    histSoin.append(tk.Label(fenetre, text="soin", borderwidth=2, relief="groove"))
    histSoin[i].grid(columnspan=1, row=laLigne+1, column=2)
    histSoin[i].config(width=20)
    histCommentSoin.append(tk.scrolledtext.ScrolledText(fenetre, wrap=tk.WORD, width=50, heigh=2, borderwidth=2, relief="groove", bg=fenetre["bg"]))
    histCommentSoin[i].insert(1.0,"Commentaire soin")
    histCommentSoin[i].config(state="disabled")
    histCommentSoin[i].grid(columnspan=3, rowspan = 2, row=laLigne, column=3)
    histPrix.append(tk.Label(fenetre, text="prix", borderwidth=2, relief="groove"))
    histPrix[i].grid(row=laLigne+1, column=7)
    histPrix[i].config(width=10, anchor='e')
    histMode.append(tk.Label(fenetre, text="Mode de paiement", borderwidth=2, relief="groove"))
    histMode[i].grid(row=laLigne+1, column=6)
    histMode[i].config(width=15,  anchor='w')
    histComment.append(tk.Label(fenetre, text="Commentaire", borderwidth=2, relief="groove"))
    histComment[i].grid(columnspan=2, row=laLigne, column=6)
    histComment[i].config(width=28, anchor='w')

    laLigne += 2
    tk.Frame(fenetre, width=1000, height=0, bd=2, bg='white', relief='sunken').grid(columnspan=9, row=laLigne, column=1,
                                                                                   padx=0, pady=6)
    laLigne+=1

    i+=1

laLigne+=1
lHeure = tk.Label(fenetre, text="*")
lHeure.grid(row=laLigne, column=2)
tick()

leSoin = tk.StringVar(fenetre)
leSoin.set(lesSoins[0])
leSoinDropDown = tk.OptionMenu(fenetre,leSoin,*lesSoins, command=leSoinUpdate)
leSoinDropDown.grid(row=laLigne+1, column=2) #ligne30

leCommentaireSoin = tk.scrolledtext.ScrolledText(fenetre, wrap=tk.WORD, width=50, height=3)
leCommentaireSoin.grid(columnspan=3, rowspan = 2, row=laLigne, column=3,padx=5, pady=5)

lePrix=tk.StringVar(fenetre)
lePrix.set(lesDonnees.detailSoin(leSoin.get())[1])

lePrixLabel=tk.Entry(fenetre, textvariable=lePrix)
lePrixLabel.grid(row=laLigne+1, column=7)
lePrixLabel.config(width=10)

lePaiement = tk.StringVar(fenetre)
lePaiement.set(lesPaiements[0])
lePaiementDropDown = tk.OptionMenu(fenetre,lePaiement,*lesPaiements)
lePaiementDropDown.grid(row=laLigne+1, column=6)
lePaiementDropDown.config(width =12, anchor='e')

leCommentaire = tk.Entry(fenetre)
leCommentaire.grid(columnspan=2, row=laLigne, column=6)
leCommentaire.config(width=28)

tk.Button(fenetre, text="+ Libellé", command=completerLibelle).grid(rowspan=2, row=laLigne-4, column=8, padx=2, pady=5)
tk.Button(fenetre, text="  Imprimer  ", command=imprimer).grid(row=laLigne, column=8, padx=2, pady=5)
tk.Button(fenetre, text="    Ajouter    ", command=ajouter ,bg='sienna1').grid(row=laLigne+1, column=8, padx=2, pady=5)

tk.Button(fenetre, text="    Exporter Compta    ", command=export).grid(rowspan=2,row=laLigne, column=0, padx=2, pady=5)

setVars(lesDonnees.lePatient(int(lesDonnees.leComptePatients()[0])))

iconbitmapLocation = os.path.join(os.path.dirname(__file__),'icon2.xbm')
fenetre.iconbitmap("@"+iconbitmapLocation)
fenetre.iconmask("@"+iconbitmapLocation)

fenetre.update()
print("taille fenêtre : " + str(fenetre.winfo_width()) + "x" + str(fenetre.winfo_height()))

fenetre.mainloop()


fenetreSoins.ferme()
lesDonnees.ferme()


