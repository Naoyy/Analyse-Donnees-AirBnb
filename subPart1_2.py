#Librairies utilisées
import pandas as pd #pour le travail sur dataset

import numpy as np

import os #pour obtenir le chemin (arborescence différente en fonction de l'ordinateur)

import datetime as dt #pour travailler sur des périodes de temps

import matplotlib.pyplot as plt #pour la réalisation de graphiques

import seaborn as sns #pour la data visualisation 


#### import des données ####

def importer():
    global calendar,listings #afin de pouvoir utiliser ces data frames en dehors de la fonction
    path=os.getcwd()
    calendar= pd.read_csv(path+"/calendar.csv", sep=",")
    listings= pd.read_csv(path+"/listings.csv", sep=",")
    return

importer() #pour importer on fait tourner la fonction. Ainsi on pourra appeler calendar et listings 


######## NETTOYAGE ##########

#Fonction de nettoyage nécessaire pour la partie 1
def nettoyage1():
    
    #nettoyage Q1
    #pour pouvoir utiliser le prix comme indicateur quantitatif on le transforme en type Float
    
    listings["price_dollar"] = listings["price"].str.replace('$','')# $ est un caractère spécial qui nous empêche de traiter les prix comme des type float
    
    listings["price_dollar"][3122] = listings["price_dollar"][3122].replace(",","")
    #l'itération 3122 pose problème, dans listings elle est la seule avec une virgule: on remplace manuellement
    
    listings["price_float"] = listings["price_dollar"].apply(float)
    #on transforme ensuite en type float avec la fonction float
    
    
    #nettoyage Q2
    #afin de manipuler des périodes de temps on transforme la date en type datetime
    calendar["date"] = pd.to_datetime(calendar["date"], format="%Y-%m-%d") 
    
    year =calendar["date"].dt.year.astype(str)# création variable year
    month = calendar["date"].dt.month.astype(str)#création variable month
    
    #on les ajoute dans le dataframe
    calendar["month"] = month
    calendar["year"] = year
    
    #nettoyage Q4
    #même opération que pour la question 1 cette fois avec le df Calendar
    calendar["price_dollar"] = calendar["price"].astype(str) 
    calendar["price_dollar"] = calendar["price"].str.replace('$','') 
    calendar["price_float"] = calendar["price_dollar"].str.replace(',','').astype(np.float64)
    
    #on crée une variable dispo pour avoir sous forme de 1 et 0 la disponibilité ce qui facilitera le comptage 
    def dispo(ligne):
        if ligne == "t" :
            return 1 #si logement dispo alors dispo=1
        else :
            return 0
    
    calendar["dispo"] = calendar["available"].apply(dispo)#on crée une nouvelle colonne et applique à chaque ligne notre fonction
    
    return

#fonction de nettoyage nécessaire pour la partie 2

def nettoyage2():
    global quartier, logement
    
    #Creation d'une liste qui comprend les types de logements possibles pour Q6
    logement=listings['property_type'].drop_duplicates().dropna().tolist()
    a=[]
    for i in range (len(logement)):#on utilise une boucle afin de mettres les types de logements dans la liste en minuscule
        a=a+[logement[i].lower()]
    logement = list(a)
    
    #Creation d'une liste qui comprend les types de quartiers possibles pour Q7
    quartier=listings["neighbourhood_cleansed"].drop_duplicates().dropna().tolist()
    a=[]
    for i in range (len(quartier)):
        a=a+[quartier[i].lower()]
    quartier = list(a)
    
    
    #Q8 sur les amenities (commodités) 
    

    
    def espace2(a) : #nettoie la colonne "amenities" pour retourner seulement les options sous formes de liste
        
        b="" #stockage
        for i in range(len(a)):#on parcours les éléments de la ligne en remplaçant les caractères spéciaux
            d=a[i].replace("{","")
            d=d.replace("}","")
            d=d.replace('"',"")
            b=b+d#on ajoute l'élément si il n'a pas été supprimé
        c=b.split(",")#On split par virgule
        return c
    
    
    
    #meme principe que la fonction dispo
    def ouitv(a):
        if "TV" in a:
            return 1#si logement possède une TV, TV=1
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
        
        
    listings["instal"]=listings["amenities"].apply(list)#Transforme en liste la colonne amenities (qu'on appelle instal)
    listings["instal"]=listings["instal"].apply(espace2)#nettoie les lignes: les mots clés sont sans caractères spéciaux, ni espaces

    listings["TV"]=listings["instal"].apply(ouitv)#création d'une colonne TV (si le logement a renseigné avoir une TV)
    listings["wifi"]=listings["instal"].apply(ouifi)
    listings["clim"]=listings["instal"].apply(ouiclim)
    listings["parking"]=listings["instal"].apply(ouiparking)
    listings["elevator"]=listings["instal"].apply(ouielevator)
    
    return


