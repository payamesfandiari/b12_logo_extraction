# B12 Logo Extractor


LogoExtractor is a Python CLI application generated that uses Scrapy and Selenium extensively. 
Make sure to install all the required libraries before running.  

Project Organization
------------
    ├── README.md       <- The top-level README for developers using this project.
    ├── logo_extractor  <- The top-level package.
    │   ├── __init__.py 
    │   ├── chrome_driver <- The default chrome driver location
    │   │   └── chromedriver
    │   ├── js          <- Javascript files go here
    │   │   └── jquery-3.3.1.min.js
    │   ├── logo.db     <- Sqlite DB for handling the extracted data    
    │   ├── logo_extractor  <- Scrapy Spider
    │   │   ├── __init__.py
    │   │   ├── db.py       <- PeeWee Database ORM Model file
    │   │   ├── items.py    <- Scrapy item def
    │   │   ├── middlewares.py  <- Not Used 
    │   │   ├── pipelines.py    <- Items get cleaned here and pushed to DB
    │   │   ├── settings.py     <- Project Settings
    │   │   └── spiders     
    │   │       ├── __init__.py
    │   │       └── logo.py     <- The actual extractor
    │   ├── main.py         <- CLI interface and main functions
    │   ├── scrapy.cfg      <- Config file for scrapy   
    │   └── urls.txt        <- the list of urls 
    └── requirements.txt    <- Requirement file
   
--------



## Basic setup

- Install the requirements:
```
$ pip install -r requirements.txt
```

- Download the Chrome driver from the link : 
[Chrome Driver](https://chromedriver.storage.googleapis.com/index.html?path=2.45/)
- Copy the `chromedriver` executable to `./logo_extractor/chrome_driver` directory.    

- It's very important to double check the `settings.py` : 
```

SANITY_CHECK_LOGO_POSITION = True   # Use Selenium to further improve the results
DB = os.path.join(BASE_DIR,'logo.db')   # Address to the sqlite DB file    
CHROME_WEBDRIVER_PATH = os.path.join(BASE_DIR,'chrome_driver/','chromedriver') # address of the chromedriver
JQUERY_LOCATION = os.path.join(BASE_DIR,'js/','jquery-3.3.1.min.js')  # jquery file location

```

## Running Steps
 Step 1 : 
 ```bash
$ cd logo_extractor/
```  

 Step 2 : To get the URLS of the logos in JSON format :
```
$ python3 main.py parse-dump urls.txt --format-json
```

 Step 3 : To extract URLs and push them in DB
```
$ python3 main.py get-urls urls.txt
```

 Step 4 : To dump data in DB into the terminal :  
```
$ python3 main.py dump-data
```
Note that `--format-json` prints out the JSON encoded string to terminal


## Using as API

To use the package as an API, you can import the three main functions in `main.py`. 

```python
from logo_extractor.main import parse_and_load,parse_and_return,return_logos
urls = ['http://www.google.com',]
parse_and_load(urls)    # finds logos and put them in DB
return_logos()          # Just returns the information in the DB
parse_and_return(urls)  # First finds the logos and then dumps the DB into a list of tuples
```

## Caveats
There are several problems with the library now, 

1. If the logo is in the Footer, this library cannot find it ! 
2. If the `<div>` or `<header>` tags does not have any `id` or `class`, this library cannot find the logo. 


In order to solve these problems, I purpose the following : 
After we exhausted the current way of finding the logo, we select the images that are on the located on the first quarter or the last 
quarter of the web page. We can get this by using a headless browser and use jquery to find the offset :  
``$('img#someID').offset()`` . This will return the location of the element relative to the document.
By looking at this value, we can determine if the image can be a good candidate for being a Logo. 
 