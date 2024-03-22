import pymongo
import pandas as pd
import streamlit as st
from pymongo import MongoClient



MONTHS_ORDER = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# ------------------------------- APP CONFIGURATION -------------------------------
def setup_app():
    st.set_page_config(page_title="Aitionics", page_icon="📊", layout="wide")
    with open("css/style.css") as css:
        st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)

    st.markdown(
        """
        <style>
            [data-testid=stHeader] {
                display:none;
            }
            [data-testid=block-container] {
                padding-top: 0px;
                # background:#eff0d1;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <style>
        [data-testid=stSidebarUserContent]{
            margin-top: -75px;
            margin-top: -75px;
            fontsize=100px;
            }
            .logo{
                font-size:3rem !important;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    with st.sidebar:
        # st.image("./assets/logo.png", width=200)
        st.markdown('<p class="logo">Aitionics</p>', unsafe_allow_html=True)


# ------------------------------- AUTHENTICATION -------------------------------
def get_mongo_collections():
    """Retrieve necessary collections from MongoDB."""
    client = MongoClient(st.secrets["mongo"]["con_string"])
    db = client[st.secrets["mongo"]["db"]]
    return db[st.secrets["mongo"]["users"]], db[st.secrets["mongo"]["delta"]], db[st.secrets["mongo"]["auth_user"]]

def initialize_session_state():
    """Initialize the session state."""
    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = None

def authenticate_user(username, password):
    """Check if the user credentials are valid."""
    if username and password:
        _, _, auth_user_collection = get_mongo_collections()
        user_record = auth_user_collection.find_one({"name": username})

        # If a user with the provided username exists and the password matches, return True
        if user_record and user_record.get("password") == password:
            return True

    return False

def authenticate():
    """Authenticate the user."""
    with st.sidebar:
        if not st.session_state['authenticated']:
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            if st.button("Login"):
                st.session_state['authenticated'] = authenticate_user(username, password)
                st.rerun()
        else:
            if st.button("Logout"):
                logout_user()

def logout_user():
    """Logout the user."""
    st.session_state['authenticated'] = None
    st.rerun()


# ------------------------------- DATA RETRIEVAL -------------------------------

def collection_hasher(collection):
    """Custom hash function for MongoDB collection objects."""
    return hash(collection.full_name)   # Use the collection's full name as a unique identifier

@st.cache_resource(hash_funcs={pymongo.collection.Collection: collection_hasher})
def fetch_data(collection):
    """Fetch data from MongoDB, caching the result to enhance performance."""
    return pd.DataFrame(list(collection.find())).drop(columns=["_id"])


# ------------------------------- DATA PROCESSING -------------------------------
def format_currency_label(value: float) -> str:
    """Formats large numbers into a readable currency format."""
    if value >= 1e9:
        return f'{value / 1e9:.2f}B'
    elif value >= 1e6:
        return f'{value / 1e6:.2f}M'
    elif value >= 1e3:
        return f'{value / 1e3:.2f}K'
    return f'{value:.2f}'


# ------------------------------- PLOTLY CONFIGURATION -------------------------------
def update_hover_layout(fig):
    """Updates the hover layout for Plotly figures."""
    fig.update_layout(
        {
            "paper_bgcolor": "rgba(0,0,0,0)",
            "plot_bgcolor": "rgba(0,0,0,0)",
        },
        hovermode = "x unified",
        hoverlabel = {
            "bgcolor": "white",
            "font_size": 16,
            "font_family": "Rockwell"
        },
        height = 400
    )
    return fig


# ------------------------------- OVERVIEW PAGE -------------------------------
def get_notification_filters(df, delta_df):
    """Filter the data based on the selected year and month."""
    selected_year = st.sidebar.selectbox(label="Year", options=df["YEAR"].unique(), placeholder="Select Year")
    if selected_year - 1 >= min(df["YEAR"].unique()):
        df_year_1 = df[df["YEAR"] == selected_year - 1]
        df_year_2 = df[df["YEAR"] == selected_year]
    else:
        st.warning("Please select a valid year.")
        st.stop()

    month_to_num = {m: i for i, m in enumerate(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], 1)}
    selected_month = st.sidebar.multiselect(label="Month", options=df["MONTH"].unique(), default=df["MONTH"].unique()[0])
    months_in_year_2 = df_year_2["MONTH"].unique()
    if len(selected_month) == 0:
        st.warning("Please select at least one month.")
        st.stop()
    elif all(item in months_in_year_2 for item in selected_month):
        selected_month_num = [month_to_num[month] for month in selected_month]
        df_year_1 = df_year_1[df_year_1['MONTH'].map(month_to_num).isin(selected_month_num)]
        df_year_2 = df_year_2[df_year_2['MONTH'].map(month_to_num).isin(selected_month_num)]
        delta_df = delta_df[delta_df['MONTH'].map(month_to_num).isin(selected_month_num)]
    else:
        st.warning("Please select a valid month.")
        st.stop()

    return df_year_1, df_year_2, delta_df

def get_notification_revenue_growth(df_1, df_2):
    """Calculate the revenue growth."""
    revenue_year_1 = df_1.groupby('Channel Category')['Revenue'].sum().reset_index()
    revenue_year_2 = df_2.groupby('Channel Category')['Revenue'].sum().reset_index()

    revenue_comparison = pd.merge(revenue_year_1, revenue_year_2, on='Channel Category', suffixes=('_2022', '_2023'))
    revenue_comparison['YTD Revenue Growth'] = ((revenue_comparison['Revenue_2023'] - revenue_comparison['Revenue_2022']) / revenue_comparison['Revenue_2022']) * 100

    overall_growth = ((revenue_comparison['Revenue_2023'].sum() - revenue_comparison['Revenue_2022'].sum()) / revenue_comparison['Revenue_2022'].sum()) * 100
    max_growth_channel = revenue_comparison.loc[revenue_comparison['YTD Revenue Growth'].idxmax()]
    min_growth_channel = revenue_comparison.loc[revenue_comparison['YTD Revenue Growth'].idxmin()]

    return overall_growth, max_growth_channel, min_growth_channel

def highlight_extremes(row, col, pivot_table):
    """
    Highlight the maximum value in green and the minimum value in red in a Series.
    """
    if row[col] == pivot_table[col].min():
        color = 'background-color: red; color: white'
    elif row[col] == pivot_table[col].max():
        color = 'background-color: green; color: white'
    else:
        color = 'color: black'
    return [color]*len(row)

def get_notification_delta(df, category):
    """
    Calculate the overall Delta Price and Delta Volume, then generate insights including highest and lowest records.
    A pivot table with highlighted max (green) and min (red) values for specified categories is also returned.
    """
    pivot_table = pd.pivot_table(
        df,
        index=['MONTH','Channel Category', 'Channel Sub-Category', 'Customer Name'],
        values=['Delta Price [CAD]', 'Delta Volume [CAD]', 'Delta Price %', 'Delta Volume %'],
        aggfunc={'Delta Price [CAD]': 'sum', 'Delta Volume [CAD]': 'sum', 'Delta Price %': 'mean', 'Delta Volume %': 'mean'}
    ).reset_index(drop=False)

    insights = {
        'overall_delta_pct': pivot_table[category].mean(),
        'highest_delta_pct': pivot_table.loc[pivot_table[category].idxmax(), category],
        'lowest_delta_pct': pivot_table.loc[pivot_table[category].idxmin(), category],
    }

    highest_record = pivot_table.loc[pivot_table[category].idxmax()]
    lowest_record = pivot_table.loc[pivot_table[category].idxmin()]

    insights.update({
        'highest_channel': highest_record['Channel Category'],
        'highest_sub_channel': highest_record['Channel Sub-Category'],
        'highest_customer': highest_record['Customer Name'],
        'lowest_channel': lowest_record['Channel Category'],
        'lowest_sub_channel': lowest_record['Channel Sub-Category'],
        'lowest_customer': lowest_record['Customer Name'],
    })

    insights['pivot_table'] = pivot_table.style.apply(lambda row: highlight_extremes(row, category, pivot_table), axis=1)
    return insights


# ------------------------------- PRICE ANALYSIS PAGE -------------------------------
def get_price_filters(df):
    """Filter the price data based on the selected filters."""
    year = st.sidebar.selectbox(label="Year", options=df["YEAR"].unique())
    df_filtered = df[df["YEAR"] == year]

    months = st.sidebar.multiselect(label="Month", options=df_filtered["MONTH"].unique(), placeholder="All")
    if months: df_filtered = df_filtered[df_filtered["MONTH"].isin(months)]

    category = st.sidebar.selectbox(label="Product Category", options=df_filtered["Product Category"].unique())
    df_filtered = df_filtered[df_filtered["Product Category"] == category]

    family = st.sidebar.selectbox(label="Product Family", options=df_filtered["Product Family"].unique())
    df_filtered = df_filtered[df_filtered["Product Family"] == family]

    product_range = st.sidebar.selectbox(label="Product Range", options=df_filtered["Product Range"].unique())
    df_filtered = df_filtered[df_filtered["Product Range"] == product_range]

    product_description = st.sidebar.selectbox(label="Product Description", options=df_filtered["Product Description"].unique())
    df_filtered = df_filtered[df_filtered["Product Description"] == product_description]

    return df_filtered


# ------------------------------- CUSTOMER INSIGHTS PAGE -------------------------------
def get_customer_filters(df):
    """Filter the customer data based on the selected filters."""
    year = st.sidebar.selectbox(label="Year", options=df["YEAR"].unique())
    df_filtered = df[df["YEAR"] == year]

    months = st.sidebar.multiselect(label="Month", options=df_filtered["MONTH"].unique(), placeholder="All")
    if months: df_filtered = df_filtered[df_filtered["MONTH"].isin(months)]

    cust_name = st.sidebar.multiselect(label="Customer Name", options=df_filtered["Customer Name"].unique(), placeholder="All", default=df_filtered["Customer Name"].unique()[:5])
    if cust_name: df_filtered = df_filtered[df_filtered["Customer Name"].isin(cust_name)]

    family = st.sidebar.selectbox(label="Product Family", options=df_filtered["Product Family"].unique(), placeholder="All")
    if family: df_filtered = df_filtered[df_filtered["Product Family"] == family]

    product_range = st.sidebar.multiselect(label="Product Range", options=df_filtered["Product Range"].unique())
    if product_range: df_filtered = df_filtered[df_filtered["Product Range"].isin(product_range)]

    channel = st.sidebar.selectbox(label="Channel", options=df_filtered["Channel Category"].unique())
    df_filtered = df_filtered[df_filtered["Channel Category"] == channel]

    return df_filtered


# ------------------------------- PRODUCT PERFORMANCE PAGE -------------------------------
def get_product_filters(df):
    """Filter the product data based on the selected filters."""
    year = st.sidebar.selectbox(label="Year", options=df["YEAR"].unique())
    df_filtered = df[df["YEAR"] == year]

    category = st.sidebar.selectbox(label="Product Category", options=df_filtered["Product Category"].unique())
    df_filtered = df_filtered[df_filtered["Product Category"] == category]

    family = st.sidebar.selectbox(label="Product Family", options=df_filtered["Product Family"].unique())
    df_filtered = df_filtered[df_filtered["Product Family"] == family]

    product_range = st.sidebar.selectbox(label="Product Range", options=df_filtered["Product Range"].unique())
    df_filtered = df_filtered[df_filtered["Product Range"] == product_range]

    product_description = st.sidebar.selectbox(label="Product Description", options=df_filtered["Product Description"].unique())
    df_filtered = df_filtered[df_filtered["Product Description"] == product_description]

    return df_filtered


# ------------------------------- SUMMARY PAGE -------------------------------
def get_summary_filters(df):
    """Filter the delta data based on the selected filters."""
    category = st.sidebar.multiselect(label="Product Category", options=df["Product Category"].unique(), placeholder="All")
    if category: df = df[df["Product Category"].isin(category)]

    family = st.sidebar.multiselect(label="Product Family", options=df["Product Family"].unique(), placeholder="All")
    if family: df = df[df["Product Family"].isin(family)]

    product_range = st.sidebar.multiselect(label="Product Range", options=df["Product Range"].unique(), placeholder="All")
    if product_range: df = df[df["Product Range"].isin(product_range)]

    ch_category = st.sidebar.multiselect(label="Channel Category", options=df["Channel Category"].unique(), placeholder="All")
    if ch_category: df = df[df["Channel Category"].isin(ch_category)]

    ch_sub_category = st.sidebar.multiselect(label="Channel Sub-Category", options=df["Channel Sub-Category"].unique(), placeholder="All")
    if ch_sub_category: df = df[df["Channel Sub-Category"].isin(ch_sub_category)]

    cust_name = st.sidebar.multiselect(label="Customer Name", options=df["Customer Name"].unique(), placeholder="All")
    if cust_name: df = df[df["Customer Name"].isin(cust_name)]

    return df
