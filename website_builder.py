import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
import os
from bs4 import BeautifulSoup
import graphviz
from PIL import Image

st.set_page_config(page_title="Analyse Real Estate!",layout = "wide",page_icon = '🔍')

#CREATING DATAFRAME FROM CSV
df1 = pd.read_csv('./data1.csv')
df = df1.rename(columns={df1.columns[0]: "Index"})
del df['Index']
locations = list(set(df['Location']))
st.header(f"**Analysis of houses for sale in different locations of Bangalore** 🏡 ")

#LOCATIONS CHOOSEN
st.subheader(f'**Locations Choosen** 📍🗺️')

def locations_tab(col_size):
    columns = st.columns(col_size)
    box = []
    for i in range(0,len(locations),col_size):
        box.append(locations[i:i+col_size])

    for i in range(len(box)):
        for j in range(len(box[i])):
            columns[j].button(box[i][j])
    
with st.spinner(text = "Loading section..."):
    locations_tab(4)

st.write("-------------------------------------------------------------------------")

#CHART DEPICTION
graph = graphviz.Digraph()
graph.edge('Parameters✅','Cost₹🤑')
graph.edge('Parameters✅','Location🌍')
graph.edge('Parameters✅','Facilities🚩')
graph.edge('Location🌍','Distance🛣️')
graph.edge('Location🌍','Environment🌳🛝')
graph.edge('Location🌍','Super Area Available🏞️🏙️')
graph.edge('Facilities🚩','Bathroom🛁')
graph.edge('Facilities🚩','Balcony🪟')
graph.edge('Facilities🚩','Parking Area🚗')

st.title(f'**_:blue[Parameters] used to analyse houses_ :book:**')
st.graphviz_chart(graph)

st.write("-------------------------------------------------------------------------")

#COST
st.subheader(f'_Cost_')
optioncost = st.selectbox('Which BHK house do you want analyse costs ?',['1 BHK','2 BHK','3 BHK'])
AorCoption = st.selectbox('Do you want to see the median or average total cost ?',['Average Cost','Median Cost'])
placeholder1 = st.empty()
if(optioncost=='1 BHK'):
    if(AorCoption=='Average Cost'):
        placeholder1.image('./AC1.png')
        img_cost_src = './AC1.png'
        img_cost = Image.open('./AC1.png')
    else:
        placeholder1.image('./MC1.png')
        img_cost_src = './MC1.png'
        img_cost = Image.open('./MC1.png')
elif(optioncost=='2 BHK'):
    if(AorCoption=='Average Cost'):
        placeholder1.image('./AC2.png')
        img_cost_src = './AC2.png'
        img_cost = Image.open('./AC2.png')
    else:
        placeholder1.image('./MC2.png')
        img_cost_src = './MC2.png'
        img_cost = Image.open('./MC2.png')
elif(optioncost=='3 BHK'):
    if(AorCoption=='Average Cost'):
        placeholder1.image('./AC3.png')
        img_cost_src = './AC3.png'
        img_cost = Image.open('./AC3.png')
    else:
        placeholder1.image('./MC3.png')
        img_cost_src = './MC3.png'
        img_cost = Image.open('./MC3.png')
image_bytesA = img_cost.tobytes()
downloadbtnA = st.download_button(label="Download",data=image_bytesA,file_name = img_cost_src.split('/')[-1],mime= 'image/png')
        
#LOCATION
st.subheader(f'_Location Based Factors_')
factor = st.selectbox('On the basis of which factor do you want to analyse ?',['Super Area Available','Environmental Quality of Locality','Distance from prominent locations in Bangalore'])
placeholder2 = st.empty()
if(factor=='Super Area Available'):
    placeholder2.image('./SuperArea.png')
    img_loc_src = './SuperArea.png'
    img_loc = Image.open('./SuperArea.png')
elif(factor=='Environmental Quality of Locality'):
    placeholder2.image('./parks.png')
    img_loc_src = './parks.png'
    img_loc = Image.open('./parks.png')
elif(factor=='Distance from prominent locations in Bangalore'):
    placeholder2.image('./Distances.png')
    img_loc_src = './Distances.png'
    img_loc = Image.open('./Distances.png')
