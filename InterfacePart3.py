import pandas as pd
import numpy as np
import os
import seaborn as sns
import datetime as dt

# modules relatifs à Tkinter
import tkinter as tk
from tkinter import IntVar, StringVar 
from tkinter.scrolledtext import ScrolledText as ScrolledText
from tkcalendar import Calendar

# modules pour les images
from PIL import Image, ImageTk
from io import BytesIO
from urllib.request import urlopen

#import des données
path=os.getcwd()

calendar= pd.read_csv(path+"/calendar.csv", sep=",")
listings= pd.read_csv(path+"/listings.csv", sep=",")

#Nettoyage

def nettoyage1():
    listings["price_dollar"] = listings["price"].str.replace('$','')
    
    listings["price_dollar"][3122] = listings["price_dollar"][3122].replace(",","")
    
    listings["price_float"] = listings["price_dollar"].apply(float)
  
    calendar["date"] = pd.to_datetime(calendar["date"], format="%Y-%m-%d") 
    year =calendar["date"].dt.year.astype(str)
    month = calendar["date"].dt.month.astype(str)
    
    calendar["month"] = month
    calendar["year"] = year
    
    calendar["price_dollar"] = calendar["price"].astype(str) 
    calendar["price_dollar"] = calendar["price"].str.replace('$','') 
    calendar["price_float"] = calendar["price_dollar"].str.replace(',','').astype(np.float64)
    
    def dispo(ligne):
        if ligne == "t" :
            return 1
        else :
            return 0
    
    calendar["dispo"] = calendar["available"].apply(dispo)
    
    return


def nettoyage2():
    global quartier, logement
    logement=listings['property_type'].drop_duplicates().dropna().tolist()
    a=[]
    for i in range (len (logement)):
        a=a+[logement[i].lower()]
    logement = list(a)
    
    quartier=listings['neighbourhood_cleansed'].drop_duplicates().dropna().tolist()
    a=[]
    for i in range (len(quartier)):
        a=a+[quartier[i].lower()]
    quartier = list(a)
    
nettoyage2()
nettoyage1()

################################################ Partie fonctions ########################################################


####### Deuxième page ########

