import numpy as np
import pandas as pd
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.ticker import MultipleLocator, FuncFormatter
from matplotlib.cm import get_cmap
import time

def calculate_distance(location1,location2):
    def distance_location(location1,location2):
        geolocator = Nominatim(user_agent="my_app")
        location1 = location1 + ", Bangalore, Karnataka"
        location2 = location2 + ", Bangalore, Karnataka"
        try:
            coordinates1 = geolocator.geocode(location1).raw
            coordinates2 = geolocator.geocode(location2).raw
        except:
            return 0

        if coordinates1 and coordinates2:
            lat1, lon1 = coordinates1['lat'], coordinates1['lon']
            lat2, lon2 = coordinates2['lat'], coordinates2['lon']
            distance_in_km = geodesic((lat1, lon1), (lat2, lon2)).km
            return distance_in_km
        else:
            return 0
    if(distance_location(location1,location2)==0):
        location1 = location1.split()[0]
        location2 = location2.split()[0]
        return distance_location(location1,location2)

    return distance_location(location1,location2)


#PARK DATA COLLECTION
parkdata = pd.read_csv("./BBMP-Detailed Park List.csv")
parkdata1 = parkdata['Zone Name'].dropna()
l1  = list(parkdata1.values)
parkdata2 = parkdata['Assembly'].dropna()
l2  = list(parkdata2.values)
parkdata3 = parkdata['Ward Name'].dropna()
l3  = list(parkdata3.values)
parkdata4 = parkdata['Park Name'].dropna()
l4  = list(parkdata4.values)

location_dict = {}
for i in l1+l2+l3+l4:
    location_dict[i] = location_dict.get(i,0) + 1


#PREPARING THE DATAFRAME BY CLEARING UNNECESSARY INFORMATION
df1 = pd.read_csv("./data.csv")
del df1['Index']

df1 = df1.drop(df1[df1['CostPerSqft'] == -1].index)
df1 = df1.reset_index(drop=True)

df = df1[['Location','Builder','Status','Transaction','BHK','TotalCost','CostPerSqft','Super Area (in sqft)','Bathroom','Balcony','Car Parking','Furnishing','Link','BuilderLink']]    
parameters = list(df.columns)
locations = list(set(df['Location']))
locations_spaced = []
for i in locations:
    locations_spaced.append(i.replace(' ','\n'))
df.to_csv("./data1.csv")

#COST
#1 BHK
total_costs1 = {}#all costs in each locality
for i in locations:
    total_costs1[i] = sorted(list(df[(df['Location']==i) & (df['BHK']==1)]['TotalCost']))

AC1 = []#average cost for each locality
aloc1 = [] #available locations
for i in locations:
    if(len(total_costs1[i])!=0):
        AC1.append(sum(total_costs1[i])/len(total_costs1[i]))
        aloc1.append(i.replace(' ','\n'))
    
MC1 = []#median cost for each locality
for i in locations:
    if(len(total_costs1[i])!=0):
        MC1.append(total_costs1[i][(len(total_costs1[i])-1)//2])
    

#2 BHK
total_costs2 = {}#all costs in each locality
for i in locations:
    total_costs2[i] = sorted(list(df[(df['Location']==i) & (df['BHK']==2)]['TotalCost']))

AC2 = []#average cost for each locality
aloc2 = []#available locations
for i in locations:
    if(len(total_costs2[i])!=0):
        AC2.append(sum(total_costs2[i])/len(total_costs2[i]))
        aloc2.append(i.replace(' ','\n'))
    
    
MC2 = []#median cost for each locality
for i in locations:
    if(len(total_costs2[i])!=0):
        MC2.append(total_costs2[i][(len(total_costs2[i])-1)//2])
   

#3 BHK
total_costs3 = {}#all costs in each locality
for i in locations:
    total_costs3[i] = sorted(list(df[(df['Location']==i) & (df['BHK']==3)]['TotalCost']))

AC3 = []#average cost for each locality
aloc3 = []#available locations
for i in locations:
    if(len(total_costs3[i])!=0):
        AC3.append(sum(total_costs3[i])/len(total_costs3[i]))
        aloc3.append(i.replace(' ','\n'))
    
    
MC3 = []#median cost for each locality

for i in locations:
    if(len(total_costs3[i])!=0):
        MC3.append(total_costs3[i][(len(total_costs3[i])-1)//2])


#PARK LOCATIONS COMPARING WITH GIVEN LOCATIONS AND COLLECTING 
parks = {}
for i in locations:
    parks[i] = 0

for i in locations:
    for j in location_dict.keys():
        if((i==j) or (i in j.split()) or (j in i.split())):
            parks[i] = parks.get(i,0) + location_dict[j]
            
for i in parks.keys():
    if(parks[i]==0):
        parks[i] = 1

#FACILITIES
bathroom = {}
for i in locations:
    info = list(df[df['Location']==i]['Bathroom'])
    data = [0,0,0,0]
    for j in range(1,4):
        data[j] = info.count(j)
    bathroom[i] = data

balcony = {}
for i in locations:
    info = list(df[df['Location']==i]['Balcony'])
    data = [0,0,0,0]
    for j in range(0,4):
        data[j] = info.count(j)
    balcony[i] = data

carparking = {}
for i in locations:
    info = list(df[df['Location']==i]['Car Parking'])
    data = [0,0,0]
    for j in range(0,3):
        data[j] = info.count(j)
    carparking[i] = data

BHK =  {}
for i in locations:
    info = list(df[df['Location']==i]['BHK'])
    data = [0,0,0,0]
    for j in range(1,4):
        data[j] = info.count(j)
    BHK[i] = data

s_area = []
for i in locations:
    s_area.append(list(df[df['Location']==i]['Super Area (in sqft)']))


furnishing = {}
for i in locations:
    data = list(df[df['Location']==i]['Furnishing'])
    info = [0,0,0]#{unfurnished,semi-furnished,furnished'}
    for j in data:
        if(j=='Unfurnished'):
            info[0] = info[0] + 1
        elif(j=='Semi-Furnished'):
            info[1] = info[1] + 1
        elif(j=='Furnished'):
            info[2] = info[2] + 1
    furnishing[i] = info

#PLOTTING
'''Average Cost for locations'''

#1BHK
plt.figure(figsize=(12, 6))
bar_width = 0.2
bar_positions = [i + bar_width / 2 for i in range(len(aloc1))]
plt.bar(bar_positions,AC1, color='purple', width=bar_width, label="1 BHK (₹)")
plt.xlabel("Locations")
plt.ylabel("Cost(₹) in crores")
plt.title("Average Total Cost of buying 1 BHK Houses in Bangalore")
plt.xticks(bar_positions, aloc1, rotation=15, ha='center',fontsize=5)
plt.legend()
plt.savefig('AC1.png')


#2BHK
plt.figure(figsize=(12, 6))
bar_width = 0.2
bar_positions = [i + bar_width / 2 for i in range(len(aloc2))]
plt.bar(bar_positions,AC2, color='orange', width=bar_width, label="2 BHK (₹)")
plt.xlabel("Locations")
plt.ylabel("Cost(₹) in crores")
plt.title("Average Total Cost of buying 2 BHK Houses in Bangalore")
plt.xticks(bar_positions, aloc2, rotation=15, ha='center',fontsize=5)
plt.legend()
plt.savefig('AC2.png')


#3BHK
plt.figure(figsize=(12, 6))
bar_width = 0.2
bar_positions = [i + bar_width / 2 for i in range(len(aloc3))]
plt.bar(bar_positions,AC3, color='blue', width=bar_width, label="3 BHK (₹)")
plt.xlabel("Locations")
plt.ylabel("Cost(₹) in crores")
plt.title("Average Total Cost of buying 3 BHK Houses in Bangalore")
plt.xticks(bar_positions, aloc3, rotation=15, ha='center',fontsize=5)
plt.legend()
plt.savefig('AC3.png')


'''Median Cost for Locations'''

#1BHK
plt.figure(figsize=(12, 6))
bar_width = 0.2
bar_positions = [i + bar_width / 2 for i in range(len(aloc1))]
plt.bar(bar_positions,MC1, color='magenta', width=bar_width, label="1 BHK (₹)")
plt.xlabel("Locations")
plt.ylabel("Cost(₹) in crores")
plt.title("Median Total Cost of buying 1 BHK Houses in Bangalore")
plt.xticks(bar_positions, aloc1, rotation=15, ha='center',fontsize=5)
plt.legend()
plt.savefig('MC1.png')


#2BHK
plt.figure(figsize=(12, 6))
bar_width = 0.2
bar_positions = [i + bar_width / 2 for i in range(len(aloc2))]
plt.bar(bar_positions,MC2, color='green', width=bar_width, label="2 BHK (₹)")
plt.xlabel("Locations")
plt.ylabel("Cost(₹) in crores")
plt.title("Median Total Cost of buying 2 BHK Houses in Bangalore")
plt.xticks(bar_positions, aloc2, rotation=15, ha='center',fontsize=5)
plt.legend()
plt.savefig('MC2.png')

#3BHK
plt.figure(figsize=(12, 6))
bar_width = 0.2
bar_positions = [i + bar_width / 2 for i in range(len(aloc3))]
plt.bar(bar_positions,MC3, color='cyan', width=bar_width, label="3 BHK (₹)")
plt.xlabel("Locations")
plt.ylabel("Cost(₹) in crores")
plt.title("Median Total Cost of buying 3 BHK Houses in Bangalore")
plt.xticks(bar_positions, aloc3, rotation=15, ha='center',fontsize=5)
plt.legend()
plt.savefig('MC3.png')
plt.clf()

def custom_autopct(pct):
  if pct == 0:
    return ""  # Return empty string for 0% slices
  else:
    return f"{pct:.1f}%"


#PIE CHART FOR FACILITIES
'''BHK'''
for i in locations:
    percentages = [0,0,0]
    for j in range(1,4):
        percentages[j-1] = (BHK[i][j]/sum(BHK[i]))*100
    plt.pie(BHK[i][1:],colors = ['red','gold','yellow'],autopct = custom_autopct)
    plt.title(f'Frquency Distribution of 1BHK,2BHK,3BHK houses in {i}')
    plt.legend(['1 BHK','2 BHK','3 BHK'], loc="best")
    plt.tight_layout()
    plt.savefig(f'BHK_{i}.png')
    plt.clf()

'''Bathroom'''
for i in locations:
    percentages = [0,0,0]
    for j in range(1,4):
        percentages[j-1] = (bathroom[i][j]/sum(bathroom[i]))*100
    plt.pie(bathroom[i][1:],colors = ['red','gold','yellow'],autopct = custom_autopct)
    plt.title(f'Number of bathrooms in houses in {i}')
    plt.legend(['1 Bathroom','2 Bathroom','3 Bathroom'], loc="best")
    plt.tight_layout()
    plt.savefig(f'Bathroom_{i}.png')
    plt.clf()

'''Balcony'''
for i in locations:
    percentages = [0,0,0,0]
    for j in range(0,4):
        percentages[j] = (balcony[i][j]/sum(balcony[i]))*100
    plt.pie(balcony[i],colors = ['red','gold','yellow','blue'],autopct = custom_autopct)
    plt.title(f'Number of balconies in houses in {i}')
    plt.legend(['No Balcony','1 Balcony','2 Balcony','3 Balcony'], loc="best")
    plt.tight_layout()
    plt.savefig(f'Balcony_{i}.png')
    plt.clf()

'''Car Parking'''
for i in locations:
    percentages = [0,0,0]
    for j in range(0,3):
        percentages[j] = (carparking[i][j]/sum(carparking[i]))*100
    plt.pie(carparking[i],colors = ['red','gold','yellow'],autopct = custom_autopct)
    plt.title(f'Number of parking slots in houses in {i}')
    plt.legend(['No Parking Slot','1 Parking Slot','2 Parking Slots'], loc="best")
    plt.tight_layout()
    plt.savefig(f'ParkingSlots_{i}.png')
    plt.clf()

'''Furnishing'''
for i in locations:
    percentages = [0,0,0]
    for j in range(0,3):
        percentages[j] = (furnishing[i][j]/sum(furnishing[i]))*100
    plt.pie(furnishing[i],colors = ['red','gold','yellow'],autopct = custom_autopct)
    plt.title(f'Furnishing status in houses in {i}')
    plt.legend(['Unfurnished','Semi-Furnished','Furnished'], loc="best")
    plt.tight_layout()
    plt.savefig(f'Furnishing_{i}.png')
    plt.clf()


'''Super Area'''
plt.figure(figsize=(12, 6))
box = plt.boxplot(s_area,vert=1,patch_artist=True,notch=True,labels=locations)
bar_width = 0.35
bar_positions = [i + bar_width for i in range(len(locations))]
colors = ["pink","violet","indigo","blue","cyan","green","lightgreen","yellow","orange","red"]
for patch,index in zip(box['boxes'],list(range(len(locations)))):
    patch.set_facecolor(colors[index%len(colors)])
plt.xticks(bar_positions,locations_spaced,rotation=60,ha="center",fontsize=5)
plt.xlabel("Locations")
plt.ylabel("Super Area(in ft)")
plt.grid(True)
plt.title("Super Area(in ft) of houses in Locations")
plt.savefig('SuperArea.png')
plt.clf()

'''Environment Analysis based on the number of parks in the locality'''#NOT EXHAUSTIVE DATA
park_data = []
for i in locations:
    park_data.append(parks[i])

plt.figure(figsize=(25, 6))
bar_width = 0.2
bar_positions = [i + bar_width / 2 for i in range(len(locations))]
plt.bar(bar_positions,park_data, color='lightgreen', width=bar_width, label="Parks")
plt.xlabel("Locations")
plt.ylabel("Number of parks")
plt.title("Analysing Environment of location based on number of parks")
plt.xticks(bar_positions,locations_spaced, rotation=15, ha='center',fontsize=6)
plt.legend()
plt.savefig('parks.png')
plt.clf()

#DISTANCE FROM CENTRAL LOCATIONS IN BANGALORE
Mdistances = []
for i in locations:
    Md = calculate_distance(i,"Majestic")
    if(i!='Majestic' and Md==0):
        Mdistances.append(16)
    else:
        Mdistances.append(Md)
        
Edistances = []
for i in locations:
    Me = calculate_distance(i,"Electronic City")
    if(i!="Electronic City" and Me==0):
        Edistances.append(10)
    else:
        Edistances.append(Me)

plt.figure(figsize=(12, 6))
bar_width = 0.35
index = range(len(locations))
plt.bar(index,Mdistances, bar_width, label="Distance from Majestic, Bangalore", color='indigo')
plt.bar([p + bar_width for p in index],Edistances, bar_width, label="Distance from Electronic City, Bangalore", color='orange')
plt.xlabel("Locations")
plt.ylabel("Distances")
plt.title("Distances of the locations from important locations in Bangalore")
plt.legend()
plt.xticks([i + bar_width / 2 for i in index],locations_spaced,rotation=15,ha="center",fontsize=4)
plt.tight_layout()
plt.subplots_adjust(bottom=0.2)
plt.savefig("Distances.png")
plt.clf()


