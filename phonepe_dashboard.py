import mysql.connector
import pandas as pd
import os
import plotly.express as px
import streamlit as st
import json
import pymysql
import mysql.connector
import pandas as pd
import psycopg2
import matplotlib.pyplot as plt
import plotly.express as px
import requests
import json
#from streamlit_plotly_events import plotly_events 




    #Connecting to SQL
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="")


print(mydb)
mycursor = mydb.cursor(buffered=True)


mycursor.execute('''select *from phonepe.AGGREGATED_TRANSACTION''')
mydb.commit()
table1=mycursor.fetchall()
Agreee_trans=pd.DataFrame(table1,columns=("State","Year","Quater","Transaction_type","Transaction_count","Transaction_amount"))

mycursor.execute('''select *from phonepe.AGGREGATED_USER''')
mydb.commit()
table2=mycursor.fetchall()
Agreee_user=pd.DataFrame(table2,columns=("State","Year","Quater","Brand","Count","Percentage"))

mycursor.execute('''select *from phonepe.MAP_TRANSACTION''')
mydb.commit()
table3=mycursor.fetchall()
map_trans=pd.DataFrame(table3,columns=("State","Year","Quater","District","Count","Amount"))

mycursor.execute('''select *from phonepe.MAP_USER''')
mydb.commit()
table4=mycursor.fetchall()
map_user=pd.DataFrame(table4,columns=("State","Year","Quater","District","Registerd_users","Appopens"))

mycursor.execute('''select *from phonepe.TOP_TRANSACTION''')
mydb.commit()
table5=mycursor.fetchall()
top_trans=pd.DataFrame(table5,columns=("State","Year","Quater","District_Pincode","Count","Amount"))


mycursor.execute('''select *from phonepe.TOP_USER''')
mydb.commit()
table6=mycursor.fetchall()
top_user=pd.DataFrame(table6,columns=("State","Year","Quater","District_Pincode","Registered_user"))





# Assuming you have already fetched the data from your database as shown in your code


# Assuming you have already fetched the data from your database as shown in your code



# Dropdowns for selecting Transactions/Users, year and quarter
# Comfiguring Streamlit GUI 
st.set_page_config(layout='wide')

# Title
st.header(':violet[Phonepe Pulse Data Visualization ]',divider='rainbow')
st.text("")
st.text("")


# Selection option
option = st.radio('**Select your option**',('Data Visualization', 'Geo-Visualization','Insight Query Analysis'),horizontal=True)

# ===================================================       /      All India      /     ===================================================== #

if option == 'Data Visualization':
    col1, col2,col3 = st.columns(3)
    with col1:
        year_option  = st.selectbox('**Select Year**', (Agreee_trans['Year'].unique()),index=None,placeholder="Choose the following year...")
    with col2:
        selected_quater = st.selectbox('**Select Quater**', ('1','2','3','4'),index=None,placeholder="Choose the following quater...",key='selected_quater')
    with col3:
        selected_state = st.selectbox('**Select State**', (Agreee_trans['State'].unique()),index=None,placeholder="Choose the following State...")
            
    # Select tab
    tab1, tab2 = st.tabs(['Transaction','User'])
    
    # -------------------------       /     All India Transaction        /        ------------------ #
    
    
    with tab1:

        option = st.selectbox("choose the type of Transaction",("Aggregated Transaction", "Map Transaction", "Top Transaction"),index=None,placeholder="Select type of transaction...")
        if option == "Aggregated Transaction":
        
            in_tr_tr_typ = st.selectbox('**Select Transaction type**', ('Recharge & bill payments','Peer-to-peer payments','Merchant payments','Financial Services','Others'),key='in_tr_tr_typ')
    

        
            sql_query = f"SELECT State, Transaction_amount, Transaction_type FROM phonepe.AGGREGATED_TRANSACTION WHERE Year = '{year_option}' AND Quater = '{selected_quater}' AND Transaction_type = '{in_tr_tr_typ }'"

            mycursor.execute(sql_query)
            val = mycursor.fetchall()
            df_in_tr_tab = pd.DataFrame(val, columns=['State', 'Transaction_amount','Transaction_type'])
            df_in_tr_tab_qry_rslt1 = df_in_tr_tab.set_index(pd.Index(range(1, len(df_in_tr_tab)+1)))

            fig_amount1 = px.bar(df_in_tr_tab_qry_rslt1 , x="State", y="Transaction_amount", color="Transaction_type",
                    title=f"Quarterly Transaction Amounts by State in {year_option}, Quarter {selected_quater}",
                    labels={'Transaction Amount': 'Transaction Amount', 'State': 'State'},
                    color_discrete_sequence=px.colors.qualitative.Prism)
            st.plotly_chart(fig_amount1)

            sql_query = f"SELECT state, Transaction_count, Transaction_amount, Transaction_type FROM phonepe.AGGREGATED_TRANSACTION WHERE Year = '{year_option}' AND Quater = '{selected_quater}' AND State = '{selected_state}'"

            mycursor.execute(sql_query)
            val = mycursor.fetchall()
            df_in_tr_agg_rslt = pd.DataFrame(val, columns=['State', 'Transaction_count', 'Transaction_amount', 'Transaction_type'])

            fig_amount = px.bar(df_in_tr_agg_rslt, x="State", y="Transaction_count", color="Transaction_type",
                                title=f"Quarterly Transaction Counts by State in {year_option}, Quarter {selected_quater}",
                                color_discrete_sequence=px.colors.qualitative.Prism)

            st.plotly_chart(fig_amount)                      


        if option == "Map Transaction":
            

