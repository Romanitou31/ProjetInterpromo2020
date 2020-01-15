from bs4 import BeautifulSoup
from selenium import webdriver
from datetime import datetime, timedelta
import time
import pandas as pd
import numpy as np
import json

# Links' companies import
df_compagnies = pd.read_csv('df_compagnies.csv', sep='§', engine='python', index_col=0, encoding='utf-8')
df_compagnies

# Find elements by x path and testing if it returns something
def Find_With_XPath(objet,el):
    ret = objet.find_elements_by_xpath(el)
    if ret: ret = ret[0].text
    else : ret = np.nan
    return ret

# Informations we will get on TripAdvisor
df_comp_reviews = pd.DataFrame(columns=["user_name","location","tags","date_voyage","commentaire","date_commentaire",
                                        "Espace pour les jambes","Confort du siège",
                                        "Divertissement à bord","Service client","Rapport qualité/prix","Propreté",
                                        "Enregistrement et embarquement","Restauration et boissons"])

# List of all the informations 
col_names = ['Date_Review','Review','Airline_Name','Airline_Type','Region_Operation','Aircraft_Type','Cabin_Class','Type_Of_Lounge',
            'Type_Of_Traveller','Date_Visit','Date_Flown','Airport','Route','Category','Category_Detail',
            'Cabin_Staff_Service','Lounge_Staff_Service','Bar_And_Beverages','Food_And_Beverages','Ground_Service','Catering','Cleanliness',
            'Lounge_Comfort','Aisle_Space','Wifi_And_Connectivity','Inflight_Entertainment','Viewing_Tv_Screen','Power_Supply',
            'Seat','Seat_type','Seat_Comfort','Seat_Legroom','Seat_Storage','Seat_Width','Seat_Recline','Washrooms',
            'Value_For_Money','Overall_Customer_Rating','Overall_Service_Rating','Overall_Airline_Rating',
            'Recommended','Title','Author','Description','Date_publication',
            'View_count','Likes','Dislikes','Nb_subscribers','Nb_comments','Nb_sharing','Hashtags','Awards','Registration','Language',
            'Location',"Contributions_Pers","Nb_Pertinent_Comments","Data_Source","Arrival_city","Nb_bus_taken","Nb_train_taken",
            'Nb_car_taken','Nb_plane_taken','Duration','Price_min','Price_max']

# Set the driver and the size of the virtual window
driver = webdriver.PhantomJS('/Users/julesboutibou/Documents/L3 Cours/Projet/Données/phantomjs-2.1.1-macosx/bin/phantomjs')
driver.set_window_size(2560,1600)

# Companies' links loop
for company in range(len(df_compagnies)):
    
    # Select name and link of the current company into comp_name and comp_url
    comp_name, comp_url = df_compagnies.loc[company,:]
    comp_name, comp_url
    driver.get(comp_url)   

    # Click on the button "all languages"
    btn_langages = driver.find_elements_by_xpath("//div[contains(@class,'is-3-tablet')]//ul[@class='location-review-review-list-parts-ReviewFilter__filter_table--1H9KD']//li//label[@for='LanguageFilter_0']")    
    btn_langages[0].find_elements_by_xpath(".//span")[0].click()
    
    # Waiting 2 seconds for the new all languages commentaries to load
    time.sleep(2)
    
    # Select number of total commentaries' number     
    nb_pages = int(driver.find_elements_by_xpath("//a[@class='pageNum ']")[-1].text) 
  
    # Loop on every pages
    for page in range(nb_pages):
        
        # Start chrono
        start = time.time()
        
        # Make a random waiting time to simulate human behavior
        wait_time_long = 0.5 + np.random.random(1)[0]/10
        wait_time_small = 0.5 + np.random.random(1)[0]/10

        # Wait for loading to finish
        print("Récupération des données en cours")
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
        nb_comments=len(results)
                
        # Loop on every block of comment
        for block in results:
            
            # block 1
            block_user_info = block.find_elements_by_xpath("div[contains(@class,'social-member-event-MemberEventOnObjectBlock')]")[0]
            
            # Select user name
            user_name = block_user_info.find_elements_by_xpath("div[1]/div[2]/span/a")
            if user_name : user_name = user_name[0].get_attribute('href').split('/')[-1]
            else : user_name = np.nan
            
            # Select location where the user posted the comment
            user_location = Find_With_XPath(block_user_info,"div[1]/div[3]/span/span[contains(@class,'MemberHometown__hometown')]")
            
            # Select the date review
            date_review = block_user_info.find_elements_by_xpath("div[1]/div[2]/span")
            if date_review : 
                date_review = date_review[0].get_attribute('innerHTML').split('</a>')[-1].split(' a écrit un avis le ')[-1]
                if date_review.lower() == "hier" : date_review = (datetime.today() - timedelta(days=1)).strftime('%d %B')
                if date_review.lower() == "aujourd'hui" : date_review = datetime.today().strftime('%d %B')
            else : date_review = np.nan
            
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
            titre = Find_With_XPath(block_user_review,"div[@data-test-target='review-title']")
            
            # Select the date flown
            date_flown = block_user_review.find_elements_by_xpath(".//span[contains(@class,'location-review-review-list-parts-EventDate__event_date')]")
            if date_flown : date_flown = date_flown[0].get_attribute('innerHTML').split("</span>")[-1].strip()
            else : date_flown = np.nan
            
            # Select the commentary
            commentary = Find_With_XPath(block_user_review,".//q[contains(@class,'location-review-review-list-parts-ExpandableReview__reviewText')]")
            
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
            all_values = {"user_name" : user_name,
                          "location" : user_location,
                          "tags" : tags,
                          "date_voyage" : date_flown,
                          "commentaire" : commentary,
                          "date_commentaire" : date_review,
                          "Airline_Name" : comp_name,
                          "Data_Source" : 'TripAdvisor'}
            all_values.update(dict_stats)
            all_values.update(dict_notes)
            df_comp_reviews = df_comp_reviews.append(pd.Series(all_values), ignore_index=True, sort=False)
        
        # Print to control the advencement
        print('Page numéro ', page,' récupérée de la compagnie ',comp_name)
        print("Temps d'exécution : ", time.time()-start)
        print('---------------------------------------------------')

        # Click on the button to acceed the next page
        next_page = driver.find_elements_by_xpath("//*//a[@class='ui_button nav next primary ']")
        if next_page : 
            next_page = next_page[0].click()

# Merge of 4 columns into 2            
for i in range(len(df_comp_reviews)):    
    if str(df_comp_reviews['contribution'][i])!="nan":
        df_comp_reviews['contributions'][i]=float(1)
        
    if str(df_comp_reviews['vote utile'][i])!="nan":
        df_comp_reviews['votes utiles'][i]=float(1)        
del df_comp_reviews['contribution'] 
del df_comp_reviews['vote utile'] 

# Creation of the last dataframe
df_comp_reviews.columns=["User_Name","Location","Hashtags","Date_Flown","Review","Date_Review",
           "Seat_Legroom","Seat_Comfort","Inflight_Entertainment","Overall_Service_Rating",
           "Value_For_Money","Cleanliness","Registration","Food_And_Beverages","Airline_Name",
           "Data_Source","Overall_Customer_Rating","Contributions_Pers","Nb_Pertinent_Comments"]               

# Export the data in Json
c = df_comp_reviews.to_json(orient='records').replace("[",'').replace("]",'')
with open('TestTripAdvisor.json', 'w', encoding='utf8') as outfile:
        json.dump(c, outfile, ensure_ascii=False,indent=4)      
    



















