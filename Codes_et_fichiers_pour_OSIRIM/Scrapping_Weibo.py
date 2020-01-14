#!/usr/bin/env python
# coding: utf-8

# ### Importations

# In[10]:


from bs4 import BeautifulSoup
import json
from urllib.request import Request, urlopen
import re
import pandas as pd
import datetime as dt
from textblob import TextBlob


# In[11]:


compagniesAeriennes=["American Airlines","Air Canada","Air France","Air Algerie","Air India","Aerolineas Argentinas","Royal Air Maroc","Finnair" ,"Alitalia "," Nouvelair","Air China","Cathay Pacific","Delta Airlines","Aer Lingus","Emirates","Ethiopian Airlines","Icelandair","Hawaiian Airlines","Iberia","Meridiana","Japan Airlines","KLM","Air Malta","Lan Airlines","Luxair","LIAT","LOT Polish Airlines","Air Madagascar","Air Mauritius","Austrian Airlines","Qatar Airways","South African Airways","SAS Scandinavian Airlines","Brussels Airlines","Singapore Airlines","Corsair","Aeroflot","Thai Airways","Turkish Airlines","TAP Portugal","Air Transat","Tunisair","Air Caraibes","United Airlines","Air Austral","Air Europa","Easyjet","Vietnam Airlines","Virgin Atlantic","Air Corsica","Condor","Flybe","Aegean Airlines","Air Tahiti Nui","Aigle Azur","HOP!","Jet Airways","Etihad Airways","Etihad Airways","Oman Air","XL Airways","Ryanair LTD","Vueling ","Norwegian","Transavia France","Germanwings","TUI Fly Belgium","Air Arabia","WOW air","Wizz Air","Air Asia","Volotea","southwest airlines"]
modelesBoeing=["Boeing 717","Boeing 727","Boeing 737-200","Boeing 737-300","Boeing 737-400","Boeing 737-500","Boeing 737-600","Boeing 737-700","Boeing 737-700ER","Boeing 737-800","Boeing 737-900","Boeing 737-900ER","Boeing 737 MAX 7","Boeing 737 MAX 8","Boeing 737 MAX 9","Boeing 737 MAX 10","Boeing 747-200","Boeing 747-400","Boeing 757-200","Boeing 757-300","Boeing 767-200","Boeing 767-300","Boeing 767-300ER","Boeing 767-400ER","Boeing 777 Triple Seven","Boeing 787 DreamLiner"]
modelesAirbus=["A300","A300-600ST","A318","A319","A320-100","A320-200","A320neo","A321-100","A321-200","A330-200","A330-300","A330-200F","A330-500","A340-200","A340-300","A340-500","A340-600","A350-900","A350-1000","A380-800","A220-300"]
motsCles=["trip","fly","plane","airplane","flight"]

equations=[]
for comp in compagniesAeriennes:
    for mod in modelesAirbus:
        equations.append('https://s.weibo.com/weibo/'+comp+'%2520'+mod)
    for mod in modelesBoeing:
        equations.append('https://s.weibo.com/weibo/'+comp+'%2520'+mod)


# In[12]:


def textToDate(text):
    
    if "今天" in text:
        return dt.date.today()
    chiffres = re.search("([0-9]*\w)*",text).group(0)
    chiffres=re.findall(r"([0-9]+)",chiffres)
    if len(chiffres)==3:
        year=chiffres[0]
        month=chiffres[1]
        day=chiffres[2]
        
    elif len(chiffres)==2:
        now=dt.date.today()
        year=now.year
        month=chiffres[0]
        day=chiffres[1]
    else:
        return dt.date.today()
    return dt.date(int(year), int(month), int(day))


# In[13]:


def recupTexteEntreBalise(texte, separateur):
    
    texte2 = []
    lisI = []
    lisS = []
    
    for i in range(0,len(texte)):
        if str(texte[i]) == "<":
            lisI.append(i)
        if texte[i] == '>':
            lisS.append(i)   

    taille = len(lisI)
    for h in range(0,taille):
        if h < (taille-1):
            texte2.append(texte[lisS[h]:lisI[h+1]])
    
    if separateur != 'non':
        description = str(texte2).replace('>','').replace(',','').replace('\'','').replace('，','')
        description = description.split(separateur)
    else:
        description = texte2
    
    return description


# In[14]:


def supprimeBlanc(Author):
    Author2 = []
    for elem in Author:
        if len(elem) != 0:
            Author2.append(elem)
    return Author2


# In[15]:


def recupWeibo(soup,date_comment,description,Author2, Partage,Comm,Like):
    
    nom_col = ['Data_Source','Airline_Name','Airline_Type','Region_Operation','Aircraft_Type','Cabin_Class','Type_Of_Lounge',
               'Type_Of_Traveller','Date_Visit','Date_Flown','Airport','Route','Category','Category_Detail',
               'Cabin_Staff_Service','Lounge_Staff_Service','Bar_And_Beverages','Food_And_Beverages','Ground_Service',
               'Catering','Cleanliness','Lounge_Comfort','Aisle_Space','Wifi_And_Connectivity','Inflight_Entertainment',
               'Viewing_Tv_Screen','Power_Supply','Date_publication'
              'Seat','Seat_type','Seat_Comfort','Seat_Legroom','Seat_Storage','Seat_Width','Seat_Recline','Washrooms',
               'Value_For_Money','Overall_Customer_Rating','Overall_Service_Rating','Overall_Airline_Rating',
              'Recommended','Departure_city','Arrival_city','Nb_bus_taken','Nb_train_taken',
               'Nb_car_taken','Nb_plane_taken','Duration','Price_min','Price_max','Nb_sharing','Awards',
               'Registration','Language']
    df = pd.DataFrame(columns = nom_col)
    
    detailVideos = {}

    detailVideos['Description'] = description
    detailVideos['Author'] = Author2
    detailVideos['Nb_sharing'] = Partage
    detailVideos['Likes'] = Like
#     detailVideos['Date3']= Date3
    detailVideos['Date_publication']= str(date_comment)

    with open('../RESULTATS_JSON/data_Weibo.json', 'a', encoding='utf8') as outfile:
        json.dump(detailVideos, outfile, ensure_ascii=False, indent=4)


# In[16]:


equations


# In[7]:


nb_day = 365
listURL = equations

with open('../RESULTATS_JSON/data_Weibo.json', 'w', encoding='utf8') as outfile :
    json
    
# for url in listURL :
for i in range(0,len(listURL)) :
    url = listURL[i] 
    #20 post
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    web_page = urlopen(req).read()
    soup = BeautifulSoup(web_page, 'html.parser')
    compteur = 0

    #     description

    texte = str(soup.findAll('p',attrs={'node-type':'feed_list_content'}))
    description = recupTexteEntreBalise(texte, '\\n')
    del description[0]


    #     autheur

    auteur = soup.findAll('a',attrs={'class':'name'})
    auteur = str(auteur)
    Author = recupTexteEntreBalise(auteur, ' ')
    Author2 = supprimeBlanc(Author)

    # Partage / Commentaire, Avis / Like
    aime = soup.findAll('div',attrs={'class':"card-act"})
    aime = str(aime)
    aime2 = recupTexteEntreBalise(aime, 'non')

    Partage = []
    Comm = []
    Like = []

    for i in range(0,len(aime2)):
        if aime2[i].startswith('> 转发'):
            Partage.append(str(re.findall(r'[0-9]+',str(aime2[i]))).replace('[','').replace(']','').replace('\'',''))
        if aime2[i].startswith('>评论'):
            Comm.append(str(re.findall(r'[0-9]+',str(aime2[i]))).replace('[','').replace(']','').replace('\'',''))
        test = re.findall(r'>[0-9]+',aime2[i])
        if (str(test))!='[]':
            test = re.findall(r'[0-9]+',str(test))
            Like.append(str(test).replace('[','').replace(']','').replace('\'','').replace('>',''))
        else:
            if aime2[i-7].startswith('>评论'):
                Like.append(str(aime2[i]).replace('[','').replace(']','').replace('\'','').replace('>',''))


    for span1 in soup.findAll('p', attrs={'class' : 'from'}):
        for span in span1.findAll('a', attrs={'target' : '_blank'}):
            if textToDate(span.text.strip()) >= (dt.date.today() - dt.timedelta(days=(nb_day))):
                if compteur < len(Partage)-1:
                    (recupWeibo(soup,textToDate(span.text.strip()),description[compteur],Author2[compteur], Partage[compteur],Comm[compteur],Like[compteur]))

        compteur += 1

    print('fini')


# In[ ]:




