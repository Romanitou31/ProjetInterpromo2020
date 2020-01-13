#!/usr/bin/env python
# coding: utf-8

# In[38]:


# Created on 09/01/2020
# Group1
# @authors: benjamin anton

import json
import re
from datetime import datetime, timedelta,date
import time
import requests
from urllib.request import Request, urlopen
from textblob import TextBlob
from langdetect import detect
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# In[39]:


def translate (texte) : 
    try :
        new = str(TextBlob(texte).translate(to='en'))
        return new
    except :
        return texte
    
def replace_all(text, dic):
    for i, j in dic.items():
        text = text.replace(i, j)
    return text


# In[40]:


def getVideos(soup, limitDate=None):
    """Documentation    
       Parameters:
            soup : soup for the request 
            limitDate : date on which we will filter video
       out : 
            list_Videos : search equation videos list        
    """
    videos = soup.findAll('a', attrs={'class': 'yt-uix-tile-link'})
    dates = soup.findAll('ul', attrs={'class': 'yt-lockup-meta-info'})
    
    list_Videos = []
    for i in range(len(videos)):
        date = DateCalculation(str(dates[i]).split(
            "</li><li>")[0].split("<li>")[-1])
        if limitDate is None:
            list_Videos.append('https://www.youtube.com'+videos[i]['href'])
        elif date > limitDate:
            list_Videos.append('https://www.youtube.com'+videos[i]['href'])
            
    return list_Videos


# # Create equation research

# In[41]:


Airline_Companies = [
    "American Airlines",
    "Air Canada",
    "Air France",
    "Air Algerie",
    "Air India",
    "Aerolineas Argentinas",
    "Royal Air Maroc",
    "Finnair",
    "Alitalia ",
    " Nouvelair",
    "Air China",
    "Cathay Pacific",
    "Delta Airlines",
    "Aer Lingus",
    "Emirates",
    "Ethiopian Airlines",
    "Icelandair",
    "Hawaiian Airlines",
    "Iberia",
    "Meridiana",
    "Japan Airlines",
    "KLM",
    "Air Malta",
    "Lan Airlines",
    "Luxair",
    "LIAT",
    "LOT Polish Airlines",
    "Air Madagascar",
    "Air Mauritius",
    "Austrian Airlines",
    "Qatar Airways",
    "South African Airways",
    "SAS Scandinavian Airlines",
    "Brussels Airlines",
    "Singapore Airlines",
    "Corsair",
    "Aeroflot",
    "Thai Airways",
    "Turkish Airlines",
    "TAP Portugal",
    "Air Transat",
    "Tunisair",
    "Air Caraibes",
    "United Airlines",
    "Air Austral",
    "Air Europa",
    "Easyjet",
    "Vietnam Airlines",
    "Virgin Atlantic",
    "Air Corsica",
    "Condor",
    "Flybe",
    "Aegean Airlines",
    "Air Tahiti Nui",
    "Aigle Azur",
    "HOP!",
    "Jet Airways",
    "Etihad Airways",
    "Etihad Airways",
    "Oman Air",
    "XL Airways",
    "Ryanair LTD",
    "Vueling ",
    "Norwegian",
    "Transavia France",
    "Germanwings",
    "TUI Fly Belgium",
    "Air Arabia",
    "WOW air",
    "Wizz Air",
    "Air Asia",
    "Volotea",
    "southwest airlines"
]
Airline_Companies = [compagnies.replace(
    ' ', '+') for compagnies in Airline_Companies]


Boeing_Models = [
    "Boeing 717",
    "Boeing 727",
    "Boeing 737-200",
    "Boeing 737-300",
    "Boeing 737-400",
    "Boeing 737-500",
    "Boeing 737-600",
    "Boeing 737-700",
    "Boeing 737-700ER",
    "Boeing 737-800",
    "Boeing 737-900",
    "Boeing 737-900ER",
    "Boeing 737 MAX 7",
    "Boeing 737 MAX 8",
    "Boeing 737 MAX 9",
    "Boeing 737 MAX 10",
    "Boeing 747-200",
    "Boeing 747-400",
    "Boeing 757-200",
    "Boeing 757-300",
    "Boeing 767-200",
    "Boeing 767-300",
    "Boeing 767-300ER",
    "Boeing 767-400ER",
    "Boeing 777 Triple Seven",
    "Boeing 787 DreamLiner"
]
Boeing_Models = [models.replace(' ', '+') for models in Boeing_Models]


