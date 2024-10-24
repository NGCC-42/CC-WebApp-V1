import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image
import numpy as np
from collections import ChainMap, defaultdict
import difflib
import altair as alt
import matplotlib.pyplot as plt
from operator import itemgetter


### SET WEB APP CONFIGURATIONS
st.set_page_config(page_title='Club Cannon Database', 
                  layout='centered')



### SET HEADER IMAGE
image = Image.open('Images/club-cannon-logo-bbb.png')
st.image(image, 
        use_column_width=True)

st.divider()
### LOAD FILES
sod_ss = 'SOD 10.24.xlsx'

quote_ss = 'Quote Report 10.23.24.xlsx'

sales_sum_csv = 'Fulcrum Sales Summary/Total Summary-2022 - Present.csv'


prod_sales = 'Product Sales Data.xlsx'

### LOAD SHEETS FROM PRODUCT SUMMARY

acc_2024 = 'Accessories 2024'
cntl_2024 = 'Controllers Sales 2024'
jet_2024 = 'Jet Sales 2024'
hh_2024 = 'Handheld Sales 2024'
hose_2024 = 'Hose Sales 2024'

acc_2023 = 'Accessories 2023'
cntl_2023 = 'Controllers Sales 2023'
jet_2023 = 'Jet Sales 2023'
hh_2023 = 'Handheld Sales 2023'
hose_2023 = 'Hose Sales 2023'

### LOAD SHEETS FROM SALES SUMMARY

total_sum = 'Total Summary'

### LOAD DATAFRAME(S) (RETAIN FORMATTING IN XLSX)

df = pd.read_excel(sod_ss,
                   dtype=object,
                   header=0)

df_quotes = pd.read_excel(quote_ss, 
                          dtype=object,
                          header=0)


### DEFINE FUNCTION TO CREATE PRODUCT DATAFRAME FROM EXCEL SPREADSHEET ###

def gen_product_df_from_excel(ss, sheet_name, cols=None):

    df_product_year = pd.read_excel(ss,
                                   usecols=cols,
                                   names=['Product', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December', 'Total'],
                                   sheet_name=sheet_name,
                                    dtype=object,
                                    header=1
                                   )
    return df_product_year

df_csv = pd.read_csv(sales_sum_csv,
                    usecols=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])