def espace(a) : # fonction qui met les majuscules au début de chaque mot. On l'utilise pour les quartiers (Q7)
    b=''
    c = a.count(' ') # compte le nombre d'espaces vides
    
    if c != 0 :
        a = a.split(' ')
        for i in range (len (a)):
            b=b+a[i].capitalize()+" "
        return b[:-1]
    
    else :
        return a.capitalize()
    
################## Prix par Nuit #######################

def budget(): #fonction pour vérifier si le budget est correct
    
    a1=input("\nWhat is your minimum budget per night?\n\n")
    a2=input("\nWhat is your maximum budget per night?\n\n ")
    a1=a1.replace("$","")
    a1=a1.replace(",","")
    a1=float(a1)
    
    a2=a2.replace("$","")
    a2=a2.replace(",","")
    a2=float(a2)
    
    if a1<=a2:
        return [a1,a2]
    
    else:
        print("\n"," Inconsistent budget. Please retry.","\n")
        return budget()# c'est une fonction récursive, elle s'appelle elle même (cela évite de faire des boucles while)



def pricenight(): #fonction qui demande le budget et affiche les annonces dispo
    
    stock=budget()#fourchette de prix dans le format correct
    
    a1=stock[0]#on récupère le budget min 
    a2=stock[1]#on récupère le budget max
    
    b=listings.sort_values(by=['price_float']) # trie les prix par ordre croissant
    b=b.loc[(b["price_float"]<=a2)&(b["price_float"]>=a1)] # affiche les lignes qui correspondant au budget donné
    
    prix_mini = listings["price_float"].min() # prix minimal d'une nuit
    prix_maxi = listings["price_float"].max() # prix maximinal d'une nuit
    
    if b.shape[0]==0 : #shape (observations, colonnes)
        flag=True #drapeau
        
        while flag==True:
            
            if a1 > prix_maxi: # si le prix minimum donné est supérieur au prix max des chambres
           
                print("\nThere is no room matching your preferences. Please decrease your budget.\n")
                stock = budget()#on redemande un nouveau budget
                a1=stock[0]
                a2=stock[1]
            
            elif a2 < prix_mini : # si le prix maximal donné est inférieur au prix mini des chambres
                print("\nThere is no room matching your preferences. Please increase your budget.\n")
                stock=budget()
                a1=stock[0]
                a2=stock[1]
            
            b=listings.sort_values(by=['price_float'])#important, il faut rénitialiser la valeur b
            b=b.loc[(b["price_float"]<=a2)&(b["price_float"]>=a1)]
            
            if b.shape[0]!=0:#cad si au moins une annonce a été trouvée
                flag=False  #on sort de la boucle while
    
    c=pd.DataFrame(b, columns=["id","name","summary","property_type","price_float","neighbourhood_cleansed","bedrooms","host_name"])
    #format du résultat
    print("\nThere are", c.shape[0], "housings available with the selected budget only.\n ")
    
    return c

########## Choix type de logement ###############

def bontype(): #fonction qui vérifie si les critères entrés sont correctement indiqués
    
    print ("\nType of housing : Apartment, House, Cabin, Condominium, Camper/RV, Bungalow, Townhouse, Loft, Boat, Bed & Breakfast, Other, Dorm, Treehouse, Yurt, Chalet, Tent\n")
    
    a=input("\nWhat type of housing do you want? Choose in the list above.\n\n ").lower()#minuscule pour faciliter le traitement
    
    
    if (a=="bed")or(a=='breakfast')or(a=="bed & breakfast")or(a=="bed and breakfast"):#cas particulier: le logement Bed & Breakfast
        a="Bed & Breakfast"
        return a
    
    if (a=="camper") or(a=="rv")or(a=="camper/rv"):
        a="Camper/RV"
        return a
    
    if a in logement:
        return a.capitalize()# car les variables sont écrites avec une majuscule 
    
    else:
        print("\n","Sorry, cannot recognize your choice, try again.","\n")
        return bontype()

def proptype(): #fonction qui renvoie les annonces correspondant au bon type de logement
    b=listings
    z=bontype()
    b1=b.loc[(b["property_type"]==z)]#récupère les lignes qui correspondent au type de logement séléctionné
    b=b1.sort_values(by=['price_float'])
    c=pd.DataFrame(b, columns=["id","name","summary","property_type","price_float","neighbourhood_cleansed","bedrooms","host_name"])
    print("There are", c.shape[0], "housings available with the selected property type only. ")
    
    return c

####### Quartier #############

def bonquart(): #vérifie que le nom entré correspond à un quartier existant
    
    print ("\nType of Neighbourhood : \n",quartier,"\n")

    a=input("\n What type of Neighbourhood do you want? Choose in the list above.\n\n ").lower()
    
    if (a == 'harrison') or (a == 'denny-blaine') or (a == 'denny blaine') or (a == 'denny') or (a == 'blaine') : #exception
        return 'Harrison/Denny-Blaine'
        
    if (a == 'north beach') or (a == 'blue ridge') :
        return 'North Beach/Blue Ridge'
    
    if (a == 'pike') or (a == 'market') or (a == 'pike market') or (a== 'pike-market') or (a=='pikemarket'): 
        return 'Pike-Market'
    
    if (a=='mid beacon hill') or (a=='mid beacon') or (a=='mid-beacon hill') :
        return 'Mid-Beacon Hill'

    if a in quartier:
        return espace(a)
    
    else:
        print("\n","Sorry, cannot recognize your choice, try again.","\n")
        
        return bonquart() 

def quartype(): #trouve les annonces qui correspondent au quartier demandé
    b=listings
    z=bonquart()
    b1=b.loc[(b["neighbourhood_cleansed"]==z)]
    b=b1.sort_values(by=['price_float'])
    c=pd.DataFrame(b, columns=["id","name","summary","property_type","price_float","neighbourhood_cleansed","bedrooms","host_name"])
    print("\nThere are", c.shape[0], "housings available with the selected neighbourhood.\n")
    
    return c


######## Amenities ####################

def boninsta2(): #vérifie que c'est le bon format d'installation
    print("\n Please choose one or more amenities among : TV, Wifi , Clim, Parking, Elevator, Nothing\n")
    a=input("\nWhat type of amenities do you need ? (give an answer separated by spaces) \n\n").lower()
    
    b=a.split(" ")#transforme mots séparé par des espaces en liste avec 1 mot par itération
    
    z=[0,0,0,0,0,0]# z=[tv,wifi,clim,parking,ascenceur,rien de tout ça]
                    

    if ("télé" in b) or ("tv" in b)or("television" in b)or("télévision" in b):
        z[0]=1#TV
    
    if ("wifi" in b)or("internet" in b)or("wireless internet"in b):
        z[1]=1#Wifi
    
    if ("ac" in b)or("aircon" in b)or("clim" in b)or ("climatisation" in b)or("a/c" in b)or("air conditioning" in b):
        z[2]=1 #Clim
    
    if ("parking" in b)or("pkg" in b)or("park" in b):
        z[3]=1#parking
    
    if ("elevator" in b)or("lift" in b):
        z[4]=1#ascenceur
        
    if ("rien" in b) or("nothing" in b):
        z=[0,0,0,0,0,1]#obligé de remplacer: si il choisit de ne rien avoir il faut 0 pour les autres
        
    
    if sum(z)!=0: #le client a décidé de prendre des options alors si z n'a "vu" aucune option c'est qu'il a mal écrit son choix
        return z
    else:
        print("\n","Nothing you said matched the corresponding options, please retry ","\n")
        return boninsta2()

    