def etape_2(): # en cliquant sur le 1er next, lance cette fonction
    
    global variable_logement2 # pour la réutiliser à l'extérieur de cette fonction
    
    frame1.destroy() # parce qu'on veut changer de page
    frame2.pack()
    
    a = variable_budget.get() # vaut 1 si "yes" a été coché
    b = variable_logement.get()
    c = variable_quartier.get()
    d = variable_install.get()
    e = variable_periode.get()
    
    tk.Label(frame2).pack()
    
    variable_logement2 = tk.StringVar() # récupère valeur du logement
    variable_quartier2 = tk.StringVar() # récupère valeur du quartier
    
    next2=tk.Button(frame2, text="Next", command=etape_3) # bouton "next" de la 2ème page pour pouvoir basculer sur la 3ème
    next2.pack(side=tk.BOTTOM)  # pour qu'il soit en bas
    
        
    if a == 1 : # si l'utilisateur veut sélectionner le budget
        
        frame20.pack(side=tk.LEFT) # affiche une sous-fenêtre
        
        ## 1ère sous-sous fenêtre
        
        def recup_var3(): # pour garder en mémoire le choix du budget minimal
            global variable_budget3
            for i in liste3.curselection() :
                variable_budget3 = liste3.get(i)
        
        frame213 = tk.Frame(frame20, borderwidth=2, highlightthickness=3, highlightbackground="white", relief=tk.GROOVE)
        frame213.pack() # 1ère sous-sous-fenêtre
        
        liste3 = tk.Listbox(frame213) #listbox pour le budget minimum
        index = liste3.curselection() #### je garde ??
        budgets3 = np.arange(20,1010,10) #intervalle par pas de 10
        
        for i in budgets3:
            liste3.insert(tk.END, i) #insert les valeurs dans la listbox
        liste3.pack()
    
        bouton_lb = tk.Button(frame213, text = 'Click here to confirm your min',command=recup_var3) # bouton pour valider le choix du budget minimum
        bouton_lb.pack(side=tk.BOTTOM)
        
        #2ème sous-sous fenêtre (même principe)
        
        def recup_var2():
            global variable_budget2
            for i in liste2.curselection() :
                variable_budget2 = liste2.get(i)
                
            
        
        frame211 = tk.Frame(frame20, borderwidth=2, highlightthickness=3, highlightbackground="white", relief=tk.GROOVE)
        frame211.pack(side=tk.BOTTOM)
        
        liste2 = tk.Listbox(frame211) 
        index = liste2.curselection() #### je garde ??
        budgets2 = np.arange(20,1010,10)
        for i in budgets2:
            liste2.insert(tk.END, i)
        liste2.pack()
    
        bouton_lb = tk.Button(frame211, text = 'Click here to confirm your max',command=recup_var2)
        bouton_lb.pack(side=tk.BOTTOM)
        
    
        
    if b == 1 : # si l'utilisateur souhaite sélectionner son type de logement
        
        frame22 = tk.Frame(frame2, borderwidth=2, highlightthickness=3, highlightbackground="white", relief=tk.GROOVE)
        frame22.pack(side=tk.LEFT)
       
        label_logement2 = tk.Label(frame22, text="Housing") # titre de la sous-fenêtre
        label_logement2.pack()
    
        # tristatevalue = 0 : pour décocher toutes les cases au début
        label_logement2a = tk.Radiobutton(frame22, text = "Apartment", variable = variable_logement2, value = "Apartment", tristatevalue = 0)
        label_logement2b = tk.Radiobutton(frame22, text = "House", variable = variable_logement2, value = "House", tristatevalue = 0)
        label_logement2c = tk.Radiobutton(frame22, text = "Cabin", variable = variable_logement2, value = "Cabin", tristatevalue = 0)
        label_logement2d = tk.Radiobutton(frame22, text = "Condomium", variable = variable_logement2, value = "Condomium", tristatevalue = 0)
        label_logement2e = tk.Radiobutton(frame22, text = "Camper/RV", variable = variable_logement2, value = "Camper/RV", tristatevalue = 0)
        label_logement2f = tk.Radiobutton(frame22, text = "Bungalow", variable = variable_logement2, value = "Bungalow", tristatevalue = 0)
        label_logement2g = tk.Radiobutton(frame22, text = "Townhouse", variable = variable_logement2, value = "Townhouse", tristatevalue = 0)
        label_logement2h = tk.Radiobutton(frame22, text = "Loft", variable = variable_logement2, value = "Loft", tristatevalue = 0)
        label_logement2i = tk.Radiobutton(frame22, text = "Boat", variable = variable_logement2, value = "Boat", tristatevalue = 0)
        label_logement2j = tk.Radiobutton(frame22, text = "Bed & Breakfast", variable = variable_logement2, value = "Bed & Breakfast", tristatevalue = 0)
        label_logement2k = tk.Radiobutton(frame22, text = "Other", variable = variable_logement2, value = "Other", tristatevalue = 0)
        label_logement2l = tk.Radiobutton(frame22, text = "Dorm", variable = variable_logement2, value = "Dorm", tristatevalue = 0)
        label_logement2m = tk.Radiobutton(frame22, text = "Treehouse", variable = variable_logement2, value = "Treehouse", tristatevalue = 0)
        label_logement2n = tk.Radiobutton(frame22, text = "Yurt", variable = variable_logement2, value = "Yurt", tristatevalue = 0)
        label_logement2o = tk.Radiobutton(frame22, text = "Chalet", variable = variable_logement2, value = "Chalet", tristatevalue = 0)
        label_logement2p = tk.Radiobutton(frame22, text = "Tent", variable = variable_logement2, value = "Tent", tristatevalue = 0)
        # affiche tous les radiobuttons
        label_logement2a.pack()
        label_logement2b.pack()
        label_logement2c.pack()
        label_logement2d.pack()
        label_logement2e.pack()
        label_logement2f.pack()
        label_logement2g.pack()
        label_logement2h.pack()
        label_logement2i.pack()
        label_logement2j.pack()
        label_logement2k.pack()
        label_logement2l.pack()
        label_logement2m.pack()
        label_logement2n.pack()
        label_logement2o.pack()
        label_logement2p.pack()
        

    if c == 1 : # si l'utilisateur veut choisir le quartier
         
        def recup_var(): # garde en mémoire le choix du quartier
            global variable_quartier2
            for i in liste1.curselection() :
                variable_quartier2 = liste1.get(i)
                return variable_quartier2
                
        
        frame23 = tk.Frame(frame2, borderwidth=2, highlightthickness=3, highlightbackground="white", relief=tk.GROOVE)
        frame23.pack(side=tk.LEFT)
        
        label_quartier2 = tk.Label(frame23, text="Neighbourhood") 
        label_quartier2.pack()
        
        quartier = listings['neighbourhood_cleansed'].drop_duplicates().dropna().tolist() # liste des quartiers
        liste = [] # on crée une liste de label_quartier20,label_quartier21,label_quartier22, etc...
        l = "label_quartier2"
        for i in range(len(quartier)): # on fait une boucle
            l = l[:len("label_quartier2")]+str(i) # pour ajouter uniquement à la fin
            liste.append(l)

         
        liste1 = tk.Listbox(frame23) # listbox
        index = liste1.curselection()
    
        quartiers = listings['neighbourhood_cleansed'].drop_duplicates().dropna().tolist()
        for i in quartiers:
            liste1.insert(tk.END, i)
        liste1.pack()
    
        bouton_lb = tk.Button(frame23, text = 'Click here to confirm your neighbourhood choice',command=recup_var, relief=tk.GROOVE)
        bouton_lb.pack(side=tk.BOTTOM) # bouton pour sauvegarder son choix car listbox faut bouton

    if d == 1 : # si l'utilisateur veut choisir ses installations
        
        global variable_install2a, variable_install2b, variable_install2c, variable_install2d, variable_install2e, variable_install2f
        
        frame24 = tk.Frame(frame2, borderwidth=2, highlightthickness=3, highlightbackground="white", relief=tk.GROOVE)
        frame24.pack(side=tk.LEFT)
        label_install2=tk.Label(frame24,text="What type of Installation do you need ? ")
        label_install2.pack()
        
        ### TV ###
        label_install2a = tk.Label(frame24, text="Do you need a TV ?") 
        label_install2a.pack()
        variable_install2a = IntVar() # vaut 1 s'il veut la TV, sinon 0
        label_install2a_yes = tk.Radiobutton(frame24, text = "Yes", variable = variable_install2a, value = 1,tristatevalue=3)
        label_install2a_yes.pack()
        label_install2a_no = tk.Radiobutton(frame24, text = "I don't mind", variable = variable_install2a, value = 0,tristatevalue=3)
        label_install2a_no.pack()
        
        ### Wi-Fi ###
        label_install2b = tk.Label(frame24, text="Do you need Wifi ?") 
        label_install2b.pack()
        variable_install2b = IntVar() # # vaut 1 s'il veut le Wi-Fi, sinon 0
        label_install2b_yes = tk.Radiobutton(frame24, text = "Yes", variable = variable_install2b, value = 1,tristatevalue=3)
        label_install2b_yes.pack()
        label_install2b_no = tk.Radiobutton(frame24, text = "I don't mind", variable = variable_install2b, value = 0,tristatevalue=3)
        label_install2b_no.pack()
        
        ### Climatisation ###
        label_install2c = tk.Label(frame24, text="Do you need Air Conditionning (A/C) ?") 
        label_install2c.pack()
        variable_install2c = IntVar()  # vaut 1 s'il veut la climatisation, sinon 0
        label_install2c_yes = tk.Radiobutton(frame24, text = "Yes", variable = variable_install2c, value = 1,tristatevalue=3)
        label_install2c_yes.pack()
        label_install2c_no = tk.Radiobutton(frame24, text = "I don't mind", variable = variable_install2c, value = 0,tristatevalue=3)
        label_install2c_no.pack()
        
        ### Parking ###
        label_install2d = tk.Label(frame24, text="Do you need a Parking place ?") 
        label_install2d.pack()
        variable_install2d = IntVar() # vaut 1 s'il veut un parking, sinon 0
        label_install2d_yes = tk.Radiobutton(frame24, text = "Yes", variable = variable_install2d, value = 1,tristatevalue=3)
        label_install2d_yes.pack()
        label_install2d_no = tk.Radiobutton(frame24, text = "I don't mind", variable = variable_install2d, value = 0,tristatevalue=3)
        label_install2d_no.pack()
        
        ### Elevator ###
        label_install2e = tk.Label(frame24, text="Do you need an Elevator ?") 
        label_install2e.pack()
        variable_install2e = IntVar() # vaut 1 s'il veut un ascenseur, sinon 0
        label_install2e_yes = tk.Radiobutton(frame24, text = "Yes", variable = variable_install2e, value = 1,tristatevalue=3)
        label_install2e_yes.pack()
        label_install2e_no = tk.Radiobutton(frame24, text = "I don't mind", variable = variable_install2e, value = 0,tristatevalue=3)
        label_install2e_no.pack()
        
        ### Nothing ###
        label_install2f = tk.Label(frame24, text="Do you want No TV, no Wifi, no AC, no Parking, no Elevator?") 
        label_install2f.pack()
        variable_install2f = IntVar() # vaut 1 s'il ne veut rien, sinon 0
        label_install2f_yes = tk.Radiobutton(frame24, text = "Yes, I'm crazy", variable = variable_install2f, value = 1,tristatevalue=3)
        label_install2f_yes.pack()
        label_install2f_no = tk.Radiobutton(frame24, text = "No", variable = variable_install2f, value = 0,tristatevalue=3)
        label_install2f_no.pack()   

    if e==1: # si l'utilisateur veut choisir sa date de début et fin de séjour
        
        global cal1 # pour pouvoir rappeler à l'extérieur de la fonction
        frame25.pack(side=tk.LEFT)
        label_calendar = tk.Label(frame25, text="Date") # nom du calendrier
        label_calendar.pack()
        # Add Calendar
        
        frame251.pack() # affiche la sous-fenêtre
        
        cal1=Calendar(frame251,selectmode='day',year=2016,month=1,date_pattern="Y-mm-dd",background="black",selectbackground ="red", mindate=dt.date(2016,1,4), maxdate= dt.date(2017,1,2))
        cal1.pack() # affiche d'abord premier calendrier
        btn_251=tk.Button(frame251, text="Click to confirm your debut", command=calen2) # puis le 2ème calendrier seulement après avoir cliqué sur le bouton
        btn_251.pack()
        