df_acc_2024 = pd.read_excel(prod_sales,
                   usecols='a:m',
                   names=['Product', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December', 'Total'],
                   sheet_name=acc_2024,
                   dtype=object,
                   header=1)
df_cntl_2024 = pd.read_excel(prod_sales,
                   usecols='a:m',
                   names=['Product', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December', 'Total'],
                   sheet_name=cntl_2024,
                   dtype=object,
                   header=1)
df_jet_2024 = pd.read_excel(prod_sales,
                   usecols='a:m',
                   names=['Product', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December', 'Total'],
                   sheet_name=jet_2024,
                   dtype=object,
                   header=1)
df_hh_2024 = pd.read_excel(prod_sales,
                   usecols='a:m',
                   names=['Product', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December', 'Total'],
                   sheet_name=hh_2024,
                   dtype=object,
                   header=1)
df_hose_2024 = pd.read_excel(prod_sales,
                   usecols='a:m',
                   names=['Product', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December', 'Total'],
                   sheet_name=hose_2024,
                   dtype=object,
                   header=1)

df_acc_2023 = pd.read_excel(prod_sales,
                   usecols='a:m',
                   names=['Product', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December', 'Total'],
                   sheet_name=acc_2023,
                   dtype=object,
                   header=1)
df_cntl_2023 = pd.read_excel(prod_sales,
                   names=['Product', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December', 'Total'],
                   sheet_name=cntl_2023,
                   dtype=object,
                   header=1)
df_jet_2023 = pd.read_excel(prod_sales,
                   usecols='a:m',
                   names=['Product', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December', 'Total'],
                   sheet_name=jet_2023,
                   dtype=object,
                   header=1)
df_hh_2023 = pd.read_excel(prod_sales,
                   usecols='a:m',
                   names=['Product', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December', 'Total'],
                   sheet_name=hh_2023,
                   dtype=object,
                   header=1)
df_hose_2023 = pd.read_excel(prod_sales,
                   usecols='a:m',
                   names=['Product', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December', 'Total'],
                   sheet_name=hose_2023,
                   dtype=object,
                   header=1)





### CREATE DATE LISTS ###

months = ['All', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
months_x = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
years = ['2022', '2023', '2024']
    
    
### DEFINE FUNCTION TO RENAME COLUMNS FOR CHART AXIS SORTING ###

def ordered_months(df):
    
    idx = 1
    temp_dict = {}
    for month in months_x:
        temp_dict[month] = str(idx)+ ' ' + month
        idx *= 10
    new_df = df.rename(columns = temp_dict)
    return new_df

def rev_ordered_months(df):
 
    idx_char = 1
    temp_dict = {}
    
    for month in df.head(0):
        if month == 'Product':
            pass
        else:
            temp_dict[month] = month[idx_char:]
            idx_char += 1

    rev_df = df.rename(columns = temp_dict)
    return rev_df


### FUNCTION TESTING ###

#st.write(df_jet2023_unt.iloc[0])

#for month in df_jet2023_unt.iloc[0]:
    #st.write(month)

### TEST CHARTING OF DATA ###


#df_test = pd.DataFrame({'Months': months_x,
                       #'Units Sold': [49,24,31,47,36,34,44,78,35,23,19,8]})
#st.write(df_test)


### DEFINE A FUNCTION TO CONVERT - SERIES --> DICT --> DATAFRAME ###

def format_for_chart(series):
    
    temp_dict = {'Months': months_x,
                'Units Sold': []}
    
    for month in series[1:]:
        if len(temp_dict['Units Sold']) >= 12:
            pass
        else:
            temp_dict['Units Sold'].append(month)
    df = pd.DataFrame(temp_dict)
    
    return df

#st.write(format_for_chart(df_cntl23_unt.iloc[0]))


### SCRIPT TO PLOT BAR GRAPH FOR PRODUCT SALES ###

def plot_bar_chart(df):
    st.write(alt.Chart(df).mark_bar().encode(
        x=alt.X('Months', sort=None).title('Month'),
        y='Units Sold',
    ).properties(height=500, width=750).configure_mark(
        color='limegreen'
    ))
    

#plot_bar_chart(df_test)



### CREATE AVG FUNCTION ###


def avg_month(dict):
    zero_count = 0
    total = 0
    for key, value in dict.items():
        if value == 0:
            zero_count += 1
        else:
            total += value
    return int(total / (len(dict) - zero_count))
            


### DEFINE FUNCTION TO CREATE DICTIONARY OF PRODUCT REVENUES AND TOTAL REVENUE FOR TYPE OF PRODUCT ###

def revenue_calculator(prod_df):
    
    product_rev_total = {}
    type_rev_total = 0
    
    
    idx = 0
    
    for row in prod_df['Product']:
        product_rev_total[row] = 0
        
        for month in months_x:
            product_rev_total[row] += prod_df[month].iloc[idx]
            type_rev_total += prod_df[month].iloc[idx]
    
        idx += 1    

    return product_rev_total, type_rev_total




### DEFINE FUNCTION TO FIND PRODUCT REVENUE PERCENTAGE OF TOTAL TYPE FROM DICTIONARY ###

def product_revenue_share(dict, total):

    percentage_dict = {}
    
    for key, value in dict.items():
        percentage_dict[key] = (value / total) * 100

    return percentage_dict

### DEFINE A FUNCTION TO TAKE PRODUCT SALES DATAFRAME AND RETURN DICTIONARY OF EACH PRODUCTS PERCENTAGE OF REVENUE OF TYPE ###

def percentage_of_revenue(prod_df):

    prod_rev_total, type_rev_total = revenue_calculator(prod_df)

    return product_revenue_share(prod_rev_total, type_rev_total)


### DEFINE A FUNCTION TO CREATE A DATAFRAME FROM DICTIONARY OF REVENUE PERCENTAGES ###

def dataframe_from_dict(dict):

    dict_of_lists = {'Products': [], 
                    'Share': []}

    for key, value in dict.items():
        dict_of_lists['Products'].append(key)
        dict_of_lists['Share'].append(value)

    df = pd.DataFrame(dict_of_lists)
    
    return df

### DEFINE A FUNCTION TO COMBINE MULTIPLE YEARS OF PRODUCT REVENUE DATA ###

def multiyear_product_revenue(list_of_dfs):

    product_revenue_totals = {}
    type_totals = 0
    
    rev_idx = 0
    
    for dfs in list_of_dfs:
    
        prod_rev, type_rev = revenue_calculator(dfs)
        type_totals += type_rev
        if rev_idx == 0:
            for key, value in prod_rev.items():
                product_revenue_totals[key] = value
        else:
            for key, value in prod_rev.items():
                product_revenue_totals[key] += value
                
        rev_idx += 1

    rev_percent_dict = product_revenue_share(product_revenue_totals, type_totals)
    
    return rev_percent_dict, product_revenue_totals, type_totals


### DEFINE A FUNCTION TO DISPLAY PRODUCT PROFIT DATA ###

def display_profit_data(df, product_selection):

    idx = 0
    for product in df['Product']:
        if product == product_selection:
            st.write('  - BOM Cost w/ Labor & Accessories:   ' + '${:,.2f}'.format(df['Cost'].iloc[idx]))
            st.write('  - Average Price:   ' + '${:,.2f}'.format(df['Avg Price'].iloc[idx]))
            st.write('  - Net Profit / Unit:   ' + '${:,.2f}'.format(df['Net Profit / Unit'].iloc[idx]))
        idx += 1

    return None


### WRITE A FUNCTION TO SORT NAMES BY CLOSEST MATCH TO INPUT ###

def sort_by_match(lst, target_string):

    return sorted(lst, key=lambda x: difflib.SequenceMatcher(None, x.lower(), target_string.lower()).ratio(), reverse=True)


def get_sales_orders(customer, dataFrame):

    temp_list = []

    ct = 0
    while df.iloc[idx + ct]['Sales Order'] == df.iloc[idx + ct + 1]['Sales Order']:
        
        temp_list.append(df.iloc[idx + ct]['Line Item Name'] + ' x ' + str(df.iloc[idx + ct]['Order Quantity']))
        ct += 1
            
    temp_dict[df.iloc[idx]['Sales Order']] = temp_list

    return temp_dict

### MAKE LIST OF PRODUCT TYPES ###

product_types = ['Jets', 'Controllers', 'Hoses', 'Accessories', 'Handhelds']


### SEPARATE SALES AND REVENUE ###

df_jet2023_unt = df_jet_2023[0:4].fillna(0)
df_jet2023_rev = df_jet_2023[13:17].fillna(0)
df_jet2023_prof = df_jet_2023[20:24].fillna(0).rename({'March': 'Cost', 'April': 'Avg Price', 'May': 'Net Profit / Unit', 'June': 'Total Net Profit'}, axis=1).drop(['January', 'February', 'July', 'August', 'September', 'October', 'November', 'December'], axis=1).reset_index()

df_cntl23_unt = df_cntl_2023[0:3].fillna(0)
df_cntl23_rev = df_cntl_2023[11:14].fillna(0)
df_cntl23_prof = df_cntl_2023[17:20].fillna(0).rename({'March': 'Cost', 'April': 'Avg Price', 'May': 'Net Profit / Unit', 'June': 'Total Net Profit'}, axis=1).drop(['January', 'February', 'July', 'August', 'September', 'October', 'November', 'December'], axis=1).reset_index()

df_h23_unt = df_hose_2023[0:22].fillna(0)
df_h23_rev = df_hose_2023[48:70].fillna(0)

df_ac23_unt = df_acc_2023[0:30].fillna(0)
df_ac23_rev = df_acc_2023[58:84].fillna(0)

df_hh23_unt = df_hh_2023[0:4].fillna(0)
df_hh23_rev = df_hh_2023[13:17].fillna(0)

df_jet2024_unt = df_jet_2024[0:4].fillna(0)
df_jet2024_rev = df_jet_2024[13:17].fillna(0)
df_jet2024_prof = df_jet_2024[20:24].fillna(0).rename({'March': 'Cost', 'April': 'Avg Price', 'May': 'Net Profit / Unit', 'June': 'Total Net Profit'}, axis=1).drop(['January', 'February', 'July', 'August', 'September', 'October', 'November', 'December'], axis=1).reset_index()

df_cntl24_unt = df_cntl_2024[0:3].fillna(0)
df_cntl24_rev = df_cntl_2024[11:14].fillna(0)
df_cntl24_prof = df_cntl_2024[17:20].fillna(0).rename({'March': 'Cost', 'April': 'Avg Price', 'May': 'Net Profit / Unit', 'June': 'Total Net Profit'}, axis=1).drop(['January', 'February', 'July', 'August', 'September', 'October', 'November', 'December'], axis=1).reset_index()
                                        
df_h24_unt = df_hose_2024[0:22].fillna(0)
df_h24_rev = df_hose_2024[48:70].fillna(0)

df_ac24_unt = df_acc_2024[0:30].fillna(0)
df_ac24_rev = df_acc_2024[59:86].fillna(0)
#st.write(df_ac24_rev)

df_hh24_unt = df_hh_2024[0:4].fillna(0)
df_hh24_rev = df_hh_2024[13:17].fillna(0)


### CREATE LISTS OF CATEGORIES FROM DATAFRAME ###

jets = df_jet2023_unt['Product'].unique().tolist()
controllers = df_cntl23_unt['Product'].unique().tolist()
hoses = df_h23_unt['Product'].unique().tolist()
acc = df_ac23_unt['Product'].unique().tolist()
hh = df_hh23_unt['Product'].unique().tolist()


### STRIP UNUSED COLUMN ###

df = df.drop(['Ordered Week', 'Ordered Month', 'Customer Item Name'], axis=1)

### RENAME DF COLUMNS FOR SIMPLICITY ###

df.rename(columns={
    'Sales Order': 'sales_order',
    'Customer': 'customer',
    'Ordered Date': 'order_date',
    'Line Item Name': 'item_sku',
    'Line Item': 'line_item',
    'Order Quantity': 'quantity',
    'Total Line Item $': 'total_line_item_spend',
    'Ordered Year': 'ordered_year'},
    inplace=True)

df_quotes.rename(columns={
    'Number': 'number',
    'Customer': 'customer',
    'CustomerContact': 'contact',
    'TotalInPrimaryCurrency': 'total',
    'CreatedUtc': 'date_created',
    'Status': 'status',
    'ClosedDate': 'closed_date'}, 
    inplace=True)


quote_cust_list = df_quotes['customer'].unique().tolist()




### MAKE DICTIONARIES OF PRODUCT SALES FOR CHARTING ###

jet_dict_2023 = {'Pro Jet': 0,
                'Quad Jet': 0,
                'Micro Jet': 0,
                'Cryo Clamp': 0}
jet_dict_2024 = {'Pro Jet': 0,
                'Quad Jet': 0,
                'Micro Jet': 0,
                'Cryo Clamp': 0}
control_dict_2023 = {'The Button': 0,
                     'Shostarter': 0,
                     'Shomaster': 0}
control_dict_2024 = {'The Button': 0,
                     'Shostarter': 0,
                     'Shomaster': 0}
handheld_dict_2023 = {'8FT - No Case': 0,
                     '8FT - Travel Case': 0,
                     '15FT - No Case': 0,
                     '15FT - Travel Case': 0}
handheld_dict_2024 = {'8FT - No Case': 0,
                     '8FT - Travel Case': 0,
                     '15FT - No Case': 0,
                     '15FT - Travel Case': 0}

idx = 0
for line_item in df.line_item:
    if line_item[:6] == 'CC-PRO':
        if df.iloc[idx].ordered_year == '2023':
            jet_dict_2023['Pro Jet'] += df.iloc[idx].quantity
        elif df.iloc[idx].ordered_year == '2024':
            jet_dict_2024['Pro Jet'] += df.iloc[idx].quantity
        else:
            pass
    idx += 1



### CREATE A LIST OF UNIQUE CUSTOMERS ###
unique_customer_list = df.customer.unique().tolist()

task_select = st.selectbox('Choose Widget Task', 
                          options=[' - Choose an Option - ', 'Customer Details', 'Customer Spending Leaders', 'Product Sales', 'Monthly Sales', 'Customer Quote Reports'])

st.divider()

if task_select == 'Customer Quote Reports':

    st.header('Quote Reports')
    
    quote_cust = st.multiselect('Search Customers',
                            options=quote_cust_list, 
                            max_selections=1,
                            placeholder='Start Typing Customer Name')

    if len(quote_cust) >= 1:
        quote_cust = quote_cust[0]
    else:
        quote_cust = ''

    idx = 0
    cust_list_q = []
    cust_won_total = 0
    cust_won_count = 0
    cust_lost_total = 0
    cust_lost_count = 0
    
    
    
    for customer in df_quotes.customer:

        if customer.upper() == quote_cust.upper():
    
            if df_quotes.iloc[idx].status == 'Won':
                cust_won_total += df_quotes.iloc[idx].total
                cust_won_count += 1
            if df_quotes.iloc[idx].status == 'Lost' or df_quotes.iloc[idx].status == 'Sent' or df_quotes.iloc[idx].status == 'Draft':
                cust_lost_total += df_quotes.iloc[idx].total
                cust_lost_count += 1
            
            cust_list_q.append('({})  {}  - ${:,.2f}  - {} - {}'.format(
                df_quotes.iloc[idx].number,
                df_quotes.iloc[idx].customer,
                df_quotes.iloc[idx].total,
                df_quotes.iloc[idx].date_created,
                df_quotes.iloc[idx].status))

        idx += 1

    
    col11, col12 = st.columns(2)
    if cust_won_count >= 1:
    
        with col11:
            st.header('')
            st.header('')
            st.header('')
            st.subheader('Quotes Won: ' + str(cust_won_count)) 
        with col11:
         
            st.subheader('For a Total of: ' + '${:,.2f}'.format(cust_won_total))
    if cust_lost_count >= 1:
        with col12:
            st.header('')
            st.header('')
            st.header('')
            st.subheader('Quotes Lost or Pending: ' + str(cust_lost_count))
        with col12:
    
            st.subheader('For a Total of: ' + '${:,.2f}'.format(cust_lost_total))

    if cust_lost_count >= 1 and cust_won_count >= 1:
        st.write('Conversion Percentage: ' + '{:,.2f}'.format((cust_won_count / (cust_lost_count + cust_won_count)) * 100) + '% of Quotes ' + '( {:,.2f}'.format((cust_won_total / (cust_lost_total + cust_won_total)) * 100) + '% of Potential Revenue )')
        st.divider()
        st.header('')
        
        for quote in cust_list_q:
            st.write(quote)


elif task_select == 'Customer Details':
    
    with st.container():
        st.header('Customer Details')
        #text_input = st.text_input('Search Customers')
        text_input = st.multiselect('Search Customers', 
                                   options=unique_customer_list, 
                                   max_selections=1,
                                   placeholder='Start Typing Customer Name')
        
        if len(text_input) >= 1:
            text_input = text_input[0]
        else:
            text_input = ''
    
        
        #st.write(text_input)
        #text_input = text_input.lower()
    
        #if text_input.upper() not in df.customer.str.upper() and len(text_input) > 1:
            #possible_cust = []
        
            #for cust in df.customer:
                #if cust[:9].upper() == text_input[:9].upper() and cust[:10].upper() == text_input[:10].upper():
                    #text_input = cust
                    #break
                #if cust[:1].upper() == text_input[:1].upper() or cust[:2].lower() == text_input[:2].lower():
                    #if cust in possible_cust:
                        #pass
                    #else:
                        #possible_cust.append(cust)
            #if text_input == cust:
                #pass
            #else:
                #possible_cust = sort_by_match(possible_cust, text_input)
                #for custs in possible_cust:
                    #if custs[:2] == text_input[:2]:
                        #possible_cust.remove(custs)
                        #possible_cust.insert(0, custs)
                #for customer in possible_cust[:14]:
                    #st.write('Are you searching for - {} - ?'.format(customer))
        #st.write(text_input)
        
        ### PRODUCT CATEGORY LISTS ###
        sales_order_list = []
        jet_list = []
        controller_list = []
        misc_list = []
        magic_list = []
        hose_list = []
        fittings_accessories_list = []
        handheld_list = []
        
        ### PRODUCT TOTALS SUMMARY DICTS ###
        jet_totals_cust = {'Quad Jet': 0, 
                          'Pro Jet': 0, 
                          'Micro Jet MKII': 0,
                          'Cryo Clamp': 0}
        controller_totals_cust = {'The Button': 0,
                                 'Shostarter': 0,
                                 'Shomaster': 0}
        cust_handheld_cnt = 0
        cust_LED_cnt = 0
        cust_RC_cnt = 0
        
        ### LISTS OF HISTORICAL SALES FOR CUSTOMER ###
        spend_total = {2023: None, 2024: None}
        spend_total_2023 = 0.0
        spend_total_2024 = 0.0
        sales_order_list = []
        
        idx = 0
        
        for customer in df.customer:
            
            if customer.upper() == text_input.upper():
                #sales_order_list.append(df.iloc[idx].sales_order)
                
                ### LOCATE AND PULL SPEND TOTALS FOR SELECTED CUSTOMER AND ADD TO LISTS ###
                if df.iloc[idx].ordered_year == '2023':
                    spend_total_2023 += df.iloc[idx].total_line_item_spend
                elif df.iloc[idx].ordered_year == '2024':
                    spend_total_2024 += df.iloc[idx].total_line_item_spend
        
        
        
                ### LOCATE ALL ITEMS FROM SOLD TO SELECTED CUSTOMER AND ADD TO LISTS ###
                if df.iloc[idx].item_sku[:5] == 'CC-QJ' or df.iloc[idx].item_sku[:5] == 'CC-PR' or df.iloc[idx].item_sku[:5] == 'CC-MJ' or df.iloc[idx].item_sku[:6] == 'CC-CC2':
                    jet_list.append('|    {}    |     ({}x)    {}  --  {}'.format(
                        df.iloc[idx].sales_order, 
                        df.iloc[idx].quantity,
                        df.iloc[idx].item_sku,
                        df.iloc[idx].line_item))
                    if df.iloc[idx].item_sku[:5] == 'CC-QJ':
                        jet_totals_cust['Quad Jet'] += df.iloc[idx].quantity
                    elif df.iloc[idx].item_sku[:5] == 'CC-PR':
                        jet_totals_cust['Pro Jet'] += df.iloc[idx].quantity
                    elif df.iloc[idx].item_sku[:5] == 'CC-MJ':
                        jet_totals_cust['Micro Jet MKII'] += df.iloc[idx].quantity
                    elif df.iloc[idx].item_sku[:6] == 'CC-CC2':
                        jet_totals_cust['Cryo Clamp'] += df.iloc[idx].quantity
                elif df.iloc[idx].item_sku[:5] == 'CC-TB' or df.iloc[idx].item_sku[:5] == 'CC-SS' or df.iloc[idx].item_sku[:5] == 'CC-SM':
                    controller_list.append('|    {}    |     ({}x)    {}  --  {}'.format(
                        df.iloc[idx].sales_order, 
                        df.iloc[idx].quantity,
                        df.iloc[idx].item_sku,
                        df.iloc[idx].line_item))
                    if df.iloc[idx].item_sku[:5] == 'CC-TB':
                        controller_totals_cust['The Button'] += df.iloc[idx].quantity
                    elif df.iloc[idx].item_sku[:5] == 'CC-SS':
                        controller_totals_cust['Shostarter'] += df.iloc[idx].quantity
                    elif df.iloc[idx].item_sku[:5] == 'CC-SM':
                        controller_totals_cust['Shomaster'] += df.iloc[idx].quantity
                elif df.iloc[idx].item_sku[:5] == 'Magic' or df.iloc[idx].item_sku[:4] == 'MFX-':
                    magic_list.append('|    {}    |     ({}x)    {}  --  {}'.format(
                        df.iloc[idx].sales_order, 
                        df.iloc[idx].quantity,
                        df.iloc[idx].item_sku,
                        df.iloc[idx].line_item))
                elif df.iloc[idx].item_sku[:5] == 'CC-CH':
                    hose_list.append('|    {}    |     ({}x)    {}  --  {}'.format(
                        df.iloc[idx].sales_order, 
                        df.iloc[idx].quantity,
                        df.iloc[idx].item_sku,
                        df.iloc[idx].line_item))
                elif df.iloc[idx].item_sku[:5] == 'CC-F-' or df.iloc[idx].item_sku[:5] == 'CC-AC' or df.iloc[idx].item_sku[:5] == 'CC-CT' or df.iloc[idx].item_sku[:5] == 'CC-WA':
                    fittings_accessories_list.append('|    {}    |     ({}x)    {}  --  {}'.format(
                        df.iloc[idx].sales_order, 
                        df.iloc[idx].quantity,
                        df.iloc[idx].item_sku,
                        df.iloc[idx].line_item))
                    if df.iloc[idx].item_sku[:9] == 'CC-AC-LA2':
                        cust_LED_cnt += df.iloc[idx].quantity                    
                elif df.iloc[idx].item_sku[:6] == 'CC-HCC' or df.iloc[idx].item_sku[:6] == 'Handhe':
                    handheld_list.append('|    {}    |     ({}x)    {}  --  {}'.format(
                        df.iloc[idx].sales_order, 
                        df.iloc[idx].quantity,
                        df.iloc[idx].item_sku,
                        df.iloc[idx].line_item))
                    cust_handheld_cnt += df.iloc[idx].quantity
                elif df.iloc[idx].item_sku[:5] == 'Shipp' or df.iloc[idx].item_sku[:5] == 'Overn' or df.iloc[idx].item_sku[:5] == 'CC-NP':
                    pass
                else:
                    misc_list.append('|    {}    |     ({}x)     {}  --  {}'.format(
                        df.iloc[idx].sales_order, 
                        df.iloc[idx].quantity,
                        df.iloc[idx].item_sku,
                        df.iloc[idx].line_item))
                    if df.iloc[idx].item_sku == 'CC-RC-2430':
                        cust_RC_cnt += df.iloc[idx].quantity

                if df.iloc[idx].sales_order in sales_order_list:
                    pass
                else:
                    sales_order_list.append(df.iloc[idx].sales_order)
            idx += 1
            
        #st.write(sales_order_list)
        st.header('')
        st.subheader('')
        st.subheader('')
        col3, col4, col5 = st.columns(3)
        
        ### DISPLAY CUSTOMER SPENDING TRENDS AND TOTALS ###
        with col3:
            if spend_total_2023 + spend_total_2024 > 0:
                st.subheader('2023 Spending:')
                st.write('${:,.2f}'.format(spend_total_2023))
        with col4:
            if spend_total_2023 + spend_total_2024 > 0:
                st.subheader('2024 Spending:')
                st.write('${:,.2f}'.format(spend_total_2024))
        with col5:
            if spend_total_2023 + spend_total_2024 > 0:
                st.subheader('Total Spending:')
                total_spending = spend_total_2023 + spend_total_2024
                st.write('${:,.2f}'.format(total_spending))
        
        ### DISPLAY PRODUCT PURCHASE SUMMARIES FOR SELECTED CUSTOMER ###
        if len(text_input) > 1:
            st.subheader('Product Totals:')
            col6, col7, col8 = st.columns(3)
            with col6:
                for jet, totl in jet_totals_cust.items():
                    if totl > 0:
                        st.write(jet + ': ' + str(totl))
            with col7:
                for controller, totl in controller_totals_cust.items():
                    if totl > 0:
                        st.write(controller + ': ' + str(totl))
                if cust_handheld_cnt > 0:
                    st.write('Handhelds: ' + str(cust_handheld_cnt))
            with col8:
                if cust_LED_cnt > 0:
                    st.write('LED Attachment II: ' + str(cust_LED_cnt))
                if cust_RC_cnt > 0:
                    st.write('Road Cases: ' + str(cust_RC_cnt))
        
        ### DISPLAY CATEGORIES OF PRODUCTS PURCHASED BY SELECTED CUSTOMER ###
        if len(jet_list) >= 1:
            st.subheader('Stationary Jets:')
            for item in jet_list:
                st.write(item)
        if len(controller_list) >= 1:
            st.subheader('Controllers:')
            for item in controller_list:
                st.write(item)
        if len(handheld_list) >= 1:
            st.subheader('Handhelds:')
            for item in handheld_list:
                st.write(item)
        if len(hose_list) >= 1:
            st.subheader('Hoses:')
            for item in hose_list:
                st.write(item)
        if len(fittings_accessories_list) >= 1:
            st.subheader('Fittings & Accessories:')
            for item in fittings_accessories_list:
                st.write(item)
        if len(misc_list) >= 1:
            st.subheader('Misc:')
            for item in misc_list:
                st.write(item)
        if len(magic_list):
            st.subheader('Magic FX:')
            for item in magic_list:
                st.write(item)
    
    
    
    st.divider()
    
    ### CREATE LISTS OF CATEGORIES FROM DATAFRAME ###
    
    jets = df_jet2023_unt['Product'].unique().tolist()
    controllers = df_cntl23_unt['Product'].unique().tolist()
    hoses = df_h23_unt['Product'].unique().tolist()
    acc = df_ac23_unt['Product'].unique().tolist()
    hh = df_hh23_unt['Product'].unique().tolist()
    
    
    
    ### CREATE DATE LISTS ###
    
    months = ['All', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    months_x = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    years = ['2022', '2023', '2024']
    
    
    


######################################################################### PRODUCT SALES DATABASE ###########################################################################


elif task_select == 'Product Sales':
    st.header('Product Sales')
    
    
    ### INSERT SELECTION MENU FOR CATEGORY ###
    
    year_select_prod = st.selectbox('Select Year:', 
                                   options=['All', '2023', '2024'])
    
    date_range = st.multiselect('Months:',
                                placeholder='Select Months',
                                options=months,
                                help='If ALL is selected do not add other months.')
    
    if date_range == ['All']:
        date_range = months_x
    
    
    product_type_selection = st.selectbox('Select Product Type:', 
                                         options=product_types)
    
    ### INSERT SELECTION MENU FOR PRODUCT TYPE ###
    
    if product_type_selection == 'Jets':
    
        
        jet_selection = st.selectbox('Jets:',
                                      options=jets,
                                      placeholder='Select Product')
        
    ### REVENUE CHECKBOX ###
    
        revenue_view = st.checkbox('Show Revenue Data')
        
        
        
    ### FILTER DATAFRAME BY SELECTION
    
        mask_jet_23 = df_jet2023_unt.loc[df_jet2023_unt['Product'] == jet_selection][date_range]
        mask_jet_24 = df_jet2024_unt.loc[df_jet2024_unt['Product'] == jet_selection][date_range]
        
        
    ### ASSIGN INDEX NUMBERS FOR ROWS ###
        j_idx = 0
    
        ct_j = 0
        for z in jets:
            if jet_selection == z:
                j_idx = ct_j
            ct_j +=1
    
    ### LOCATE AND DISPLAY RESULTS ###
    
        if year_select_prod == 'All':
            
            st.subheader(sum(mask_jet_23.loc[j_idx][date_range])+sum(mask_jet_24.loc[j_idx][date_range]))  
    
            if revenue_view == True and date_range == months_x:
                prod_rev_share, prod_rev, type_rev = multiyear_product_revenue([df_jet2023_rev, df_jet2024_rev])
                st.write(' - Total Revenue:  $' + '{:,.2f}'.format(prod_rev[jet_selection]) + ' - ' + '{:,.2f}'.format(prod_rev_share[jet_selection]) + '% of revenue from jets')
     
                
                #st.write(dataframe_from_dict(multiyear_product_revenue([df_jet2023_rev, df_jet2024_rev])))
                
            
        elif year_select_prod == '2023':
            avg_per_month = {}
            mbd_display_jet = st.checkbox('Display Monthly Breakdown')
            st.subheader(sum(mask_jet_23.loc[j_idx][date_range]))
            if revenue_view == True and date_range == months_x:
                prod_rev_share, prod_rev, type_rev = multiyear_product_revenue([df_jet2023_rev])
                st.write(' - 2023 Revenue:  $' + '{:,.2f}'.format(prod_rev[jet_selection]) + ' - ' + '{:,.2f}'.format(prod_rev_share[jet_selection]) + '% of revenue from jets')
                display_profit_data(df_jet2023_prof, jet_selection)
            if mbd_display_jet == True:
                for month in date_range:
                    avg_per_month[month] = mask_jet_23.loc[j_idx][month]
                    st.write(month + ' - ' + str(mask_jet_23.loc[j_idx][month]))
                st.write('( - Average per month: ' + str(avg_month(avg_per_month)) + ' - )')
                plot_bar_chart(format_for_chart(df_jet2023_unt.iloc[j_idx]))
    
        else:
            avg_per_month = {}
            mbd_display_jet = st.checkbox('Display Monthly Breakdown')
            st.subheader(sum(mask_jet_24.loc[j_idx][date_range]))
            if revenue_view == True and date_range == months_x:
                prod_rev_share, prod_rev, type_rev = multiyear_product_revenue([df_jet2024_rev])
                st.write(' - 2024 Revenue:  $' + '{:,.2f}'.format(prod_rev[jet_selection]) + ' - ' + '{:,.2f}'.format(prod_rev_share[jet_selection]) + '% of revenue from jets')
                display_profit_data(df_jet2024_prof, jet_selection)
            if mbd_display_jet == True:
                for month in date_range:
                    avg_per_month[month] = mask_jet_24.loc[j_idx][month]
                    st.write(month + ' - ' + str(mask_jet_24.loc[j_idx][month]))
                st.write('( - Average per month: ' + str(avg_month(avg_per_month)) + ' - )')
                plot_bar_chart(format_for_chart(df_jet2024_unt.iloc[j_idx]))
    
            
    elif product_type_selection == 'Controllers':
    
        control_selection = st.selectbox('Controllers:',
                                      options=controllers,
                                      placeholder='Choose an Option')
    ### REVENUE CHECKBOX ###
    
        revenue_view = st.checkbox('Show Revenue Data')
        
        mask_cntl_23 = df_cntl23_unt.loc[df_cntl23_unt['Product'] == control_selection][date_range]
        mask_cntl_24 = df_cntl24_unt.loc[df_cntl24_unt['Product'] == control_selection][date_range]
    
        
        cntl_idx = 0
        if control_selection == 'ShoStarter':
            cntl_idx += 1
        if control_selection == 'ShoMaster':
            cntl_idx += 2
            
        if year_select_prod == '2023':
            avg_per_month = {}
            mbd_display = st.checkbox('Display Monthly Breakdown')
            st.subheader(sum(mask_cntl_23.loc[cntl_idx][date_range]))
            if revenue_view == True and date_range == months_x:
                prod_rev_share, prod_rev, type_rev = multiyear_product_revenue([df_cntl23_rev])
                st.write(' - 2023 Revenue:  $' + '{:,.2f}'.format(prod_rev[control_selection]) + ' - ' + '{:,.2f}'.format(prod_rev_share[control_selection]) + '% of revenue from controllers')
                display_profit_data(df_cntl23_prof, control_selection)
    
    
            if mbd_display == True:
                for month in date_range:
                    avg_per_month[month] = mask_cntl_23.loc[cntl_idx][month]
                    st.write(month + ' - ' + str(mask_cntl_23.loc[cntl_idx][month]))
                st.write('( - Average per month: ' + str(avg_month(avg_per_month)) + ' - )')
                plot_bar_chart(format_for_chart(df_cntl23_unt.iloc[cntl_idx]))
    
            
        elif year_select_prod == '2024':
            avg_per_month = {}
            mbd_display_cntl = st.checkbox('Display Monthly Breakdown')
            st.subheader(sum(mask_cntl_24.loc[cntl_idx][date_range]))
            if revenue_view == True and date_range == months_x:
                prod_rev_share, prod_rev, type_rev = multiyear_product_revenue([df_cntl24_rev])
                st.write(' - 2024 Revenue:  $' + '{:,.2f}'.format(prod_rev[control_selection]) + ' - ' + '{:,.2f}'.format(prod_rev_share[control_selection]) + '% of revenue from controllers')
                display_profit_data(df_cntl24_prof, control_selection)
    
    
            if mbd_display_cntl == True:
                for month in date_range:
                    avg_per_month[month] = mask_cntl_24.loc[cntl_idx][month]
                    st.write(month + ' - ' + str(mask_cntl_24.loc[cntl_idx][month]))
                st.write('( - Average per month: ' + str(avg_month(avg_per_month)) + ' - )')
                plot_bar_chart(format_for_chart(df_cntl24_unt.iloc[cntl_idx]))
    
        
        else:
            st.subheader(sum(mask_cntl_23.loc[cntl_idx][date_range])+sum(mask_cntl_24.loc[cntl_idx][date_range]))
            if revenue_view == True and date_range == months_x:
                prod_rev_share, prod_rev, type_rev = multiyear_product_revenue([df_cntl23_rev, df_cntl24_rev])
                st.write(' - Total Revenue:  $' + '{:,.2f}'.format(prod_rev[control_selection]) + ' - ' + '{:,.2f}'.format(prod_rev_share[control_selection]) + '% of revenue from controllers')
    
    
            
    
        
    elif product_type_selection == 'Hoses':   
        
        hose_selection = st.multiselect('Hoses:',
                                      options=hoses,
                                      placeholder='Choose an Option')
            
        hose_sum = 0
        
        if len(hose_selection) < 1:
            pass
        else:
            if year_select_prod == '2023':
                for x in hose_selection:
    
                    mask_hose = df_h23_unt.loc[df_h23_unt['Product'] == x][date_range]
                    
                    for y in mask_hose:
                        hose_sum += int(mask_hose[y])
                        
            elif year_select_prod == '2024':
                for x in hose_selection:
                    
                    mask_hose = df_h24_unt.loc[df_h24_unt['Product'] == x][date_range]
                    
                    for y in mask_hose:
                        hose_sum += int(mask_hose[y])
                        
            else:
                for x in hose_selection:
                    
                    mask_hose_23 = df_h23_unt.loc[df_h23_unt['Product'] == x][date_range]
                    mask_hose_24 = df_h24_unt.loc[df_h24_unt['Product'] == x][date_range]
                    
                    for y in mask_hose_23:
                        hose_sum += int(mask_hose_23[y]) + int(mask_hose_24[y])
                        
                    
                
            st.subheader(hose_sum)
    
    
        
    elif product_type_selection == 'Accessories':
        
        acc_selection = st.selectbox('Accessories:',
                                      options=acc,
                                      placeholder='Choose an Option')
    
        
    
        mask_acc_23 = df_ac23_unt.loc[df_ac23_unt['Product'] == acc_selection][date_range]
        mask_acc_24 = df_ac24_unt.loc[df_ac24_unt['Product'] == acc_selection][date_range]
        
        ac_idx = 0
    
        ct_ac = 0
        
        for y in acc:
            if acc_selection == y:
                ac_idx = ct_ac
            else:
                ct_ac += 1
    
        if year_select_prod == '2023':
            avg_per_month = {}
            mbd_display_acc = st.checkbox('Display Monthly Breakdown')
            if mbd_display_acc == True:
                for month in date_range:
                    avg_per_month[month] = mask_acc_23.loc[ac_idx][month]
                    st.write(month + ' - ' + str(mask_acc_23.loc[ac_idx][month]))
                st.write('( - Average per month: ' + str(avg_month(avg_per_month)) + ' - )')
            st.subheader(sum(mask_acc_23.loc[ac_idx][date_range]))     
            
        elif year_select_prod == '2024':
            avg_per_month = {}
            mbd_display_acc = st.checkbox('Display Monthly Breakdown')
            if mbd_display_acc == True:
                for month in date_range:
                    avg_per_month[month] = mask_acc_24.loc[ac_idx][month]
                    st.write(month + ' - ' + str(mask_acc_24.loc[ac_idx][month]))
                st.write('( - Average per month: ' + str(avg_month(avg_per_month)) + ' - )')
            st.subheader(sum(mask_acc_24.loc[ac_idx][date_range]))
        
        else:
            st.subheader(sum(mask_acc_23.loc[ac_idx][date_range])+sum(mask_acc_24.loc[ac_idx][date_range]))
            
    elif product_type_selection == 'Handhelds':
    
        hh_selection = st.multiselect('Handhelds:',
                                      options=hh,
                                      placeholder='Choose an Option')
            
        hh_sum = 0
        
        if len(hh_selection) < 1:
            pass
        else:
            if year_select_prod == '2023':
                for x in hh_selection:
    
                    mask_hh = df_hh23_unt.loc[df_hh23_unt['Product'] == x][date_range]
                    
                    for y in mask_hh:
                        hh_sum += int(mask_hh[y])
                        
            elif year_select_prod == '2024':
                for x in hh_selection:
                    
                    mask_hh = df_hh24_unt.loc[df_hh24_unt['Product'] == x][date_range]
                    
                    for y in mask_hh:
                        hh_sum += int(mask_hh[y])
                        
            else:
                for x in hh_selection:
                    
                    mask_hh_23 = df_hh23_unt.loc[df_hh23_unt['Product'] == x][date_range]
                    mask_hh_24 = df_hh24_unt.loc[df_hh24_unt['Product'] == x][date_range]
                    
                    for y in mask_hh_23:
                        hh_sum += int(mask_hh_23[y]) + int(mask_hh_24[y])
                                      
                
            st.subheader(hh_sum)
            
    
    st.divider()


###################################################################### MONTHLY SALES REPORTS ##############################################################################

elif task_select == 'Monthly Sales':
    st.header('Monthly Sales')    
    mbd_display_sales = st.checkbox('Display Sales by Month')
    comp_display = st.checkbox('Show Comparison Column')
            
    ### REPLACE NULL VALUES WITH ZERO ###
        
    df_csv = df_csv.fillna(0)
    #st.write(df_csv)
    
    ### DEFINE A FUNCTION TO FORMAT MONTHLY SALES FOR CHART PLOTTING ###
    def format_for_chart_ms(dict):
        
        temp_dict = {'Months': months_x,
                    'Total Sales': []}
        
        for month, sales in dict.items():
            if len(temp_dict['Total Sales']) >= 12:
                pass
            else:
                temp_dict['Total Sales'].append(sales)
        df = pd.DataFrame(temp_dict)
        
        return df
    
    #st.write(format_for_chart(df_cntl23_unt.iloc[0]))
    
    
    ### SCRIPT TO PLOT BAR GRAPH FOR MONTHLY SALES ###
    
    def plot_bar_chart_ms(df):
        st.write(alt.Chart(df).mark_bar().encode(
            x=alt.X('Months', sort=None).title('Month'),
            y='Total Sales',
        ).properties(height=500, width=750).configure_mark(
            color='limegreen'
        ))
    
    def plot_bar_chart_ms_comp(df):
        st.write(alt.Chart(df).mark_bar().encode(
            x=alt.X('Months', sort=None).title('Month'),
            y='Total Sales',
        ).properties(height=500, width=350).configure_mark(
            color='limegreen'
        ))
    
    
    col1, col2 = st.columns(2)
    
    ### CREATE YEAR SELECTION ###
    with col1:
        year_select = st.selectbox('Select Year:',
                         placeholder='Select Year',
                         options=years)
    
    ### CREATE MONTHLY MULTISELECT ###
    
        month_range_sales = st.multiselect('Month Select:',
                                   placeholder='Select Months',
                                   options=months)
    
        #mbd_display_sales = st.checkbox('Display Sales by Month')
        
            
    ### CREATE LIST OF SELECTIONS ###
    
        df_csv_ts = df_csv.drop([1, 2, 4, 5, 7, 8])
        df_csv_ts = df_csv_ts.rename(index={0: '2022', 3: '2023', 6: '2024'})
        #st.write(df_csv_ts)
        #st.write(df_csv_ts['January'].iloc[2])
    
        idx_select = 0
        if year_select == '2023':
            idx_select += 1
        elif year_select == '2024':
            idx_select += 2
            
        s_tot = 0
    
        if month_range_sales == ['All']:
            month_range_sales = months_x
        avg_sales_per_month = {}
        for month in month_range_sales:
            try:
                avg_sales_per_month[month] = float(df_csv_ts[month].iloc[idx_select].strip('$'))
                #st.write(float(df_csv_ts[month].iloc[idx_select].strip('$')))
            except:
                avg_sales_per_month[month] = 0.0
            if df_csv_ts.at[year_select, month] == 0:
                pass
            else:
                if mbd_display_sales == True:
                    st.write(month + ' - ' + '$' + '{:,.2f}'.format(float(df_csv_ts.at[year_select, month].strip('$'))))
                    
                s_tot += float(df_csv_ts.at[year_select, month].strip('$'))
        if len(month_range_sales) >= 1:
            s_tot_st = '{:,.2f}'.format(s_tot)
            if len(month_range_sales) > 1:
                st.write('( - Average per month: ' + '$' + '{:,.2f}'.format(avg_month(avg_sales_per_month)) + ' - )')
            st.subheader('$' + s_tot_st)
            
            
            if month_range_sales == months_x:
                sales_per_month = format_for_chart_ms(avg_sales_per_month)
                if comp_display == False:
                    plot_bar_chart_ms(sales_per_month)
                else:
                    plot_bar_chart_ms_comp(sales_per_month)
    
        #s_tot_st = '{:,.2f}'.format(s_tot)
        
        #st.subheader('$' + s_tot_st)
        
    if comp_display == True:
        with col2:
        ### DUPLICATE SALES REPORTER FOR COMPARISON ###
        
            year_select_x = st.selectbox('Select Years:',
                             placeholder='Select Year',
                             options=years)
        
        ### CREATE MONTHLY MULTISELECT
        
            month_range_sales_x = st.multiselect('Month Selection:',
                                       placeholder='Select Months',
                                       options=months)
        
            #mbd_display_sales_x = st.checkbox('Display Sales by Months')
            
                
        ### CREATE LIST OF SELECTIONS ###
        
            df_csv_ts = df_csv.drop([1, 2, 4, 5, 7, 8])
            df_csv_ts = df_csv_ts.rename(index={0: '2022', 3: '2023', 6: '2024'})
        
            idx_select = 0
            if year_select_x == '2023':
                idx_select += 1
            elif year_select_x == '2024':
                idx_select += 2
                
            s_tot = 0
        
            if month_range_sales_x == ['All']:
                month_range_sales_x = months_x
            avg_sales_per_month = {}
            for month in month_range_sales_x:
                try:
                    avg_sales_per_month[month] = float(df_csv_ts[month].iloc[idx_select].strip('$'))
                    #st.write(float(df_csv_ts[month].iloc[idx_select].strip('$')))
                except:
                    avg_sales_per_month[month] = 0.0
    
                if df_csv_ts.at[year_select_x, month] == 0:
                    pass
                else:
                    if mbd_display_sales == True:
                        st.write(month + ' - ' + '$' + '{:,.2f}'.format(float(df_csv_ts.at[year_select_x, month].strip('$'))))
                    s_tot += float(df_csv_ts.at[year_select_x, month].strip('$'))
            
            if len(month_range_sales_x) >= 1:
                
                s_tot_st = '{:,.2f}'.format(s_tot)
                if len(month_range_sales_x) > 1:
                    st.write('( - Average per month: ' + '$' + '{:,.2f}'.format(avg_month(avg_sales_per_month)) + ' - )')
                st.subheader('$' + s_tot_st)
                if month_range_sales_x == months_x:
                    sales_per_month = format_for_chart_ms(avg_sales_per_month)
                    plot_bar_chart_ms_comp(sales_per_month)
                    
        

    

######################################################### CUSTOMER SPEND RANKINGS #######################################################################

### DEFINE A FUNCTION TO MAKE A LIST OF TUPLES OF A CUSTOMER AND THEIR SPENDING, LIMIT TO TOP 20 ###

    
def sort_top_20(dict, number):

    leaderboard_list = []
    
    for key, value in dict.items():
        if value >= 2500:
            leaderboard_list.append((key, value))
    

    sorted_leaderboard = sorted(leaderboard_list, key=itemgetter(1), reverse=True)

    return sorted_leaderboard[:number]


if task_select == 'Customer Spending Leaders':
    st.header('Customer Spending Leaderboards')
    
    spend_year = st.selectbox('Choose Year', 
                             ['2023', '2024'])
    
    ranking_number = st.selectbox('Choose Leaderboard Length',
                                 [5, 10, 15, 20, 25, 50])
    
    cust_spend_dict_2023 = {}
    cust_spend_dict_2024 = {}
    
    
    for cust in unique_customer_list:
        cust_spend_dict_2023[cust] = 0
        cust_spend_dict_2024[cust] = 0
        
    idx = 0
    
    for customer in df.customer:
        #st.write(df.iloc[idx].total_line_item_spend)
        if df.iloc[idx].ordered_year == '2023':
            cust_spend_dict_2023[customer] += float(df.iloc[idx].total_line_item_spend)
        elif df.iloc[idx].ordered_year == '2024':
            cust_spend_dict_2024[customer] += float(df.iloc[idx].total_line_item_spend)
        idx += 1
        
    rank = 1
    if spend_year == '2023':

        result = sort_top_20(cust_spend_dict_2023, ranking_number)
        for leader in result:
            st.subheader(str(rank) + ')  ' + leader[0] + ' : $' + '{:,.2f}'.format(leader[1]))
            
            rank += 1
            
    elif spend_year == '2024':
        
        result = sort_top_20(cust_spend_dict_2024, ranking_number)
        for leader in result:
            st.subheader(str(rank) + ')  ' + leader[0] + ' : $' + '{:,.2f}'.format(leader[1]))
        
            rank += 1
    
    
    
  













