#!/usr/bin/env python
# coding: utf-8

# ### Importations 

# In[1]:


import urllib.request
import urllib.parse
import urllib.error
from bs4 import BeautifulSoup
# import ssl
import json
# import ast
# import os
from urllib.request import Request, urlopen
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re
import pandas as pd
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs
import requests
from langdetect import detect
from datetime import date, datetime, timedelta


# ### Lancement du scrapping + Enregistrement en json

# In[3]:


def getAirportLinks(texte):
    # Récupération des aéroports
    airport = re.findall("\">(.*?)</a></li>", str(texte))[0]
    link = re.findall("href\=(.*?)>", str(texte))[0].replace("\"", "")
    return airport, link


def createDictionnary():
    # Création du dictionnaire contenant le nom de l'aéroport ainsi que son URL
    dic = {}
    racine = "https://www.airlinequality.com"
    url_page = racine+"/review-pages/a-z-airport-reviews/"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
    req = Request(url_page, headers=headers)
    webpage = urlopen(req).read()
    soup = BeautifulSoup(webpage, 'html.parser')

    r = soup.find_all('li')
    liste_text = [str(val) for val in r if "href=\"/airport-reviews/" in str(val)
                  and "article" not in str(val)]
    for texte in liste_text:
        airport, link = getAirportLinks(texte)
        dic[airport.rstrip()] = racine+link

    return dic


dic = createDictionnary()


# In[4]:


def recupTexteEntreBalise(texte, separateur):
    # Récupération du code entre deux balises
    texte2 = []
    lisI = []
    lisS = []

    for i in range(0, len(texte)):
        if str(texte[i]) == "<":
            lisI.append(i)
        if texte[i] == '>':
            lisS.append(i)

    taille = len(lisI)
    for h in range(0, taille):
        if h < (taille-1):
            texte2.append(texte[lisS[h]:lisI[h+1]])

    if separateur != 'non':
        description = str(texte2).replace('>', '').replace(
            ',', '').replace('\'', '').replace('，', '')
        description = description.split(separateur)
    else:
        description = texte2

    return description


# In[5]:


def corp(dic):
    # 
    nom_col = ['Airline_Name', 'Airline_Type', 'Region_Operation', 'Aircraft_Type', 'Cabin_Class', 'Type_Of_Lounge',
               'Type_Of_Traveller', 'Date_Visit', 'Date_Flown', 'Airport', 'Route', 'Category', 'Category_Detail',
               'Cabin_Staff_Service', 'Lounge_Staff_Service', 'Bar_And_Beverages', 'Food_And_Beverages', 'Ground_Service', 'Catering', 'Cleanliness',
               'Lounge_Comfort', 'Aisle_Space', 'Wifi_And_Connectivity', 'Inflight_Entertainment', 'Viewing_Tv_Screen', 'Power_Supply',
               'Seat', 'Seat_type', 'Seat_Comfort', 'Seat_Legroom', 'Seat_Storage', 'Seat_Width', 'Seat_Recline', 'Washrooms',
               'Value_For_Money', 'Overall_Customer_Rating', 'Overall_Service_Rating', 'Overall_Airline_Rating',
               'Recommended', 'Departure_city', 'Arrival_city', 'Nb_bus_taken', 'Nb_train_taken',
               'Nb_car_taken', 'Nb_plane_taken', 'Duration', 'Price_min', 'Price_max', 'Nb_sharing', 'Awards', 'Registration', 'Language',
               'Queuing Times', 'Terminal_Seating', 'Terminal Signs', 'Airport_Shopping', 'Experience_At_Airport', 'Date_Review']

    dataAirline = pd.DataFrame(columns=nom_col)

    for azerty, qsdfg in dic.items():
        r = requests.get(qsdfg)
        page = r.text
        soup = bs(page, 'html.parser')
        nb_page = Nb_pages(soup)

        for j in range(1, nb_page+1):
            r = requests.get(qsdfg+'/page/'+str(j)+'/')
            page = r.text
            soup = bs(page, 'html.parser')

            title = titre(soup)
            desc = description(soup)
            note = UserNot(soup)
            notGlo = NoteGlobale(soup)
            Date_Review = dateReview(soup)

            airport = []
            for i in range(0, len(desc)):
                airport.append(azerty)

            df = pd.DataFrame(data=[title, desc, note, airport])
            df = df.transpose()

            Title = df[0]
            Review = df[1]
            Date_Visit, Terminal_Cleanliness, Food_Beverages, Wifi_Connectivity, Airport_Staff, Recommended, Type_Of_Traveller, Queuing_Times, Terminal_Seating, Terminal_Signs, Airport_Shopping, Experience_At_Airport = dic_col(
                df[2])
            Airport = df[3]

            o = pd.DataFrame({'Date_Flown': Date_Visit, 'Cleanliness': Terminal_Cleanliness, 'Food_And_Beverages': Food_Beverages,
                              'Wifi_And_Connectivity': Wifi_Connectivity, 'Cabin_Staff_Service': Airport_Staff, 'Overall_Customer_Rating': notGlo,
                              'Recommended': Recommended, 'Title': Title, 'Review': Review, 'Airport': Airport, 'Type_Of_Traveller': Type_Of_Traveller,
                              'Queuing_Times': Queuing_Times, 'Terminal_Seating': Terminal_Seating, 'Terminal_Signs': Terminal_Signs,
                              'Airport_Shopping': Airport_Shopping, 'Experience_At_Airport': Experience_At_Airport, 'Date_Review': Date_Review})

            dataAirline = pd.concat([dataAirline, o])

    return dataAirline


