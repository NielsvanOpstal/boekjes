import requests
from bs4 import BeautifulSoup as soup
import pandas as pd
import openpyxl


def scrape(search_term):

    # dit is de uitgekleede link als je zoekt op orlando virginia woolf
    page = 1
    myUrlOriginal="https://www.boekwinkeltjes.nl/s/?q=avonden+reve&p="
    myUrl = myUrlOriginal + str(page)
    df = pd.DataFrame(columns = ["auteur", "titel"]) # create a dataframe


    while True:
        # getting the page and parsing it to soup (something like that)
        page_soup = soup(requests.get(myUrl).text, "html.parser")
        table = page_soup.find(class_="table-responsive") #gets the table

        if table == None:
            break # als table leeg is, dwz geen (extra?) resultaten, stop met zoeken

        print("looking at page: " + str(page))

        rows = table.findAll("tr") #gets all the rows from the table

        # pak een rij uit de tabel
        for row in rows[1:]: # skipt de eerst rij want die is leeg
                data = {} #maak een lege dictionary die gevuld gaat worden met rij data

                autheurTitel = row.findAll(class_="table-text")
                data["auteur"] = autheurTitel[0].text

                titel = autheurTitel[1].text
                if "meer info" in titel: #clean title
                    titel = titel[17:-34] #haalt de whitespaces aan begin en eind weg
                else:
                    titel = titel[17:-12]

                data["titel"] = titel
                data["bijzonderheden"] = row.findAll(class_="extra")[1].text
                data["prijs"] = row.find(class_="price").select("strong")[0].text #Kan dit anders?/sneller?

                plaatje = row.find(class_="order").find("a").find("img") #haalt het plaatje op

                if plaatje == None: #als er geen plaatje is staat de winkelnaam in de text
                    winkelnaam = row.find(class_="order").find("a").text

                else: # anders in de alt
                    winkelnaam = plaatje.get("alt")
                    if winkelnaam.endswith(" button"): #soms staat er button achter
                        winkelnaam = winkelnaam[:-7] #strip button

                data["winkelnaam"] = winkelnaam

                df = df.append(data, ignore_index = True)


        page +=1
        myUrl = myUrlOriginal + str(page)

    return df

    print("klaar")
