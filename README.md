# **Scrape-and-Analyse--Hacknite2024**
## **Team Humanoid**
## **Track**: Data Analytics
## **Contributors** : Sriram Srikanth (IMT2023115)

## **Problem Statement:**
Houses put up for sale on real estate websites have some aspects/data regarding them missing which makes selecting houses difficult.

## **Goal:**
To collect data regarding houses for sale on different real estate websites and then analyse the data to help us choose the optimal house to buy.

## **Features:**
My data analytics project collects data from real estate website, extracts and analyses all the necessary information with the help of graphs.Currently it collects data about houses in Bangalore. We have analysed the houses based on factors :
a> Based on information given on website : Cost of Purchase,Utilities available(Balcony,Bathroom,Parking Area)
b> Based on some external information : Distance of house location from prominent locations in Bangalore
                                        Quality of nature and environment in the location of the house
(*Quality of environment has been compared based on the number of parks in the locality. This is due to the lack of data on other factors such as number of trees,etc. Since greater number of parks would imply more trees in general scenarios.*)
I have also collected additional data(*builder links,more information on the house*) using live scraping with the help of selenium.
The real estate buildings for sale data has also been depicted as a dataframe(*table*) for people to go through incase they want further information.(*Live Scraping has been used to get the link field links in the dataframe*)
**Additional Function**: I have also designed a image scraper which gets us the image by web-scrapping a image website. This image scraper has multiple apllications and in my project it is just a functionality for the website user to play with in case they are ~~tired of~~  done with analysis(*Image Scraper is built as a side utility of this website.*)
All the images on the web page(*analysis plots and image scraper images*) can be downloaded using the download button on the website.

## **Tech Stack**
### **Python Libraries Used** :
1. **requests** : Used to retrieve the web data in html format
2. **bs4 (Beautiful Soup)** : Used to parse the html data obtained from the requests' get url call into lxml format text and helps navigate and extract data from the html data.
3. **selenium** :(*used for live scraping*) Used to simulate events like clicking on an element, etc. and then extracting data that can be accessing only through that event(ex: clicking on an element) 
4. **pandas** : Used to format and cleanse data. It helps create .csv file using pre-existing dataframe and extract data from a pre-existing .csv file to a dataframe.
5. **matplotlib**: Used to visualise and analyse the cleansed data using charts like bar-graph,pie-char,box-chart,etc.
6. **geopy** : Used to convert addresses,locations,landmarks into geographic co-ordinates and vice versa. It is also used to compute the distance between two geographic coordinates.
* Nominatim : To get geographic coordinates
* geodesic : To compute distance between geographic coordinates
7. **streamlit**: Used to create and deploy web apps which display analysed data.
8. **graphviz**: Used to create pictorial depictions of information to display on the website.
9. **PIL (Image)** : Used for image extraction and download.

## **How does this project work ?**
1. This project initially contains 3 python files, 1 csv file(*BBMP Parks data csv file*), chromedriver files(*for selenium*).
2.  **'scraping_data.py'** file scrapes data from the websites, stores them in a pandas dataframe and then creates a 'data.csv' file from that dataframe.
3. **'analyse_data.py'** file converts 'data.csv' file into a dataframe, cleanses and collects necessary data from it and stores the cleansed data in 'data1.csv' file. It then uses this cleansed data to plot charts with the help of matlplotlib.These charts are downloaded as .png files and stored in the same directory.
4. The .png files and 'data1.csv' file is used by the **'website_builder.py'** file to create the website.
**NOTE :** The 3 python files must be run in the same order in which they have been explained. This process needs to done only once and then later everything can be viewed on the webpage. However this need not be done since all the contents created after these files are ran are already present in the github repository.

## **How to run ?**
1. Download the entire github repository
2. Open command prompt/terminal in the downloaded github repository folder
3. type - streamlit run website_builder.py
**Please go through the website and all its functionalities using the steps given above**


## **Applications**
It can help homebuyers choose the optimal house based on their requirements, from a large pool of houses put up for sale on real estate websites.

## **Further Improvements**
1. The project can be expanded to extract,arrange and analyse data regarding houses for sale from various cities not only Bangalore. It can also expanded to display more number of retrieved images.
2. Instead of using geopy we can use google maps API (*It is a paid service*) to make the distances more accurate.
3. If more accurate information regarding the vegetation(*number of trees,cleaning history,etc*) of localities are collected and stored properly , analysis regarding the environment can be done more accurately.

## **Demo**
**Youtube Video Link for demo video:** https://youtu.be/ASFgOzbj_u4
