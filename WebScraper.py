import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

donor_namelist = []
donor_addresslist = []
donor_numlist = []

name_list = pd.read_csv("C:\\Users\\junog\\Documents\\GGR322\\donorlist.csv")

url_name = name_list['FN'] + "+" + name_list['LN']

y = 0

for url in url_name:
    namer = url_name[y]
    pages = requests.get("https://www.canada411.ca/search/si/1/" + str(namer) + "/Hamilton+ON/?pgLen=25")
    soup = bs(pages.text, 'lxml')
    donor_restop = soup.find(class_ = 'c411ResultsTop')
    donor_results = str(donor_restop)
    y+=1
    print(y)

    try:
        donor_realnum = donor_results.split('>')[2]
        donor_resnum = int(donor_realnum.split()[0])

    except Exception as e:
        donor_resnum = 0

    if "similar" in donor_realnum:
        donor_resnum = 0
    else:
        try:
            donor_resnum = int(donor_realnum.split()[0])
        except Exception as e:
            donor_resnum = 0

    if donor_resnum > 0:
        donor_name = soup.find_all(class_ = "c411ListedName")
        donor_namestr = str(donor_name)
        donor_address = soup.find_all(class_="adr")
        donor_addstr = str(donor_address)
        donor_phone = soup.find_all(class_="c411Phone")
        donor_phonestr = str(donor_phone)

        try:

            for i in range(0, donor_resnum):
                donor_namelistee = donor_namestr.split('h2 class="c411ListedName"')
                if len(donor_namelistee) > 1:
                    donor_namelistee = donor_namestr.split('h2 class="c411ListedName"')[i]
                    if len(donor_namelistee) > 1:
                        donor_namesplit = donor_namelistee.split("=")[-1]
                        donor_address = donor_namesplit.split(">")[0]
                        donor_testing = donor_address.split("on")[0]
                donor_namelist.append(donor_testing)

                donor_addsplit = donor_addstr.split('span class="adr"')
                if len(donor_addsplit) > 1:
                    donor_addsplit = donor_addstr.split('span class="adr"')[i]
                    donor_addlister = donor_addsplit.split(">")
                    if len(donor_addlister) > 1:
                        donor_addlister = donor_addlister[1].split("<")[0]
                donor_addresslist.append(donor_addlister)

                donor_phonestring = donor_phonestr.split()
                if len(donor_phonestring) > 1:
                    donor_phonestring = donor_phonestr.split('class="c411Phone"')[i]
                    donor_phonesplit = donor_phonestring.split(">")
                    if len(donor_phonesplit) > 1:
                        donor_phonesplit = donor_phonestring.split(">")[1]
                        if len(donor_phonesplit) > 1:
                            donor_phonesplit = donor_phonesplit.split("<")[0]
                donor_numlist.append(donor_phonesplit)

            donor_list = pd.DataFrame({'name':donor_namelist,
                                       'address':donor_addresslist,
                                       'phone-number':donor_numlist})
        except Exception as e:
            donor_resnum = 0

donor_list.to_csv("C:\\Users\\junog\\Documents\\GGR322\\donorinfo.csv")






















