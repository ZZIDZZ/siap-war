from bs4 import BeautifulSoup
from html.parser import HTMLParser
import os
from htmldom import htmldom
import requests
import json

# get sia_app_session from env
sia_app_session = os.environ.get('SIA_APP_SESSION')

url = 'https://siap.undip.ac.id/irs/mhs/irs/ajax_irs_data/table'
cookies = {'sia_app_session': sia_app_session}
body = {
    'include_makul[36907]': '36907',
    'include_makul[40697]': '40697',
    'include_makul[40736]': '40736',
    'include_makul[40738]': '40738',
    'include_makul[40750]': '40750',
    'include_makul[41157]': '41157',
    'include_makul[41187]': '41187',
    'include_makul[41188]': '41188',
    'include_makul[41197]': '41197',
    'include_makul[41199]': '41199',
    'include_makul[41205]': '41205',
    'include_makul[41211]': '41211',
    'include_makul[41217]': '41217',
    'include_makul[41220]': '41220',
    'include_makul[41224]': '41224',
    'include_makul[41229]': '41229',
    'include_makul[41234]': '41234',
    'include_makul[41235]': '41235',
    'include_makul[41237]': '41237',
    'include_makul[41813]': '41813',
    'include_makul[41814]': '41814',
    'include_makul[41815]': '41815',
    'include_makul[41816]': '41816',
    'include_makul[41819]': '41819',
    'include_makul[41821]': '41821',
    'include_makul[41823]': '41823',
    'include_makul[41825]': '41825',
    'requested_makul[36907]': '36907',
    'requested_makul[40697]': '40697',
    'requested_makul[40736]': '40736',
    'requested_makul[40738]': '40738',
    'requested_makul[40750]': '40750',
    'requested_makul[41157]': '41157',
    'requested_makul[41187]': '41187',
    'requested_makul[41188]': '41188',
    'requested_makul[41197]': '41197',
    'requested_makul[41199]': '41199',
    'requested_makul[41205]': '41205',
    'requested_makul[41211]': '41211',
    'requested_makul[41217]': '41217',
    'requested_makul[41220]': '41220',
    'requested_makul[41224]': '41224',
    'requested_makul[41229]': '41229',
    'requested_makul[41234]': '41234',
    'requested_makul[41235]': '41235',
    'requested_makul[41237]': '41237',
    'requested_makul[41813]': '41813',
    'requested_makul[41814]': '41814',
    'requested_makul[41815]': '41815',
    'requested_makul[41816]': '41816',
    'requested_makul[41819]': '41819',
    'requested_makul[41821]': '41821',
    'requested_makul[41823]': '41823',
    'requested_makul[41825]': '41825',
}

def send_irs_request():
    r = requests.post(url, cookies=cookies, data=body)
    res = r.text
    # steps to clean: remove double quotes at the start and end of the file -> remove \r -> remove \n -> remove \t -> remove \
    res = res.replace('\\"', '"')
    res = res.replace('\\r', '')
    res = res.replace('\\n', '')
    res = res.replace('\\t', '')
    res = res.replace('\\', '')


    dom = htmldom.HtmlDom()
    dom = dom.createDom(res)
        

    # # find common divs used to display class info
    divs = dom.find('div.bs-callout-grey').text()

    # Split the string into lines
    divs = divs.replace('\n:\n', ' : ')

    lines = divs.strip().split('\n')
    output=  ""
    classes = []
    class_obj = {}
    it = 0
    for line in lines:
        # get line if contain: ("Jenis mata kuliah : PILIHAN", "Kelas", "Kuota kelas", "Kuota terisi", "Waktu mulai", "Waktu selesai", "International Name")
        if "International Name" in line:
            it = 1
            name = line.split(":")[1].strip()
            class_obj["name"] = name
        if "Jenis mata kuliah" in line:
            type = line.split(":")[1]
            class_obj["type"] = type
        if "Kelas" in line:
            class_ = line.split(":")[1]
            class_obj["class"] = class_
        if "Kuota kelas" in line:
            quota = int(line.split(":")[1].strip())
            class_obj["quota"] = quota
        if "Kuota terisi" in line:
            filled = int(line.split(":")[1].strip())
            class_obj["filled"] = filled
        if "Waktu mulai" in line:
            start = line.split(":")[1]
            class_obj["start"] = start
        if "Waktu selesai" in line:
            end = line.split(":")[1]
            class_obj["end"] = end
            class_obj["avl_quota"] = class_obj["quota"] - class_obj["filled"]
            classes.append(class_obj)
            class_obj = {}

    output += "IRS WAR UPDATE\n\n"
            
    for cl in classes:
        if cl['type'] == " PILIHAN" and cl['avl_quota'] > 0:
            class_full = cl['avl_quota'] <= 0
            if class_full:
                output += f"{cl['name']} (FULL)\n"
            else:
                output += f"{cl['name']} (AVAILABLE)\n"
            output += f"available: {cl['avl_quota']}\n"
            output += f"quota: {cl['quota']}\n"
            output += f"filled: {cl['filled']}\n"
            output += f"start: {cl['start']}\n"
            output += f"end: {cl['end']}\n"
            output += f"class: {cl['class']}\n"
            output += f"\n"
            
    if "AVAILABLE" not in output:
        output += "Zannen, no available class yet\n"

    return output


    
            