def calen2():
    global cal1_min,cal2
    cal1_min = str(cal1.get_date()).split('-') # récupère la valeur du 1er calendrier et le split selon les tirets
    cal1_min[0] = int(cal1_min[0]) # prend la valeur entière de l'année
    cal1_min[1] = int(cal1_min[1]) # prend la valeur entière du mois car on ne veut pas que ça commence par 0 
    cal1_min[2] = int(cal1_min[2]) # idem pour le jour
    frame252.pack()
    cal2=Calendar(frame252,selectmode='day',year=2016,month=1,date_pattern="Y-mm-dd",background="black",selectbackground ="red", mindate=dt.date(cal1_min[0], cal1_min[1], cal1_min[2]) + dt.timedelta(1), maxdate= dt.date(2017,1,2))
    cal2.pack() # affiche le 2ème calendrier
    btn_252=tk.Button(frame252, text="Click to confirm your end") # bouton optionnel, sert d'esthétique
    btn_252.pack()

######### Fin fonctions de la deuxième page ###########


######### Troisième page ############
        
def etape_3(): # fonction de la 3ème page qui affiche les résultats demandés
    
    global final, frame3 # dataframe final qui contient les résultats
    frame2.destroy() # détruit la 2ème frame
    frame3 = tk.Frame(window)
    frame3.pack() # pour la 3ème frame
    
    frame31 = tk.Frame(frame3, borderwidth=2, highlightthickness=3, highlightbackground="white", relief=tk.GROOVE)
    frame31.pack(side=tk.LEFT)
    
    frame32 = tk.Frame(frame3, borderwidth=2, highlightthickness=3, highlightbackground="white", relief=tk.GROOVE)
    
    def destroy_frame3(): # fonction pour relancer l'interface
        frame3.destroy()
        window.destroy()
        reset()
        
    # Bouton pour relancer l'interface
    frame33 = tk.Frame(frame3, borderwidth=2, highlightthickness=3, highlightbackground="white", relief=tk.GROOVE)
    frame33.pack(side=tk.TOP)    
    bouton_reset = tk.Button(frame33, text = 'New search', command = destroy_frame3,relief=tk.GROOVE)
    bouton_reset.pack()
    
    
    # ScrolledText pour afficher les résultats dans une fenêtre Tkinter
    text_result= ScrolledText(frame31, width=120, height= 70) # configuration du ScrolledText
    text_result.pack()
    
    #stock=[prix,logement,quartier,installation,période]
    # récupère la valeur 1 ou 0 de chaque option
    stock=[variable_budget.get(),variable_logement.get(),variable_quartier.get(),variable_install.get(),variable_periode.get()]
    
    # dataframe de chacune des options
    a=pd.DataFrame(listings, columns=["id","name","summary","property_type","price_float","neighbourhood_cleansed","bedrooms","host_name","TV","wifi","clim","parking","elevator","listing_url","picture_url"])
    b=pd.DataFrame(listings, columns=["id","name","summary","property_type","price_float","neighbourhood_cleansed","bedrooms","host_name","TV","wifi","clim","parking","elevator","listing_url","picture_url"])
    c=pd.DataFrame(listings, columns=["id","name","summary","property_type","price_float","neighbourhood_cleansed","bedrooms","host_name","TV","wifi","clim","parking","elevator","listing_url","picture_url"])
    d=pd.DataFrame(listings, columns=["id","name","summary","property_type","price_float","neighbourhood_cleansed","bedrooms","host_name","TV","wifi","clim","parking","elevator","listing_url","picture_url"])
    e=pd.DataFrame(listings, columns=["id","name","summary","property_type","price_float","neighbourhood_cleansed","bedrooms","host_name","TV","wifi","clim","parking","elevator","listing_url","picture_url"])
    
    if stock[0]==1:#si il veut séléctionner un budget alors on appelle la fonction budget() pour choisir budget et voir ce qui correspond
        a=budget()
    if stock[1]==1: # s'il veut choisir le type de logement
        b=proptype()
    if stock[2]==1: # type de quartier
        c=quartype()
    if stock[3]==1: # choix des installations
        d=instatype()
    if stock[4]==1: # choix de la date
        e=logement_dispo()
    
    # une fois les dataframe relatives à chaque option obtenues, on les merge 1 à 1 pour former le dataframe final
    final=pd.merge(a,b,how="inner") 
    final=pd.merge(final,c,how="inner") # inner pour garder ce qui est en commun
    final=pd.merge(final,d,how="inner")
    final=pd.merge(final,e,how="inner") # ici le dataframe final
    final=final.sort_values(by=['price_float'])
    
    # on récupère les éléments de chaque colonne du dataframe dans une liste pour voir les afficher dans le ScrolledText
    id_txt = final['id'].tolist() # tous les ID dans une liste
    name_txt= final['name'].tolist()
    summary_txt = final['summary'].tolist()
    property_txt = final['property_type'].tolist()
    price_txt = final['price_float'].tolist() 
    neighbourhood_txt = final['neighbourhood_cleansed'].tolist()
    bedrooms_txt = final['bedrooms'].tolist()
    hostname_txt = final['host_name'].tolist()
    tv_txt = final['TV'].tolist()
    wifi_txt = final['wifi'].tolist()
    clim_txt = final['clim'].tolist()
    parking_txt = final['parking'].tolist()
    elevator_txt = final['elevator'].tolist()
    url_txt = final['listing_url'].tolist()
    picture_txt = final['picture_url'].tolist()
    
    if final.shape[0]==0: # si aucun résultat ne correspond aux critères, c'est-à-dire si le dataframe final est vide
        text_result.insert(tk.END,"Sorry, there is no result.")
    
    else: # s'il y a au moins un résultat correspondant aux recherches
        for i in range(len(id_txt)): # toutes les listes font la même longueur donc on prend n'importe laquelle
            findelafin = " \n                                         ||| ID of the housing : " + str(id_txt[i]) + " |||" + "\n Name of the housing : " + str(name_txt[i])+ "\n Summary : " + str(summary_txt[i])+ "\n Type of property : "+ str(property_txt[i])+ "\n Price per night is : " + str(price_txt[i])+ "$"+"\n Neighbourhood :  " + str(neighbourhood_txt[i])+ "\n Number of bedrooms : "+ str(bedrooms_txt[i]) +" rooms" + "\n Host name is : " + str(hostname_txt[i])+ "\n TV : "+ str(tv_txt[i]==1)+ "\n Wi-Fi : "+ str(wifi_txt[i]==1)+"\n Air Conditionning (AC) : "+str(clim_txt[i]==1)+"\n Parking : "+ str(parking_txt[i]==1)+"\n Elevator : "+str(elevator_txt[i]==1)+"\n URL : " + str(url_txt[i])+"\n Picture's URL :"+ str(picture_txt[i])+"\n"+"\n"+"\n"+"\n"
            text_result.insert(tk.END,findelafin) # affiche dans le ScrolledText
        
        frame32.pack(side=tk.LEFT) # fenêtre de la listbox pour pouvoir choisir la photo à afficher
        
        def afficher(): #fonction qui permet d'afficher la photo
            for i in listbox_image.curselection() :
                a= tk.Toplevel() # dans une nouvelle fenêtre
                choix = listbox_image.get(i) # choix du logement
                URL = picture_txt[i] # URL du logement sélectionné
                u = urlopen(URL) # ouvre URL
                raw_data = u.read()
                u.close()
            
                im = Image.open(BytesIO(raw_data)) # met dans le bon format
                photo = ImageTk.PhotoImage(im)

                label_image = tk.Label(a,text='This is housing n°'+str(id_txt[i])) # titre de la photo
                label_image.pack()

                label_photo = tk.Label(a,image=photo) # photo
                label_photo.image = photo
                label_photo.pack(side=tk.BOTTOM)
                
         
        listbox_image = tk.Listbox(frame32) # listbox pour les photos
       
        
        for i in id_txt:
            listbox_image.insert(tk.END, i)
        listbox_image.pack()
    
        bouton_im = tk.Button(frame32, text = 'Click here to see the image',command=afficher, relief=tk.GROOVE) #bouton pour lancer la fonction qui affiche l'image
        bouton_im.pack(side=tk.BOTTOM) # bouton pour sauvegarder son choix
        
        

