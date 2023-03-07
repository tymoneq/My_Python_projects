from pandas_datareader import wb
import pickle
matches = wb.search('gdp.*capita.*const')
CountryList = []
CountryIso = []
CounrtyMap = {}
for w in wb.get_countries()['name']:
    CountryList.append(w.lower())
for iso in wb.get_countries()['iso2c']:
    CountryIso.append(iso)
for i in range(0, len(CountryIso)):
    CounrtyMap[CountryList[i]] = CountryIso[i]

with open('saved_dictionary.pkl', 'wb') as f:
    pickle.dump(CounrtyMap, f)
