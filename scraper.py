#!python3
# Program to make a decision of republican vs independent candidates on the Michigan ballot in Nov 2020. 

# import modules
import logging, googlesearch, random, tempfile, shutil, sys, nltk, fake_useragent, wordcloud, bs4, selenium, pandas, numpy, os, selenium, openpyxl, requests, re, time, urllib.request, cert_human, pycparser, cffi, cryptography, OpenSSL, asn1crypto, certifi, ssl
from os import path
from itertools import cycle
from fake_useragent import UserAgent
from fake_useragent import FakeUserAgentError
from bs4 import BeautifulSoup
from selenium import webdriver
from googlesearch import search
from wordcloud import WordCloud
from nltk.corpus import stopwords
from pathlib import PurePath, Path
from nltk.tokenize import word_tokenize
from urllib.request import Request, urlopen
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select #Selenium.Support
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


"""
Set logging
# https://docs.python.org/2/howto/logging.html#logging-basic-tutorial
# https://medium.com/web-scraping-a-z/web-scraping-project-with-python-a-to-z-b04114e7289d#a7a9
"""
class Logger:
    def __init__(self):
        # Initiating the logger object
        self.logger = logging.getLogger(__name__)

        # Set the level of the logger. This is SUPER USEFUL since it enables you to decide what logging level to use
        self.logger.setLevel(logging.DEBUG)

        # Create the log.log file
        handler = logging.FileHandler('logs.log')

        # Format the logs sructure so that every line would include the time, name, level name and log message
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        # Adding the format thandler
        self.logger.addHandler(handler)

        # And printing th logs to the console too
        self.logger.addHandler(logging.StreamHandler(sys.stdout))

        # Usage: logger = Logger().logger

        logging.basicConfig(filename="log.log", level=logging.DEBUG)

"""
Set directory
"""

print("Working dir:", os.getcwd())
#os.chdir(str(os.getcwd()) + r'/Scripts/')

"""
Set NLTK stopwords
"""

try:
    nltk.download('stopwords', quiet=True)
    nltk.download('punkt', quiet=True)
    print("[nltk_data] Downloading package stopwords...")
except:
    raise Exception

stop_words = set(stopwords.words('english'))


"""
Access MI voting website
"""
# Chrome 86.0.4240.111 (Official Build) ChromeDriver 86.0.4240.22   
woptions = webdriver.ChromeOptions()
woptions.add_argument("--ignore-ssl-errors")
woptions.add_argument("--ignore-certificate-errors")
woptions.add_argument("--ignore-certificate-errors-spki-list")
#woptions.add_argument("user-data-dir=C:\\Users\\Joe\\AppData\\Local\\Google\\Chrome\\User Data\\Default")
binary = os.path.abspath("C:\chromedriver.exe")
driver = webdriver.Chrome(executable_path="C:\\chromedriver.exe", service_args=["--verbose", "--log-path=C:\\qc1.log"], options = woptions) # make sure Chromedriver version matches Chrome browser version
driver.get("https://mvic.sos.state.mi.us/PublicBallot")
print("Got MI State website...")

"""
Select drop-down menu items for my voting district
"""

select = Select(driver.find_element_by_xpath('//*[@id="Elections"]')).select_by_visible_text('State General - 11/3/2020') # <option value="683">State General - 11/3/2020</option>
time.sleep(2)

county = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "Counties"))) #<option value="41">Kent County</option>
county.click()
time.sleep(2)
count_select = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#Counties > option:nth-child(42)")))
count_select.click()
time.sleep(1)

jurisdiction = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "Jurisdictions")))
jurisdiction.click()
time.sleep(2)
jurisdiction_select = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#Jurisdictions > option:nth-child(15)")))
jurisdiction_select.click()
time.sleep(1)


ward = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "WardPrecincts")))
ward.click()
time.sleep(2)
ward_select = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#WardPrecincts > option:nth-child(17)")))
ward_select.click()
time.sleep(1)

submit = driver.find_element_by_xpath('//*[@id="btnGenerateBallot"]')
submit.click()
time.sleep(10)
print("Sleeping to get page_source...")

page_source = driver.page_source
print("Got page_source...")
time.sleep(2)
# Scrape results
soup = BeautifulSoup(page_source, 'html.parser')
print("Made beautiful soup...")
time.sleep(8)

"""
get list of candidates from soup'd MI State website
"""

print("Making non-Democrats candidates list...")
time.sleep(4)

candidates = []
print("Made empty candidates list...")

# <div class="row row-eq-height row-striped"><div class="col-xs-7 candidate">Joseph R. Biden<br/>Kamala D. Harris</div><div class="col-xs-1 financeLink"> </div><div class="col-xs-4 party" valign="middle">Democratic</div></div>
# Pull only non-Dems
for divs in soup.findAll('div', attrs={'class':'row row-eq-height row-striped'}):
    time.sleep(1)
    print("Got a new div in soup...")

    if divs is None:

        print("Div is empty returning to top of loop...")

        break

    else:

        for child in divs.children:

            if child.text is None:

                print("Element text is blank returning to div...")

                break

            else:

                if child.findNext('div', {"class":"col-xs-4 party"}).text is None:

                        print("Party is blank returning to div...")
                        
                        break

                elif child.findNext('div', {"class":"col-xs-4 party"}).text is not None:

                    if "Democractic" in child.findNext('div', {"class":"col-xs-4 party"}).text != "Democratic" is None: #  

                        print("Democratic candidate: returning to div...")

                        time.sleep(1.5)

                        break
                        
                    elif child.findNext('div', {"class":"col-xs-4 party"}).text != "Democratic":

                        if child.findNext('div', {"class":"col-xs-7 candidate"}) is None:

                            print("Candidate element is blank so returning to top of loop...")
    
                            break

                        elif child.findNext('div', {"class":"col-xs-7 candidate"}):

                            if child.findNext('div', {"class":"col-xs-7 candidate"}).text is None:

                                        print("Candidate text is blank so returning to top of loop...")
                                        
                                        break

                            elif child.findNext('div', {"class":"col-xs-7 candidate"}).text is not None:

                                    candidates.append(child.findNext('div', {"class":"col-xs-7 candidate"}).text)

                                    print("Added candidate to list...")
                        

print("Sorting and deduping list...")
my_candidates = sorted(set(candidates)) #dedupe

"""
create urls text document
"""

# https://stackoverflow.com/questions/2918362/writing-string-to-a-file-on-a-new-line-every-time
print("Pulling candidates websites into url.txt...")
try:
    with open("urls.txt", 'w+') as f:
        print("Creating url.txt...")
        for i in my_candidates:
            for url in search(str(i)+"candidate", tld='com', lang='en', tbs='0', safe='off', num=1, start=0, stop=1, pause=3):
                print("Googled url and writing to txt...")
                f.write(f'{url}\n') # use f-string
                print(url, "written to file...")
		
except:
    raise Exception
        
"""
scrape data (https://www.freecodecamp.org/news/webscraping-in-python/)
"""

try:
    with open("urls.txt", 'rt') as f:
        print("Striping url.txt for unique file creation...")
        urls = f.readlines()
        urls = [url.strip() for url in urls] # strip \n'
except:
    raise Exception

# Retreive all the proxies' IPs and ports and returns a list
def proxies_pool():
    url = 'https://www.sslproxies.org/'

    # Retrieve the site's page.
    with requests.Session() as res:
        proxies_page = res.get(url, timeout=5)

    # Create a BeautifulSoup object and find the table element which consists of all proxies
    soup = BeautifulSoup(proxies_page.content, 'html.parser')
    proxies_table = soup.find(id = 'proxylisttable')

    # Go through all rows in the proxies table and store them in the right format (IP:port) in our proxies list
    proxies = []
    for row in proxies_table.tbody.find_all('tr'):
        proxies.append('{}:{}'.format(row.find_all('td')[0].string, row.find_all('td')[1].string))
    return proxies

# Create random headers for making sure to get all urls with requests
def random_header(logger):
    # Create a dict of accept headers for each user-agent.
    accepts = {"Firefox": "text/html, application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
               "Safari, Chrome": "application/xhtml+xml,application/xml, text/html;q=0.9, text/plainlq=0.8,image/png,*/*,q=0.5"}

    # Get a random user-agent. We used Chrome and Firefox user agents.
    # More at: https://pypi.org/project/fake-useragent/
    try:
        # Getting a suer agent using the fake_useragent package
        ua = UserAgent(cache=True)
        ua.update()
        if random.random() > 0.5:
            random_user_agent = ua.chrome
        else:
            random_user_agent = ua.firefox

    # In case there's a problem with the fake-useragent package, we still want the scraper to function
    # so there's a list of ua's (https://developers.whatismybrowser.com/) that we created and swap to another ua.
    # Be aware of a need to update the list periodically.
    except FakeUserAgentError as error:
        # Save a message to the logs file.
        logger.error("FakeUserAgent didn't work. Generating headers from the pre-defined list of headers. error: {}".format(error))
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
            "Mozilla/5.0 (Windows NT 5.1; rv:7.0.1) Gecko/20100101 Firefox/7.0.1"]
        random_user_agent = random.choice(user_agents)

        # Create the headers dictionary. It's key to match between the ua and the accept headers
    finally:
        valid_accept = accepts["Firefox"] if random_user_agent.find("Firefox") > 0 else accepts ["Safari, Chrome"]
        headers = {"User-Agent": random_user_agent,
                   "Accept": valid_accept}
    return headers