####### Fin fonction de la page 3 ######
        

###### Fonctions issues de la partie 2 (et adaptées) ######

def budget(): # fonction qui retourne les logements selon le budget
    mi=float(variable_budget3)
    ma=float(variable_budget2)
    if mi>ma:
        alt1=mi
        alt2=ma
        mi=alt2
        ma=alt1
    if mi<=ma:
        b=listings.sort_values(by=['price_float']) # trie par ordre croissant
        b=b.loc[(b["price_float"]<=ma)&(b["price_float"]>=mi)] # affiche les lignes qui correspondent au budget donné
    #changer b en nouveau df pour optimiser le code
        prix_mini = listings["price_float"].min() # prix minimal d'une nuit
        prix_maxi = listings["price_float"].max() # prix maximinal d'une nuit
       
        c=pd.DataFrame(b, columns=["id","name","summary","property_type","price_float","neighbourhood_cleansed","bedrooms","host_name","listing_url","picture_url"])
        
        return c
    
    
def proptype(): # fonction qui retourne les types de logements selon le type
    b=listings
    z=variable_logement2.get()
    b1=b.loc[(b["property_type"]==z)]
    b=b1.sort_values(by=['price_float'])
    c=pd.DataFrame(b, columns=["id","name","summary","property_type","price_float","neighbourhood_cleansed","bedrooms","host_name","listing_url","picture_url"])
    
    
    return c


