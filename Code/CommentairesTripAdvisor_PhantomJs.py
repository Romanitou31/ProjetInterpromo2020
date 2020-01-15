from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd
import numpy as np
import json
from datetime import datetime, timedelta

df_compagnies = pd.read_csv('df_compagnies.csv', sep='§', engine='python', index_col=0, encoding='utf-8')
df_compagnies

def FindWithXPath(objet,el):
    ret = objet.find_elements_by_xpath(el)
    if ret: ret = ret[0].text
    else : ret = np.nan
    return ret

df_comp_reviews = pd.DataFrame(columns=["user_name","location","tags","date_voyage","commentaire","date_commentaire",
                                        "Espace pour les jambes","Confort du siège",
                                        "Divertissement à bord","Service client","Rapport qualité/prix","Propreté",
                                        "Enregistrement et embarquement","Restauration et boissons"])

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

driver = webdriver.PhantomJS('/Users/julesboutibou/Documents/L3 Cours/Projet/Données/phantomjs-2.1.1-macosx/bin/phantomjs')
driver.set_window_size(2560,1600)

for comp in range(len(df_compagnies)):
    
    # Select company from the .csv list
    comp_name, comp_url = df_compagnies.loc[comp,:]
    comp_name, comp_url
    driver.get(comp_url)   
    soup=BeautifulSoup(driver.page_source, 'html.parser')

    # Select "all languages"
    btn_langages = driver.find_elements_by_xpath("//div[contains(@class,'is-3-tablet')]\
                    //ul[@class='location-review-review-list-parts-ReviewFilter__filter_table--1H9KD']\
                    //li\
                    //label[@for='LanguageFilter_0']")    
    btn_langages[0].find_elements_by_xpath(".//span")[0].click()
    
    time.sleep(2)
    
    # Select total number of pages      
    Nb_Pages=int(driver.find_elements_by_xpath("//a[@class='pageNum ']")[-1].text) 
  
    for page in range(Nb_Pages):
        
        start = time.time()
        wait_time_long = 0.5 + np.random.random(1)[0]/1000
        wait_time_small = 0.5 + np.random.random(1)[0]

        # wait for loading to finish
        print("Récupération des données en cours")
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
                
        # for every block of comment
        for block in results:
            
            # block 1
            block_user_info = block.find_elements_by_xpath("div[contains(@class,'social-member-event-MemberEventOnObjectBlock')]")[0]
            
            user_name = block_user_info.find_elements_by_xpath("div[1]/div[2]/span/a")
            if user_name : user_name = user_name[0].get_attribute('href').split('/')[-1]
            else : user_name = np.nan
            
            user_location = FindWithXPath(block_user_info,"div[1]/div[3]/span/span[contains(@class,'MemberHometown__hometown')]")
            
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
            
            titre = FindWithXPath(block_user_review,"div[@data-test-target='review-title']")
            
            date_voyage = block_user_review.find_elements_by_xpath(".//span[contains(@class,'location-review-review-list-parts-EventDate__event_date')]")
            if date_voyage : date_voyage = date_voyage[0].get_attribute('innerHTML').split("</span>")[-1].strip()
            else : date_voyage = np.nan
            
            commentaire = FindWithXPath(block_user_review,".//q[contains(@class,'location-review-review-list-parts-ExpandableReview__reviewText')]")
            
            vol_note = block_user_review.find_elements_by_xpath(".//div[contains(@class,'location-review-review-list-parts-RatingLine')]/span")
            if vol_note : vol_note = vol_note[0].get_attribute('class').split('_')[-1]
            else : vol_note = np.nan
            
            notes = block_user_review.find_elements_by_xpath(".//div[contains(@class,'location-review-review-list-parts-AdditionalRatings__ratings')]/div")
            dict_notes = {}
            for e in notes:
                categorie_name = e.find_elements_by_xpath("span")[1].text
                categorie_note = e.find_elements_by_xpath("span/span")[0].get_attribute('class').split('_')[-1][0]
                dict_notes[categorie_name] = categorie_note
            dict_notes['Overall_Customer_Rating'] = int(vol_note[0])*2
            
            # ajout des infos dans le dataframe
            all_values = {"user_name" : user_name,
                          "location" : user_location,
                          "tags" : tags,
                          "date_voyage" : date_voyage,
                          "commentaire" : commentaire,
                          "date_commentaire" : date_commentaire,
                          "Airline_Name" : comp_name,
                          "Data_Source" : 'TripAdvisor'}
            all_values.update(dict_stats)
            all_values.update(dict_notes)
            
            df_comp_reviews = df_comp_reviews.append(pd.Series(all_values), ignore_index=True, sort=False)
            
        print('Page numéro ', page,' récupérée de la compagnie ',comp_name)
        print("Temps d'exécution : ", time.time()-start)
        print('---------------------------------------------------')

        
        suivant = driver.find_elements_by_xpath("//*//a[@class='ui_button nav next primary ']")
        if suivant : 
            suivant = suivant[0].click()
            
for i in range(len(df_comp_reviews)):    
    if str(df_comp_reviews['contribution'][i])!="nan":
        df_comp_reviews['contributions'][i]=float(1)
        
    if str(df_comp_reviews['vote utile'][i])!="nan":
        df_comp_reviews['votes utiles'][i]=float(1)
        
del df_comp_reviews['contribution'] 
del df_comp_reviews['vote utile'] 

df_comp_reviews.columns=["User_Name","Location","Hashtags","Date_Flown","Review","Date_Review",
           "Seat_Legroom","Seat_Comfort","Inflight_Entertainment","Overall_Service_Rating",
           "Value_For_Money","Cleanliness","Registration","Food_And_Beverages","Airline_Name",
           "Data_Source","Overall_Customer_Rating","Contributions_Pers","Nb_Pertinent_Comments"]               

c = df_comp_reviews.to_json(orient='records').replace("[",'').replace("]",'')
with open('TestTripAdvisor.json', 'w', encoding='utf8') as outfile:
        json.dump(c, outfile, ensure_ascii=False,indent=4)      
        
fichier = open('SoupTripAdvisor','w',encoding='utf8')    
fichier.write(str(soup))  
fichier.close()



