# In[6]:


def UserNot(soup):
    liste = notation2(soup)
    noteUser = []
    value = []
    liste1 = [' 1', '2', '3', '4', '5']
    for z in range(0, len(liste)):
        dico = {}
        del liste[z][0]
        for i in range(0, len(liste[z])-2):
            if len(str(liste[z][i]).replace(' ', '')) > 1:
                if len(str(liste[z][i+1]).replace(' ', '')) > 1:
                    if liste[z][i] not in value:
                        dico[liste[z][i]] = liste[z][i+1]
                        value.append(liste[z][i+1])
                else:
                    j = i
                    while str(liste[z][j+1]) in liste1:
                        dico[liste[z][i]] = liste[z][j+1]
                        j = j+1
        noteUser.append(dico)

    y = 0
    f = 0
    p = notation(soup)
    for k in noteUser:
        value = []
        t = 0
        for cle, valeur in k.items():
            if valeur != 'N/A':
                if valeur == '5':
                    noteUser[y][cle] = p[f][t]
                    t = t + 1
                    if t == len(p[f]):
                        f = f + 1

        y = y+1
    return noteUser


# In[7]:


def dic_col(o):
    # Prend en paramètre la colonne du DF contenant le dictionnaire des notes
    Date_Visit = []
    Terminal_Cleanliness = []
    Food_Beverages = []
    Wifi_Connectivity = []
    Airport_Staff = []
    Recommended = []
    Type_Of_Traveller = []
    Queuing_Times = []
    Terminal_Seating = []
    Airport_shopping = []
    Terminal_Signs = []
    Experience_At_Airport = []

    for i in range(0, len(o)):
        if 'Date Visit' in (o[i]).keys():
            Date_Visit.append((o[i]['Date Visit']))
        else:
            Date_Visit.append(' ')

        if ' Terminal Cleanliness' in (o[i]).keys():
            Terminal_Cleanliness.append((o[i][' Terminal Cleanliness']))
        else:
            Terminal_Cleanliness.append(' ')

        if ' Food Beverages' in (o[i]).keys():
            Food_Beverages.append((o[i][' Food Beverages']))
        else:
            Food_Beverages.append(' ')

        if ' Wifi Connectivity' in (o[i]).keys():
            Wifi_Connectivity.append((o[i][' Wifi Connectivity']))
        else:
            Wifi_Connectivity.append(' ')

        if ' Airport Staff' in (o[i]).keys():
            Airport_Staff.append((o[i][' Airport Staff']))
        else:
            Airport_Staff.append(' ')

        if ' Recommended' in (o[i]).keys():
            Recommended.append((o[i][' Recommended']))
        else:
            Recommended.append(' ')

        if 'Type Of Traveller' in (o[i]).keys():
            Type_Of_Traveller.append((o[i]['Type Of Traveller']))
        else:
            Type_Of_Traveller.append(' ')

        if 'Queuing Times' in (o[i]).keys():
            Queuing_Times.append((o[i]['Queuing Times']))
        else:
            Queuing_Times.append(' ')

        if ' Terminal Seating' in (o[i]).keys():
            Terminal_Seating.append((o[i][' Terminal Seating']))
        else:
            Terminal_Seating.append(' ')

        if ' Airport Shopping' in (o[i]).keys():
            Airport_shopping.append((o[i][' Airport Shopping']))
        else:
            Airport_shopping.append(' ')

        if ' Terminal Signs' in (o[i]).keys():
            Terminal_Signs.append((o[i][' Terminal Signs']))
        else:
            Terminal_Signs.append(' ')

        if 'Experience At Airport' in (o[i]).keys():
            Experience_At_Airport.append((o[i]['Experience At Airport']))
        else:
            Experience_At_Airport.append(' ')

    return Date_Visit, Terminal_Cleanliness, Food_Beverages, Wifi_Connectivity, Airport_Staff, Recommended, Type_Of_Traveller, Queuing_Times, Terminal_Seating, Terminal_Signs, Airport_shopping, Experience_At_Airport