def quartype(): # fonction qui retourne les logements selon les quartiers
    b=listings
    z=variable_quartier2 #.get()
    b1=b.loc[(b["neighbourhood_cleansed"]==z)]
    b=b1.sort_values(by=['price_float'])
    c=pd.DataFrame(b, columns=["id","name","summary","property_type","price_float","neighbourhood_cleansed","bedrooms","host_name","listing_url","picture_url"])
   
    
    return c


def instatype(): # fonction pour retourner les logements ayant les installations souhaitées

    a=pd.DataFrame(listings, columns=["id","name","summary","property_type","price_float","neighbourhood_cleansed","bedrooms","host_name","TV","wifi","clim","parking","elevator","listing_url","picture_url"])
    b=pd.DataFrame(listings, columns=["id","name","summary","property_type","price_float","neighbourhood_cleansed","bedrooms","host_name","TV","wifi","clim","parking","elevator","listing_url","picture_url"])
    c=pd.DataFrame(listings, columns=["id","name","summary","property_type","price_float","neighbourhood_cleansed","bedrooms","host_name","TV","wifi","clim","parking","elevator","listing_url","picture_url"])
    d=pd.DataFrame(listings, columns=["id","name","summary","property_type","price_float","neighbourhood_cleansed","bedrooms","host_name","TV","wifi","clim","parking","elevator","listing_url","picture_url"])
    e=pd.DataFrame(listings, columns=["id","name","summary","property_type","price_float","neighbourhood_cleansed","bedrooms","host_name","TV","wifi","clim","parking","elevator","listing_url","picture_url"])
    
    z=[variable_install2a.get(),variable_install2b.get(),variable_install2c.get(),variable_install2d.get(),variable_install2e.get(),variable_install2f.get()]
    
    if z[0]==1:
        a=a.loc[a["TV"]==1]#TV
    if z[1]==1:
        b=b.loc[b["wifi"]==1]#wifi
    if z[2]==1:
        c=c.loc[c["clim"]==1]#clim
    if z[3]==1:
        d=d.loc[d["parking"]==1]#parking
    if z[4]==1:
        e=e.loc[e["elevator"]==1]#Elevator
    if z[5]==1:#s'il sélectionne "rien"
        l=listings
        p=l.loc[(l["TV"]==0)&(l["wifi"]==0)&(l["clim"]==0)&(l["parking"]==0)&(l["elevator"]==0)]
        c=pd.DataFrame(p, columns=["id","name","summary","property_type","price_float","neighbourhood_cleansed","bedrooms","host_name","TV","wifi","clim","parking","elevator","listing_url","picture_url"])
        return c
    ref1=pd.merge(a,b,how="inner")
    ref1=pd.merge(ref1,c,how="inner")
    ref1=pd.merge(ref1,d,how="inner")
    ref1=pd.merge(ref1,e,how="inner")
    ref=ref1.sort_values(by=['price_float'])
    c=pd.DataFrame(ref, columns=["id","name","summary","property_type","price_float","neighbourhood_cleansed","bedrooms","host_name","TV","wifi","clim","parking","elevator","listing_url","picture_url"])
    return c


