from googlesearch import search
import whois
import datetime
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="YOUR-MYSQL-PASSWORD",
  database="Inspectinator"
)

SUS_SCORE = 0
DOMAIN = ""
HYPHENS = 0
GOOGLE = 0
TLDs = 0

def insert_to_db():
    """inserts result into record table of Inspectinator database,
    for better recall."""
    global DOMAIN
    mycursor = mydb.cursor()
    query = f"INSERT INTO record (domain, sus_score, hyphens, google, tlds) VALUES ('{DOMAIN}', {SUS_SCORE}, {HYPHENS}, {GOOGLE}, {TLDs})"
    mycursor.execute(query)
    mydb.commit()

def is_exisit_in_db():
    """returns domain if DOMAIN is present in database"""
    global DOMAIN
    mycursor = mydb.cursor()

    mycursor.execute(f"SELECT * FROM record where domain='{DOMAIN}'")
    myresult = mycursor.fetchall()
    if len(myresult) == 0:
        return None
    return myresult

def hyphens(url : str):
    """Checks for no. of hyphens in a url,
    if a url contains too many hyphens, then its sus.
    Value of SUS_SCORE is incremented by 1, if url has more than 1 hyphens."""

    global SUS_SCORE
    global HYPHENS
    no_of_hyphens = url.count("-")
    if no_of_hyphens > 1:
        SUS_SCORE += 1
        HYPHENS = 1

def googleAnalysis(url : str):
    """Analyse results of google search,
    if result contains -ve words(like, scam, fake, real....),
    SUS_SCORE is incremented by 4-5.
    very important parameter to be checked."""
    global SUS_SCORE
    global GOOGLE
    results = search(url, num_results=10, sleep_interval=2, advanced=True)
    negative_words = ["fake", "real", "scam", "legit", "fraud", "illegal"]
    negative_words_counter = 0

    for i in results:
        title = i.title.lower()
        description = i.description.lower()

        for words in negative_words:
            negative_words_counter += title.count(words)
            negative_words_counter += description.count(words)

    if negative_words_counter in range(1, 4):
        SUS_SCORE += 4
    
    elif negative_words_counter > 3:
        SUS_SCORE += 5
    GOOGLE = 1

def age(url : str) -> int:
    """Age of the url is checked with whois.
    scam or fake sites are mostly new.
    increments SUS_SCORE by 1 if age is 100-300 days,
    and by 2 if age is less than 100."""
    global SUS_SCORE

    info = whois.whois(url)
    try:
        age_in_days = (datetime.datetime.now() - info.creation_date).days
    except TypeError:
        age_in_days = (datetime.datetime.now() - info.creation_date[0]).days
    
    if age_in_days in range(100, 300):
        SUS_SCORE += 1
    elif age_in_days in range(50, 100):
        SUS_SCORE += 2
    elif age_in_days < 50:
        SUS_SCORE += 3
    
    return age_in_days

def tldCheck(url : str):
    """TLDs(like, com, gov, in....) are more trusted then tlds(like, .bizz),
    increments SUS_SCORE by 1 if not a trusted TLDs."""
    global SUS_SCORE
    global TLDs
    trusted_tlds = ["com", "gov", "in", "org", "us", "net"]
    tld = url.split(".")[-1].removesuffix("/")
    
    if tld not in trusted_tlds:
        SUS_SCORE += 1
    TLDs = 1

def check_all_parameters(url : str):
    """checks all parameters:
        -no. of hyphens
        -analysis of google search results
        -age of the url
        -tld check"""
    global SUS_SCORE
    global DOMAIN
    global HYPHENS
    global GOOGLE
    global TLDs

    SUS_SCORE = 0
    DOMAIN = whois.whois(url).domain
    HYPHENS = 0
    GOOGLE = 0
    TLDs = 0

    db_search_result = is_exisit_in_db()
    if db_search_result != None:
        SUS_SCORE = db_search_result[0][1]
        HYPHENS = db_search_result[0][2]
        GOOGLE = db_search_result[0][3]
        TLDs = db_search_result[0][4]
    
    else:
        hyphens(url)
        googleAnalysis(url)
        age(url)
        tldCheck(url)
        insert_to_db()

# check_all_parameters("https://www.steadyhays.com")
# check_all_parameters("https://www.arw-barrie-transport.com/")
# check_all_parameters("https://www.amazon.com")
# check_all_parameters("https://www.shaadi.com")
# print((SUS_SCORE/10)*100)