# In[8]:


def notation(soup):
    note = []
    for span in soup.findAll('article', attrs={'itemprop': 'review'}):
        toto = span.findAll('span', attrs={'class': 'star fill'})
        top = re.findall(r'[0-9]', str(toto))
        if len(top) > 0:
            noteUser = []
            taille = len(top)
            for i in range(0, taille-1):
                if top[i] >= top[i+1]:
                    noteUser.append(top[i])
            noteUser.append(top[taille-1])
            note.append(noteUser)
    return note


# In[9]:


def titre(soup):
    title = []
    for span in soup.findAll('article', attrs={'itemprop': 'review'}):
        top = span.findAll('h2', attrs={'class': 'text_header'})
        top = recupTexteEntreBalise(str(top), 'non')
        title.append(top[0][1:len(top[0])])

    return title


# In[10]:


def dateReview(soup):
    dateR = []
    for span in soup.findAll('article', attrs={'itemprop': 'review'}):
        top = span.findAll('time', attrs={'itemprop': 'datePublished'})

        dateR.append(recupTexteEntreBalise(str(top), ','))

    return dateR


# In[11]:


def NoteGlobale(soup):
    notGlo = []
    for span in soup.findAll('article', attrs={'itemprop': 'review'}):
        top = span.findAll('span', attrs={'itemprop': 'ratingValue'})
        notGlo.append(recupTexteEntreBalise(str(top), ','))

    return notGlo


# In[12]:


def description(soup):
    desc = []
    for span in soup.findAll('article', attrs={'itemprop': 'review'}):
        top = span.findAll('div', attrs={'class': 'text_content'})
        desc.append(recupTexteEntreBalise(str(top), ','))

    return desc


# In[13]:


def notation2(soup):
    note = []
    for span in soup.findAll('article', attrs={'itemprop': 'review'}):
        toto = span.findAll('table', attrs={'class': 'review-ratings'})
        toto = (recupTexteEntreBalise(str(toto), ','))
        note.append(str(str(toto).replace(
            '\\n', '').replace('\\', '')).split('  '))

    Rating = []
    for elem in note:
        if len(elem) != 0:
            Rating.append(elem)

    return Rating


# In[14]:


def Nb_pages(soup):
    toto = soup.find('div', attrs={'class': 'pagination-total'})
    if toto != None:
        toto = str(toto)
        nb_pages = int(toto[41:len(toto)-14])//10 + 1
    else:
        nb_pages = 1
    return(nb_pages)


# In[2]:


df = corp(dic)
js = df.to_json(orient='records').replace("[", '').replace("]", '')
with open('testWeibo.json', 'w', encoding='utf8') as outfile:
    json.dump(js, outfile, ensure_ascii=False, indent=4)