def demander_date(): # fonction pour avoir les id des logements disponibles entre début et fin du séjour
    
    debut = cal1.get_date()
    fin = cal2.get_date()
    
    calendar.sort_values(by='date') 
    debut_time = dt.datetime.strptime(debut, "%Y-%m-%d").date()
    fin_time = dt.datetime.strptime(fin, "%Y-%m-%d").date()
    
    diff = fin_time - debut_time 
    duree = str(diff) 
    duree = duree.split(' ') 
          
    if int(duree[0]) > 0:
        ligne_date = calendar.loc[(calendar["date"] <= fin) & (calendar["date"] >= debut) & (calendar["dispo"] == 1)] 
        liste_id = ligne_date['listing_id'].drop_duplicates().dropna().tolist() 
    
        liste_id_definitive = [] 
        for i in (liste_id):    
            df = ligne_date.loc[ligne_date["listing_id"] == i] 
            if df.shape[0] ==  int(duree[0]) : 
                liste_id_definitive += [i]
        
        
    
        return liste_id_definitive
    
    
def logement_dispo(): # fonction pour avoir les logements disponibles
    liste = demander_date() 
    annonce = listings.loc[listings["id"].isin(liste), ["id","name","summary","property_type","price_float","neighbourhood_cleansed","bedrooms","host_name","listing_url","picture_url"]]
    annonce=annonce.sort_values(by=['price_float'])
    return annonce
    
    
