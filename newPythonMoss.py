from bs4 import BeautifulSoup
from pandas.core import base
import requests
import re
import pandas as pd
import os

finish = ''
basePath = "D:\\Fikri\\projects\\PYTHON\\check answer\\data\\for_submit"
problems = os.listdir(basePath)

dat = {}
for p in problems:
    dat[p] = [x[0].split("\\")[len(x[0].split("\\"))-1] for x in os.walk(basePath+"\\"+p)]
    dat[p].pop(0)
import mosspy

userid = 959859792

m = mosspy.Moss(userid, "c")
m.setIgnoreLimit(5)
m.setNumberOfMatchingFiles(250)

datas = []
# Submission Files
for prob in dat:
    print("PROB: "+prob)
    m.files = []
    m.addFilesByWildcard("D:/Fikri/projects/PYTHON/check answer/data/for_submit/"+prob+"/**/*.c")
    m.addFilesByWildcard("D:/Fikri/projects/PYTHON/check answer/data/for_submit/"+prob+"/**/*.cpp")

    # progress function optional, run on every file uploaded
    # result is submission URL
    url = m.send(lambda file_path, display_name: print('*', end='', flush=True))
    print()
    print ("Report Url: " + url)

    url = url if url.startswith('http') else ('http://' + url)


    # parse web
    html_content = requests.get(url).text

    soup = BeautifulSoup(html_content, "lxml")

    constraints = 80
    exist = False
    table = soup.find_all('table')[0]
    for child in table.tr.next_siblings:
        dat = []
        pairs = []
        for td in child:
            a = td.find('a')
            if a is not None:
                pairs.append(a.text.split("/")[len(a.text.split("/"))-2])
                pairs.append(a.text.split("/")[len(a.text.split("/"))-1])
        if(pairs[1].split("_")[0] != pairs[3].split("_")[0]):
            left = int(re.findall(r"\d*%",pairs[1].split(" ")[1])[0][:-1])
            right = int(re.findall(r"\d*%",pairs[3].split(" ")[1])[0][:-1])
            if(left >= constraints and right >= constraints):
                dat.append(pairs[0].split("-")[0])
                dat.append(pairs[0].split("-")[1])
                dat.append(pairs[2].split("-")[0])
                dat.append(pairs[2].split("-")[1])
                dat.append(prob)
                dat.append(pairs[1].split("_")[0])
                dat.append(pairs[3].split("_")[0])
                dat.append(pairs[1].split(" ")[0])
                dat.append(pairs[3].split(" ")[0])
                dat.append(pairs[1].split(" ")[1])
            else:
                continue
        else:
            continue
        datas.append(dat)
    print(datas)
data = pd.DataFrame(datas, columns=['dosen 1','kelas 1','dosen 2','kelas 2','problem','Mahasiswa 1', 'Mahasiswa 2', 'File 1','File 2','percentage'])
print(data)
data.to_excel('D:/Fikri/projects/PYTHON/parse_moss/data_plagiarism_tmp_new.xlsx',index=False)