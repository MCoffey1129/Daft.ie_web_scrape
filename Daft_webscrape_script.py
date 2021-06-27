# There is a package called daftlistings which was created by Anthony Bloomer and 6 other contributors
# if you want to check that out

# For this code we are assuming that we want to download information from the Daft.ie using BeautifulSoup and
# on a periodic basis.

# Qs 1) Define exactly what we ar looking for?
# Ans 1) For this problem we are looking at what are the prices of all houses in Ireland on the Daft.ie website.

# Qs 2) Where exactly would we get this information if we had to go on the Daft.ie website
# Ans 2) We would go to the following URL - https://www.daft.ie/property-for-sale/ireland for the first 20 properties
#        https://www.daft.ie/property-for-sale/ireland?from=20&pageSize=20 for properties 20 - 40
#        https://www.daft.ie/property-for-sale/ireland?pageSize=20&from=40 for properties 40 - 60
#        https://www.daft.ie/property-for-sale/ireland?pageSize=20&from=60 for properties 60 - 80 etc.
#        as you can see we will be able to creat a loop to bring in all these properties.

# Qs 3) What does the html code look like?
# Ans 3) Go to the main page https://www.daft.ie/property-for-sale/ireland, right click on the page and select "inspect"
#

# Before performing a webscrape of any website the first thing I like to do is to take a look at the html code
# in the website:
# 1) Go to the webpage
# 2) Right click on the page and select "inspect"
# 3) The html code will pop up on your screen


# Import Packages
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import re
import numpy as np


# Connect to the daft website - showing the first 20 houses for sale

req = requests.get('https://www.daft.ie/property-for-sale/ireland')
req_str = req.text

req2 = requests.get('https://www.daft.ie/property-for-sale/ireland?from=20&pageSize=20')
req_str = req_str + req2.text

for i in range(40, 15000, 20):
    url_n = 'https://www.daft.ie/property-for-sale/ireland?pageSize=20&from='+str(i)
    req_n = requests.get(url_n).text
    req_str = req_str + req_n

# Create a beautiful soup object search which will be used to parse the daft.ie website
soup = bs(req_str , 'html.parser')
print(type(soup))



# Use the search object to extract the information required from the html code
# For location it will search the html code where class = 'TitleBlock__Address-sc-1avkvav-7 knPImU'

# There are two styles of ad:
#       A regular ad which contains one property per ad
#       An add which contains multiple properties (issue is that Price is coming in incorrectly)

loc_bs = soup.findAll('p', {'class': 'TitleBlock__Address-sc-1avkvav-7 knPImU'})
bed_bath_area_bs = soup.findAll('div',{'class': 'TitleBlock__CardInfo-sc-1avkvav-9 QvaxK'})
btype_bs = soup.findAll('p', {'class': 'TitleBlock__CardInfoItem-sc-1avkvav-8 bcaKbv'})
price_span_bs = soup.findAll('span', {'class': 'TitleBlock__StyledSpan-sc-1avkvav-4 gDBFnc'})
print(len(loc_bs))

print(bed_bath_area_bs)

# Location and building type do not pick up the "featured value properties" while
# bed/bath/area and price do, however these values are incorrect and need to be deleted

price_lst = []
bba_lst = []
for i in range(len(price_span_bs)):
    pc_txt_i = price_span_bs[i].text
    pc_parent_txt_i = price_span_bs[i].find_parent('a')['href']
    price_lst.append((pc_parent_txt_i,pc_txt_i))

    bba_txt_i = bed_bath_area_bs[i].get_text(separator='·')
    if len(bba_txt_i) > 0:
        bba_lst.append(bba_txt_i)
print(len(price_lst))
print(len(bba_lst))

bed_bath_area_bs[10].text

loc_lst = []
btype_lst = []
for i in range(len(loc_bs)):
    loc_txt_i = loc_bs[i].text
    btype_txt_i = btype_bs[i].text
    loc_lst.append(loc_txt_i)
    btype_lst.append(btype_txt_i)
print(len(loc_lst))
print(len(btype_lst))

#
loc_df = pd.DataFrame(loc_lst,columns = ['address'])


