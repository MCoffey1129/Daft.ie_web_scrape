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
print(req_str)  # prints the html code

# Create a beautiful soup object soup which will be used to parse the html code
soup = bs(req_str, 'html.parser')
print(type(soup))

# From looking at the html code the location information for the first property is in the following block of html
# <p data-testid="address" class="TitleBlock__Address-sc-1avkvav-7 knPImU">30 Cedarmount Road, Mount Merrion,
# Co. Dublin</p>
# You can obviously try using string operations to pull out the address for each property but the best way of doing this
# is through BeautifulSoup. We want to search our html for each paragraph ('p') which contains class = "TitleBlock...."
# We repeat for bringing in the bed, bath and area (this is in one section of code), building type and price.

loc_bs = soup.findAll('p', {'class': 'TitleBlock__Address-sc-1avkvav-7 knPImU'})
bed_bath_area_bs = soup.findAll('div', {'class': 'TitleBlock__CardInfo-sc-1avkvav-9 QvaxK'})
btype_bs = soup.findAll('p', {'class': 'TitleBlock__CardInfoItem-sc-1avkvav-8 bcaKbv'})
price_span_bs = soup.findAll('span', {'class': 'TitleBlock__StyledSpan-sc-1avkvav-4 gDBFnc'})

len(loc_bs)  # not all of the ads are brought into Python at the time of running this only 19 properties are included

# Let us put the first 17 values into a list and then a dataframe to see if there are any issues
prop_info = []
for i in range(17):
    prop_info_i = [loc_bs[i].text, bed_bath_area_bs[i].text, btype_bs[i].text, price_span_bs[i].text]
    prop_info.append(prop_info_i)

prop_info_df = pd.DataFrame(prop_info)
print(prop_info_df)

# Findings:
# The code correctly brings in the location (column 1), bed, bath and area (column 2), property type (column 3)
# and price (column 4). There are a number of issues however, the html code is written differently
# for the "special" or ads which contain multiple properties. At present we are not taking in any information on these
# properties except that we are incorrectly bringing in the Price which looks to actually be a statement. You should
# be able to see this in your code as the price and location are not matched.
# We need to take note of this when we do our webscrape!!


################################################################################################################
# Section 2 - This is a webscrape of the "normal" or "typical" ads on Daft.ie such that
#             each block of html code contains information on one property (price, location, bedrooms etc.)
################################################################################################################

# Pull the html code in text format into a variable called req_str for the first 15,000 properties
# which is close to the total number of properties for sale on Daft.
req = requests.get('https://www.daft.ie/property-for-sale/ireland')
req_str = req.text

req2 = requests.get('https://www.daft.ie/property-for-sale/ireland?from=20&pageSize=20')
req_str = req_str + req2.text

for i in range(40, 15000, 20):
    url_n = 'https://www.daft.ie/property-for-sale/ireland?pageSize=20&from=' + str(i)
    req_n = requests.get(url_n).text
    req_str = req_str + req_n

# Create a beautiful soup object soup which will be used to parse the html code
soup = bs(req_str, 'html.parser')
print(type(soup))

# Parse the html code (similar to previous)
loc_bs = soup.findAll('p', {'class': 'TitleBlock__Address-sc-1avkvav-7 knPImU'})
bed_bath_area_bs = soup.findAll('div', {'class': 'TitleBlock__CardInfo-sc-1avkvav-9 QvaxK'})
btype_bs = soup.findAll('p', {'class': 'TitleBlock__CardInfoItem-sc-1avkvav-8 bcaKbv'})
price_span_bs = soup.findAll('span', {'class': 'TitleBlock__StyledSpan-sc-1avkvav-4 gDBFnc'})
print(len(loc_bs))
print(bed_bath_area_bs)