def instatype(): #trouve des locations qui ont les installations demandées
    a=pd.DataFrame(listings, columns=["id","name","summary","property_type","price_float","neighbourhood_cleansed","bedrooms","host_name","TV","wifi","clim","parking","elevator"])
    b=pd.DataFrame(listings, columns=["id","name","summary","property_type","price_float","neighbourhood_cleansed","bedrooms","host_name","TV","wifi","clim","parking","elevator"])
    c=pd.DataFrame(listings, columns=["id","name","summary","property_type","price_float","neighbourhood_cleansedd","bedrooms","host_name","TV","wifi","clim","parking","elevator"])
    d=pd.DataFrame(listings, columns=["id","name","summary","property_type","price_float","neighbourhood_cleansed","bedrooms","host_name","TV","wifi","clim","parking","elevator"])
    e=pd.DataFrame(listings, columns=["id","name","summary","property_type","price_float","neighbourhood_cleansed","bedrooms","host_name","TV","wifi","clim","parking","elevator"])
    
    z=boninsta2()# z est notre compteur il recense les choix d'options du client (1 si il désire l'option)
    # z=[tv,wifi,clim,parking,ascenceur,rien de tout ça]
    
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
        
    if z[5]==1:#nothing from above
        l=listings
        p=l.loc[(l["TV"]==0)&(l["wifi"]==0)&(l["clim"]==0)&(l["parking"]==0)&(l["elevator"]==0)]
        c=pd.DataFrame(p, columns=["id","name","summary","property_type","price_float","neighbourhood_cleansed","bedrooms","host_name","TV","wifi","clim","parking","elevator"])
        return c 
    
    #pour éviter d'avoir à faire les combinaisons en fonction des choix du client on merge avec la liste entière
    #(logique car merge A (inclus dans R) avec R donne A)
    
    ref1=pd.merge(a,b,how="inner")
    ref1=pd.merge(ref1,c,how="inner")
    ref1=pd.merge(ref1,d,how="inner")
    ref1=pd.merge(ref1,e,how="inner")
    ref=ref1.sort_values(by=['price_float'])
    c=pd.DataFrame(ref, columns=["id","name","summary","property_type","price_float","neighbourhood_cleansed","bedrooms","host_name","TV","wifi","clim","parking","elevator"])
    print("\nThere are", c.shape[0], "housings available with the selected amenities.\n")
    return c


############# Choix de période de vacances ##################


