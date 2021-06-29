
Python code used to extract property price information from Daft.ie (Ireland's largest property website)
===

Summary
---

Many Financial Institutions, Government Agencies and Real Estate companies are very interested in having up-to-date property price information.

* This code can be used to extract all price information from Daft.ie. The code can also be adapted to read in all text data from properties on the website.
* An excel containing property price information from Daft.ie has been included in this repository


Advantages of having up-to-date information for Financial Institutions:
---
* Bank's can assess if their property valuations are correct by comparing similar properties in the same location.
* If we run our web scraping code on Daft.ie every 3 days we can see if the price trend for similar properties are positive or negative.
* Using KNN we could look at the 3-5 nearest properties with the same features and construct a model for a fair price for our property, based on this we could flag 
  properties which may need to be re-valued
  
* Banks index the value of their properties to the CSO index but Daft.ie will give the bank more granular information on house price movement i.e. house price movement 
  for 3 bedroom properties in Dublin 6 over the course of the last 3 months
* By tracking the house price trend on certain types of properties the bank my be able to assess if it may be "overweight" (have a large amount of exposure) on ceratin properties
  which have a negative trend i.e. 25% of mortgages in the bank are on one bedroom apartments in Cork City which may have seen a 20% fall in price on
  Daft.ie over the last year
* Compare the bank's average property values with Daft.ie. If the average of all 4 bedroom houses in Wexford town is €350,000 but the bank has an average value on their mortgages
  of €500,000 they may need to re-assess the value of their properties.
* Periodically extracting data from Daft.ie would be extremely useful for predicting short term house price forecasts, location based forecasts, increase/decrease in sale activity 
  of certain property types or sizes and other important information which may help the bank's medium term plan (including the identification of optimal locations for new
  branches). 