# Assuming you have data related to transactions
            sql_query = f"SELECT  DISTINCT State, SUM(Transaction_amount) as Transaction_amount, SUM(Transaction_count) as Transaction_count FROM phonepe.MAP_TRANSACTION WHERE Year = '{year_option}' AND Quater = '{selected_quater}'  GROUP BY State"

            mycursor.execute(sql_query)
            val = mycursor.fetchall()
            df_tr = pd.DataFrame(val, columns=['State', 'Transaction_amount', 'Transaction_count'])

            fig_map_user_plot_1 = px.line(df_tr, x="State", y=["Transaction_amount"], markers=True,
                              title=f"Transaction Amount by State - {year_option}, Quarter {selected_quater}",
                              width=1000, height=800, color_discrete_sequence=px.colors.sequential.Rainbow_r)
            
           
            sql_query = f"SELECT DISTINCT State, SUM(Transaction_amount) as Transaction_amount, SUM(Transaction_count) as Transaction_count FROM phonepe.MAP_TRANSACTION WHERE Year = {year_option} AND Quater = {selected_quater} GROUP BY State"

            mycursor.execute(sql_query)
            val = mycursor.fetchall()
            df_in_tr_tab_qry_rslt = pd.DataFrame(val, columns=['State', 'Transaction_amount', 'Transaction_count'])

            fig_map_user_plot_2 = px.line(df_in_tr_tab_qry_rslt, x="State", y=["Transaction_count"], markers=True,
                    title=f"{year_option}, {selected_quater} QUATER",
            width=1000, height=800, color_discrete_sequence=px.colors.sequential.Rainbow_r)

            st.plotly_chart(fig_map_user_plot_1)
        
            st.plotly_chart(fig_map_user_plot_2)

        if option == "Top Transaction":
           
            
            sql_query = f"SELECT  DISTINCT State, SUM(Amount) as Transaction_amount, SUM(Count) as Transaction_count FROM phonepe.TOP_TRANSACTION WHERE Year = '{year_option}' AND Quater = '{selected_quater}'  GROUP BY State"

            mycursor.execute(sql_query)
            val = mycursor.fetchall()
            df_in_tr_tab_qry_rslt = pd.DataFrame(val, columns=['State', 'Transaction_amount', 'Transaction_count'])

            fig_map_user_plot_1 = px.line(df_in_tr_tab_qry_rslt, x="State", y=["Transaction_amount"], markers=True,
                              title=f"Transaction Amount by State - {year_option}, Quarter {selected_quater}",
                              width=1000, height=800, color_discrete_sequence=px.colors.sequential.Rainbow_r)
            st.plotly_chart(fig_map_user_plot_1)

            sql_query = f"SELECT  DISTINCT State, SUM(Amount) as Transaction_amount, SUM(Count) as Transaction_count FROM phonepe.TOP_TRANSACTION WHERE Year = '{year_option}' AND Quater = '{selected_quater}'  GROUP BY State"

            mycursor.execute(sql_query)
            val = mycursor.fetchall()
            df_in_tr_tab_qry_rslt = pd.DataFrame(val, columns=['State', 'Transaction_amount', 'Transaction_count'])

            fig_map_user_plot_2 = px.line(df_in_tr_tab_qry_rslt, x="State", y=["Transaction_count"], markers=True,
                              title=f"Transaction Count by State - {year_option}, Quarter {selected_quater}",
                              width=1000, height=800, color_discrete_sequence=px.colors.sequential.Rainbow_r)
            st.plotly_chart(fig_map_user_plot_2)
            


    with tab2:

        option = st.selectbox("choose the type of User",("Aggregated User", "Map User", "Top User"),index=None,placeholder="Select type of user...")
        if option == "Aggregated User":
           
            

            query = f"SELECT Brand, SUM(Count) AS Total_Count FROM phonepe.AGGREGATED_USER WHERE Year = '{year_option}' AND Quater = '{selected_quater}' GROUP BY Brand"
            mycursor.execute(query)
            results = mycursor.fetchall()

