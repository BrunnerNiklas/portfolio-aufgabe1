#Verwendete zusätzliche Packages: selenium, beautifulsoup4, webdriver-manager, lxml, SQLAlchemy

import time
import datetime

from searchresult import Searchresult

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from base import Base,engine,Session


def main():

    searchterm = "data science"
    pages = 3

    crawleGoogle(searchterm, pages)


# BASIC SETTINGS
basesite = "https://www.google.com/search?q="

#ID des Buttons "Weiter zu nächster Seite"
identifier_next_page = "pnnext"
#Klasse der einzelnen Info-Blöcke: Meta-Titel + Meta-Text
identifier_meta_block = "g Ww4FFb tF2Cxc"
identifier_meta_title = "LC20lb MBeuO DKV0Md"
identifier_meta_text = "VwiC3b yXK7lf MUxGbd yDYNvb lyLwlc lEBKkf"


def crawleGoogle(searchterm, pages):

    #Übergabe von Chrome-Parametern
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    #Prüfung, ob Chrome Treiber bereits installiert sind. Falls nicht, Installation automatisch durchführen
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    #Aufrufen der URL
    driver.get(basesite + searchterm)
    #5 Sekunden warten, bis die URL vollständig geladen ist
    driver.implicitly_wait(5)
    # Prüfung, ob nach Cookie-Sammlung gefragt wird. Ggf. Sammlung aller Cookies durch "Klicken" des entsprechenden Buttons akzeptieren
    ActionChains(driver).click(driver.find_element(by=By.ID, value="L2AGLb")).perform()
    #Erneutes Aufrufen der URL
    driver.get(basesite + searchterm)
    #10 Sekunden warten, bis die URL vollständig geladen ist
    time.sleep(10)

    #SQLAlchemy Engine starten
    Base.metadata.create_all(engine)
    #Session eröffnen
    session = Session()

    #Counter für die Ergebnis-URLs, die gecrawlt werden
    pagecounter = 1

    #Iteration der While-Schleife. Am Ende der Schleife pagecounter += 1, bis die Höhe der gewünschten Seitenzahl "pages" erreicht ist
    while pagecounter <= pages:

        #Print-Konsolenausgabe der Nummer, der jeweiligen Ergebnis-URL; Für die Datenbank/Tabelle nicht notwendig.
        print("\nPage #", pagecounter)

        #Soup wird erzeugt. Driver übergibt Ziel-URL. Parser = lxml.
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'lxml')

        #Anzahl der "Meta-Blocks" bzw. Anzahl der Suchergebnisse der URL
        number_of_meta_blocks = len(soup.find_all("div", class_=identifier_meta_block))

        #Counter für die Ergebnisse auf der Ziel-URL, die gecrawlt werden
        searchresultcounter = 1

        #Iteration durch die Suchergebnisse: soup.find_all erzeugt eine Liste, deren Elemente über den jeweiligen Index angesprochen werden können
        while searchresultcounter <= number_of_meta_blocks:

            # Erzeugung des Datum-Strings für das jeweilige Suchergebnis
            fulldate = datetime.datetime.now()
            date = fulldate.strftime("%Y-%m-%d")

            #Meta-Titel-String wird erzeugt; searchresultcounter - 1, da Listenindex bei 0 beginnt.
            meta_title = soup.find_all("h3", class_= identifier_meta_title)[searchresultcounter - 1].text
            # Meta-Text-String wird erzeugt; searchresultcounter - 1, da Listenindex bei 0 beginnt.
            meta_text = soup.find_all("div", class_= identifier_meta_text)[searchresultcounter - 1].text

            #Suchergebnis-Objekt der Klasse Searchresult wird instanziiert; Entspricht einer Zeile der Tabelle
            searchresult = Searchresult(date=date, title=meta_title, text=meta_text)
            #Suchergebis-Instanz wird der Session hinzugefügt
            session.add(searchresult)

            #Print-Konsolenausgabe des Suchergebnisses; Für die Datenbank/Tabelle nicht notwendig.
            print("#" + str(searchresultcounter) + "|" + date + "|" + meta_title + ": " + meta_text)

            searchresultcounter += 1

        # Button "Weiter" klicken, um zur nächsten Seite zu gelangen
        ActionChains(driver).click(driver.find_element(by=By.ID, value=identifier_next_page)).perform()

        pagecounter += 1

        # 10 Sekunden warten, bis die URL vollständig geladen ist
        time.sleep(10)

    #Commit der Session an die SQLAlchemy Engine
    session.commit()
    #Schließen der Session
    session.close()

#Aufruf der Main-Methode
main()