county_lst= ['Co.Antrim','Co.Armagh','Co.Carlow','Co.Cavan','Co.Clare','Co.Cork','Co.Donegal','Co.Down','Co.Dublin',
'Co.Fermanagh','Co.Galway','Co.Kerry','Co.Kildare','Co.Kilkenny','Co.Laois','Co.Leitrim','Co.Limerick','Co.Derry',
'Co.Longford','Co.Louth','Co.Mayo','Co.Meath','Co.Monaghan','Co.Offaly','Co.Roscommon','Co.Sligo','Co.Tipperary',
'Co.Tyrone','Co.Waterford','Co.Westmeath','Co.Wexford','Co.Wicklow']

loc_df.loc[loc_df['address'].isin(county_lst), ['county']] = loc_df['address']
loc_df.head()


pc_df = pd.DataFrame(price_lst,columns = ['ref', 'price'])
pc_df =pc_df.loc[pc_df['ref'].str[:9]=='/for-sale']

bba_df =pd.DataFrame(bba_lst,columns=['bba'])
bba_wrk = bba_df['bba'].str.split(pat='·',expand=True)
bba_wrk.columns = ['bed_t', 'bath_t', 'area_t', 'prop_type_t', 'extra_t']

bba_wrk = bba_wrk.fillna('')



bba_wrk.loc[bba_wrk['bed_t'].str.contains('Bed'), ['bed']] = bba_wrk['bed_t']

bba_wrk.loc[bba_wrk['bed_t'].str.contains('Bath'), ['bath']] = bba_wrk['bed_t']
bba_wrk.loc[bba_wrk['bath_t'].str.contains('Bath'), ['bath']] = bba_wrk['bath_t']

bba_wrk.loc[(bba_wrk['bed_t'].str.contains(r'\d m'))
             | (bba_wrk['bed_t'].str.contains(r'\d ac')) , ['area']] = bba_wrk['bed_t']

bba_wrk.loc[(bba_wrk['bath_t'].str.contains(r'\d m'))
             | (bba_wrk['bath_t'].str.contains(r'\d ac')), ['area']] = bba_wrk['bath_t']

bba_wrk.loc[(bba_wrk['area_t'].str.contains(r'\d m'))
             | (bba_wrk['area_t'].str.contains(r'\d ac')), ['area']] = bba_wrk['area_t']

bba_wrk.loc[(bba_wrk['prop_type_t'].str.contains(r'\d m'))
             | (bba_wrk['prop_type_t'].str.contains(r'\d ac')), ['area']] = bba_wrk['prop_type_t']

bba_wrk.loc[bba_wrk['bed_t'].str.contains(r'\d m'), ['area']] = bba_wrk['bed_t']


prop_lst = ['Apartment','Bungalow','Detached','Duplex','End of Terrace','House','Semi-D','Site ','Studio'\
    ,'Terrace','Townhouse']
bba_wrk.loc[bba_wrk['bed_t'].isin(prop_lst), ['prop_type']] = bba_wrk['bed_t']
bba_wrk.loc[bba_wrk['bath_t'].isin(prop_lst) , ['prop_type']] = bba_wrk['bath_t']
bba_wrk.loc[bba_wrk['area_t'].isin(prop_lst) , ['prop_type']] = bba_wrk['area_t']
bba_wrk.loc[bba_wrk['prop_type_t'].isin(prop_lst), ['prop_type']] = bba_wrk['prop_type_t']



bba_wrk[]

bba_wrk.to_csv(r'Files\bba_wrk.csv', index=False, header=True)

loc_df.shape
pc_df.shape
bba_df.head()

bba_wrk.head(10)

daft_df = pd.concat

bba_wrk.to_csv(r'Files\bba_wrk.csv', index=False, header=True)

################################################################################

req_daft2 = requests.get('https://www.daft.ie/property-for-sale/ireland?from=20&pageSize=20')
req_daft2.text # shows the html code as is which is useless at the moment

https://www.daft.ie/property-for-sale/ireland?pageSize=20&from=40
https://www.daft.ie/property-for-sale/ireland?pageSize=20&from=60
https://www.daft.ie/property-for-sale/ireland?pageSize=20&from=80
https://www.daft.ie/property-for-sale/ireland?pageSize=20&from=100


