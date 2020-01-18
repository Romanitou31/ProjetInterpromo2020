#!/usr/bin/env python
# coding: utf-8

# <h1>Group 1 - Data Collection<span class="tocSkip"></span>

# # Introduction

# One of the sources we need to scrap was the TripAdvisor website. This notebook contains the code to retrieve the data and also the Robot to retrieve informations posted since a date given in the function. 
# This application navigates in the 240 biggest companies of Tripadvisor 
# 
# V0 : Scrap of a single page of reviews
# 
# V1 : Loops to navigate into several pages of several companies
# 
# V2 : Add functions to translate Tripadvisor dates into universal type and change chromedriver to phantomJS
# 
# V3 : Function that retrieves all the reviews that have been posted in the last n days (n is chosen by user)

# # Environment

# ## Libraries

# In[3]:


import time
import pandas as pd
import numpy as np
import json
import re
from selenium import webdriver
from datetime import datetime, timedelta
from textblob import TextBlob
from langdetect import detect


# ## Data Loading

# ## Functions

# This part contains all the functions we developped during the project

# In[4]:


# Detect language and translate it in english
def translate (text) : 
    """Documentation    
       Parameters:
            text : character string 
       out : 
            text : text translated in english
    """
    try :
        new = str(TextBlob(text).translate(to='en'))
        return new
    except :
        return text


# In[5]:


# Replace words with a dictionnary
def replace_all(text, dic):
    """Documentation    
       Parameters:
            text : character string
            dic : dictionary which contains the changes to be made
       out : 
            text : text with all changes made 
    """
    for i, j in dic.items():
        text = text.replace(i, j)
    return text


# In[6]:


# Changing TripAdvisor commentaries dates type into universal one
def Date_Convertion(date,dico_date):
    """Documentation    
       Parameters:
            date : character string
            dico_date : dictionnary to translate Tripadvisor's dates
       out : 
            date : date day/month/year 
    """    
    date = date.lower()    
    if "hier" in date:
        date = (datetime.today() - timedelta(days=1))
    elif "aujourd'hui" in date:
        date = datetime.today()
    else:
        date = replace_all(str(date),dico_date)
        if (re.search("\d\d\d\d", date)) == None:
            date = datetime.strptime(date + " " + datetime.today().strftime('%Y'), '%d %b %Y' )
        else:
            date = datetime.strptime(date, '%b %Y')
    return date.strftime('%d %b %Y')


# In[7]:


# Finds elements by x_path and testing if the function returns something or not
def Find_With_XPath(objet,el):
    """Documentation    
       Parameters:
            object : "WebElement" html 
            dic : dictionary which contains the changes to be made
       out : 
            text : text with all changes made 
    """
    ret = objet.find_elements_by_xpath(el)
    if ret: ret = ret[0].text
    else : ret = np.nan
    return ret


# In[8]:


# This function finds a date in character string format and converts it in a date format
def format_date(date):
    """Documentation
       Parameters :
             date : String format
       out :
             m : timedata : format is YYYY-MM-DD HH:MM:SS
    """
    date_str = date
    #
    date_str = date_str.replace("st","").replace("th","")        .replace("nd","").replace("rd","").replace(" Augu "," Aug ")
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
                    m = datetime.strptime(date_str,"%d/%m/%Y %H:%M:%S")
                except ValueError:
                    try:
                        m = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
                    except ValueError:
                        try :
                            m = datetime.strptime(date_str,
                                                       "%d %m %Y")
                        except ValueError:
                            # HERE ADD A FORMAT TO CHECK
                            print("Format not recognised. \nConsider "
                                  "adding a date format "
                                  "in the function \"format_date\".")

    return m


# In[9]:


# Big function scraping a list of reviews from different pages from a list of the 240 biggest airline companies
# of Tripadvisor
def Lets_Scrape(n_days,phantom_js_file,df_companies_file,export_file):
    """Documentation    
       Parameters:
            n_days : int : Number of days before today where you scrap reviews
            phantom_js_file : character string : way to acceed and execute phantomJs
            df_companies_file : character string : way to acceed and import the df_companies file
            export_file : character string : file where to export final json data
    """   
    ##### Settings
    # Set the driver and the size of the virtual window
    driver = webdriver.PhantomJS(phantom_js_file)
    driver.set_window_size(2560,1600)
    
    # Links' companies import
    df_compagnies = pd.read_csv(df_companies_file, sep='§', engine='python', index_col=0, encoding="utf-8")
    
    # Informations we will get on TripAdvisor
    df_comp_reviews = pd.DataFrame(columns=["location","tags","date_voyage","commentaire","date_commentaire",
                                        "Espace pour les jambes","Confort du siège",
                                        "Divertissement à bord","Service client","Rapport qualité/prix","Propreté",
                                        "Enregistrement et embarquement","Restauration et boissons"])
    
    # Dictionnary to universalise months
    dico_date = {'.':'','avr':'apr','janv':'jan','mars':'mar','mai':'may','juin':'jun','févr':'feb','juil':'jul','déc':'dec','août':'aug','sept':'sep'}

    # Companies' links loop
    for company in range(len(df_compagnies)):
        
        # Select name and link of the current company into comp_name and comp_url
        comp_name, comp_url = df_compagnies.loc[company,:]
        comp_name, comp_url
        driver.get(comp_url)   
        
        # Waiting for the download of the source code
        time.sleep(6)
        
        # Click on the button "all languages"
        btn_langages = driver.find_elements_by_xpath("//div[contains(@class,'is-3-tablet')]//ul[@class='location-review-review-list-parts-ReviewFilter__filter_table--1H9KD']//li//label[@for='LanguageFilter_0']")    
        if btn_langages !=[]:
            btn_langages[0].find_elements_by_xpath(".//span")[0].click()
        
        # Waiting 5 seconds for the new all languages commentaries to load
        time.sleep(6)
        
        # Select number of total commentaries' number     
        nb_pages = driver.find_elements_by_xpath("//a[@class='pageNum ']")
        
        # Testing if the number of pages is found
        if nb_pages == []:
            nb_pages = 0
        else:
            nb_pages = int(nb_pages[-1].text)
            
        print('Compagnie : ',comp_name,' / Nombre de pages = ',nb_pages)
        
        # Loop on every pages
        for page in range(nb_pages):

            # Start chrono
            start = time.time()

            # Make a random waiting time to simulate human behavior
            wait_time_long = 1 + np.random.random(1)[0]
            wait_time_small = 1 + np.random.random(1)[0]

            # Wait for loading to finish
            time.sleep(wait_time_long)

            # Go to the bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
            time.sleep(wait_time_small)

            # Load comments details
            butons = driver.find_elements_by_xpath("//*[contains(@class,'ui_icon caret-down location-review-review-list-parts-ExpandableReview')]")
            if butons : 
                if butons[0].is_displayed() :
                    butons[0].click()
                    time.sleep(wait_time_small)

            # Select every block of comment and count them
            results = driver.find_elements_by_xpath("//div[@data-tab='TABS_REVIEWS'][1]//div[@class=''][1]//*[contains(@class, 'location-review-card-Card__ui_card')]")

            # Loop on every block of comment
            for block in results:

                # block 1
                block_user_info = block.find_elements_by_xpath("div[contains(@class,'social-member-event-MemberEventOnObjectBlock')]")[0]

                # Select the date review
                date_review = block_user_info.find_elements_by_xpath("div[1]/div[2]/span")
                date_review = date_review[0].get_attribute('innerHTML').split('</a>')[-1].split(' a écrit un avis le ')[-1]

                # Testing if the date review is in the period 
                pivot_date = format_date(Date_Convertion(date_review,dico_date)) >= (datetime.now() - timedelta(n_days))

                if pivot_date:
                    # Select user name
                    user_name = block_user_info.find_elements_by_xpath("div[1]/div[2]/span/a")
                    if user_name : user_name = user_name[0].get_attribute('href').split('/')[-1]
                    else : user_name = np.nan

                    # Select location where the user posted the comment
                    user_location = Find_With_XPath(block_user_info,"div[1]/div[3]/span/span[contains(@class,'MemberHometown__hometown')]")

                    # Select the user statistics
                    user_stats = block_user_info.find_elements_by_xpath("div[1]/div[3]/span[contains(@class,'MemberHeaderStats__stat_item')]/span")
                    dict_stats = {}
                    for us in user_stats:
                        stat_name = us.get_attribute('innerHTML').split('</span>')[-1].strip()
                        stat_value = us.find_elements_by_xpath("span")[0].text
                        dict_stats[stat_name] = stat_value

                    # block 2
                    block_user_review = block.find_elements_by_xpath("div[contains(@class,'location-review-review-list-parts-SingleReview__mainCol')]")[0]

                    # Select hashtags
                    tags = block_user_review.find_elements_by_xpath("div[contains(@class,'location-review-review-list-parts-RatingLine')]")
                    if tags : tags = tags[0].text.split("\n")
                    else : tags = np.nan

                    # Select title
                    title = translate(Find_With_XPath(block_user_review,"div[@data-test-target='review-title']"))

                    # Select the date flown
                    date_flown = block_user_review.find_elements_by_xpath(".//span[contains(@class,'location-review-review-list-parts-EventDate__event_date')]")
                    if date_flown : date_flown = date_flown[0].get_attribute('innerHTML').split("</span>")[-1].strip()
                    else : date_flown = np.nan

                    # Select the commentary
                    commentary = translate(Find_With_XPath(block_user_review,".//q[contains(@class,'location-review-review-list-parts-ExpandableReview__reviewText')]"))

                    # Select the global notes
                    vol_note = block_user_review.find_elements_by_xpath(".//div[contains(@class,'location-review-review-list-parts-RatingLine')]/span")
                    if vol_note : vol_note = vol_note[0].get_attribute('class').split('_')[-1]
                    else : vol_note = np.nan

                    # Select the specific note(s), user can post from 0 to 8 of these notes
                    notes = block_user_review.find_elements_by_xpath(".//div[contains(@class,'location-review-review-list-parts-AdditionalRatings__ratings')]/div")
                    dict_notes = {}
                    for e in notes:
                        categorie_name = e.find_elements_by_xpath("span")[1].text
                        categorie_note = e.find_elements_by_xpath("span/span")[0].get_attribute('class').split('_')[-1][0]
                        dict_notes[categorie_name] = categorie_note
                    dict_notes['Overall_Customer_Rating'] = int(vol_note[0])*2

                    # make a local dictionnaries wich will be put in the final dataframe
                    all_values = {"location" : user_location,
                                  "tags" : tags,
                                  "date_voyage" : date_flown,
                                  "commentaire" : commentary,
                                  "date_commentaire" : date_review,
                                  "Airline_Name" : comp_name,
                                  "Data_Source" : 'TripAdvisor',
                                  "Title" : title}
                    all_values.update(dict_stats)
                    all_values.update(dict_notes)
                    df_comp_reviews = df_comp_reviews.append(pd.Series(all_values), ignore_index=True, sort=False)

            # Print to control the advencement        
            print("Page numéro ",page,"récupérée en ",round(time.time()-start,2),"sec")
            #print('---------------------------------------------------') 

            # Click on the button to acceed the next page
            if pivot_date:
                next_page = driver.find_elements_by_xpath("//*//a[@class='ui_button nav next primary ']")
                if next_page : 
                    next_page = next_page[0].click()
            else:
                break
        print("***Compagnie ",comp_name," récupérée ( num ",company,")")
        print('---------------------------------------------------')
        print(" ")
    # Merge of 4 columns into 2            
    if 'contribution' in df_comp_reviews.columns:
        for i in range(len(df_comp_reviews)):
            if str(df_comp_reviews['contribution'][i])!="nan":
                df_comp_reviews['contributions'][i]=float(1)
        del df_comp_reviews['contribution'] 
        
    if 'vote utile' in df_comp_reviews.columns:
        for i in range(len(df_comp_reviews)):
            if str(df_comp_reviews['vote utile'][i])!="nan":
                df_comp_reviews['votes utiles'][i]=float(1)                
        del df_comp_reviews['vote utile'] 
    
    #Re-nomation of the variables to match with the chart
    df_comp_reviews.columns = ["Location","Hashtags","Date_Flown","Review","Date_Review","Seat_Legroom","Seat_Comfort",
                             "Inflight_Entertainment","Overall_Service_Rating","Value_For_Money","Cleanliness",
                             "Registration","Food_And_Beverages","Airline_Name","Data_Source",
                             "Overall_Customer_Rating","Title","Contributions_Pers","Nb_Pertinent_Comments"]                
    
    name_col = pd.DataFrame(columns= ['Data_Source', 'Airline_Name', 'Airline_Type', 'Region_Operation', 'Aircraft_Type', 'Cabin_Class', 'Type_Of_Lounge',
                'Type_Of_Traveller', 'Date_Visit', 'Date_Flown', 'Airport', 'Route', 'Category', 'Category_Detail',
                'Cabin_Staff_Service', 'Lounge_Staff_Service', 'Bar_And_Beverages', 'Food_And_Beverages', 'Ground_Service', 'Catering', 'Cleanliness',
                'Lounge_Comfort', 'Aisle_Space', 'Wifi_And_Connectivity', 'Inflight_Entertainment', 'Viewing_Tv_Screen', 'Power_Supply',
                'Seat', 'Seat_type', 'Seat_Comfort', 'Seat_Legroom', 'Seat_Storage', 'Seat_Width', 'Seat_Recline', 'Washrooms',
                'Value_For_Money', 'Overall_Customer_Rating', 'Overall_Service_Rating', 'Overall_Airline_Rating',
                'Recommended', 'Departure_city', 'Arrival_city', 'Nb_bus_taken', 'Nb_train_taken',
                'Nb_car_taken', 'Nb_plane_taken', 'Duration', 'Price_min', 'Price_max', 'Nb_sharing', 'Awards', 'Registration', 'Language',
                'Queuing Times', 'Terminal_Seating', 'Terminal Signs', 'Airport_Shopping', 'Experience_At_Airport', 'Date_Review'])
    
    #Puting the Tripadvisor informations into the general dataframe
    df_comp_reviews = pd.concat([df_comp_reviews, name_col])
    
    # Export the data in Json
    c = df_comp_reviews.to_json(orient='records')
    with open(export_file, 'w', encoding='utf8') as outfile:
            json.dump(c, outfile, ensure_ascii=False,indent=4)


# # Crawl

# This part contains the crawl of Tripadvisor website with the execution of the scraping function 

# In[10]:


Lets_Scrape(7,'./phantomjs','df_compagnies.csv','../RESULTATS_JSON/data_Tripadvisor.json')


# # Descriptive statistics on recovered data

# In[12]:


with open('SortiePourStatsDesc.json') as train_file:
            dict_train = json.load(train_file)
df = pd.read_json(dict_train, orient="records")


# In[13]:


df


# In[ ]:


col_to_describe=["Overall_Customer_Rating","Cleanliness","Food_And_Beverages","Inflight_Entertainment","Registration","Seat_Comfort","Seat_Legroom","Value_For_Money"]
df[col_to_describe].describe()


# In[ ]:


fig=plt.figure(figsize = (10, 15))
for i in range(8):
    axes=fig.add_subplot(8,1,i+1)
    plt.hist(df[col_to_describe[i]])
    axes.set_xlabel(col_to_describe[i])
plt.show()


# In[ ]:




