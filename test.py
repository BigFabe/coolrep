import yfinance as yf
import pandas as pd

# Liste von https://github.com/datasets/s-and-p-500-companies/blob/main/data/constituents.csv
symbollist=pd.read_csv("constituents.csv", usecols=["Symbol", "Security", "GICS Sub-Industry"])

stocklist = symbollist["Symbol"].tolist() #macht die Abkürzungen in eine Liste
industrylist = symbollist["GICS Sub-Industry"].tolist() #macht die Kategoien in eine Liste
securitylist = symbollist["Security"].tolist() #Macht die Unternehmensnamen in eine Liste

i=0
namelist = {"Date":"Date"}

for element in stocklist:
    namelist[element]=f"{securitylist[i]} ({element}) | {industrylist[i]}"
    i+=1

try: #versucht einen neuen Tag anzuführen
    data = pd.read_csv("stockwerte.csv",index_col=[0], skipinitialspace=True, header=[0,1])
    #data = data.drop(data.tail(1).index,inplace=True) #das muss weg
    data1 = (yf.download(stocklist, period="1d", group_by="column", keepna=True))
    data1 = data1.rename(columns=namelist)
    stockdata = pd.concat([data, data1], axis=0)
except FileNotFoundError: # wenn Tag nicht gefunden wurde, erstellt neue Tabelle für 1 Jahr
    stockdata = pd.DataFrame()
    stockdata = yf.download(stocklist, period="1y", group_by="column", keepna=True)
    stockdata = stockdata.rename(columns=namelist)
    #print(stockdata)

#print(namelist)#


stockdata.to_csv("stockwerte.csv")