# Due to the make up of how the html code information on Bed/bath/area and price  from the "special" or multiple
# property ads are included.
# For Bed/bath/area these have been brought in with a missing text value for which we will remove by
# specifying that the length must be greater than zero.
# Price for "special" ads has been brought in incorrectly, we can distinguish these cases  which we do not want
# included based off of their parent value (we use the anchor reference as the parent value).
# To learn more about parents, siblings and the whole family tree in beautifulSoup there are some
# excellent YouTube videos which I am happy to share

price_lst = []
bba_lst = []
for i in range(len(price_span_bs)):
    pc_txt_i = price_span_bs[i].text
    pc_parent_txt_i = price_span_bs[i].find_parent('a')['href']
    price_lst.append((pc_parent_txt_i, pc_txt_i))

    # Creating a seperator as this will make it easier to split into separate columns later
    bba_txt_i = bed_bath_area_bs[i].get_text(separator='·')
    if len(bba_txt_i) > 0:
        bba_lst.append(bba_txt_i)
print(len(price_lst))
print(len(bba_lst))

# Location and property/building type

loc_lst = []
btype_lst = []
for i in range(len(loc_bs)):
    loc_txt_i = loc_bs[i].text
    btype_txt_i = btype_bs[i].text
    loc_lst.append(loc_txt_i)
    btype_lst.append(btype_txt_i)
print(len(loc_lst))
print(len(btype_lst))

#   Location
#   Convert the location list into a dataframe
#   Use regex to extract the county from the address column, we can achieve this because we know that
#   the County on the address will always follow "Co." If you are ever in doubt on regex use the following website
#   https://regex101.com/r/CMGOHz/1

#   Going forward you may want to do more segregation on the address column. You may want to get the town associated
#   with each property by passing in the list of all towns and villages in Ireland that you have pulled from the
#   following Wikipedia page https://en.wikipedia.org/wiki/List_of_towns_and_villages_in_the_Republic_of_Ireland

loc_df = pd.DataFrame(loc_lst, columns=['address'])
loc_df['county'] = loc_df['address'].str.extract('(Co. [A-Z][a-z]+)', expand=True)
loc_df.head()

#   Price
#   Only keep properties which have a parent address which starts with '/for-sale' as we know that these are
#   the properties we are interested in

pc_df = pd.DataFrame(price_lst, columns=['ref', 'price'])
pc_df = pc_df.loc[pc_df['ref'].str[:9] == '/for-sale']
pc_df.reset_index(inplace=True)
pc_df.drop(columns=['index', 'ref'], inplace=True)
pc_df.head()

# The price field is a character field. We want to remove all €,£, and any character fields such as price on
# application
pc_df['price'] = pc_df['price'].str.strip()
pc_df['price_n'] = pc_df['price'].replace({'\€': '',  # € symbols replaced with ''
                                           ',': '',  # , replaced with ''
                                           'AMV: ': '',  # AMV replaced with ''
                                           'AMV: Price on Application': '0', # AMV PoA replaced with '0'
                                           'Price on Application': '0', # PoA replaced with '0'
                                           '(£.*?)[\s]': '',   # converts '£2,000 (€2,300)' to '(€2,300)'
                                           '[\(\)]': '' } # converts (2300) to 2300
                                          , regex=True).astype(float)

pc_df.info() # check to ensure price_n is numeric


#   Bed/Bath/Area
#   Split the Bed/Bath/Area dataframe into each of its components, please note the 'extra' column contains
#   auctioneer information which we are not interested in
#   Each of the columns are given a suffix '_t' as they are temporary columns as info for many properties are in the
#   wrong columns e.g. prop_type info could be in the "bath" column.


bba_df = pd.DataFrame(bba_lst, columns=['bba'])
bba_wrk = bba_df['bba'].str.split(pat='·', expand=True)
bba_wrk.columns = ['bed_t', 'bath_t', 'area_t', 'prop_type_t', 'extra_t']
# useful code for removing the trailing balanks for the char fields in the dataset
bba_wrk = bba_wrk.apply(lambda x: x.str.strip())
bba_wrk = bba_wrk.fillna('')
bba_wrk.head()