# Create DataFrame
            df = pd.DataFrame(results, columns=['Brand', 'Total_Count'])

# Plotly pie chart
            fig = px.pie(df, values='Total_Count', names='Brand', 
                    title=f"Transaction Counts by Brand in {year_option}, Quarter {selected_quater}")

# Show the chart 
            
            st.plotly_chart(fig)


            query = f"SELECT State,Brand , SUM(Count) AS Total_Count FROM phonepe.AGGREGATED_USER WHERE State = '{selected_state}' AND Year = '{year_option}' AND Quater = '{selected_quater}' GROUP BY Brand,State"
            mycursor.execute(query)
            results = mycursor.fetchall()

# Create DataFrame for the bar chart
            df = pd.DataFrame(results, columns=['State', 'Brand' ,'Total_Count'])

# Plotly bar chart

            fig1 = px.bar(df, x="State", y="Total_Count", color="Brand",
                    title=f"Total Transaction Counts by State in {year_option}, Quarter {selected_quater}",
                    color_discrete_sequence=px.colors.qualitative.Prism)
# Show the bar chart
            st.plotly_chart(fig1)

        if option == "Map User":
            
            sql_query = f"SELECT  distinct State, SUM(Registered_Users) as Registered_Users, SUM(App_opens) as App_opens FROM phonepe.MAP_USER WHERE Year = {year_option} AND Quater = {selected_quater} GROUP BY State"

            mycursor.execute(sql_query)
            val = mycursor.fetchall()
            df_in_tr_tab_qry_rslt = pd.DataFrame(val, columns=['State', 'Registered_Users', 'App_opens'])

            fig = px.area(df_in_tr_tab_qry_rslt, x="State", y="Registered_Users",
            color="App_opens",
            hover_data=['Registered_Users'],title=f"Transaction Counts by Brand in {year_option}, Quarter {selected_quater}")
            st.plotly_chart(fig)


            sql_query = f"SELECT  State, District, SUM(Registered_Users) AS Registered_Users FROM phonepe.MAP_USER  WHERE Year = {year_option} AND Quater = {selected_quater} AND State = '{selected_state}' GROUP BY  District"

            mycursor.execute(sql_query)
            val = mycursor.fetchall()
            df_in_tr_map = pd.DataFrame(val, columns=['State', 'District','Registered_Users'])

            fig_map= px.area(df_in_tr_map, x="District", y="Registered_Users",
            color="Registered_Users",
            title=f"Registered Users in Districts of {selected_state}",
            hover_data=['Registered_Users'])
            st.plotly_chart(fig_map)
            

        if option == "Top User":
            

            sql_query = f"SELECT  distinct State, SUM(Registered_Users) as Registered_Users FROM phonepe.TOP_USER WHERE Year = {year_option} AND Quater = {selected_quater} GROUP BY State"

            mycursor.execute(sql_query)
            val = mycursor.fetchall()
            df_in_tr_tab_qry_rslt = pd.DataFrame(val, columns=['State', 'Registered_Users'])
            fig_amount = px.bar(df_in_tr_tab_qry_rslt , x="State", y="Registered_Users", color="Registered_Users",
                    title=f"Quarterly Registered Users by State in {year_option}",
                    color_discrete_sequence=px.colors.qualitative.Prism)
            st.plotly_chart(fig_amount)

            sql_query = f"SELECT   State, SUM(Registered_Users) as Registered_Users FROM phonepe.TOP_USER WHERE Year = {year_option}  GROUP BY State"

            mycursor.execute(sql_query)
            val = mycursor.fetchall()
            df_in_tr_tab_qry_rslt = pd.DataFrame(val, columns=['State','Registered_Users'])
            fig_amount1 = px.bar(df_in_tr_tab_qry_rslt , x="State", y="Registered_Users", color="Registered_Users",
                    title=f"Yearly Registered Users by State  in {year_option}",
                    color_discrete_sequence=px.colors.qualitative.Prism)
            st.plotly_chart(fig_amount1)

