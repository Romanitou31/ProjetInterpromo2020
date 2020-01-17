#!/usr/bin/env python
# coding: utf-8

# <h1>Group 1 - Data Collection<span class="tocSkip"></span>

# # Introduction

# One of the sources we need to scrap was the Airlinequality website. This notebook contains the code to retrieve the data and also the Robot to retrieve the data once a week. We scrapped the comments of air travellers. They contain the person's opinion of their flight as well as various notes about the airport and its components. We also collected the date of his flight and his overall rating.
# 
# #### V0 : basic scrap
# We only retrieve the title and description of the comment. We also have the notes (not yet processable).
# 
# #### V1 : Feature adding 
# Starting the treatment. 
# Notable categories can be used (NA not taken into account).
# Mini-function to switch pages (depending on the total number of comments). Consideration of new categories for the data dictionary.
# 
# #### V2 : Generalization
# 
# Bug on number pages corrected.Scrap on all airports.
# Note "N/A" Ok.
# 
# #### V3 : Add Information
# 
# Add Date_Review
# 
# #### V4 : Automatization
# 
# Begin of respect of quality chart. Scrap over a given number of days + date format changed 
# 
# #### V5 : Automatization
# 
# Translate of description and title comments. JSON management (we complete it instead of overwriting it).

# # Environment

# ## Libraries

# In[8]:


import re
import json
import requests
import numpy as np
import pandas as pd
from textblob import TextBlob
from langdetect import detect
from bs4 import BeautifulSoup as bs
from urllib.request import Request, urlopen
from datetime import date, datetime, timedelta


# ## Data Loading

# ## Functions

# This part contains all the functions we developped during the project

# In[1]:


def getAirportLinks(text_airport: str):
    """ Airport Recovery 
    Parmeters: 
        text_airport = description of airport
    Outers:
        airport = name of airport
        link = link of airport
    """ 
    airport = re.findall("\">(.*?)</a></li>", str(text_airport))[0]
    link = re.findall("href\=(.*?)>", str(text_airport))[0].replace("\"", "")
    return airport, link


def createDictionnary():
    """  Creation of the dictionary containing the name of the airport and its URL 
    Outers: 
        dic = dictionnary having the name of airport and link
    """
    dic = {}
    root = "https://www.airlinequality.com"
    url_page = root+"/review-pages/a-z-airport-reviews/"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
    req = Request(url_page, headers=headers)
    webpage = urlopen(req).read()
    soup = bs(webpage, 'html.parser')

    r = soup.find_all('li')
    list_text = [str(val) for val in r if "href=\"/airport-reviews/" in str(val)
                 and "article" not in str(val)]
    for texte in list_text:
        airport, link = getAirportLinks(texte)
        dic[airport.rstrip()] = root+link

    return dic


# In[ ]:


def translate (texte: str) : 
    """
    Paramters:
        texte = Text to be translated
    Outers:
        new = Text translated
    """
    try :
        new = str(TextBlob(texte).translate(to='en'))
        return new
    except :
        return texte


# In[ ]:


def recovTextBetweenTags(texts: str, separator: str):
    """ Retrieving code between two tags
    
    Paramters:
        texts = Part of soup
        separator = Separator of soup
    Outers:
        description = Text wanted
    """ 
    text_clean = []
    lisI = []
    lisS = []

    for i in range(0, len(texts)):
        if str(texts[i]) == "<":
            lisI.append(i)
        if texts[i] == '>':
            lisS.append(i)

    len_lis = len(lisI)
    for h in range(0, len_lis):
        if h < (len_lis-1):
            text_clean.append(texts[lisS[h]:lisI[h+1]])

    if separator != 'non':
        description = str(text_clean).replace('>', '').replace(
            ',', '').replace('\'', '').replace('，', '')
        description = description.split(separator)
    else:
        description = text_clean

    return description


# In[ ]:


