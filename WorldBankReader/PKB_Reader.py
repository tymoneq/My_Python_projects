from pandas_datareader import wb
import pickle


def textFormat(text):
    formatedText = ""
    for s in range(0,len(text)):
        if text[s] != ' ' or (s+1 < len(text) and text[s+1] !=' '):
            formatedText += text[s]
    return formatedText


with open('saved_dictionary.pkl', 'rb') as f:
    CounrtyMap = pickle.load(f)

Countries = []
n = int(input("How many countries do you want to compare? "))
for i in range(0, n):
    country = str(input("Add Country: ").lower())
    country = textFormat(country)
    try:
        Countries.append(CounrtyMap[country])
    except KeyError:
        print("Wrong country name!")
    except:
        print("Upss Error")

Countries = sorted(set(Countries))
start = int(input("Input start year: "))
end = int(input("Input end year: "))
try:
    dat = wb.download(indicator='NY.GDP.PCAP.KD', country=Countries, start=start, end=end)
    print(dat)
except ValueError:
    print("Wrong data")