if option == 'Geo-Visualization':

    col1, col2= st.columns(2)
    with col1:
        year_option  = st.selectbox('**Select Year**', (Agreee_trans['Year'].unique()),index=None,placeholder="Choose the following year...")
    with col2:
        selected_quater = st.selectbox('**Select Quater**', ('1','2','3','4'),index=None,placeholder="Choose the following quater...",key='selected_quater')
    

    tap1, tap2 = st.tabs(['Transaction','User'])

    # Clone the GeoJSON data
    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response = requests.get(url)
    data2 = json.loads(response.content)

    # Extract state names and sort them in alphabetical order
    state_names_use = [feature['properties']['ST_NM'] for feature in data2['features']]
    state_names_use.sort()

# Create a DataFrame with all state names
    df_state_names_use = pd.DataFrame({'State': state_names_use})

    with tap1:

        opt = st.selectbox("choose the type of Transaction",("Aggregated Transaction", "Map Transaction", "Top Transaction"),index=None,placeholder="Select type of transaction...")
        if opt == "Aggregated Transaction":

            sql_query = f"SELECT  DISTINCT State, SUM(Transaction_amount) as Transaction_amount, SUM(Transaction_count) as Transaction_count FROM phonepe.MAP_TRANSACTION WHERE Year = '{year_option}' AND Quater = '{selected_quater}'  GROUP BY State"

            mycursor.execute(sql_query)
            val = mycursor.fetchall()
            df_tr = pd.DataFrame(val, columns=['State', 'Transaction_amount', 'Transaction_count'])

            # Group by state and aggregate transaction data
            df_agg = df_tr.groupby('State').agg({
            'Transaction_count': 'sum',
            'Transaction_amount': 'mean',
            }).reset_index()

# Merge state names with transaction data
            df_use = pd.merge(df_state_names_use, df_agg, on='State', how='left')

# Save merged DataFrame to CSV
            df_use.to_csv('State_user.csv', index=False)

# Read CSV
            df_aggtrans = pd.read_csv('State_user.csv')

# Plot choropleth map
            fig_agg = px.choropleth(df_aggtrans,
                    geojson=data2,
                    featureidkey='properties.ST_NM',
                    locations="State",
                    color='Transaction_count',  # Set this to the column you want to visualize
                    color_continuous_scale='Viridis',
                    title='Choropleth Map of  Total Transaction by State',
                    hover_data=['State', 'Transaction_amount', 'Transaction_count'])

            st.plotly_chart(fig_agg.update_geos(fitbounds="locations", visible=False))

        if opt == "Map Transaction":
            sql_query = f"SELECT  DISTINCT State, SUM(Transaction_amount) as Transaction_amount, SUM(Transaction_count) as Transaction_count FROM phonepe.MAP_TRANSACTION WHERE Year = '{year_option}' AND Quater = '{selected_quater}'  GROUP BY State"

            mycursor.execute(sql_query)
            val = mycursor.fetchall()
            df_maptr = pd.DataFrame(val, columns=['State', 'Transaction_amount', 'Transaction_count'])

            df_agg = df_maptr.groupby('State').agg({
            'Transaction_count': 'sum',
            'Transaction_amount': 'mean',
            }).reset_index()

# Merge state names with transaction data
            df_use = pd.merge(df_state_names_use, df_agg, on='State', how='left')

# Save merged DataFrame to CSV
            df_use.to_csv('State_user.csv', index=False)

# Read CSV
            map_tr = pd.read_csv('State_user.csv')

# Plot choropleth map
            fig_maptr = px.choropleth(map_tr,
                    geojson=data2,
                    featureidkey='properties.ST_NM',
                    locations="State",
                    color='Transaction_count',  # Set this to the column you want to visualize
                    color_continuous_scale='speed',
                    title='Choropleth Map of  Total Transaction by State',
                    hover_data=['State', 'Transaction_amount', 'Transaction_count'])

            st.plotly_chart(fig_maptr.update_geos(fitbounds="locations", visible=False))

        if opt == "Top Transaction":
            sql_query = f"SELECT  DISTINCT State, SUM(Amount) as Transaction_amount, SUM(Count) as Transaction_count FROM phonepe.TOP_TRANSACTION WHERE Year = '{year_option}' AND Quater = '{selected_quater}'  GROUP BY State"

            mycursor.execute(sql_query)
            val = mycursor.fetchall()
            df_in_top = pd.DataFrame(val, columns=['State', 'Transaction_amount', 'Transaction_count'])
            
            # Group by state and aggregate transaction data
            df_agg = df_in_top.groupby('State').agg({
            'Transaction_count': 'sum',
            'Transaction_amount': 'mean',
            }).reset_index()