def scrap(dic: dict, nb: int):
    """ Code allows to recup datas. 
        Calling up all other functions.
    Paramters: 
        dic = dictionnary having name and link airport
    Outer:
        dataAirline = dataFrame having scrap informations

    """
    name_col = ['Data_Source', 'Airline_Name', 'Airline_Type', 'Region_Operation', 'Aircraft_Type', 'Cabin_Class', 'Type_Of_Lounge',
                'Type_Of_Traveller', 'Date_Visit', 'Date_Flown', 'Airport', 'Route', 'Category', 'Category_Detail',
                'Cabin_Staff_Service', 'Lounge_Staff_Service', 'Bar_And_Beverages', 'Food_And_Beverages', 'Ground_Service', 'Catering', 'Cleanliness',
                'Lounge_Comfort', 'Aisle_Space', 'Wifi_And_Connectivity', 'Inflight_Entertainment', 'Viewing_Tv_Screen', 'Power_Supply',
                'Seat', 'Seat_type', 'Seat_Comfort', 'Seat_Legroom', 'Seat_Storage', 'Seat_Width', 'Seat_Recline', 'Washrooms',
                'Value_For_Money', 'Overall_Customer_Rating', 'Overall_Service_Rating', 'Overall_Airline_Rating',
                'Recommended', 'Departure_city', 'Arrival_city', 'Nb_bus_taken', 'Nb_train_taken',
                'Nb_car_taken', 'Nb_plane_taken', 'Duration', 'Price_min', 'Price_max', 'Nb_sharing', 'Awards', 'Registration', 'Language',
                'Queuing Times', 'Terminal_Seating', 'Terminal Signs', 'Airport_Shopping', 'Experience_At_Airport', 'Date_Review']

    dataAirline = pd.DataFrame(columns=name_col)

    for dic_key, dic_val in dic.items():
        r = requests.get(dic_val)
        page = r.text
        soup = bs(page, 'html.parser')
        nb_page = Nb_pages(soup)

        for j in range(1, nb_page+1):
            r = requests.get(dic_val + '/page/' + str(j) + '/')
            page = r.text
            soup = bs(page, 'html.parser')

            Date_Review = dateReview(soup, nb)
            title = title_comm(soup, nb)
            desc = description(soup, nb)
            note = UserNot(soup, nb)
            notGlo = NoteGlobal(soup, nb)

            airport = []
            source = []

            for i in range(0, len(desc)):
                airport.append(dic_key)
                source.append('AirlineQuality')

            df = pd.DataFrame(data=[title, desc, note, airport])
            df = df.transpose()

            Title = df[0]
            Review = df[1]
            Date_Visit, Terminal_Cleanliness, Food_Beverages, Wifi_Connectivity, Airport_Staff, Recommended, Type_Of_Traveller, Queuing_Times, Terminal_Seating, Terminal_Signs, Airport_Shopping, Experience_At_Airport = transformColInDic(
                df[2])
            Airport = df[3]

            df_template = pd.DataFrame({'Data_Source': source, 'Date_Flown': Date_Visit, 'Cleanliness': Terminal_Cleanliness, 'Food_And_Beverages': Food_Beverages,
                                        'Wifi_And_Connectivity': Wifi_Connectivity, 'Cabin_Staff_Service': Airport_Staff, 'Overall_Customer_Rating': notGlo,
                                        'Recommended': Recommended, 'Title': Title, 'Review': Review, 'Airport': Airport, 'Type_Of_Traveller': Type_Of_Traveller,
                                        'Queuing_Times': Queuing_Times, 'Terminal_Seating': Terminal_Seating, 'Terminal_Signs': Terminal_Signs,
                                        'Airport_Shopping': Airport_Shopping, 'Experience_At_Airport': Experience_At_Airport, 'Date_Review': Date_Review})

            dataAirline = pd.concat([dataAirline, df_template])

    return dataAirline


# In[5]:


def UserNot(soup: str, nb: int):
    """ Function to retrieve users' notes using the two notes functions. 
        The first one retrieves the maximum notes for each user. 
        The second one retrieves the category 'NA' 

    """
    list_not = notation2(soup, nb)
    noteUser = []
    value = []
    list_total = [' 1', '2', '3', '4', '5']

    for z in range(0, len(list_not)):
        dico = {}
        # Delete of the first element because it's not a user
        del list_not[z][0]
        # We look if the next note is a value, if yes we take it because when we scrape, we recover the whole list of the barem 
        # (ex: we note a 4, we recover 12345. Each noted category is separated by non-numeric characters.
        for i in range(0, len(list_not[z])-2):
            if len(str(list_not[z][i]).replace(' ', '')) > 1:
                if len(str(list_not[z][i+1]).replace(' ', '')) > 1:
                    if list_not[z][i] not in value:
                        dico[list_not[z][i]] = list_not[z][i+1]
                        value.append(list_not[z][i+1])
                else:
                    # The last value of the note list
                    j = i
                    while str(list_not[z][j+1]) in list_total:
                        dico[list_not[z][i]] = list_not[z][j+1]
                        j = j + 1
        noteUser.append(dico)

    counter_user = 0
    c_user_not_w_NA = 0
    p = notation(soup, nb)
    for k in noteUser:
        value = []
        # Counter of notes for all users
        t = 0
        for key, val in k.items():
            if val != 'N/A':
                if val == '5':
                    # The category detected by the previous code takes as a note the value scrapped by the function "notation"
                    noteUser[counter_user][key] = p[c_user_not_w_NA][t]
                    t = t + 1
                    if t == len(p[c_user_not_w_NA]):
                        c_user_not_w_NA = c_user_not_w_NA + 1

        counter_user = counter_user + 1
    return noteUser


# In[6]:


# Transform a date to standard format
def format_date(date):
    # Transform a string date into a standard format by trying each
    # date format. If you want to add a format, add a try/except in the
    # last except
    # date : str : the date to transform
    # return : m : timedata : format is YYYY-MM-DD HH:MM:SS
    date_str = date
    #
    date_str = date_str.replace("st", "").replace("th", "").replace(
        "nd", "").replace("rd", "").replace(" Augu ", " Aug ")
    m = None
    try:
        m = datetime.strptime(date_str, "%d %B %Y")
    except ValueError:
        try:
            m = datetime.strptime(date_str, "%d %b %Y")
        except ValueError:
            try:
                m = datetime.strptime(date_str, "%Y/%m/%d")
            except ValueError:
                try:
                    m = datetime.strptime(date_str, "%d/%m/%Y %H:%M:%S")
                except ValueError:
                    try:
                        m = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
                    except ValueError:
                        try:
                            m = datetime.strptime(date_str,
                                                  "%d %m %Y")
                        except ValueError:
                            # HERE ADD A FORMAT TO CHECK
                            print("Format not recognised. \nConsider "
                                  "adding a date format "
                                  "in the function \"format_date\".")

    return m


# In[7]:


def transformColInDic(col_dic: dict):
    """ Transforms a dictionary into a set of lists in order to put them in the dataframe.
    Parameters:
        col_dic = columns
    Outers:
        Date_Visit = Date of comment
        Terminal_Cleanliness = Confort of seat
        Food_Beverages = Quality of food and beverages
        Wifi_Connectivity = Quality of connection
        Airport_Staff = Competence of airport staff
        Recommended = Recommandation of user
        Type_Of_Traveller = Situation of user (couple, single)
        Queuing_Times = Notation of Queuing Times in the airport
        Terminal_Seating = Confort of terminal seat 
        Terminal_Signs = Quality of terminal signs
        Airport_shopping = Quality of airport shopping
        Experience_At_Airport = Depart or arrival in the airport
    """
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

    for i in range(0, len(col_dic)):
        if 'Date Visit' in (col_dic[i]).keys():
            Date_Visit.append((col_dic[i]['Date Visit']))
        else:
            Date_Visit.append(' ')

        if ' Terminal Cleanliness' in (col_dic[i]).keys():
            Terminal_Cleanliness.append((col_dic[i][' Terminal Cleanliness']))
        else:
            Terminal_Cleanliness.append(' ')

        if ' Food Beverages' in (col_dic[i]).keys():
            Food_Beverages.append((col_dic[i][' Food Beverages']))
        else:
            Food_Beverages.append(' ')

        if ' Wifi Connectivity' in (col_dic[i]).keys():
            Wifi_Connectivity.append((col_dic[i][' Wifi Connectivity']))
        else:
            Wifi_Connectivity.append(' ')

        if ' Airport Staff' in (col_dic[i]).keys():
            Airport_Staff.append((col_dic[i][' Airport Staff']))
        else:
            Airport_Staff.append(' ')

        if ' Recommended' in (col_dic[i]).keys():
            Recommended.append((col_dic[i][' Recommended']))
        else:
            Recommended.append(' ')

        if 'Type Of Traveller' in (col_dic[i]).keys():
            Type_Of_Traveller.append((col_dic[i]['Type Of Traveller']))
        else:
            Type_Of_Traveller.append(' ')

        if 'Queuing Times' in (col_dic[i]).keys():
            Queuing_Times.append((col_dic[i]['Queuing Times']))
        else:
            Queuing_Times.append(' ')

        if ' Terminal Seating' in (col_dic[i]).keys():
            Terminal_Seating.append((col_dic[i][' Terminal Seating']))
        else:
            Terminal_Seating.append(' ')

        if ' Airport Shopping' in (col_dic[i]).keys():
            Airport_shopping.append((col_dic[i][' Airport Shopping']))
        else:
            Airport_shopping.append(' ')

        if ' Terminal Signs' in (col_dic[i]).keys():
            Terminal_Signs.append((col_dic[i][' Terminal Signs']))
        else:
            Terminal_Signs.append(' ')

        if 'Experience At Airport' in (col_dic[i]).keys():
            Experience_At_Airport.append((col_dic[i]['Experience At Airport']))
        else:
            Experience_At_Airport.append(' ')

    return Date_Visit, Terminal_Cleanliness, Food_Beverages, Wifi_Connectivity, Airport_Staff, Recommended, Type_Of_Traveller, Queuing_Times, Terminal_Seating, Terminal_Signs, Airport_shopping, Experience_At_Airport


# In[8]:


def notation(soup: str, nb:int):
    """
    Retrieving notes from the table on the Airline page
    Parameters:
        soup: soup of the page
        nb: number of days for recovery for scraping
    Outers:
        note = note of users for each category
    """
    note = []
    for span in soup.findAll('article', attrs={'itemprop': 'review'}):
        dat = str(recovTextBetweenTags(str(span.findAll('time', attrs={
                  'itemprop': 'datePublished'})), ',')).replace("['[", '').replace("]']", '')
        dat = (format_date(dat))
        
        if (dat) > (datetime.now() - timedelta(nb)):
            tab_not = span.findAll('span', attrs={'class': 'star fill'})
            notation_categ = re.findall(r'[0-9]', str(tab_not))
            if len(notation_categ) > 0:
                noteUser = []
                len_not_categ = len(notation_categ)
                for i in range(0, len_not_categ-1):
                    if notation_categ[i] >= notation_categ[i+1]:
                        noteUser.append(notation_categ[i])

                noteUser.append(notation_categ[len_not_categ-1])
                note.append(noteUser)
    
    return note


# In[9]:


def title_comm(soup: str, nb:int):
    """
    Recovery of title comment
    Parameters:
        soup = soup of the page
        nb = number of days for recovery for scraping
    Outers:
        title = title comment 
    """
    title = []
    for span in soup.findAll('article', attrs={'itemprop': 'review'}):
        dat = str(recovTextBetweenTags(str(span.findAll('time', attrs={
                  'itemprop': 'datePublished'})), ',')).replace("['[", '').replace("]']", '')
        dat = (format_date(dat))
        if (dat) > (datetime.now() - timedelta(nb)):
            top = span.findAll('h2', attrs={'class': 'text_header'})
            top = translate(recovTextBetweenTags(str(top), 'non'))
            title.append(top[0][1:len(top[0])])

    return title


# In[10]:


def dateReview(soup: str, nb:int):
    """
    Recovery of Date comment
    Parameters:
        soup = soup of the page
        nb = number of days for recovery for scraping
    Outers:
        dateR = date comment 
    """
    dateR = []
    for span in soup.findAll('article', attrs={'itemprop': 'review'}):
        dat = str(recovTextBetweenTags(str(span.findAll('time', attrs={
                  'itemprop': 'datePublished'})), ',')).replace("['[", '').replace("]']", '')
        dat = (format_date(dat))

        if (dat) > (datetime.now() - timedelta(nb)):
            top = span.findAll('time', attrs={'itemprop': 'datePublished'})
            dateR.append(recovTextBetweenTags(str(top), ','))

    return dateR


# In[11]:


def NoteGlobal(soup: str, nb: int):
    """
    Recovery of Note Global
    Parameters:
        soup = soup of the page
        nb = number of days for recovery for scraping
    Outers:
        notGlo = Note Global 
    """
    notGlo = []
    for span in soup.findAll('article', attrs={'itemprop': 'review'}):
        dat = str(recovTextBetweenTags(str(span.findAll('time', attrs={
                  'itemprop': 'datePublished'})), ',')).replace("['[", '').replace("]']", '')
        dat = (format_date(dat))
        if (dat) > (datetime.now() - timedelta(nb)):
            top = span.findAll('span', attrs={'itemprop': 'ratingValue'})
            notGlo.append(recovTextBetweenTags(str(top), ','))

    return notGlo