# Bed
# Information on the number of bedrooms will only ever be contained in the bed column
bba_wrk.loc[bba_wrk['bed_t'].str.contains('Bed'), ['bed']] = bba_wrk['bed_t']

# Bath
# The number of bathrooms could be contained in either 'bed_t' or bath_t
bba_wrk.loc[bba_wrk['bed_t'].str.contains('Bath'), ['bath']] = bba_wrk['bed_t']
bba_wrk.loc[bba_wrk['bath_t'].str.contains('Bath'), ['bath']] = bba_wrk['bath_t']

# Proprty Type
# For property type we pass a list through the dataframe to create our property type column
prop_lst = ['Apartment', 'Bungalow', 'Detached', 'Duplex', 'End of Terrace', 'House', 'Semi-D', 'Site', 'Studio' \
    , 'Terrace', 'Townhouse']
bba_wrk.loc[bba_wrk['bed_t'].isin(prop_lst), ['prop_type']] = bba_wrk['bed_t']
bba_wrk.loc[bba_wrk['bath_t'].isin(prop_lst), ['prop_type']] = bba_wrk['bath_t']
bba_wrk.loc[bba_wrk['area_t'].isin(prop_lst), ['prop_type']] = bba_wrk['area_t']
bba_wrk.loc[bba_wrk['prop_type_t'].isin(prop_lst), ['prop_type']] = bba_wrk['prop_type_t']
bba_wrk.head()

# Area
# For getting the area of each property we use regex to look for either the pattern "[some number] m" or
# "[some number] ac" to get the area as the area of properties will either be quoted in m^2 or in acres.
bba_wrk.loc[(bba_wrk['bed_t'].str.contains(r'\d m'))
            | (bba_wrk['bed_t'].str.contains(r'\d ac')), ['area']] = bba_wrk['bed_t']

bba_wrk.loc[(bba_wrk['bath_t'].str.contains(r'\d m'))
            | (bba_wrk['bath_t'].str.contains(r'\d ac')), ['area']] = bba_wrk['bath_t']

bba_wrk.loc[(bba_wrk['area_t'].str.contains(r'\d m'))
            | (bba_wrk['area_t'].str.contains(r'\d ac')), ['area']] = bba_wrk['area_t']

bba_wrk.loc[(bba_wrk['prop_type_t'].str.contains(r'\d m'))
            | (bba_wrk['prop_type_t'].str.contains(r'\d ac')), ['area']] = bba_wrk['prop_type_t']

# Remove the temporary columns
bba_df_final = bba_wrk.drop(columns=['bed_t', 'bath_t', 'area_t', 'prop_type_t', 'extra_t'])
bba_df_final.fillna('', inplace=True)
bba_df_final.head()

# Create a dataframe containing all of the information on "normal" ads quoted on Daft.ie
daft_df_1 = pd.concat([loc_df, bba_df_final, pc_df], axis=1)
daft_df_1.head()



################################################################################################################
# Section 3 - This is a webscrape of the "special" or "multiple property" ads on Daft.ie such that
#             the address and the properties are in separate blocks of html code
################################################################################################################


# Extract the required information using soup
loc_bs_sp = soup.findAll("p", {'class': 'TitleBlock__Address-sc-1avkvav-7 eARcqq'})
bed_bath_area_bs_sp = soup.findAll("div", {'class': 'SubUnit__CardInfoItem-sc-10x486s-7 AsGHw'})
price_bs_sp = soup.findAll({"span", "p"}, {'class': 'SubUnit__Title-sc-10x486s-5 keXaVZ'})

# Similar to Section 2 we get the location, price and bba lists by looping through each of the text fields
# The issue we face with these properties is that we have multiple properties associated with singular locations
# so we will have to create an identifier for linking each property to the correct location
# We know that the parent ("li")['data-testid'] of the location is equal to the "grandparent" (the second result
# of the find_parents) of the price and bba, we will use this to join the dataframes later in the code.

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


#   Location
#   No change from the previous code except we now have a 'join_value'
loc_sp_df = pd.DataFrame(loc_sp_lst, columns=['join_value', 'address'])
loc_sp_df['county'] = loc_sp_df['address'].str.extract('(Co. [A-Z][a-z]+)', expand=True)
loc_sp_df.head()
loc_sp_df.shape

#   Location
#   No change from the previous code except we now have a 'join_value'
pc_sp_df = pd.DataFrame(price_sp_lst, columns=['join_value', 'price'])
pc_sp_df.head()
pc_sp_df.shape

pc_sp_df['price_n'] = pc_sp_df['price'].replace({'\€': '',
                                                 ',': '',
                                                 'AMV: ': '',
                                                 'AMV: Price on Application': '0',
                                                 'Price on Application': '0',
                                                 '(£.*?)[\s]': '',
                                                 '[\(\)]': ''}
                                                , regex=True).astype(float)

pc_sp_df.info()


#   Bed/Bath/Area
#   No change from the previous code, we do not have any information on area so we will create an Area field
#   which is blank

bba_sp_df = pd.DataFrame(bba_sp_lst, columns=['join_value', 'bba'])
bba_sp_df.head()
bba_sp_df.shape

bba_sp_wrk = bba_sp_df['bba'].str.split(pat='·', expand=True)
bba_sp_wrk.columns = ['bed_t', 'bath_t', 'prop_type_t']
bba_sp_wrk = bba_sp_wrk.apply(lambda x: x.str.strip())
bba_sp_wrk = bba_sp_wrk.fillna('')
bba_sp_wrk.head()

# Bed
bba_sp_wrk.loc[bba_sp_wrk['bed_t'].str.contains('Bed'), ['bed']] = bba_sp_wrk['bed_t']

# Bath
bba_sp_wrk.loc[bba_sp_wrk['bed_t'].str.contains('Bath'), ['bath']] = bba_sp_wrk['bed_t']
bba_sp_wrk.loc[bba_sp_wrk['bath_t'].str.contains('Bath'), ['bath']] = bba_sp_wrk['bath_t']

# Property Type
bba_sp_wrk.loc[bba_sp_wrk['bed_t'].isin(prop_lst), ['prop_type']] = bba_sp_wrk['bed_t']
bba_sp_wrk.loc[bba_sp_wrk['bath_t'].isin(prop_lst), ['prop_type']] = bba_sp_wrk['bath_t']
bba_sp_wrk.loc[bba_sp_wrk['prop_type_t'].isin(prop_lst), ['prop_type']] = bba_sp_wrk['prop_type_t']

# Area
bba_sp_wrk['area'] = ''

# Concatenate the bba_sp_wrk with the join_value
bba_sp_df_final = pd.concat([bba_sp_df['join_value'], bba_sp_wrk.drop(columns=['bed_t', 'bath_t', 'prop_type_t'])]
                            , axis=1)
bba_sp_df_final.fillna('', inplace=True)
bba_sp_df_final.head()



# Join each of the tables based on the 'join_value'
daft_df_2 = pd.merge(pd.merge(loc_sp_df, bba_sp_df_final, on=['join_value'], how='inner')
                     , pc_sp_df, on=['join_value'], how='inner')

# Remove any duplicates
daft_df_2.drop_duplicates(subset=['join_value', 'address', 'county', 'price', 'bed', 'bath', 'prop_type']
                          , inplace=True)

# Drop the 'join_value' field as it is no longer required
daft_df_2.drop(columns=['join_value'], axis=1, inplace=True)

# Concatenate the two tables to create your final daft table
daft_df = pd.concat([daft_df_1, daft_df_2], ignore_index=True)
daft_df.head()
daft_df.tail()

# Write out the file as a csv on your computer
pc_df.to_csv(r'Files\pc_df.csv', index=False, header=True)