Airbus_Models = [
    "A300",
    "A300-600ST",
    "A318",
    "A319",
    "A320-100",
    "A320-200",
    "A320neo",
    "A321-100",
    "A321-200",
    "A330-200",
    "A330-300",
    "A330-200F",
    "A330-500",
    "A340-200",
    "A340-300",
    "A340-500",
    "A340-600",
    "A350-900",
    "A350-1000",
    "A380-800",
    "A220-300"
]

key_words = [
    "trip",
    "fly",
    "plane",
    "airplane",
    "flight"
]


equations = []
for comp in Airline_Companies:
    for mod in Airbus_Models:
        equations.append(comp+"+"+mod)
    for mod in Boeing_Models:
        equations.append(comp+"+"+mod)

# quibbling function


# In[42]:


def ChangeDate(chain):
    """Documentation    
       Parameters:
            chain : character string in format "ex :il ya 300 ans"    
       out : 
            expression.group(0) : character string in format  "ex 300 ans"          
    """
    expression = re.search("[0-9]*\s[a-zA-Z]*$", chain)
    return(expression.group(0))


def Simplification(chain):
    # transform M into 1000000,  and K into 1000
    """Documentation    
       Parameters:
            chain : character string in format "ex : 300K"    
       out : 
            int(float(expression) * coef) : integer  "ex 300 000"          
    """
    chain = chain.replace(',', '.')
    if '.' in chain:
        expression = (re.search("\d+\.\d+", chain)).group(0)
    else:
        expression = (re.search("\d+", chain)).group(0)
    coef = 1
    if 'k' in chain:
        coef = 1000
    if 'M' in chain:
        coef = 1000000
    return(int(float(expression) * coef))


def DateCalculation(chain):
    # calculate the exact date of publication of the video
    """Documentation    
       Parameters :
            chain : character string in format "ex : il ya 300 ans"    
       out : 
            chain : date           
    """

    chain = (chain).replace('il y a ', '')
    day_nb=0
    if 'hier' in chain:
        day_nb = 1
    else:
        day_nb = int((re.search("\d+", chain)).group(0))
    if 'mois' in chain:
        day_nb = day_nb * 30
    if 'an' in chain:
        day_nb = day_nb * 365
    if 'semaine' in chain:
        day_nb = day_nb * 7

    now = date.today()
    return str(now - timedelta(days=(day_nb)))


# # Creation of the url list

# In[43]:


def URLlist(Research_Equations,limitDate):
    # returns the list of videos of the search equation passed in parameter
    """Documentation    
       Parameters:
            Research_Equations : search equation we want to launch    
       out : 
            list_Videos : search equation videos list        
    """
    root_URL = "https://www.youtube.com/results?search_query="
    #ResearchEquations = "airbus+A380"

    r = requests.get(root_URL + Research_Equations)
    page = r.text
    soup = BeautifulSoup(page, 'html.parser')
    
    list_Videos = getVideos(soup,limitDate)
    return list_Videos


# # Function that creates our filled Json file

# In[44]:


def GetCodeHTML(URL_list, fig):
    """Documentation    

       Parameters:
            URL_list : list of url   
            fig : url index processed
       out :  
            BeautifulSoup(web_page, 'html.parser') : return html code of the url page      
    """
    url = URL_list[fig]
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    web_page = urlopen(req).read()
    return BeautifulSoup(web_page, 'html.parser')


