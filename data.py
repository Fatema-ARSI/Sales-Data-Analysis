import pandas as pd
import calendar

######## get all the excel file from githuv sorted_product_unique

def read_multi_csv(months):
    dfs = []
    for m in months:
        file = 'https://raw.githubusercontent.com/Fatema-ARSI/Sales-Data-Analysis/main/Data/Sales_'+str(m)+'_2019.csv'
        #print (file)
        df = pd.read_csv(file)
        dfs.append(df)
    return dfs

months=list(calendar.month_name)[1:13]
frames=read_multi_csv(months)
sales_data = pd.concat(frames)

############ Data cleaning and Manipulation

df["Order Date"] = pd.to_datetime(df["Order Date"], errors='coerce') ### order dat to date format
##### slice the Year,Month and Hour from the order Date

df['Month']=df["Order Date"].dt.month
df["Year"]=df["Order Date"].dt.year
df["Hour"]=df["Order Date"].dt.hour
df=df.dropna() ##### dropping null values
df['Month']=df['Month'].astype(int) ##### int format foe the column
df["Year"]=df["Year"].astype(int) ##### int format foe the column
df["Hour"]=df["Hour"].astype(int) ##### int format foe the column

########## add the Month name for the filer in Dashboard

months = {}
for i in df['Month'].unique():
  months[i]=calendar.month_name[i]

df['Month Name'] = df['Month'].map(months)

df['Quantity Ordered']=df['Quantity Ordered'].astype(int) #### int format foe the column
df['Price Each']=df['Price Each'].astype(float) ##### float format foe the column

df['Sales']=df['Quantity Ordered']*df['Price Each'].round(decimals=2) ###### Create sales column
df['City']=(df['Purchase Address'].str.split(',').str[1]).str.split('.').str[0] ###### Create city from slicing purchase address
df.info()

df.to_excel("sales.xlsx",index=False)   ###### download the excel
