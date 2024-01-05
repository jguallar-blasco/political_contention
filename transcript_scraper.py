from bs4 import BeautifulSoup
import requests
import re
from urllib import request
from urllib.request import Request, urlopen
import os
from PyPDF2 import PdfReader
import fitz
import json
#from pdfminer.six import extract_text
#import slate3k as slate

 # generates a dictionary of appropriate transcript paths
 # if you already have the text data, set path_to_local_txt to True. 
link_to_file_on_website = True
path_to_local_pdf = False
path_to_local_txt = False

if link_to_file_on_website:
    base_url = "https://www.federalreserve.gov/monetarypolicy/"
if path_to_local_pdf or path_to_local_txt:
    base_directory = "./feddata/"

transcript_links = {}
all_text_files = {}
for year in range(1979, 1987): # from 1982 - 2008
    all_text_files[str(year)] = []
    
    if link_to_file_on_website:
        path = "fomchistorical" + str(year) + ".htm"
        html_doc = requests.get(base_url + path)
        soup = BeautifulSoup(html_doc.content, 'html.parser')
        links = soup.find_all("a", string=re.compile('Transcript .*'))
        link_base_url = "https://www.federalreserve.gov"
        transcript_links[str(year)] = [link_base_url + link["href"] for link in links]
        
    elif path_to_local_pdf or path_to_local_txt:
        files = []
        path_to_folder = base_directory + str(year)
        new_files = os.walk(path_to_folder)
        for file in new_files:
            for f in file[2]:
                if path_to_local_pdf:
                    if f[-3:] == "meeting.pdf":
                        files.append(str(file[0]) + "/" + f)
                elif path_to_local_txt:
                    if f[-11:] == "meeting.txt":
                        files.append(str(file[0]) + "/" + f)
        transcript_links[str(year)] = files
    print("Year Complete: ", year)

all_transcripts = []


for year in transcript_links.keys():
    if not os.path.exists("./feddata/" + year):
        os.makedirs("./feddata/" + year)
    for link in transcript_links[year]:
        #print(link)
        response = Request(str(link), headers={"User-Agent": "Mozilla/5.0"})
        name = re.search("[^/]*$", str(link))
        #print(link)
        all_transcripts.append("./feddata/" + year + "/" + name.group())
        with open("./feddata/" + year + "/" + name.group(), 'wb') as f:
            f.write(urlopen(response).read())
        print("file uploaded")


#print(all_transcripts)


for pdf_transcript in all_transcripts:
    cur_text = ''
    doc = fitz.open(pdf_transcript)
    for page in doc:
        text = page.get_text()
        text_ = text.replace("\n", "")
        cur_text = cur_text + text_
        


    with open(pdf_transcript[:-4] + ".txt", 'w') as f:
        f.write(cur_text)
        print(pdf_transcript)
        print(all_text_files)
        all_text_files[pdf_transcript[10:14]].append(pdf_transcript[:-4] + ".txt")


with open('80s_all_text_files.json', 'w') as fp:
    json.dump(all_text_files, fp)
    



        


