from bs4 import BeautifulSoup
from pandas.core import base
import requests
import re
import pandas as pd
import os

finish = ''
datas = []
while finish != 'y':
    url=input("Input MossApp url: ")
    url = url if url.startswith('http') else ('http://' + url)
    dosen= input("Input kode dosen dan kelas (Dxxxx-Lxxx): ")
    prob = input("Input problem: ")
    html_content = requests.get(url).text
    soup = BeautifulSoup(html_content, "lxml")
    constraints = 80
    exist = False
    table = soup.find_all('table')[0]
    for child in table.tr.next_siblings:
        dat = [dosen, prob]
        pairs = []
        for td in child:
            a = td.find('a')
            if a is not None:
                pairs.append(a.text)
        if(pairs[0].split("_")[0] != pairs[1].split("_")[0]):
            left = int(re.findall(r"\d*%",pairs[0].split(" ")[1])[0][:-1])
            right = int(re.findall(r"\d*%",pairs[1].split(" ")[1])[0][:-1])
            if(left >= constraints and right >= constraints):
                dat.append(pairs[0].split("_")[0])
                dat.append(pairs[1].split("_")[0])
                dat.append(pairs[0].split(" ")[0])
                dat.append(pairs[1].split(" ")[0])
                dat.append(pairs[0].split(" ")[1])
                # exist = True
            else:
                continue
        else:
            continue
        datas.append(dat)
    print(datas)
    finish = input('finish? ')
print(datas)
data = pd.DataFrame(datas, columns=['dosen','problem','Mahasiswa 1', 'Mahasiswa 2', 'File 1','File 2','percentage'])
data.to_excel('data_plagiarism_'+prob+'.xlsx',index=False)
print(data)