# In[12]:


def description(soup: str, nb:int):
    """
    Recovery of description trip
    Parameters:
        soup = soup of the page
        nb = number of days for recovery for scraping
    Outers:
        desc = description of fly
    """
    desc = []
    for span in soup.findAll('article', attrs={'itemprop': 'review'}):
        dat = str(recovTextBetweenTags(str(span.findAll('time', attrs={
                  'itemprop': 'datePublished'})), ',')).replace("['[", '').replace("]']", '')
        dat = (format_date(dat))
        if (dat) > (datetime.now() - timedelta(nb)):
            top = span.findAll('div', attrs={'class': 'text_content'})
            desc.append(translate(recovTextBetweenTags(str(top), ',')))

    return desc


# In[13]:


def notation2(soup: str, nb:int):
    note = []
    for span in soup.findAll('article', attrs={'itemprop': 'review'}):
        
        dat = str(recovTextBetweenTags(str(span.findAll('time', attrs={
                  'itemprop': 'datePublished'})), ',')).replace("['[", '').replace("]']", '')
        dat = (format_date(dat))
        if (dat) > (datetime.now() - timedelta(nb)):
            
            not_tot_tab = span.findAll('table', attrs={'class': 'review-ratings'})
            not_tot_tab = (recovTextBetweenTags(str(not_tot_tab), ','))
            note.append(str(str(not_tot_tab).replace(
                '\\n', '').replace('\\', '')).split('  '))

    Rating = []
    for elem in note:
        if len(elem) != 0:
            Rating.append(elem)

    return Rating


# In[14]:


def Nb_pages(soup: str):
    """
    Calcul of number page of airport comments
    Parameters:
        soup = soup of the page
    Outers:
        nb_pages = number page of airport comments
    """
    nb_page_total = soup.find('div', attrs={'class': 'pagination-total'})
    if nb_page_total != None:
        nb_page_total = str(nb_page_total)
        nb_pages = int(nb_page_total[41:len(nb_page_total)-14])//10 + 1
    else:
        nb_pages = 1
    return(nb_pages)


# In[15]:


def addJSON(file: str, df, creat: bool):
    """
    Add of dataFrame in an existant JSON
    Parameters:
        file = path of JSON
        df = dataFrame of news datas
    """
    if creat is False :
        with open(file) as train_file:
            dict_train = json.load(train_file)
        data = pd.read_json(dict_train, orient="records")
        df = pd.concat([data, df])
    
    js = df.to_json(orient='records').replace(
        "[\\\"[", '').replace("]\\\"]", '')
    
    with open(file, 'w', encoding='utf8') as outfile:
        json.dump(js, outfile, ensure_ascii=False, indent=4)


# # Crawl

# This part contains the crawl of AirlineQuality website with the execution of all functions 

# In[ ]:


# Creation of dictionnary having airports names and airports URL
dic = createDictionnary()
# Starting the scrap function
df = scrap(dic, 20000)
# Transformation and Complete of Json
addJSON(file, df, True)


# # Descriptive statistics on recovered data

# In[9]:


file ='../RESULTATS_JSON/data_Airline.json'

with open(file) as train_file:
    dict_train = json.load(train_file)
data = pd.read_json(dict_train, orient="records")


# ##### A complet Airline scraping:

# 82,5 Mo with
# 38002 rows X 63 columns (18 columns not NA)

# In[62]:


lis = ['Cleanliness','Food_And_Beverages', 'Wifi_And_Connectivity','Cabin_Staff_Service',
        'Queuing_Times','Terminal_Seating','Terminal_Signs','Airport_Shopping']

for j in lis:    
    cl = []
    for i in data[j].transpose():
        if i != ' ': 
            if i != ' N/A':
                cl.append(int(i))

    print(j)            
    print('moy', np.mean(cl))
    print('med', np.median(cl))
    print('min', np.min(cl))
    print('max', np.max(cl))
    print('ecart-type', np.std(cl))
    print('')

