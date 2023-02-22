import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import calendar
from heapq import nlargest
import openpyxl
from itertools import combinations
from collections import Counter


############## App Page width  ####################

st.set_page_config(page_title="Sales Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",)


################# Data loading and storing #############@
@st.cache(allow_output_mutation=True)

def load_data(file):
    data= pd.read_excel(file)
    return data

dataframe =load_data('sales.xlsx')

############## filter for the graph  ####################

st.markdown(f'<h1 style="color:#FF5349;font-size:50px;">{"Sales Dashboard"}</h1>', unsafe_allow_html=True)

my_expander = st.expander(label='Graph Filter')
with my_expander:
    ####### year filter
    years=dataframe['Year'].unique()
    selected_year= st.radio('Select Year', years, horizontal=True)
    df=dataframe.loc[(dataframe['Year'] ==selected_year)]
    c1, c2,c3 = st.columns((3,3,4))

    with c1:
        ####### month filter
        sorted_month=df["Month Name"].unique()
        selected_month = st.multiselect('Select Months',sorted_month,sorted_month)
        df = df[df['Month Name'].isin(selected_month)]
    with c2:
        ####### city filter
        sorted_city=df["City"].unique()
        selected_city = st.multiselect('Select City',sorted_city,sorted_city)
        if selected_city is not None:
            df = df[df['City'].isin(selected_city)]
        else:
            df=df
    with c3:
        ####### product filter
        sorted_product_unique=df['Product'].unique()
        selected_product = st.selectbox('Select Product', sorted_product_unique,index=0)



####### Graphs container ########

# Row A

c1, c2 = st.columns((6,4))
with c1:
    st.markdown(f'<h1 style="color:#FF5349;font-size:20px;">{"Most Sold Products"}</h1>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<h1 style="color:#FF5349;font-size:20px;">{"Month with Highest Sales"}</h1>', unsafe_allow_html=True)

st.markdown("""
<style>
div[data-testid="metric-container"] {
   background-color: rgba(28, 131, 225, 0.1);
   border: 1px solid rgba(28, 131, 225, 0.1);
   padding: 5% 5% 5% 10%;
   border-radius: 5px;
   color: rgb(30, 103, 119);
   overflow-wrap: break-word;
}

/* breakline for metric text         */
div[data-testid="metric-container"] > label[data-testid="stMetricLabel"] > div {
   overflow-wrap: break-word;
   white-space: break-spaces;
   color: red;
}
</style>
"""
, unsafe_allow_html=True)

#### product metric with most sold in sales

product_data=df.groupby("Product")[["Quantity Ordered","Sales"]].sum()
most_sold=nlargest(3, zip(product_data.index,product_data["Sales"]))

col1, col2, col3,col4,col5 = st.columns(5)

col1.metric(most_sold[0][0],"$ "+"%.1f" % most_sold[0][1],help="1st best product by sales")
col1.markdown("###### Quantity Ordered:")
col1.write(str(product_data.loc[(product_data.index ==most_sold[0][0])]["Quantity Ordered"][0]))

col2.metric(most_sold[1][0], "$ "+"%.1f" % most_sold[1][1],help="2nd best product by sales")
col2.markdown("###### Quantity Ordered:")
col2.write(str(product_data.loc[(product_data.index ==most_sold[1][0])]["Quantity Ordered"][0]))

col3.metric(most_sold[2][0], "$ "+"%.1f" % most_sold[2][1],help="3rd best product by sales")
col3.markdown("###### Quantity Ordered:")
col3.write(str(product_data.loc[(product_data.index ==most_sold[2][0])]["Quantity Ordered"][0]))

######## sales by month graph

sales_data=df.groupby(['Month Name']).agg({ "Month":"unique",'Sales' : 'sum'}).sort_values('Month')
high_sales_color=list(sales_data['Sales']).index(max(sales_data['Sales']))
colors = ['#ADD8E6',] * len(sales_data)
colors[high_sales_color] = "#01579b"

fig1 = go.Figure(data=[go.Bar(x=list(sales_data.index),y=list(sales_data["Sales"]),marker_color=colors,width=[0.8])])
fig1.update_layout(margin=dict(l=10, r=10, t=10, b=10),autosize=False,width=500,height=200)
col4.plotly_chart(fig1)

st.markdown("***")

# Row B

c1, c2= st.columns((5,5))

with c1:
    ########## sales by product
    st.markdown(f'<h1 style="color:#FF5349;font-size:20px;">{"Sales by Product"}</h1>', unsafe_allow_html=True)

    prod_sales=df.groupby(['Product']).agg({ "Quantity Ordered":"sum",'Sales' : 'sum'}).sort_values('Sales')

    fig2 = px.bar(prod_sales, x="Sales", y=prod_sales.index, orientation='h',hover_data=["Quantity Ordered"])
    fig2.update_layout(margin=dict(l=0, r=0, t=10, b=0),yaxis_title=None,autosize=False,width=500,height=300)
    st.plotly_chart(fig2)
