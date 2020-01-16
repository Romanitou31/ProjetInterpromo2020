How launch the different scraping and cron? 

- Import the "phantomjs" file on OSIRIM and execute the command "chmod +x path_of_your_file/phantomjs"


Weibo :
Step 1 : Open the file 'Report_Notebook_Weibo.ipynb'
Step 2 : Change the json save path in "createJson" function and in crawl part.
Step 3 : Change the variable nb_days in the crawl part. Write 7 if you want only the articles published the 7 last days, or 20 000 if you want all articles published. 
Step 4 : Export the file "Report_Notebook_Weibo" in py.file.
Step 5 : Connect to OSIRIM
Step 6 : Import the script 'Scraping_Weibo.sh' and "Report_Notebook_Weibo.py" on OSIRIM
Step 7 : Execute the cron on OSIRIM every monday with the command "SBATCH 00 3 * * 1 path_of_your_file/Scraping_Weibo.sh"

Youtube :
Step 1 : Open the file 'Report_Notebook_Youtube.ipynb'
Step 2 : Change the variable "path" for PhantomJs path. Choose the phantomJs linux. 
Step 3 : Change the json save path in "createJson" function and in "global implementation" part.
Step 4 : Change the variable "take7days" in "URLlist" call function. Write 'True' if you want only the video published the 7 last days, or "False" if you want all video published. 
Step 5 : Export the file "Report_Notebook_Youtube" in py.file.
Step 6 : Connect to OSIRIM
Step 7 : Import the script 'Scraping_Youtube.sh' and "Report_Notebook_Youtube.py" on OSIRIM
Step 8 : Execute the cron on OSIRIM every monday with the command "SBATCH 00 3 * * 1 path_of_your_file/Scraping_Youtube.sh"

Rome2Rio :
WARNING : This code don't work on OSIRIM (with phantomJS driver). It works only with the Chromedriver.exe.
We don't have robot for Rome2Rio because we don't have comments and no date to retrieve only the recents routes so we need to scrap manually the site all month
Step 1 : Open the file 'Report_Notebook_Rome2rio.ipynb'
Step 2 : Change the variable "webdriver" for Chromedriver path with your chromedriver.exe path. 
Step 3 : Change the json save path in "crawl" part.
Step 4 : Execute the script "Report_Notebook_Rome2rio.ipynb" manually every month (the 1st of the Month)
