from boek import *
import pandas as pd
import numpy as np



boeken = ["perennial philosophy", "island", "doors of perception", "hemel", "de avonden"]
authors = ["huxley", "huxley", "huxley", "Mulisch", "reve"]

# boeken = ["de aanslag", "ontdekking van de hemel", "twee vrouwen"]
# author = "Mulisch"
dfs = {}
totalresults = pd.DataFrame()
# dict with all found books per title
for boek, author in zip(boeken, authors):
    dfs[boek] = scrape(boek, author)
    totalresults = totalresults.append(dfs[boek])

# Shops per book
shops = {}

# All unique shops
shops_unique = np.array([])


for boek in boeken:
    shops[boek] = pd.unique(dfs.get(boek)["winkelnaam"])
    shops_unique = np.append(shops_unique, pd.unique(dfs.get(boek)["winkelnaam"]))
shops_unique = np.unique(shops_unique)

# Number of books searched per store on sale
winkels = {}

for unique_shop in shops_unique:
    winkels[unique_shop] = 0
    for boek in boeken:
        if unique_shop in shops[boek]:
            winkels[unique_shop] += 1

sorter = sorted(winkels, key = lambda x: winkels[x], reverse = True)
totalresults.winkelnaam = totalresults.winkelnaam.astype("category")
totalresults.winkelnaam.cat.set_categories(sorter, inplace = True)
totalresults = totalresults.sort_values(["winkelnaam", "prijs"])

totalresults.to_excel("total.xlsx")

df = pd.DataFrame({"winkelnaam": pd.Series([], dtype = "str"),
                    "titel": pd.Series([], dtype = "str"),
                    "prijs": pd.Series([], dtype = "float"),
                    "bijzonderheden": pd.Series([], dtype = "str")})
