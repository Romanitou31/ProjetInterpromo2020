import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

df_compagnies = pd.read_csv('df_compagnies.csv', sep='§', engine='python', index_col=0, encoding='utf-8')
df_compagnies

#df_comp_reviews = pd.DataFrame(columns=["Location","Hashtags","Date_Flown","Review","Date_Review",
#                                        "Contributions_Pers","Nb_Pertinent_Comments","Seat_Legroom","Seat_Comfort",
#                                        "Inflight_Entertainment","Overall_Service_Rating","Value_For_Money","Cleanliness",
#                                        "Ground_Service","Food_And_Beverages","Overall_Customer_Rating"])

df_comp_reviews = pd.DataFrame(columns=["user_name","location","tags","date_voyage","commentaire","date_commentaire",
                                        "contributions","votes utiles","Espace pour les jambes","Confort du siège",
                                        "Divertissement à bord","Service client","Rapport qualité/prix","Propreté",
                                        "Enregistrement et embarquement","Restauration et boissons","Vol"])

col_names = ['Date_Review','Review','Airline_Name','Airline_Type','Region_Operation','Aircraft_Type','Cabin_Class','Type_Of_Lounge',
               'Type_Of_Traveller','Date_Visit','Date_Flown','Airport','Route','Category','Category_Detail',
               'Cabin_Staff_Service','Lounge_Staff_Service','Bar_And_Beverages','Food_And_Beverages','Ground_Service','Catering','Cleanliness',
              'Lounge_Comfort','Aisle_Space','Wifi_And_Connectivity','Inflight_Entertainment','Viewing_Tv_Screen','Power_Supply',
              'Seat','Seat_type','Seat_Comfort','Seat_Legroom','Seat_Storage','Seat_Width','Seat_Recline','Washrooms',
               'Value_For_Money','Overall_Customer_Rating','Overall_Service_Rating','Overall_Airline_Rating',
              'Recommended','Title','Author','Description','Date_publication',
           'View_count','Likes','Dislikes','Nb_subscribers','Nb_comments','Nb_sharing','Hashtags','Awards','Registration','Language'
           ,"Location","Contributions_Pers","Nb_Pertinent_Comments","Data_Source","Arrival_city","Nb_bus_taken","Nb_train_taken",
           "Nb_car_taken","Nb_plane_taken","Duration","Price_min","Price_max"]
options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)