def CreateJs(comment, nb_com, soup, comment_date):
    # create the json file with all the information on the page
    """Documentation    

       Parameters:
            comment : character string of the comment
            nb_com : number of comment
            comment_date : comment date

    """
    name_col = ['Airline_Name',
                'Airline_Type',
                'Region_Operation',
                'Aircraft_Type',
                'Cabin_Class',
                'Type_Of_Lounge',
                'Type_Of_Traveller',
                'Date_Visit',
                'Date_Flown',
                'Airport',
                'Route',
                'Category',
                'Category_Detail',
                'Cabin_Staff_Service',
                'Lounge_Staff_Service',
                'Bar_And_Beverages',
                'Food_And_Beverages',
                'Ground_Service',
                'Catering', 'Cleanliness',
                'Lounge_Comfort',
                'Aisle_Space',
                'Wifi_And_Connectivity',
                'Inflight_Entertainment',
                'Viewing_Tv_Screen',
                'Power_Supply',
                'Seat',
                'Seat_type',
                'Seat_Comfort',
                'Seat_Legroom',
                'Seat_Storage',
                'Seat_Width',
                'Seat_Recline',
                'Washrooms',
                'Value_For_Money',
                'Overall_Customer_Rating',
                'Overall_Service_Rating',
                'Overall_Airline_Rating',
                'Recommended',
                'Departure_city',
                'Arrival_city',
                'Nb_bus_taken',
                'Nb_train_taken',
                'Nb_car_taken',
                'Nb_plane_taken',
                'Duration',
                'Price_min',
                'Price_max',
                'Nb_sharing',
                'Awards',
                'Registration',
                'Language']

    soup = soup
    video_details = {}

# Fill data

    video_details['Data_Source'] = 'Youtube'

    for i in range(39):
        video_details[name_col[i]] = ' '

    video_details['Date_Review'] = DateCalculation(comment_date)
    video_details['Review'] = translate(comment)

    for i in range(39, 48):
        video_details[name_col[i]] = ' '

# get the title of the video
    video_details['Title'] = soup.find(
        'span', attrs={'class': 'watch-title'}).text.strip()

# get the name of the chain
    for script in soup.findAll('script', attrs={'type': 'application/ld+json'}):
        channelDescription = json.loads(script.text.strip())
        video_details['Author'] = channelDescription['itemListElement'][0]['item']['name']

# get description
    video_details['Description'] = soup.find(
        'p', attrs={'id': "eow-description"}).text.strip()

# get the date of publication
    dic = {'.':'','avr':'apr','janv':'jan','mars':'mar','mai':'may','juin':'jun','févr':'feb','juil':'jul','déc':'dec','août':'aug','sept':'sep','aoÃ»t':'aug','dÃ©c':'dec'}
    var_date_of_public = soup.find('strong',attrs={'class': "watch-time-text"}).text.strip().replace('.','')
    var_date_of_public = replace_all(var_date_of_public,dic)
    var_date_not_None = re.search("[0-9][0-9]* [a-zA-Z]* [0-9]*", var_date_of_public)
    if var_date_not_None == None :
        video_details['Date_publication'] = ''
    else :
        video_details['Date_publication'] = str(datetime.strptime(var_date_not_None.group(0), '%d %b %Y')). replace('00:00:00', '')

# get the number of views
    video_details['View_Count'] = (soup.find(
        'div', attrs={'class': 'watch-view-count'}).text.strip()).replace('vues', '')

# get a likes button
    for span in soup.findAll('', attrs={'class': "yt-uix-button yt-uix-button-size-default yt-uix-button-opacity yt-uix-button-has-icon no-icon-markup like-button-renderer-like-button like-button-renderer-like-button-unclicked yt-uix-clickcard-target yt-uix-tooltip"}):
        video_details['Likes'] = span.find(
            'span', attrs={'class': 'yt-uix-button-content'}).text.strip()

# get a dislikes button
    for button in soup.findAll('button', attrs={'class': "yt-uix-button yt-uix-button-size-default yt-uix-button-opacity yt-uix-button-has-icon no-icon-markup like-button-renderer-dislike-button like-button-renderer-dislike-button-unclicked yt-uix-clickcard-target yt-uix-tooltip"}):
        video_details['Dislikes'] = button.find(
            'span', attrs={'class': 'yt-uix-button-content'}).text.strip()

# get subscriber number
    if (soup.find('span', attrs={'class': 'yt-subscription-button-subscriber-count-branded-horizontal yt-subscriber-count'}) == None):
        video_details["Nb_subscribers"] = 0
    else:
        video_details["Nb_subscribers"] = Simplification(soup.find('span', attrs={
                                                         'class': 'yt-subscription-button-subscriber-count-branded-horizontal yt-subscriber-count'}).text.strip())

    video_details['Nb_comments'] = (nb_com).replace('commentaires', '')

    video_details[name_col[48]] = ' '
# get hashtags
    hashtags = []

    for span in soup.findAll('span', attrs={'class': 'standalone-collection-badge-renderer-text'}):
        for a in span.findAll('a', attrs={'class': 'yt-uix-sessionlink'}):
            hashtags.append(a.text.strip())
    video_details['hashtags'] = hashtags

    for i in range(49, 51):
        video_details[name_col[i]] = ' '

    video_details['Language'] = 'unknown'

    if re.search("([a-z]).*", str(comment).lower()) : 
        try :
            video_details['Language'] = detect(comment)
        except :
            video_details['Language'] = 'unknown'

        
    with open('../RESULTATS_JSON/data_youtube.json', 'a', encoding='utf8') as outfile:
        json.dump(video_details, outfile, ensure_ascii=False, indent=4)


def scroll(url, nb_scroll):
    #scroll down in the page
    """Documentation    
       Parameters:
            url : page url 
            nb_scroll : number of times you scroll  
       out : 
            BeautifulSoup(driver.page_source, 'html.parser') : the new page after scroll
            

    """
    options = Options()
    options.add_argument("--start-maximized")
    driver =  webdriver.PhantomJS('./phantomjs')
    driver.get(url)
    Y = 0
    for _ in range(nb_scroll):
        time.sleep(4)
        driver.execute_script("window.scrollTo("+str(Y)+","+str(Y+800)+")")
        Y += 1200

    return BeautifulSoup(driver.page_source, 'html.parser')


# # global implementation

# In[45]:


# Create a new json

with open('../RESULTATS_JSON/data_youtube.json', 'w', encoding='utf8') as outfile:
    json

for Equation in equations:
    list_Videos = URLlist(Equation,None)
    # len(list_Videos)
    if len(list_Videos) > 1 :
        for URL_unique in range(min(len(list_Videos),7)):
            soup1 = scroll(list_Videos[URL_unique], 4)
            SoupCréeJS = GetCodeHTML(list_Videos, URL_unique)
        # date comment
            date1 = []
            for span1 in soup1.findAll('span', attrs={'class': "comment-renderer-time"}):
                a = (span1.find('a', attrs={'class': "yt-uix-sessionlink spf-link"}).text.strip())
                date1.append(a)
            date_Track = 0
            for span in soup1.findAll('div', attrs={'class': 'comment-renderer-text-content'}):
                if span.text.strip() != '':
                    comment = span.text.strip()
                    nb_com = re.search("[0-9][0-9]*", (soup1.find('h2', 
                                                                 attrs={'class': 'comment-section-header-renderer'}).text.strip()).replace('\xa0',' ').replace('\u202f','')).group(0)
                    CreateJs(comment, nb_com, SoupCréeJS, date1[date_Track])
                    date_Track += 1
            print('vidéo numéro : ', URL_unique, ' fini')
        print('équation finie :', Equation)
print('extraction complete')


# In[ ]:


dic = {'.':'','avr':'apr','janv':'jan','mars':'mar','mai':'may','juin':'jun','févr':'feb','juil':'jul','déc':'dec','août':'aug','sept':'sep','aoÃ»t':'aug','dÃ©c':'dec'}
var_date_of_public = SoupCréeJS.find('strong',attrs={'class': "watch-time-text"}).text.strip().replace('.','')
var_date_of_public = replace_all(var_date_of_public,dic)
str(datetime.strptime(re.search("[0-9][0-9]* [a-zA-Z]* [0-9]*", var_date_of_public).group(0), '%d %b %Y')). replace('00:00:00', '')


# In[ ]:


SoupCréeJS.find('span', attrs={'class': 'watch-title'}).text.strip()


# In[ ]:




