
When you recover all notebooks, you need to create a folder which contains the following folders :
- "Driver" which contains the Driver you need to use (here, chromedriver and phantomjs)
- "External_CSV" which contains all CSV (or other data) you need to load in reports.
- "Notebooks" which contains the notebooks with the code you want to execute.
- "Reports" which contains the report you can made
- "Results_json" which contains all results of your notebooks
- "Script_sh" which contains all script sh that you need to execute the notebook on OSIRIM server

You need also th made the phantomjs on linux executable. For this, execute follow this line : 
- Import the "phantomjs" file on OSIRIM and execute the command "chmod +x path_of_your_file/phantomjs" to made it executable.

----------------------------------------------------------
------------ HOW TO LAUNCH EACH NOTEBOOK -----------------
----------------------------------------------------------

Rome2Rio :
WARNING : This code don't work on OSIRIM (with phantomJS driver). It works only with the Chromedriver.exe.
We don't have robot for Rome2Rio because we don't have comments and no date to retrieve only the recents routes so we need to scrap manually the site all month
Step 1 : Open the file 'Report_Notebook_Rome2rio.ipynb'
Step 2 : Change the variable "webdriver" in "getdata" function with your chromedriver.exe path (Warning : your version of chromedriver needs to be equal to your version of Google Chrome)
Step 3 : Change the json save path in "crawl" part.
Step 4 : Execute the script "Report_Notebook_Rome2rio.ipynb" manually every month (the 1st of each Month)

AirlineQuality :
Step 1 : Open the file 'Report_Notebook_AirlineQuality.ipynb' 
Step 2 : Change the json save path in "Crawl" part (1 path to change).
Step 3 : Change the number in the call of "scrap" function (in Crawl part). Write 7 if you want only the comments published the 7 last days, or 20 000 if you want all articles published. 
Step 4 : Export the file "Report_Notebook_AirlineQuality.ipynb" in py.file with the name "Scraping_Airlines.py"
Step 5 : Connect to OSIRIM
Step 6 : Import the script 'Scraping_Airlines.sh' and the code "Scraping_Airlines.py" on OSIRIM
Step 7 : Execute the cron on OSIRIM every monday with the following command : 
	- "crontab -e" to edit the crontab and add a line inside
	- write in the file the line "00 3 * * 1 SBATCH path_of_your_file/Scraping_Airlines.sh" to execute the code every monday at 3h00 am
Step 8 : If you want to kill the cron, you need just to reopen the crontab and delete the lines you want to kill

Weibo :
Step 1 : Open the file 'Report_Notebook_Weibo.ipynb'
Step 2 : Change the json save path in "Crawl" part (1 path to change) and in "Some statistics" part (1 path to change).
Step 3 : Change the variable nb_days in the "Crawl" part. Write 7 if you want only the articles published the 7 last days, or 20 000 if you want all articles published. 
Step 4 : Export the file "Report_Notebook_Weibo.ipynb" in py.file with the name "Scraping_Weibo.py"
Step 5 : Connect to OSIRIM
Step 6 : Import the script 'Scraping_Weibo.sh' and "Scraping_Weibo.py" on OSIRIM
Step 7 : Execute the cron on OSIRIM every monday with the following command : 
	- "crontab -e" to edit the crontab and add a line inside
	- write in the file the line "00 3 * * 1 SBATCH path_of_your_file/Scraping_Weibo.sh" to execute the code every monday at 3h00 am
Step 8 : If you want to kill the cron, you need just to reopen the crontab and delete the lines you want to kill

Youtube :
Step 1 : Open the file 'Report_Notebook_Youtube.ipynb'
Step 2 : Change the variable "path" for PhantomJs path. Choose the phantomJs linux. 
Step 3 : Change the json save path in "global implementation" part (2 path to change) and in "descriptive statistics on recovered data" .
Step 4 : Change the variable "take7days" in "URLlist" call function. Write 'True' if you want only the videos published the 7 last days, or "False" if you want all video published. 
Step 5 : Export the file "Report_Notebook_Youtube.ipynb" in py.file with the name "Scraping_Youtube.py".
Step 6 : Connect to OSIRIM
Step 7 : Import the script 'Scraping_Youtube.sh' and "Scraping_Youtube.py" on OSIRIM
Step 8 : Execute the cron on OSIRIM every monday with the following command : 
	- "crontab -e" to edit the crontab and add a line inside
	- write in the file the line "00 3 * * 1 SBATCH path_of_your_file/Scraping_Youtube.sh" to execute the code every monday at 3h00 am
Step 9 : If you want to kill the cron, you need just to reopen the crontab and delete the lines you want to kill





