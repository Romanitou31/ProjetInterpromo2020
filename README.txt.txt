How launch the different scraping and cron? 

- Import the "phantomjs" file on OSIRIM and execute the command "chmod +x path_of_your_file/phantomjs" to made it executable.


Weibo :
Step 1 : Open the file 'Report_Notebook_Weibo.ipynb'
Step 2 : Change the json save path in crawl part (2 path to change).
Step 3 : Change the variable nb_days in the crawl part. Write 7 if you want only the articles published the 7 last days, or 20 000 if you want all articles published. 
Step 4 : Export the file "Report_Notebook_Weibo.ipynb" in py.file with the name "Scraping_Weibo.py"
Step 5 : Connect to OSIRIM
Step 6 : Import the script 'Scraping_Weibo.sh' and "Scraping_Weibo.py" on OSIRIM
Step 7 : Execute the cron on OSIRIM every monday with the command "SBATCH 00 3 * * 1 path_of_your_file/Scraping_Weibo.sh"

Youtube :
Step 1 : Open the file 'Report_Notebook_Youtube.ipynb'
Step 2 : Change the variable "path" for PhantomJs path. Choose the phantomJs linux. 
Step 3 : Change the json save path in "global implementation" part (2 path to change) and in "descriptive statistics on recovered data" .
Step 4 : Change the variable "take7days" in "URLlist" call function. Write 'True' if you want only the videos published the 7 last days, or "False" if you want all video published. 
Step 5 : Export the file "Report_Notebook_Youtube.ipynb" in py.file with the name "Scraping_Youtube.py".
Step 6 : Connect to OSIRIM
Step 7 : Import the script 'Scraping_Youtube.sh' and "Scraping_Youtube.py" on OSIRIM
Step 8 : Execute the cron on OSIRIM every monday with the command "SBATCH 00 3 * * 1 path_of_your_file/Scraping_Youtube.sh"

Rome2Rio :
WARNING : This code don't work on OSIRIM (with phantomJS driver). It works only with the Chromedriver.exe.
We don't have robot for Rome2Rio because we don't have comments and no date to retrieve only the recents routes so we need to scrap manually the site all month
Step 1 : Open the file 'Report_Notebook_Rome2rio.ipynb'
Step 2 : Change the variable "webdriver" for Chromedriver path with your chromedriver.exe path (Warning : your version of chromedriver needs to be equal to your version of Google Chrome)
Step 3 : Change the json save path in "crawl" part.
Step 4 : Execute the script "Report_Notebook_Rome2rio.ipynb" manually every month (the 1st of the Month)

AirlineQuality :
Step 1 : Open the file 'Report_Notebook_AirlineQuality.ipynb' 
Step 2 : Change the json save path in "Crawl" part (1 path to change).
Step 3 : Change the number in the call of "scrap" function (in Crawl part). Write 7 if you want only the comments published the 7 last days, or 20 000 if you want all articles published. 
Step 4 : Export the file "Report_Notebook_AirlineQuality.ipynb" in py.file with the name "Scraping_Airlines.py"
Step 5 : Connect to OSIRIM
Step 6 : Import the script 'Scraping_Airlines.sh' and "Scraping_Airlines.py" on OSIRIM
Step 7 : Execute the cron on OSIRIM every monday with the command "SBATCH 00 3 * * 1 path_of_your_file/Scraping_Airlines.sh"
