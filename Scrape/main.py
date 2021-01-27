from boek import *
import pandas as pd

df = pd.DataFrame()
df = df.append(scrape("Niels"))

print(df)
