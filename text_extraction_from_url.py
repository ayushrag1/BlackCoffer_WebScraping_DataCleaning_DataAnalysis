#importing Neccesary Library
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry





#reading input Excel_file
url_df=pd.read_excel(r'D:\20211030 Test Assignment\Input.xlsx')


headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0"
}

# All text with title extraction function 
def data_extraction(url):
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    r=session.get(url,headers=headers)
    content=r.content
    soup = BeautifulSoup(content, 'html.parser')
    para_title=soup.title.string
    job_elements = str(soup.find_all("div", class_="td-post-content"))
    para=job_elements.replace('</p>, <p>','\n')
    cleanr = re.compile(r'<[^>]+>')
    para = cleanr.sub('', job_elements)
    cleantext=para.strip('[]')
    all_data= para_title+"\n"+cleantext
    return all_data




file_name=1
for url in url_df['URL_ID']:
    filepath=r'D:\20211030 Test Assignment\Extracted_Data\{i}.txt'.format(file_name)
    data=data_extraction(url)
    # Writing the content of website to the txt file
    with open(filepath,'w',encoding="utf-8") as d:
        for i in data:
            d.write(i)
        file_name+=1