image_bytesB = img_loc.tobytes()
downloadbtnB = st.download_button(label="Download",data=image_bytesB,file_name = img_loc_src.split('/')[-1],mime= 'image/png')

#FACILITIES
st.subheader(f'_Facilities_')
facility = st.selectbox('Which utility of the house do you want to analyse ?',['Balcony','Bathroom','ParkingSlots','Furnishing','BHK'])
loc1 = st.selectbox('Houses of which location do you want to analyse ?',locations)
placeholder3 = st.empty()
placeholder3.image(f'./{facility}_{loc1}.png')
img_fac_src = f'./{facility}_{loc1}.png'
img_fac = Image.open(f'./{facility}_{loc1}.png')
image_bytesC = img_fac.tobytes()
downloadbtnC = st.download_button(label="Download",data=image_bytesC,file_name = img_fac_src.split('/')[-1],mime= 'image/png')

st.write("-------------------------------------------------------------------------")

#ANALYSIS
st.header(f'**Analysis**')
st.write("People interested in 1BHK houses should look at houses in Electronic City due to their low cost,relatively nearer to prominent locations and decent environment.")
st.write("In case of 2BHK,3BHK we can look at houses in Yelhanka due to their relatively lower cost,cleaner environment,greater frequency of utilities. The only issue would be that it is relatively farther from prominent places in Bangalore.")
st.write("Alternatively, for 3BHK houses from Hebbal can be choosen due to their good environment,utilities. The major issue would be the high cost of buying houses in Hebbal")
st.write("Please note that the above analysis is only based on my assumptions,these decisions may depend on what factor does a person priortise.")

st.write("-------------------------------------------------------------------------")

#DISPLAY TABLE
st.header(f'**Want More Information**❓')
placeholder = st.empty()
if 'displayed_rows' not in st.session_state:
  st.session_state['displayed_rows'] = 4

displayed_rows = st.session_state['displayed_rows']
def update():
    placeholder.dataframe(df.iloc[:displayed_rows,:])
update()
showmore = st.button("Show More")
showall = st.button("Show entire table")
if(showmore):
    new_rows = min(displayed_rows+4,len(df))
    st.session_state['displayed_rows'] = new_rows
    update()
if(showall):
    placeholder.dataframe(df)
st.write("-------------------------------------------------------------------------")

#BONUS : IMAGE SCRAPER
st.header("BONUS FUNCTION🥳 : IMAGE RETREIVER🖼️")
st.subheader("Enter name of the object whose image you need")
with st.form("Search"):
    keyword = st.text_input("Enter object name")
    search = st.form_submit_button("Search")
placeholder = st.empty()
if(keyword):
    page = requests.get(f'https://unsplash.com/s/photos/{keyword}')
    soup = BeautifulSoup(page.text,'lxml')
    rows = soup.find_all("div",class_ = 'ripi6')
    column1,column2 = placeholder.columns(2)
    counter = 0
    for index,row in enumerate(rows):
      figures = row.find_all("figure",itemprop='image')
      for i,figure in enumerate(figures):
        divA = figure.div.a.div
        divB = divA.find("div",class_="MorZF")
        img_src = None
        if(divB!=None):
          img_src = divB.img['src']
        if(img_src!=None):
          if(counter%2==0):
            column1.image(img_src)
            btnkey1 = str(index)+str(i)
            downloadbtn1 = column1.button("Download",key = btnkey1)
            counter = counter + 1
            if(downloadbtn1):
                print("Download Button Clicked")
                response = requests.get(img_src)
                img_data = response.content
                file_name = f'{keyword}_image_{btnkey1}.jpg'
                with open(file_name,"wb") as f:
                    f.write(img_data)
          else:
            column2.image(img_src)
            btnkey2 = str(index) + str(i)
            downloadbtn2 = column2.button("Download",key = btnkey2)
            counter = counter + 1
            if(downloadbtn2):
                print("Download Button Clicked")
                response = requests.get(img_src)
                img_data = response.content
                file_name = f'{keyword}_image_{btnkey2}.jpg'
                with open(file_name,"wb") as f:
                    f.write(img_data)
            

#os.system("streamlit run website.py")