def demander_date(): #On récupère les dates souhaitées
    
    print("\nChoose a date between <2016-01-04> and <2017-01-02>.","\n")
    
    debut = input("\nWhen will your vacation start ?  (yyyy-mm-dd) \n\n")#date de début de séjour
    fin = input("\nWhen will your vacation end ? (yyyy-mm-dd) \n\n")#date de fin de séjour
    
    #faire respecter le format:
    calendar.sort_values(by='date') # trie par date croissante
    if(len(debut)!=10)or(len(fin)!=10):#Si le format n'est pas respecté (yyyy-mm-dd)
        print("\n Please use the assigned format. Retry \n")
        return demander_date()
    
    if (debut[4] != '-') or (debut[7] != '-') or (fin[4] != '-')  or (fin[7] != '-') : 
        print("\n Please type in the assigned format. Retry\n")
        return demander_date()#redemande d'écrire les dates si ce format n'est pas respecté
    
    #transforme les dates en datetime
    debut_time = dt.datetime.strptime(debut, "%Y-%m-%d").date()
    fin_time = dt.datetime.strptime(fin, "%Y-%m-%d").date()
    
    # on doit récupérer les id qui sont disponibles tous les jours entre le debut et la fin
    
    diff = fin_time - debut_time # durée du séjour
    duree = str(diff) # str pcq c'est en datetime
    duree = duree.split(' ') #split par espace et récupère le 1er élément car "1 day, 00:00:00"
    
    if  debut_time==fin_time:# on ne peut pas rester 0 jour
        print("\nYou can go on a vacation for 0 days, please retry.\n")
        return demander_date()
    if (int(duree[0]) < 0) and ((fin < '2016-01-04') or (debut > '2017-01-02')):
        print("\nThere is nothing available for the requested period and you have switched the start date and end date of your stay, please retry.\n")
        return demander_date()
              
    
    if (int(duree[0]) < 0)  :#date de début et de fin inversées
        print("\nYou have switched the start date and end date of your stay, We will swap it automatically.\n")
        swap1=debut
        swap2=fin
        debut=swap2
        fin=swap1
        
        debut_time = dt.datetime.strptime(debut, "%Y-%m-%d").date()
        fin_time = dt.datetime.strptime(fin, "%Y-%m-%d").date()
        
        diff = fin_time - debut_time 
        duree = str(diff) 
        duree = duree.split(' ')
        
        ligne_date = calendar.loc[(calendar["date"] <= fin) & (calendar["date"] >= debut) & (calendar["dispo"] == 1)] # affiche les lignes qui correspondent aux dates et disponibles
        liste_id = ligne_date['listing_id'].drop_duplicates().dropna().tolist() # récupère les id dispo et met dans les listes
    
        liste_id_definitive = [] # liste vide pour stocker les bon id
        for i in (liste_id):    
            df = ligne_date.loc[ligne_date["listing_id"] == i] # on veut les lignes des df qui correspondent à l'id et qui soit dispo
            if df.shape[0] ==  int(duree[0]) : #durée du séjour
                liste_id_definitive += [i] # on récupère les id des logements qui sont dispo tous les jours du séjour
        
        print("\nThere are",len(liste_id_definitive),"housings avaible between", debut,"and",fin,".\n")
    
        return liste_id_definitive
    
    if (debut < '2016-01-04') or (fin > '2017-01-02') : #date hors calendrier disponible
        print("\nThere is nothing available for the requested period, please retry.\n")
        return demander_date()     
    
    else :
    
        ligne_date = calendar.loc[(calendar["date"] <= fin) & (calendar["date"] >= debut) & (calendar["dispo"] == 1)] # affiche les lignes qui correspondent aux dates et disponibles
        liste_id = ligne_date['listing_id'].drop_duplicates().dropna().tolist() # récupère les id dispo et met dans les listes
    
        liste_id_definitive = [] # liste vide pour stocker les bon id
        for i in (liste_id):    
            df = ligne_date.loc[ligne_date["listing_id"] == i] # on veut les lignes des df qui correspondent à l'id et qui soit dispo
            if df.shape[0] ==  int(duree[0]) : #durée du séjour
                liste_id_definitive += [i] # on récupère les id des logements qui sont dispo tous les jours du séjour
        
        print("\nThere are",len(liste_id_definitive),"housings avaible between", debut,"and",fin,".\n")
    
        return liste_id_definitive


def logement_dispo(): #trouver des locations en fonction de la période donnée
    liste = demander_date() # récupère les id
    #affiche les lignes qui correspondent aux logements des dates demandées
    # isin(liste) : pour dire qu'on veut ceux de cette liste, raccourci
    annonce = listings.loc[listings["id"].isin(liste), ["id","name","summary","property_type","price_float","neighbourhood_cleansed","bedrooms","host_name"]]
    annonce=annonce.sort_values(by=['price_float'])
    return annonce


######################################################

################# Recherche ########################

############## Quelles options le client veut-il personnaliser ? ############