# Create a beautiful soup object search which will be used to parse the daft.ie website
search2 = bs(req_daft2.content, 'html.parser')
print(type(search2))

# Use the search object to extract the information required from the html code
# For location it will search the html code where class = 'TitleBlock__Address-sc-1avkvav-7'
# Please note we cut off the last few digits in the class in order to bring in the
# featured property

loc_bs = soup.findAll("p", {'class': 'TitleBlock__Address-sc-1avkvav-7 knPImU'})
bed_bath_area_bs = soup.findAll("div",{'class': 'TitleBlock__CardInfo-sc-1avkvav-9 QvaxK'})
btype_bs = soup.findAll("p", {'class': 'TitleBlock__CardInfoItem-sc-1avkvav-8 bcaKbv'})
price_span_bs = soup.findAll("span", {'class': 'TitleBlock__StyledSpan-sc-1avkvav-4 gDBFnc'})

# Location and building type do not pick up the "featured value properties" while
# bed/bath/area and price do, however these values are incorrect and need to be deleted

price_lst = []
bba_lst = []
for i in range(len(price_span_bs)):
    pc_txt_i = price_span_bs[i].text
    price_lst.append((pc_parent_txt_i, pc_txt_i))

    bba_txt_i = bed_bath_area_bs[i].text
    if len(bba_txt_i) > 0:
        bba_lst.append(bba_txt_i)
print(len(price_lst))
print(len(bba_lst))

loc_lst = []
btype_lst = []
for i in range(len(loc_bs)):
    loc_txt_i = loc_bs[i].text
    btype_txt_i = btype_bs[i].text
    loc_lst.append(loc_txt_i)
    btype_lst.append(btype_txt_i)
print(len(loc_lst))
print(len(btype_lst))



loc_bs_sp = search2.findAll("p", {'class': 'TitleBlock__Address-sc-1avkvav-7 eARcqq'})
bed_bath_area_bs_sp = search2.findAll("div",{'class': 'SubUnit__CardInfoItem-sc-10x486s-7 AsGHw'})
price_bs_sp = search2.findAll({"span","p"}, {'class': 'SubUnit__Title-sc-10x486s-5 keXaVZ'})




loc_sp_lst = []
for i in range(len(loc_bs_sp)):
    loc_sp_txt_i = loc_bs_sp[i].text
    loc_parent_txt_i = loc_bs_sp[i].find_next("li")['data-testid']
    loc_sp_lst.append((loc_parent_txt_i, loc_sp_txt_i))

print(loc_sp_lst)




price_sp_lst = []
for i in range(len(price_bs_sp)):
    pc_sp_txt_i = price_bs_sp[i].text
    pc_parent_txt_i = price_bs_sp[i].find_parent("li")['data-testid']
    price_sp_lst.append((pc_parent_txt_i, pc_sp_txt_i))


bba_sp_lst = []
for i in range(len(bed_bath_area_bs_sp)):
    if len(bed_bath_area_bs_sp[i].text) > 0:
        bba_sp_txt_i = bed_bath_area_bs_sp[i].text
        bba_parent_txt_i = bed_bath_area_bs_sp[i].find_parent("li")['data-testid']
        bba_sp_lst.append((bba_parent_txt_i, bba_sp_txt_i))

print(bba_sp_lst)

len(bed_bath_area_bs_sp[0].text)

loc_sp_df = pd.DataFrame(loc_sp_lst,columns = ['join_value', 'address'])
pc_sp_df = pd.DataFrame(price_sp_lst,columns = ['join_value', 'price'])
bba_sp_df =pd.DataFrame(bba_sp_lst,columns=['join_value','bba'])

df_sp = pd.merge(pd.merge(loc_sp_df, pc_sp_df, on=['join_value'], how='outer')
                                    ,bba_sp_df, on=['join_value'], how='outer')

df_sp['address'].fillna(method='ffill', inplace=True)

# df_sp.to_csv(r'Files\df_sp.csv', index=False, header=True)

df_sp['bba'].str.split('·',expand=True,columns=['bedroom', 'bathroom', 'btype', 'area'])

bba_df['bba'].str.split(pat='·',expand=True)