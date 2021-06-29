# There is a package called daftlistings which was created by Anthony Bloomer and 6 other contributors
# if you want to check that out

# For this code we are assuming that we want to download information from the Daft.ie using BeautifulSoup and
# on a periodic basis.

# For webscraping there are some key questions you first want to answer:

# Qs 1) Define exactly what you ar looking for?
# Ans 1) We want to pull the following information from properties which are for sale on the Daft.ie website:
#        Property price, location, number of bedrooms, number of bathrooms and type of property
#        (we will also include any land that is for sale which can be easily deleted at a later time)


# Qs 2)  Where exactly would we get this information on the Daft.ie website?
# Ans 2) We would go to the following URL - https://www.daft.ie/property-for-sale/ireland for the first 20 adverts
#        https://www.daft.ie/property-for-sale/ireland?from=20&pageSize=20 for adverts 20 - 40
#        https://www.daft.ie/property-for-sale/ireland?pageSize=20&from=40 for adverts 40 - 60
#        https://www.daft.ie/property-for-sale/ireland?pageSize=20&from=60 for adverts 60 - 80 etc.
#        as you can see we will be able to create a loop to bring in all these properties.

# Qs 3)  What does the html code look like?
# Ans 3) Go to the main page https://www.daft.ie/property-for-sale/ireland, right click on the page and select "inspect"
#        The html code will show up on your screen.

# Qs 4)  Is there any potential inconsistencies in the html code which will make it difficult to scrape property info?
# Ans 4) Most properties on "Daft.ie" are in the let us say the "normal" format whereby each block of code contains the
#        price, location, bedrooms etc. all in one section of the code.
#        There are however "special" ads, these are ads that usually have multiple properties for sale at one location,
#        the issue for us is that the html code for these properties is inconsistent with code for the other properties.
#        We will pull these two sets of properties out separately and combine them at the end.

# Import Packages
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import re
import numpy as np


################################################################################################################
# Section 1 - We will firstly do a simple webscrape of the first 20 ads on Daft.ie to see if there is
#             any potential issues with the code
################################################################################################################

# Pull the html code into a variable called req
req = requests.get('https://www.daft.ie/property-for-sale/ireland')
req_str = req.text
print(req_str) # prints the html code

# Create a beautiful soup object soup which will be used to parse the html code
soup = bs(req_str, 'html.parser')
print(type(soup))

# From looking at the html code the location information for the first property is in the following block of html
# <p data-testid="address" class="TitleBlock__Address-sc-1avkvav-7 knPImU">30 Cedarmount Road, Mount Merrion,
# Co. Dublin</p>
# You can obviously try using string operations to pull out the address for each property but the best way of doing this
# is through BeautifulSoup. We want to search our html for each paragraph whic
loc_bs = soup.findAll('p', {'class': 'TitleBlock__Address-sc-1avkvav-7 knPImU'})
bed_bath_area_bs = soup.findAll('div', {'class': 'TitleBlock__CardInfo-sc-1avkvav-9 QvaxK'})
btype_bs = soup.findAll('p', {'class': 'TitleBlock__CardInfoItem-sc-1avkvav-8 bcaKbv'})
price_span_bs = soup.findAll('span', {'class': 'TitleBlock__StyledSpan-sc-1avkvav-4 gDBFnc'})






# Connect to the daft website - showing the first 20 houses for sale

req = requests.get('https://www.daft.ie/property-for-sale/ireland')
req_str = req.text

req2 = requests.get('https://www.daft.ie/property-for-sale/ireland?from=20&pageSize=20')
req_str = req_str + req2.text

for i in range(40, 15000, 20):
    url_n = 'https://www.daft.ie/property-for-sale/ireland?pageSize=20&from=' + str(i)
    req_n = requests.get(url_n).text
    req_str = req_str + req_n

# Create a beautiful soup object search which will be used to parse the daft.ie website
soup = bs(req_str, 'html.parser')
print(type(soup))

# Use the search object to extract the information required from the html code
# For location it will search the html code where class = 'TitleBlock__Address-sc-1avkvav-7 knPImU'

# There are two styles of ad:
#       A regular ad which contains one property per ad
#       An add which contains multiple properties (issue is that Price is coming in incorrectly)

loc_bs = soup.findAll('p', {'class': 'TitleBlock__Address-sc-1avkvav-7 knPImU'})
bed_bath_area_bs = soup.findAll('div', {'class': 'TitleBlock__CardInfo-sc-1avkvav-9 QvaxK'})
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
    price_lst.append((pc_parent_txt_i, pc_txt_i))

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
loc_df = pd.DataFrame(loc_lst, columns=['address'])
loc_df['county'] = loc_df['address'].str.extract('(Co. [A-Z][a-z]+)', expand=True)
loc_df.head()

pc_df = pd.DataFrame(price_lst, columns=['ref', 'price'])
pc_df = pc_df.loc[pc_df['ref'].str[:9] == '/for-sale']
pc_df.reset_index(inplace=True)
pc_df.drop(columns=['index', 'ref'], inplace=True)
pc_df.head()

# Create a numeric price field
pc_df['price'] = pc_df['price'].str.strip()
pc_df['price_n'] = pc_df['price'].replace({'\€': '', ',': '', 'AMV: ': '', 'AMV: Price on Application': '0'
                                              , 'Price on Application': '0'
                                              , '(£.*?)[\s]': ''
                                              , '[\(\)]': ''}
                                          , regex=True).astype(float)

pc_df.info()

bba_df = pd.DataFrame(bba_lst, columns=['bba'])
bba_wrk = bba_df['bba'].str.split(pat='·', expand=True)
bba_wrk.columns = ['bed_t', 'bath_t', 'area_t', 'prop_type_t', 'extra_t']
bba_wrk = bba_wrk.apply(lambda x: x.str.strip())
bba_wrk = bba_wrk.fillna('')
bba_wrk.head()

bba_wrk.loc[bba_wrk['bed_t'].str.contains('Bed'), ['bed']] = bba_wrk['bed_t']

bba_wrk.loc[bba_wrk['bed_t'].str.contains('Bath'), ['bath']] = bba_wrk['bed_t']
bba_wrk.loc[bba_wrk['bath_t'].str.contains('Bath'), ['bath']] = bba_wrk['bath_t']

prop_lst = ['Apartment', 'Bungalow', 'Detached', 'Duplex', 'End of Terrace', 'House', 'Semi-D', 'Site', 'Studio' \
    , 'Terrace', 'Townhouse']
bba_wrk.loc[bba_wrk['bed_t'].isin(prop_lst), ['prop_type']] = bba_wrk['bed_t']
bba_wrk.loc[bba_wrk['bath_t'].isin(prop_lst), ['prop_type']] = bba_wrk['bath_t']
bba_wrk.loc[bba_wrk['area_t'].isin(prop_lst), ['prop_type']] = bba_wrk['area_t']
bba_wrk.loc[bba_wrk['prop_type_t'].isin(prop_lst), ['prop_type']] = bba_wrk['prop_type_t']
bba_wrk.head()

bba_wrk.loc[(bba_wrk['bed_t'].str.contains(r'\d m'))
            | (bba_wrk['bed_t'].str.contains(r'\d ac')), ['area']] = bba_wrk['bed_t']

bba_wrk.loc[(bba_wrk['bath_t'].str.contains(r'\d m'))
            | (bba_wrk['bath_t'].str.contains(r'\d ac')), ['area']] = bba_wrk['bath_t']

bba_wrk.loc[(bba_wrk['area_t'].str.contains(r'\d m'))
            | (bba_wrk['area_t'].str.contains(r'\d ac')), ['area']] = bba_wrk['area_t']

bba_wrk.loc[(bba_wrk['prop_type_t'].str.contains(r'\d m'))
            | (bba_wrk['prop_type_t'].str.contains(r'\d ac')), ['area']] = bba_wrk['prop_type_t']

bba_df_final = bba_wrk.drop(columns=['bed_t', 'bath_t', 'area_t', 'prop_type_t', 'extra_t'])
bba_df_final.fillna('', inplace=True)
bba_df_final.head()

daft_df_1 = pd.concat([loc_df, bba_df_final, pc_df], axis=1)
daft_df_1.head()

daft_df_1.shape

################################################################################


# Use the search object to extract the information required from the html code
# For location it will search the html code where class = 'TitleBlock__Address-sc-1avkvav-7'
# Please note we cut off the last few digits in the class in order to bring in the
# featured property

loc_bs_sp = soup.findAll("p", {'class': 'TitleBlock__Address-sc-1avkvav-7 eARcqq'})
bed_bath_area_bs_sp = soup.findAll("div", {'class': 'SubUnit__CardInfoItem-sc-10x486s-7 AsGHw'})
price_bs_sp = soup.findAll({"span", "p"}, {'class': 'SubUnit__Title-sc-10x486s-5 keXaVZ'})

loc_sp_lst = []
for i in range(len(loc_bs_sp)):
    loc_sp_txt_i = loc_bs_sp[i].text
    loc_next_txt_i = loc_bs_sp[i].find_parent("li")['data-testid']
    loc_sp_lst.append((loc_next_txt_i, loc_sp_txt_i))

price_sp_lst = []
for i in range(len(price_bs_sp)):
    pc_sp_txt_i = price_bs_sp[i].text
    pc_parent_txt_i = price_bs_sp[i].find_parents("li")[1]['data-testid']
    price_sp_lst.append((pc_parent_txt_i, pc_sp_txt_i))

print(price_sp_lst)

bba_sp_lst = []
for i in range(len(bed_bath_area_bs_sp)):
    if len(bed_bath_area_bs_sp[i].text) > 0:
        bba_sp_txt_i = bed_bath_area_bs_sp[i].text
        bba_parent_txt_i = bed_bath_area_bs_sp[i].find_parents("li")[1]['data-testid']
        bba_sp_lst.append((bba_parent_txt_i, bba_sp_txt_i))

bba_sp_lst[0:4]

loc_sp_df = pd.DataFrame(loc_sp_lst, columns=['join_value', 'address'])
loc_sp_df['county'] = loc_sp_df['address'].str.extract('(Co. [A-Z][a-z]+)', expand=True)
loc_sp_df.head()
loc_sp_df.shape

pc_sp_df = pd.DataFrame(price_sp_lst, columns=['join_value', 'price'])
pc_sp_df.head()
pc_sp_df.shape

pc_sp_df['price_n'] = pc_sp_df['price'].replace({'\€': '', ',': '', 'AMV: ': '', 'AMV: Price on Application': '0'
                                                    , 'Price on Application': '0'
                                                    , '(£.*?)[\s]': ''
                                                    , '[\(\)]': ''}
                                                , regex=True).astype(float)

pc_sp_df.info()

bba_sp_df = pd.DataFrame(bba_sp_lst, columns=['join_value', 'bba'])
bba_sp_df.head()
bba_sp_df.shape

bba_sp_wrk = bba_sp_df['bba'].str.split(pat='·', expand=True)
bba_sp_wrk.columns = ['bed_t', 'bath_t', 'prop_type_t']
bba_sp_wrk = bba_sp_wrk.apply(lambda x: x.str.strip())
bba_sp_wrk = bba_sp_wrk.fillna('')
bba_sp_wrk.head()

bba_sp_wrk.loc[bba_sp_wrk['bed_t'].str.contains('Bed'), ['bed']] = bba_sp_wrk['bed_t']

bba_sp_wrk.loc[bba_sp_wrk['bed_t'].str.contains('Bath'), ['bath']] = bba_sp_wrk['bed_t']
bba_sp_wrk.loc[bba_sp_wrk['bath_t'].str.contains('Bath'), ['bath']] = bba_sp_wrk['bath_t']

bba_sp_wrk.loc[bba_sp_wrk['bed_t'].isin(prop_lst), ['prop_type']] = bba_sp_wrk['bed_t']
bba_sp_wrk.loc[bba_sp_wrk['bath_t'].isin(prop_lst), ['prop_type']] = bba_sp_wrk['bath_t']
bba_sp_wrk.loc[bba_sp_wrk['prop_type_t'].isin(prop_lst), ['prop_type']] = bba_sp_wrk['prop_type_t']

bba_sp_wrk['area'] = ''

bba_sp_df_final = pd.concat([bba_sp_df['join_value'], bba_sp_wrk.drop(columns=['bed_t', 'bath_t', 'prop_type_t'])]
                            , axis=1)
bba_sp_df_final.fillna('', inplace=True)
bba_sp_df_final.head()

daft_df_2 = pd.merge(pd.merge(loc_sp_df, bba_sp_df_final, on=['join_value'], how='inner')
                     , pc_sp_df, on=['join_value'], how='inner')

daft_df_2.drop_duplicates(subset=['join_value', 'address', 'county', 'price', 'bed', 'bath', 'prop_type']
                          , inplace=True)

daft_df_2.to_csv(r'Files\daft_df_2.csv', index=False, header=True)

daft_df_2.drop(columns=['join_value'], axis=1, inplace=True)

daft_df = pd.concat([daft_df_1, daft_df_2], ignore_index=True)
daft_df.head()
daft_df.tail()

# Write out the file to excel
pc_df.to_csv(r'Files\pc_df.csv', index=False, header=True)