def reponseBudget(): #fonction qui demande au client s'il souhaite choisir un budget personnalisé
    print("\nAnswer by <yes> or <no>","\n")
    b=input("\nDo you want to select a specific budget?\n\n ").lower()
    if (b=="yes")or(b=="oui"):
        return 1
    if (b=="non")or(b=="no"):
        return 0
    else:
        print("\nCannot understand.\n")
        return reponseBudget()
    
def reponseLogement():
    print("\n","Answer by <yes> or <no>","\n")
    b=input("\nDo you want to select a particular type of housing?\n\n ").lower()
    if (b=="yes")or(b=="oui"):
        return 1
    if (b=="non")or(b=="no"):
        return 0
    else:
        print("\nCannot understand.\n")
        return reponseLogement()
    
def reponseQuart():
    print("\n","Answer by <yes> or <no>","\n")
    b=input("\nDo you want to select a specific neighbourhood?\n\n ").lower()
    if (b=="yes")or(b=="oui"):
        return 1
    if (b=="non")or(b=="no"):
        return 0
    else:
        print("\nCannot understand.\n")
        return reponseQuart()
    
def reponseInsta():
    print("\n","Answer by <yes> or <no>","\n")
    b=input("\nDo you want to select specific installations (Wifi, Air Conditionning, TV,...) ?\n\n ").lower()
    if (b=="yes")or(b=="oui"):
        return 1
    if (b=="non")or(b=="no"):
        return 0
    else:
        print("\nCannot understand.\n")
        return reponseInsta()
    
def reponsePeriode():
    print("\n","Answer by <yes> or <no>","\n")
    b=input("\nDo you want to select a specific time period ?\n\n ").lower()
    if (b=="yes")or(b=="oui"):
        return 1
    if (b=="non")or(b=="no"):
        return 0
    else:
        print("\nCannot understand.\n")
        return reponsePeriode()
    
    
############# Fonction de recherche finale #########################

def recherche():
    stock=[0,0,0,0,0]#stock=[prix,logement,quartier,installation,période]
    stock=[reponseBudget(),reponseLogement(),reponseQuart(),reponseInsta(),reponsePeriode()] 
    
    a=pd.DataFrame(listings, columns=["id","name","summary","property_type","price_float","neighbourhood_cleansed","bedrooms","host_name","TV","wifi","clim","parking","elevator"])
    b=pd.DataFrame(listings, columns=["id","name","summary","property_type","price_float","neighbourhood_cleansed","bedrooms","host_name","TV","wifi","clim","parking","elevator"])
    c=pd.DataFrame(listings, columns=["id","name","summary","property_type","price_float","neighbourhood_cleansed","bedrooms","host_name","TV","wifi","clim","parking","elevator"])
    d=pd.DataFrame(listings, columns=["id","name","summary","property_type","price_float","neighbourhood_cleansed","bedrooms","host_name","TV","wifi","clim","parking","elevator"])
    e=pd.DataFrame(listings, columns=["id","name","summary","property_type","price_float","neighbourhood_cleansed","bedrooms","host_name","TV","wifi","clim","parking","elevator"])
    if stock[0]==1:#si il veut séléctionner un budget alors on appelle la fonction pricenight
        #pour choisir budget et voir ce qui correspond
        a=pricenight()
    if stock[1]==1:
        b=proptype()
    if stock[2]==1:
        c=quartype()
    if stock[3]==1:
        d=instatype()
    if stock[4]==1:
        e=logement_dispo()
        
    #ici même principe que pour les amenities ( installations). Pour éviter de faire tout les cas en fonction de ce que le client a sélectionné on effectue un inner merge avec la liste entière
    #(pour A inclus dans R, A inner merge R = A)
    final=pd.merge(a,b,how="inner")
    final=pd.merge(final,c,how="inner")
    final=pd.merge(final,d,how="inner")
    final=pd.merge(final,e,how="inner")
    
    if final.shape[0]==0: #cas où rien n'a pu être trouvé
        print("\nNothing could be found according to your choices, please retry", "\n")
        return recherche()
    
    print("\nThere are", final.shape[0], "housings available.\n")
    
    return final.sort_values(by=['price_float'])












