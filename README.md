# IITK-Search-Engine
To say in brief it searchs page and people within IITK when provided a key to look for.<br>

## Details of the Program
The Program consists of three components:
   - Student search and its database creation
   - Crawling the web on the allowed domains
   - Setting up an elasticsearch for the scraped data

The program is still under development.

## Requirements
- Scrapy
- Elasticsearch
- Kibana
- BeautifulSoup
- urllib

## Running the program
Follow the following steps to setup your own search-engine:
   - create and update databases as defined in funtions in db_amend.py . Use __python3__.
   - run `python3 fillUsers.py` to generate a list of users with available homepages.
     - modify the year list according to your choice
   - then run `scrapy runspider crawler.py` to get the json file scrapedData.json
   - Now, with the data with us we need to create an index for it to be used in elasticsearch. I am using bulkAPI. So in this case insert_index.sh will do the thing. Simply run `bash insert_index.sh`
   - then run the elasticsearch server and curl POST the json data.
   - the database has been setup. Now comes the search part. Run `python search.py` while running the elasticsearch server and search for whatever you want.
