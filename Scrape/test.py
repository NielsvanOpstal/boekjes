# from urllib.request import urlopen as uReq
import requests
from bs4 import BeautifulSoup as soup
import pandas as pd
# dit is de uitgekleede link als je zoekt op orlando virginia woolf
my_url="https://www.boekwinkeltjes.nl/s/?q=orlando+virginia+woolf&p=1"

# getting the page
print(requests.get(my_url).text)
# response = requests.get(my_url)

# page = response.text
# response.close()
# print(page)

page_soup = soup(page, "html.parser") # put the page in soup


table = page_soup.find(class_="table-responsive") #gets the table

rows = table.findAll("tr") #gets all the rows from the table

df = pd.DataFrame(columns = ["auteur", "titel"]) # create a dataframe:

for i in rows:
    data = {}
    tel = 0
    for ja in i.findAll(class_="table-text"):
        if tel == 0:
            data["auteur"] = ja.text
            tel += 1
        elif tel == 1:
            data["titel"] = ja.text
            df = df.append(data, ignore_index = True)
            break

print(df, sep="\n")
print(type(rows))