# Generate the header pools for the url request
def create_pools():
    global proxies
    global proxies_pool
    proxies = proxies_pool()
    global logger
    logger = logging.DEBUG
    headers = [random_header(logger) for ind in range(len(proxies))]

    # This traqnsforms the list into itertools.cycle object (iterator) that we can run
    # through using the next() function
    proxies_pool = cycle(proxies)
    global headers_pool
    headers_pool = cycle(headers)
    return proxies_pool, headers_pool

# Usage
print("Creating proxy and header pools...")
proxies_pool, headers_pool = create_pools()
current_proxy = next(proxies_pool)
current_headers = next(headers_pool)

"""
# Introduce the proxy and headers in the GET request
with requests.Session() as req:
    page = req.get(link, )
"""

# Define ETL functions
def download_urls(urls, dir): # write urls to files
    paths = []
    
    for url in urls:
        folder_path = os.getcwd()
        file_name = PurePath(url).parts[1] # Use .name to get everything after the / # control the naming of the txt file (www.donblankenship.com)
        file_path = PurePath(folder_path, str(file_name) + ".txt")
        text = ''

        try:        
            response = requests.get(url,proxies = {"http": current_proxy, "https": current_proxy},
                   headers=current_headers,timeout=10)
            print("Pinged website...")
            
            if response.ok:
                print("Response okay. Sleeping for 5...")
                time.sleep(5)
                print("Requesting website...", url)
                if url == "https://www.linkedin.com/in/elaine-sterrett-isely-382b3b11":
                    continue #skip this item
                req = urllib.request.Request(url, headers=current_headers)
                soup = BeautifulSoup(urllib.request.urlopen(req, timeout=10).read(), features="html.parser") # spoof the server by openning as browser not as urllib
                print("Made soup from candidate website...")
                text = soup.get_text()
            else:
                print(' Bad response for request: ', url, response.status_code)
        except requests.exceptions.ConnectionError as exc:
            print(exc)

        with open(file_path, 'wb') as fh: # save url HTML to text file with website as filename
            fh.write(text.encode('utf-8'))
            print("Wrote candidate HTML to file...")

        paths.append(file_path)

    return paths

def parse_html(path):
    with open(path, 'r', encoding ="utf8") as f:
        print("Openning candidate text file and parsing HTML into soup...") 
        content = f.read().replace('\n','')

    return(BeautifulSoup(content, 'html.parser'))

def download(urls):
    print("Downloading urls...")
    return(download_urls(urls, '.'))

def extract(path):
    print("Sending url to be parsed...")
    return(parse_html(path))

def transform(soup):
    text = soup.get_text()
    if text is not None:
        print("Turning HTML soup into only text...")
        return(text)

def load(key, value):
    d = {}
    d[key] = value # make the dict key subscript equal to the value
    print("Turning urls into a dictionary to be parsed...")
    return(d)

def run_single_command(path):
    soup = extract(path)
    text = transform(soup)
    print("Transforming soup...")
    unserialised = load(path, text if text is not None else '')
    remove_stops(unserialised, text)
    input("Return to exit")
    return(unserialised)

# pre-process text
def remove_stops(stop_word, text):
    word_tokens = word_tokenize(text)
    filtered_txt = [w for w in word_tokens if not w in stop_words]
    filtered_txt = []
    for w in filtered_txt:
        if w not in stop_words:
            print("Creating the new text without the stopwords...")
            filtered_txt.append(w)
    return(word_tokens, filtered_txt)

# function to run full ETL + pre-process
def run_everything(): # default is to run_everything
    l = []

    with open("urls.txt", 'rt') as f:
        urls = f.readlines()
        print("Reading lines from...", f)
        urls = [url.strip() for url in urls] # strip \n'
        print("Made list of urls and stripped spaces from candidate sites for example...", url)

        paths = download(urls)
        print("Downloading url...")
        for path in paths:
            print('Data written to', path.parts[10])
            l.append(run_single_command(path))
            print("Added", path, "to list")# run single ETL process on each file

        return(l)

# set command-line logic
if __name__ == "__main__":
    args = sys.argv

    if len(args) == 1: 
        run_everything()
    else:
        if args[1] == 'download': # only create HTML files
            download([args[2]])
            print('Done')
        if args[1] == 'parse': # use with a single url
            path = args[2]
            result = run_single_command(path)
            print(result)
            
            
"""
Run keyword search
"""
input = ("Do you want to run the keyword search program? Y/N")
if input == "Y":
    import keyword_ranking
else:
    pass


"""
keep command line open
"""

input("Enter to Exit")