##############################################################    

    
                        ############ Première fenêtre et définitions de frames ###########

def reset():# stocker dans une fonction pour pouvoir recommencer la procédure
    global frame1, frame2, frame20,frame25,frame251,frame252,framef1,window,variable_budget,variable_logement,variable_quartier,variable_install,variable_periode
    window=tk.Tk()
    window.title("Interface Airbnb")
    window.config(bg="#6b8496")
    label=tk.Label(window,text="Welcome")
    label.pack()

    frame1 = tk.Frame(window,borderwidth=2, highlightthickness=3, highlightbackground="white", relief=tk.GROOVE)
    frame1.pack()

    frame2 = tk.Frame(window)
    frame20 = tk.Frame(frame2, borderwidth=2, highlightthickness=3, highlightbackground="white", relief=tk.GROOVE)

    frame25 = tk.Frame(frame2, borderwidth=2, highlightthickness=3, highlightbackground="white", relief=tk.GROOVE)
    frame251 = tk.Frame(frame25, borderwidth=2, highlightthickness=3, highlightbackground="white", relief=tk.GROOVE)
    frame252 = tk.Frame(frame25, borderwidth=2, highlightthickness=3, highlightbackground="white", relief=tk.GROOVE)

    framef1 = tk.Frame(frame1, borderwidth=2, highlightthickness=3, highlightbackground="white", relief=tk.GROOVE) # tk.GROOVE : pour les bordures de la fenêtre
    framef1.pack(side=tk.TOP, padx=1, pady=1)  

    label_budget = tk.Label(frame1, text="Do you want to select a budget ?") #dans frame1
    label_budget.pack()
    variable_budget = tk.IntVar() #récupère valeur
    label_budget_yes = tk.Radiobutton(frame1, text = "Yes", variable = variable_budget, value = 1) #radiobutton : cocher 1 case uniquement
    label_budget_yes.pack()
    label_budget_no = tk.Radiobutton(frame1, text = "No", variable = variable_budget, value = 0)
    label_budget_no.pack()