for comp in range(len(df_compagnies)):
    
    # Select company from the .csv list
    comp_name, comp_url = df_compagnies.loc[comp,:]
    comp_name, comp_url
    driver.get(comp_url)
    
    # Select "all languages"
    btn_langages = driver.find_elements_by_xpath("//div[@class='ui_column  is-3-tablet is-shown-at-tablet ']\
                        //ul[contains(@class,'location-review-review-list-parts-ReviewFilter__filter_table')]\
                        //li")
    btn_langages[0].find_elements_by_xpath(".//span")[0].click()
    
    # Select total number of pages
    nbPages=int(driver.find_elements_by_xpath("//a[@class='pageNum ']")[0].text)
        
    
    for page in range(nbPages+1):

        wait_time_long = 5 + np.random.random(1)[0]*5
        wait_time_small = 0.5 + np.random.random(1)[0]
        # wait for loading to finish
        print("wait", wait_time_long, ", loading page...")
        time.sleep(wait_time_long)
                
        # go to the bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        time.sleep(wait_time_small)
        
        # load comments details
        boutons = driver.find_elements_by_xpath("//*[contains(@class,'ui_icon caret-down location-review-review-list-parts-ExpandableReview')]")
        if boutons : 
            if boutons[0].is_displayed() :
                boutons[0].click()
                time.sleep(wait_time_small)
                
        results = driver.find_elements_by_xpath("//div[@data-tab='TABS_REVIEWS'][1]\
                                                //div[@class=''][1]\
                                                //*[contains(@class, 'location-review-card-Card__ui_card')]")
        nbComments=len(results)
        print('Page', page,' récupérée de la compagnie ',comp_name)
        
        # for every block of comment
        for block in results:
            
            # block 1
            block_user_info = block.find_elements_by_xpath("div[contains(@class,'social-member-event-MemberEventOnObjectBlock')]")[0]
    
            user_name = block_user_info.find_elements_by_xpath("div[1]/div[2]/span/a")
            if user_name : user_name = user_name[0].get_attribute('href').split('/')[-1]
            else : user_name = np.nan
    
            user_location = block_user_info.find_elements_by_xpath("div[1]/div[3]/span/span[contains(@class,'MemberHometown__hometown')]")
            if user_location: user_location = user_location[0].text
            else : user_location = np.nan
    
            date_commentaire = block_user_info.find_elements_by_xpath("div[1]/div[2]/span")
            if date_commentaire : 
                date_commentaire = date_commentaire[0].get_attribute('innerHTML').split('</a>')[-1].split(' a écrit un avis le ')[-1]
                if date_commentaire.lower() == "hier" : date_commentaire = (datetime.today() - timedelta(days=1)).strftime('%d %B')
                if date_commentaire.lower() == "aujourd'hui" : date_commentaire = datetime.today().strftime('%d %B')
            else : date_commentaire = np.nan
    
            user_stats = block_user_info.find_elements_by_xpath("div[1]/div[3]/span[contains(@class,'MemberHeaderStats__stat_item')]/span")
            dict_stats = {}
            for us in user_stats:
                stat_name = us.get_attribute('innerHTML').split('</span>')[-1].strip()
                stat_value = us.find_elements_by_xpath("span")[0].text
                dict_stats[stat_name] = stat_value
    
            # block 2
            block_user_review = block.find_elements_by_xpath("div[contains(@class,'location-review-review-list-parts-SingleReview__mainCol')]")[0]
    
            tags = block_user_review.find_elements_by_xpath("div[contains(@class,'location-review-review-list-parts-RatingLine')]")
            if tags : tags = tags[0].text.split("\n")
            else : tags = np.nan
    
            titre = block_user_review.find_elements_by_xpath("div[@data-test-target='review-title']")
            if titre: titre = titre[0].text
            else : titre = np.nan
    
            date_voyage = block_user_review.find_elements_by_xpath(".//span[contains(@class,'location-review-review-list-parts-EventDate__event_date')]")
            if date_voyage : date_voyage = date_voyage[0].get_attribute('innerHTML').split("</span>")[-1].strip()
            else : date_voyage = np.nan
    
            commentaire = block_user_review.find_elements_by_xpath(".//q[contains(@class,'location-review-review-list-parts-ExpandableReview__reviewText')]")
            if commentaire : commentaire = commentaire[0].text
            else : commentaire = np.nan
    
            vol_note = block_user_review.find_elements_by_xpath(".//div[contains(@class,'location-review-review-list-parts-RatingLine')]/span")
            if vol_note : vol_note = vol_note[0].get_attribute('class').split('_')[-1]
            else : vol_note = np.nan
    
            notes = block_user_review.find_elements_by_xpath(".//div[contains(@class,'location-review-review-list-parts-AdditionalRatings__ratings')]/div")
            dict_notes = {}
            for e in notes:
                categorie_name = e.find_elements_by_xpath("span")[1].text
                categorie_note = e.find_elements_by_xpath("span/span")[0].get_attribute('class').split('_')[-1][0]
                dict_notes[categorie_name] = categorie_note
            dict_notes['Overall_Customer_Rating'] = vol_note[0]
            
            # ajout des infos dans le dataframe
            all_values = {"user_name" : user_name,
                          "location" : user_location,
                          "tags" : tags,
                          "date_voyage" : date_voyage,
                          "commentaire" : commentaire,
                          "date_commentaire" : date_commentaire,
                          "Airline_Name" : comp_name}
            all_values.update(dict_stats)
            all_values.update(dict_notes)
            
            df_comp_reviews = df_comp_reviews.append(pd.Series(all_values), ignore_index=True, sort=False)
            
    
        df_comp_reviews.to_csv('Reviews_'+comp_name+'.csv', sep='§', encoding='utf-8')
        
        suivant = driver.find_elements_by_xpath("//*//a[@class='ui_button nav next primary ']")
        if suivant : 
            suivant = suivant[0].click()























