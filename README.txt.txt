How launch the different scraping and cron? 

Weibo :
Step 1 : Open the file 'Report_Notebook_Weibo.ipynb'
Step 2 : Change the json save path in "createJson" function and in crawl part.
Step 3 : Change the variable nb_days in the crawl part. Write 7 if you want only the articles published the 7 last days, or 20 000 if you want all articles published. 
Step 4 : Export the file "Report_Notebook_Weibo" in py.file.
Step 5 : Connect to OSIRIM
Step 6 : Import the script 'Scraping_Weibo.sh' and "Report_Notebook_Weibo.py" on OSIRIM
Step 7 : Execute the cron on OSIRIM every monday with the command "SBATCH 00 3 * * 1 path_of_your_file/Scraping_Weibo.sh"


Weibo :
Step 1 : Open the file 'Report_Notebook_Weibo.ipynb'
Step 2 : Change the json save path in "createJson" function and in crawl part.
Step 3 : Change the variable nb_days in the crawl part. Write 7 if you want only the articles published the 7 last days, or 20 000 if you want all articles published. 
Step 4 : Export the file "Report_Notebook_Weibo" in py.file.
Step 5 : Connect to OSIRIM
Step 6 : Import the script 'Scraping_Weibo.sh' and "Report_Notebook_Weibo.py" on OSIRIM
Step 7 : Execute the cron on OSIRIM every monday with the command "SBATCH 00 3 * * 1 path_of_your_file/Scraping_Weibo.sh"