## demander type de logement particulier

    label_logement= tk.Label(frame1, text="Do you want to select a particular housing ?") #dans frame1
    label_logement.pack()
    variable_logement = tk.IntVar() #récupère valeur
    label_logement_yes = tk.Radiobutton(frame1, text = "Yes", variable = variable_logement, value = 1)
    label_logement_yes.pack()
    label_logement_no = tk.Radiobutton(frame1, text = "No", variable = variable_logement, value = 0)
    label_logement_no.pack()

## demander un quartier en particulier 

    label_quartier = tk.Label(frame1, text="Do you want to select a particular neighbourhood ?") #dans frame1
    label_quartier.pack()
    variable_quartier = IntVar() #récupère valeur
    label_quartier_yes = tk.Radiobutton(frame1, text = "Yes", variable = variable_quartier, value = 1)
    label_quartier_yes.pack()
    label_quartier_no = tk.Radiobutton(frame1, text = "No", variable = variable_quartier, value = 0)
    label_quartier_no.pack()

## demander des installations en particulier

    label_install = tk.Label(frame1, text="Do you want to select specific amenities (Air Conditionner, Wi-Fi, Parking, etc.) ?") #dans frame1
    label_install.pack()
    variable_install = IntVar() #récupère valeur
    label_install_yes = tk.Radiobutton(frame1, text = "Yes", variable = variable_install, value = 1)
    label_install_yes.pack()
    label_install_no = tk.Radiobutton(frame1, text = "No", variable = variable_install, value = 0)
    label_install_no.pack()


## demander une période en particulier

    label_periode = tk.Label(frame1, text="Do you want to select a specific date ?") #dans frame1
    label_periode.pack()
    variable_periode = IntVar() #récupère valeur
    label_periode_yes = tk.Radiobutton(frame1, text = "Yes", variable = variable_periode, value = 1)
    label_periode_yes.pack()
    label_periode_no = tk.Radiobutton(frame1, text = "No", variable = variable_periode, value = 0)
    label_periode_no.pack()

# bouton "next step"

    next1=tk.Button(frame1, text="Next", command=etape_2) # cliquer sur "next" doit afficher autre chose)
    next1.pack()
    
    def ouitv(a):
        if "TV" in a:
            return 1
        else:
            return 0
        
    def ouifi(a):
        if ("Wireless Internet" in a) or("Internet" in a):
            return 1
        else: 
            return 0
        
    def ouiclim(a):
        if "Air Conditioning" in a:
            return 1
        else: 
            return 0
        
    def ouiparking(a):
        if "Free Parking on Premises" in a:
            return 1
        else:
            return 0
    
    def ouielevator(a):
        if "Elevator in Building" in a:
            return 1
        else:
            return 0 
        
    def espace2(a) :  
        b="" #stockage
        for i in range(len(a)):#on parcourt les éléments de la ligne en remplaçant les caractères spéciaux
            d=a[i].replace("{","")
            d=d.replace("}","")
            d=d.replace('"',"")
            b=b+d
        c=b.split(",")#on utilise la virgule (",")qui était le séparateur pour split la ligne et en faire une liste avec seulement les mots
        return c    
    
    listings["instal"]=listings["amenities"].apply(list)#on transforme en liste la colonne amenities (qu'on appelle instal)
    listings["instal"]=listings["instal"].apply(espace2)
    #crée des colonnes qui valent 1 ou 0
    listings["TV"]=listings["instal"].apply(ouitv)
    listings["wifi"]=listings["instal"].apply(ouifi)
    listings["clim"]=listings["instal"].apply(ouiclim)
    listings["parking"]=listings["instal"].apply(ouiparking)
    listings["elevator"]=listings["instal"].apply(ouielevator)

    window.mainloop()

reset()