# Merge state names with transaction data
            df_use = pd.merge(df_state_names_use, df_agg, on='State', how='left')

# Save merged DataFrame to CSV
            df_use.to_csv('State_user.csv', index=False)

# Read CSV
            toptr = pd.read_csv('State_user.csv')

# Plot choropleth map
            fig_toptr = px.choropleth(toptr,
                    geojson=data2,
                    featureidkey='properties.ST_NM',
                    locations="State",
                    color='Transaction_count',  # Set this to the column you want to visualize
                    color_continuous_scale='speed',
                    title='Choropleth Map of  Total Transaction by State',
                    hover_data=['State', 'Transaction_amount', 'Transaction_count'])

            st.plotly_chart(fig_toptr.update_geos(fitbounds="locations", visible=False))

    with tap2:

        opt = st.selectbox("choose the type of User",("Aggregated User", "Map User", "Top User"),index=None,placeholder="Select type of transaction...")
        if opt == "Aggregated User":
            query = f"SELECT State,Brand, SUM(Count) AS Total_Count FROM phonepe.AGGREGATED_USER WHERE Year = '{year_option}' AND Quater = '{selected_quater}' GROUP BY Brand"
            mycursor.execute(query)
            results = mycursor.fetchall()

# Create DataFrame
            df_agg = pd.DataFrame(results, columns=['State','Brand', 'Total_Count'])
            
            # Merge with your original data to include all states
            df_use_full = pd.merge(df_state_names_use, df_agg, on='State', how='left')

# Aggregate data to find the highest number of brands used in each state
            df_agg_brand = df_use_full.groupby('State').agg({'Brand': 'count'}).reset_index()
            df_agg_brand.rename(columns={'Brand': 'Max_Brand_Count'}, inplace=True)

# Aggregate data to find the sum of transactions in each state
            df_agg_count = df_use_full.groupby('State').agg({'Total_Count': 'sum'}).reset_index()

# Merge both aggregated DataFrames
            df_merged = pd.merge(df_agg_brand, df_agg_count, on='State', how='left')

# Plot choropleth map
            fig_agguser= px.choropleth(df_merged,
                    geojson=data2,
                    featureidkey='properties.ST_NM',
                    locations="State",
                    color='Max_Brand_Count',  # Set this to the column you want to visualize
                    color_continuous_scale='Sunsetdark',
                    hover_data={'State': True, 'Max_Brand_Count': True, 'Total_Count': True},
                    title='Choropleth Map of  Registered Users by State',
                    labels={'Max_Brand_Count': 'Max Brand Count', 'Total_Count': 'Total Count'})
            #fig_agguser.update_layout(title='Choropleth Map of Max Brand Counts in {year_option} in {selected_quater} by State')
            st.plotly_chart(fig_agguser.update_geos(fitbounds="locations", visible=False))
            
        if opt == "Map User":

            sql_query = f"SELECT  distinct State, SUM(Registered_Users) as Registered_Users, SUM(App_opens) as App_opens FROM phonepe.MAP_USER WHERE Year = {year_option} AND Quater = {selected_quater} GROUP BY State"

            mycursor.execute(sql_query)
            val = mycursor.fetchall()
            df_map_user = pd.DataFrame(val, columns=['State', 'Registered_Users', 'App_opens'])
#Merge with your original data to include all states
            df_use_full = pd.merge(df_state_names_use, df_map_user, on='State', how='left')

# Aggregate data to find the highest number of brands used in each state
            df_reg = df_use_full.groupby('State').agg({'Registered_Users': 'count'}).reset_index()


# Aggregate data to find the sum of transactions in each state
            df_agg_count = df_use_full.groupby('State').agg({'App_opens': 'sum'}).reset_index()

# Merge both aggregated DataFrames
            map_user = pd.merge(df_reg, df_agg_count, on='State', how='left')

# Plot choropleth map
            fig_mapuser = px.choropleth(map_user,
                    geojson=data2,
                    featureidkey='properties.ST_NM',
                    locations="State",
                    color='Registered_Users',  # Set this to the column you want to visualize
                    color_continuous_scale='Sunsetdark',
                    hover_data={'State': True, 'Registered_Users': True, 'App_opens': True},
                    title='Choropleth Map of  Registered Users by State',
                    labels={'State': 'State', 'Registered_Users': 'Registered_Users','App_opens' : 'App_opens'})

            st.plotly_chart(fig_mapuser.update_geos(fitbounds="locations", visible=False))
#fig.update_layout(title='Choropleth Map of Registered Users Counts by State')
        
        if opt == "Top User":

            sql_query = f"SELECT  distinct State, SUM(Registered_Users) as Registered_Users FROM phonepe.TOP_USER WHERE Year = {year_option} AND Quater = {selected_quater} GROUP BY State"

            mycursor.execute(sql_query)
            val = mycursor.fetchall()
            df_top_user = pd.DataFrame(val, columns=['State', 'Registered_Users'])


# Merge with your original data to include all states
            df_top = pd.merge(df_state_names_use, df_top_user, on='State', how='left')

# Aggregate data to find the highest number of brands used in each state
            df_reg = df_top.groupby('State').agg({'Registered_Users': 'sum'}).reset_index()


# Plot choropleth map
            fig_topuser = px.choropleth(df_reg,
                    geojson=data2,
                    featureidkey='properties.ST_NM',
                    locations="State",
                    color='Registered_Users',  # Set this to the column you want to visualize
                    color_continuous_scale='Viridis_r',  # Reversed color scale
                    hover_data={'State': True, 'Registered_Users': True},
                    title='Choropleth Map of  Registered Users by State')

            st.plotly_chart(fig_topuser.update_geos(fitbounds="locations", visible=False))



if option == 'Insight Query Analysis':
    optn=st.selectbox(
    "Select a query to execute:",
    ['1.Retrive Top 10 States with Highest Total count 2023?',
    '2. Retrieve the top 10 States with Lowest Total count 2023?',
    '3. Retrieve Top 10 Register users In 2023?',
    '4. Retrieve State wise Transaction Amount?',
    '5. Retrieve State wise Transaction count distribution?',
    '6. Retrieve Transaction type count over the Years?',
    '7. Retrive State wise Transaction count over Years?',
    '8. Retrive the Percentage of Users Brand wise?',
    '9. Retrive the State wise Register User?',
    '10.Retrive the State wise App opened Data?'

    ]

)
 
    def execute_selected_query(optn):
        if optn == '1.Retrive Top 10 States with Highest Total count 2023?':
            sql_query ='''SELECT State, SUM(Transaction_count) AS Total_count
            FROM phonepe.AGGREGATED_TRANSACTION
            WHERE Year = 2023
            GROUP BY State
            ORDER BY Total_count DESC
            LIMIT 10'''


            mycursor.execute(sql_query)
            val = mycursor.fetchall()
            df_ques1 = pd.DataFrame(val, columns=[ 'State', 'Total_count'])

            fig_ques1 = px.bar(df_ques1, x="State", y="Total_count",
                    title="Top 10 States with Highest Total Count 2023 ",
                    color="Total_count",
                    color_discrete_sequence=px.colors.qualitative.Prism)
            st.plotly_chart(fig_ques1)
            st.write("Insights:")
            st.write("- The top state with the highest total count in 2023 is: Karnataka")
            st.write("- Urbanization and Tech Hubs: Karnataka is home to major tech cities like Bangalore (Bengaluru), which is of ten referred to as the Silicon Valley of India. These urban centers have a higher concentration of tech-savvy individuals who are more likely to adopt digital payment platforms like PhonePe.")
            st.write("-  Youth Population: Karnataka has a relatively young population, with a significant proportion of its residents being young professionals and students. Younger demographics are generally more open to adopting new technologies, including digital payment solutions.")
            st.write("- This visualization helps identify the distribution of transactions across states.")

            

            

        elif optn == "2. Retrieve the top 10 States with Lowest Total count 2023?":
            sql_query='''SELECT State, SUM(Transaction_count) AS Total_count
            FROM phonepe.AGGREGATED_TRANSACTION
            WHERE Year = 2023
            GROUP BY State
            ORDER BY Total_count ASC
            LIMIT 10'''

            mycursor.execute(sql_query)
            val = mycursor.fetchall()
            df_ques2 = pd.DataFrame(val, columns=['State', 'Total_count'])


            fig_ques2 = px.bar(df_ques2, x="State", y="Total_count", color="Total_count",
                    title="The top 10 states with Lowest Total count 2023",
                    color_discrete_sequence=px.colors.qualitative.Prism)
            st.plotly_chart(fig_ques2)

            st.write("Insights:")
            st.write("- The state with the lowest total count in 2023 is Lakshadweep")
            st.write("-  Geographical Constraints: Lakshadweep is a group of islands with a small land area and population. The limited physical infrastructure and remoteness of the islands may restrict economic activities and, consequently, digital transactions.")
            st.write("-  Population: Size Lakshadweep has one of the smallest populations among Indian territories. With fewer residents, there may be fewer transactions overall, both in terms of the number of users and the volume of transactions.")
            st.write("- Potential reasons for lower transaction counts could include lower population density, lesser economic activity, or slower adoption of digital payment platforms in these states.")
            

        elif optn == "3. Retrieve Top 10 Register users In 2023?":
            sql_query = '''SELECT State, SUM(Registered_users) AS Registered_users
            FROM phonepe.MAP_USER
            WHERE Year = 2023
            GROUP BY State
            ORDER BY Registered_users DESC
            LIMIT 10'''

            mycursor.execute(sql_query)
            val = mycursor.fetchall()
            df_ques3 = pd.DataFrame(val, columns=['State', 'Registered_users'])

            # Create bar plot
            fig_ques3 = px.bar(df_ques3, x="State", y="Registered_users",
            title="Top 10 Register users In 2023",
            color="Registered_users",
            color_continuous_scale=px.colors.sequential.Mint)
            st.plotly_chart(fig_ques3)
            st.write("Insights:")
            st.write("- The top state with the highest number of registered users in 2023 is: Maharashtra")
            st.write("- This visualization provides an overview of user adoption across different states.")
        elif optn == "4. Retrieve State wise Transaction Amount?":
            sql_query='''SELECT State, SUM(Transaction_amount) AS Transaction_amount
                FROM phonepe.AGGREGATED_TRANSACTION\
                    where year between 2018 and 2023\
            GROUP BY State'''
            mycursor.execute(sql_query)
            val = mycursor.fetchall()
            df_ques4 = pd.DataFrame(val, columns=['State', 'Transaction_amount'])

            # Create bar plot
            fig_ques4 = px.bar(df_ques4, x="State", y="Transaction_amount",
            title="State wise Transaction Amount",
            color="Transaction_amount",
            color_continuous_scale=px.colors.sequential.Mint)
            st.plotly_chart(fig_ques4)
            st.write("Insights:")
            st.write("- The visualization shows the total transaction amounts across different states from 2018 to 2023.")
            st.write("- States with higher transaction amounts may indicate greater economic activity or higher adoption of digital payment platforms.")
            st.write("- Analyzing trends over time can help identify states that are experiencing significant growth in transaction amounts.")

        elif optn == "5. Retrieve State wise Transaction count distribution?":
            sql_query='''SELECT State, SUM(Transaction_count) AS Transaction_count
                FROM phonepe.AGGREGATED_TRANSACTION\
                    where year between 2018 and 2023\
            GROUP BY State'''

            mycursor.execute(sql_query)
            val = mycursor.fetchall()
            df_ques5 = pd.DataFrame(val, columns=[ 'State','Transaction_count'])

            # Create bar plot
            fig_ques5 = px.bar(df_ques5, x="State", y="Transaction_count",
            title=" State wise Transaction count distribution",
            color="Transaction_count",
            color_discrete_sequence=px.colors.qualitative.Prism)
            st.plotly_chart(fig_ques5)
            st.write("Insights:")
            st.write("- The visualization illustrates the distribution of transaction counts across different states and transaction types.")
            st.write("- Examining transaction counts by type can reveal insights into consumer behavior, such as preferences for payment methods or transaction categories.")
            st.write("- Analyzing transaction count distribution can also help identify states with diverse transaction patterns or potential areas for targeted interventions.")


        elif optn == "6. Retrieve Transaction type count over the Years?":
            sql_query='''SELECT Year, Transaction_type, SUM(Transaction_count) AS Transaction_count
            FROM phonepe.AGGREGATED_TRANSACTION
            GROUP BY Year, Transaction_type'''

            mycursor.execute(sql_query)
            val = mycursor.fetchall()
            df_ques6 = pd.DataFrame(val, columns=[ 'State','Transaction_type', 'Transaction_count'])

            # Create bar plot
            fig_ques6 = px.bar(df_ques6, x="State", y="Transaction_count",
            title="Transaction type count over the Years",
            color="Transaction_type",
            color_discrete_sequence=px.colors.qualitative.Prism)
            st.plotly_chart(fig_ques6)
            st.write("Insights:")
            st.write("- The visualization displays the trends in transaction types over the years.")
            st.write("- Analyzing transaction type counts over time can reveal shifts in consumer behavior or changes in the usage of different payment methods.")
            st.write("- Trends such as increasing or decreasing transaction counts for specific types can indicate evolving preferences or market dynamics.")


        elif optn == "7. Retrive State wise Transaction count over Years?":
            sql_query= '''SELECT Year, State, SUM(Transaction_count) AS Transaction_count
            FROM phonepe.AGGREGATED_TRANSACTION
            GROUP BY Year, State'''

            mycursor.execute(sql_query)
            val = mycursor.fetchall()
            df_ques7 = pd.DataFrame(val, columns=[ 'State','Year','Transaction_count'])

            # Create bar plot
            fig_ques7 = px.bar(df_ques7, x="Year", y="State",
            title=" State wise Transaction count over Years",
            color="Transaction_count",
            color_discrete_sequence=px.colors.qualitative.Prism)
            st.plotly_chart(fig_ques7)
            st.write("Insights:")
            st.write("- The visualization illustrates how transaction counts have varied across different states over the years.")
            st.write("- Examining transaction counts by state and year can reveal insights into regional trends and the growth of digital transactions.")
            st.write("- States with significant increases in transaction counts may indicate strong adoption of digital payment platforms or increasing economic activity.")

        elif optn == "8. Retrive the Percentage of Users Brand wise?":
            sql_query = '''SELECT Brand, SUM(Percentage) AS Percentage
            FROM phonepe.AGGREGATED_USER
            GROUP BY Brand'''

            # Execute the SQL query
            mycursor.execute(sql_query)

            # Fetch the result
            result = mycursor.fetchall()

            # Create DataFrame
            df_ques8 = pd.DataFrame(result, columns=[ 'Brand', 'Percentage'])


            # Create bar plot
            fig_ques8 = px.bar(df_ques8, x="Brand", y="Percentage",
            title=" Percentage of Users Brand wise",
            color="Percentage",
            color_discrete_sequence=px.colors.qualitative.Prism)
            st.plotly_chart(fig_ques8)
            st.write("Insights:")
            st.write("- The visualization represents the distribution of users among different brands.")
            st.write("- Examining the percentage of users by brand can provide insights into brand loyalty or market share.")
            st.write("- Brands with higher percentages may have a larger user base or stronger adoption rates.")

        elif optn == "9. Retrive the State wise Register User?":
            sql_query='''SELECT State, SUM(Registered_users) AS Registered_users
            FROM phonepe.MAP_USER
            GROUP BY State'''

            mycursor.execute(sql_query)
            val = mycursor.fetchall()
            df_ques9 = pd.DataFrame(val, columns=[ 'State','Registered_users'])

            # Create bar plot
            fig_ques9 = px.bar(df_ques9, x="State", y="Registered_users",
                                title="The State wise Register User",
                                color="Registered_users",
                                color_discrete_sequence=px.colors.qualitative.Prism)
            st.plotly_chart(fig_ques9)
            st.write("Insights:")
            st.write("- The visualization represents the distribution of registered users among different states.")
            st.write("- Examining the percentage of register users by state can provide insights into regional adoption rates or user engagement.")
            st.write("- States with higher percentages may have a larger user base or stronger adoption of the platform.")
        elif optn == "10.Retrive the State wise App opened Data?":
            sql_query = '''SELECT State, SUM(App_opens) AS App_opens
             FROM phonepe.MAP_USER
             GROUP BY State'''

            # Execute the SQL query
            mycursor.execute(sql_query)

            # Fetch the result
            result = mycursor.fetchall()

            # Create DataFrame
            df_ques10 = pd.DataFrame(result, columns=[ 'State', 'App_opens'])


            # Create bar plot
            fig_ques10 = px.bar(df_ques10, x="State", y="App_opens",
                                title="The State wise App opened Data",
                                color="App_opens",
                                color_discrete_sequence=px.colors.qualitative.Prism)
            st.plotly_chart(fig_ques10)
            st.write("Insights:")
            st.write("- The visualization represents the distribution of app openings among different states in 2023.")
            st.write("- Examining app openings by state can provide insights into regional engagement levels or user activity.")
            st.write("- States with higher percentages may have a larger user base or stronger user engagement with the app.")



    if st.button("Execute Query"):
        execute_selected_query(optn)
    