with c2:
    ########## hours where orderes are high can be used for advertisment
    st.markdown(f'<h1 style="color:#FF5349;font-size:20px;">{"Hours to show Advertisement"}</h1>', unsafe_allow_html=True)

    hours_data=df.groupby(['Hour']).agg({ 'Order ID' : 'count'})

    fig3 = px.line(hours_data, x=hours_data.index, y='Order ID', markers=True,text=hours_data.index,labels={'Order ID':'Count of Orders'})
    fig3.update_traces(textposition='top center',textfont_size=14)
    fig3.update_layout(margin=dict(l=0, r=0, t=10, b=0),
                      xaxis = None,
                      yaxis_title='Count Of Orders',
                      xaxis_title=None,
                      autosize=False,width=500,height=300)
    st.plotly_chart(fig3)

st.markdown("***")

# Row C

c1, c2 = st.columns((4,6))

########## product bought together volume

prod_data=df[df['Order ID'].duplicated(keep=False)]
prod_data['Product Bundle']=prod_data.groupby('Order ID')['Product'].transform(lambda x: ','.join(x))
prod_data=prod_data[['Order ID','Product Bundle']].drop_duplicates()
prod_data = prod_data.loc[prod_data['Product Bundle'].str.contains(selected_product )]

if len(prod_data)!=0:
    count=Counter()
    for row in prod_data["Product Bundle"]:
      row_list=row.split(',')
      count.update(Counter(combinations(row_list,2)))
      new_counter = Counter(
        (t[1], t[0]) if t[0] != selected_product else t
        for t in count.elements()).most_common(10)


    prod=pd.DataFrame(index=[0])
    for i in new_counter:
      prod[i[0][1]]=i[1]
    prod=prod.transpose()

    with c1:
        st.markdown(f'<h1 style="color:#FF5349;font-size:20px;">{"Most-bought Product together with "+str(selected_product)}</h1>', unsafe_allow_html=True)
        fig4 = px.bar(prod, x=prod.index, y=0 ,labels={'index':'Most bought product','0':'Quantity Ordered count'})
        fig4.update_layout(
             autosize=False,
             width=500,)
        st.plotly_chart(fig4)

else:
    with c1:
        st.markdown(f'<h1 style="color:#FF5349;font-size:20px;">{"Most-bought Product together with "+str(selected_product)}</h1>', unsafe_allow_html=True)
        st.markdown('##### No Items bought together')


with c2:
    ########## correlation between products
    st.markdown(f'<h1 style="color:#FF5349;font-size:20px;">{"Correlation of " + str(selected_product)+" with volume of other products "}</h1>', unsafe_allow_html=True)

    corr_data=df.groupby(['Month','Product']).agg({ 'Sales' : 'sum'}).sort_values('Month')
    corr_data=corr_data.reset_index().pivot(index='Month',columns='Product',values='Sales')
    corr_data = corr_data.rename_axis(None, axis=1)
    corr_data=corr_data.reset_index(drop=True)
    corr_data=corr_data.corr().round(2)
    corr_data=corr_data.filter(items =[selected_product], axis=0)

    fig4 = px.imshow(corr_data, text_auto=True, aspect="auto")
    fig4.update_layout(autosize=False,width=700,margin=dict(l=0, r=0, t=10, b=0),)
    st.plotly_chart(fig4)


st.markdown("***")

# Row D
c1, c2 = st.columns((5,5))

with c1:
    ######### quantity ordered by sales and price
    st.markdown(f'<h1 style="color:#FF5349;font-size:20px;">{"Quantity Ordered with Sales and Price"}</h1>', unsafe_allow_html=True)

    price_quant=df.groupby(['Product']).agg({ 'Quantity Ordered' : 'sum','Price Each':'mean','Sales':'sum'})

    fig5 = px.scatter(price_quant, x="Quantity Ordered", y="Price Each",hover_name=price_quant.index,size="Sales", size_max=70,
                 labels={'Quantity Ordered':'Sum of Quantity Ordered','Price Each':'Average Price of the Product'})
    fig5.update_layout(autosize=False,width=500,margin=dict(l=0, r=0, t=10, b=0),)
    st.plotly_chart(fig5)
with c2:
    ######### correlation of quantity ordered and price
    st.markdown(f'<h1 style="color:#FF5349;font-size:20px;">{"Correlation between Price and Quantity Ordered"}</h1>', unsafe_allow_html=True)

    price_data=df.groupby('Product')[["Quantity Ordered","Price Each"]].sum()

    fig6 = make_subplots(specs=[[{"secondary_y": True}]])
    fig6.add_trace(go.Bar(x=price_data.index, y=price_data['Quantity Ordered'], name="Quantity"),secondary_y=False)
    fig6.add_trace(go.Scatter(x=price_data.index, y=price_data['Price Each'], name="Price"),secondary_y=True,)
    fig6.update_layout(showlegend=False,autosize=False,width=600,margin=dict(l=0, r=0, t=10, b=0),)
    fig6.update_yaxes(title_text="Quantity Ordered", secondary_y=False)
    fig6.update_yaxes(title_text="Price($)", secondary_y=True)
    st.plotly_chart(fig6)

st.markdown("***")



st.info('Coded by 👩🏻‍💻[Fatema ARSIWALA](https://www.linkedin.com/in/fatemaarsi/)')
st.markdown("""
<script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
""", unsafe_allow_html=True)
