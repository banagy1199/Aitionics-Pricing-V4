import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from utils import *



# colors = ["#880d1e", "#f26a8d", "#dd2d4a", "#f49cbb", "#cbeef3", "#880d1e"]
COLOR_PALETTE = colors = ["#2a9d8f", "#264653", "#e9c46a", "#f4a261", "#e76f51", "#ef233c", "#f6bd60", "#84a59d", "#f95738"]


def create_card_figure(title, value, value_prefix="", value_suffix="", height=250):
    """Generalized function to create card figures with Plotly."""
    fig = go.Figure(go.Indicator(
        mode="number",
        value=value,
        number={"prefix": value_prefix, "suffix": value_suffix, "font": {"size": 20}},
        title={"text": title, "font": {"size": 20}},
        domain={'y': [0, 1], 'x': [0.25, 0.75]}
    ))
    fig.update_layout(height=height)
    return fig

def create_time_series_figure(df, x_col, y_col, title, mode="lines", fill='tozeroy', height=250):
    """Generalized function to create time-series figures with Plotly."""
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df[x_col],
        y=df[y_col],
        mode=mode,
        fill=fill,
        name=title,
    ))
    fig.update_xaxes(showticklabels=False, showgrid=False)
    fig.update_yaxes(showticklabels=False, showgrid=False)
    fig = update_hover_layout(fig)
    fig.update_layout(height=height, title_text=title)
    return fig

def create_pie_chart(labels, values, title, name, hole=0.4):
    """Generalized function to create pie charts with Plotly."""
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=hole, title=name, name=name, marker_colors=COLOR_PALETTE)])
    fig.update_layout(title_text=title) #, annotations=[dict(text=title, x=0.5, y=0.5, font_size=15, showarrow=False)])
    fig = update_hover_layout(fig)
    return fig

def create_bar_chart(df, x, y, title, color=None, barmode='group'):
    """Generalized function to create bar charts with Plotly."""
    if color:
        fig = px.bar(df, x=x, y=y, title=title, color=color, barmode=barmode, color_discrete_sequence=COLOR_PALETTE)
    else:
        fig = px.bar(df, x=x, y=y, title=title, color_discrete_sequence=[COLOR_PALETTE[0]])
    fig = update_hover_layout(fig)
    return fig

def create_line_chart(df, x, y, title, color="blue", height=250):
    """Generalized function to create line charts with Plotly."""
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df[x], y=df[y], mode='lines+markers', line=dict(color=color)))
    fig.update_layout(title_text=title, height=height)
    fig = update_hover_layout(fig)
    return fig

def create_scatter_chart(df, x, y, title, color="red", size=None, height=250):
    """Generalized function to create scatter charts with Plotly."""
    fig = px.scatter(df, x=x, y=y, color=color, size=size, title=title, color_continuous_scale=px.colors.sequential.Viridis)
    fig.update_layout(height=height)
    fig = update_hover_layout(fig)
    return fig

def create_indicator_card(df, metric, title, prefix="", suffix="", height=250):
    """Creates an indicator card showing a single key metric."""
    value = df[metric].mean() if metric in df.columns else 0
    fig = go.Figure(go.Indicator(
        mode="number",
        value=value,
        number={'prefix': prefix, 'suffix': suffix},
        title={'text': title},
        domain={'x': [0.25, 0.75], 'y': [0.2, 0.9]}
    ))
    fig.update_layout(height=height)
    return fig

def sales_revenue_card(df):
    """Generates a card displaying total sales revenue over time."""
    sales_by_month = df.groupby("MONTH")["Revenue"].sum().reindex(MONTHS_ORDER).reset_index()
    total_revenue = sales_by_month["Revenue"].sum()
    fig = create_card_figure("Total Sales Revenue", total_revenue, value_prefix="$")
    fig = create_time_series_figure(sales_by_month, "MONTH", "Revenue", "Total Revenue")
    return fig

def list_price_sales_card(df):
    """Generates a card displaying average list price over time."""
    sales_by_month = df.groupby("MONTH")["List Price [CAD]"].mean().reindex(MONTHS_ORDER).reset_index()
    avg_list_price = sales_by_month["List Price [CAD]"].mean()
    fig = create_card_figure("List Price Avg", avg_list_price, value_prefix="$")
    fig = create_time_series_figure(sales_by_month, "MONTH", "List Price [CAD]", "Avg List Price")
    return fig

def net_sales_card(df):
    """Generates a card displaying average net sales over time."""
    sales_by_month = df.groupby("MONTH")["Net Price [CAD]"].mean().reindex(MONTHS_ORDER).reset_index()
    avg_net_sales = sales_by_month["Net Price [CAD]"].mean()
    fig = create_card_figure("Net Sales", avg_net_sales, value_prefix="$")
    fig = create_time_series_figure(sales_by_month, "MONTH", "Net Price [CAD]", "Net Sales")
    return fig

def units_sold_card(df):
    """Generates a card displaying total units sold over time."""
    qty_sold = df.groupby("MONTH")["QTY [Units]"].sum().reindex(MONTHS_ORDER).reset_index()
    total_units = qty_sold["QTY [Units]"].sum()
    fig = create_card_figure("Total Units Sold", total_units, value_suffix=" units")
    fig = create_time_series_figure(qty_sold, "MONTH", "QTY [Units]", "Qty Sold")
    return fig

def profit_margin_card(df):
    """Generates a card displaying profit margin over time."""
    monthly_financials = df.groupby("MONTH").agg({"Revenue": "sum", "Total GM [CAD]": "sum"})
    monthly_financials['Profit Margin'] = (monthly_financials['Total GM [CAD]'] / monthly_financials['Revenue']) * 100
    overall_profit_margin = (monthly_financials['Total GM [CAD]'].sum() / monthly_financials['Revenue'].sum()) * 100
    fig = create_card_figure("Profit Margin", overall_profit_margin, value_suffix="%")
    fig = create_time_series_figure(monthly_financials.reset_index(), "MONTH", "Profit Margin", "Profit Margin")
    return fig

def average_discount_rate_card(df):
    """Generates a card displaying average discount rate over time."""
    df = calculate_weighted_discounts(df)
    monthly_discounts = calculate_monthly_discounts(df)
    overall_avg_discount_rate = calculate_overall_avg_discount_rate(monthly_discounts)
    fig = create_card_figure("Average Discount Rate", overall_avg_discount_rate * 100, value_suffix="%")
    fig = create_time_series_figure(monthly_discounts, "MONTH", "Avg Discount Rate", "Avg Discount Rate", mode="lines", fill='tozeroy')
    return fig

def average_selling_price_card(df):
    """Generates a card and time series showing average selling price over time."""
    monthly_sales = df.groupby("MONTH").agg({"Revenue": "sum", "QTY [Units]": "sum"}).reset_index()
    monthly_sales['ASP'] = monthly_sales['Revenue'] / monthly_sales['QTY [Units]']
    overall_asp = monthly_sales['ASP'].mean()
    fig = create_card_figure("Average Selling Price", overall_asp, value_prefix="$")
    fig = create_time_series_figure(monthly_sales, "MONTH", "ASP", "Average Selling Price")
    return fig

def income_statement(df):
    """Generates an income statement bar chart."""
    financial_data = df.groupby("MONTH")[['Total Expense', 'CoGS', 'Revenue', 'Net Profit']].sum().reindex(MONTHS_ORDER).reset_index()
    fig = go.Figure()
    for index, col in enumerate(['Total Expense', 'CoGS', 'Revenue', 'Net Profit']):
        fig.add_trace(go.Bar(
            x=financial_data["MONTH"],
            y=financial_data[col],
            name=col,
            marker=dict(color=COLOR_PALETTE[index])
        ))
    fig.update_layout(
        barmode="group",
        title="Income Statement",
        xaxis_title="Month",
        yaxis_title="Amount",
        height=450
    )
    fig = update_hover_layout(fig)
    fig.update_xaxes(type='category')
    return fig

def expenses_pie(df):
    """Generates a pie chart for expenses analysis."""
    summed_discounts = df[['Standard Discount [SD1][CAD]', 'Standard Discount [SD2][CAD]',
                           'Special Discount [DSP][CAD]', 'Promo Campaign [DPR][CAD]',
                           'Rebates [DREB][CAD]']].sum()
    fig = go.Figure(data=[go.Pie(labels=summed_discounts.index, values=summed_discounts.values, hole=.4, marker_colors=COLOR_PALETTE)])
    fig.update_layout(title_text='Discounts and Promos Analysis', annotations=[dict(text='Expenses', x=0.5, y=0.5, font_size=15, showarrow=False)])
    fig = update_hover_layout(fig)
    return fig


def monthly_rev_gm(df):
    data = df.groupby("MONTH").agg({"Revenue": "sum", "Total GM [CAD]": "sum"}).reindex(MONTHS_ORDER).reset_index()
    fig = make_subplots()
    fig.add_trace(go.Scatter(x=data["MONTH"], y=data["Revenue"], name="Revenue", mode="lines+markers+text", marker=dict(color=COLOR_PALETTE[0]), line=dict(color=COLOR_PALETTE[0])))
    fig.add_trace(go.Scatter(x=data["MONTH"], y=data["Total GM [CAD]"], name="Profit Margin", mode="lines+markers", marker=dict(color=COLOR_PALETTE[-1]), line=dict(color=COLOR_PALETTE[-1])))
    fig.update_layout(title="Revenue and Gross Margin Over Time", xaxis_title="Month", yaxis_title="Amount")
    fig = update_hover_layout(fig)
    return fig

def product_performance(df):
    """Generates a bar chart showing product performance."""
    data = df.groupby("Product Range").agg({"QTY [Units]": "sum", "Unit GM [%]": "mean"}).reset_index().sort_values(by="QTY [Units]", ascending=False)
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(x=data["Product Range"], y=data["QTY [Units]"], name="Quantity Sold", marker=dict(color=COLOR_PALETTE[0])), secondary_y=False)
    fig.add_trace(go.Scatter(x=data["Product Range"], y=data["Unit GM [%]"], name="Profit Margin Contribution", mode="markers+lines", marker=dict(color=COLOR_PALETTE[1])), secondary_y=True)
    fig.update_layout(title="Product Selling Performance", xaxis_title="Product Range", yaxis_title="Units")
    fig = update_hover_layout(fig)
    return fig

def customer_distribution(df):
    """Generates a pie chart showing customer distribution of revenue."""
    data = df.groupby('Customer Name')['Revenue'].sum().reset_index()
    fig = create_pie_chart(data['Customer Name'], data['Revenue'], 'Customer Distribution of Revenue', 'Revenue')
    return fig

def channel_distribution(df):
    """Generates a pie chart showing channel distribution of quantity sold."""
    data = df.groupby('Channel Category')['QTY [Units]'].sum().reset_index()
    fig = create_pie_chart(data['Channel Category'], data['QTY [Units]'], 'Channel Distribution of Quantity Sold', 'Quantity Sold')
    return fig

def average_list_price_card(df):
    monthly_sales = df.groupby("MONTH")["List Price [CAD]"].mean()
    monthly_sales = monthly_sales.reindex(MONTHS_ORDER).reset_index()
    fig = go.Figure(
        go.Indicator(
            mode="number",
            value=df["List Price [CAD]"].mean(),
            number={"prefix": "C$", "font": {"size": 32}},
            title={"text": "Average List Price", "font": {"size": 20}},
            domain={'y': [0, 1], 'x': [0.25, 0.75]}
        ))
    fig.add_trace(go.Scatter(
        x=monthly_sales["MONTH"],
        y=monthly_sales["List Price [CAD]"],
        mode="lines",
        fill='tozeroy',
        name="Avg. List Price",
    ))

    fig.update_xaxes(showticklabels=False, showgrid=False)
    fig.update_yaxes(showticklabels=False, showgrid=False)
    fig = update_hover_layout(fig)
    fig.update_layout(height=250)

    return fig


def total_prod_qty_card(df):
    monthly_sales = df.groupby("MONTH")["QTY [Units]"].sum()
    monthly_sales = monthly_sales.reindex(MONTHS_ORDER).reset_index()
    fig = go.Figure(
        go.Indicator(
            mode="number",
            value=df["QTY [Units]"].sum(),
            number={"suffix": " units", "font": {"size": 32}},
            title={"text": "Qty Sold", "font": {"size": 20}},
            domain={'y': [0, 1], 'x': [0.25, 0.75]}
        ))
    fig.add_trace(go.Scatter(
        x=monthly_sales["MONTH"],
        y=monthly_sales["QTY [Units]"],
        mode="lines",
        fill='tozeroy',
        name="Qty Sold",
    ))

    fig.update_xaxes(showticklabels=False, showgrid=False)
    fig.update_yaxes(showticklabels=False, showgrid=False)
    fig = update_hover_layout(fig)
    fig.update_layout(height=250)

    return fig


def total_prod_rev_card(df):
    monthly_sales = df.groupby("MONTH")["Revenue"].sum()
    monthly_sales = monthly_sales.reindex(MONTHS_ORDER).reset_index()
    fig = go.Figure(
        go.Indicator(
            mode="number",
            value=df["Revenue"].sum(),
            number={"prefix": "C$ ", "font": {"size": 32}},
            title={"text": "Total Revenue", "font": {"size": 20}},
            domain={'y': [0, 1], 'x': [0.25, 0.75]}
        ))
    fig.add_trace(go.Scatter(
        x=monthly_sales["MONTH"],
        y=monthly_sales["Revenue"],
        mode="lines",
        fill='tozeroy',
        name="Total Revenue",
    ))

    fig.update_xaxes(showticklabels=False, showgrid=False)
    fig.update_yaxes(showticklabels=False, showgrid=False)
    fig = update_hover_layout(fig)
    fig.update_layout(height=250)

    return fig


def total_prod_GM_card(df):
    monthly_sales = df.groupby("MONTH")["Total GM [CAD]"].sum()
    monthly_sales = monthly_sales.reindex(MONTHS_ORDER).reset_index()
    fig = go.Figure(
        go.Indicator(
            mode="number",
            value=df["Total GM [CAD]"].sum(),
            number={"prefix": "C$ ", "font": {"size": 32}},
            title={"text": "Profit Margin", "font": {"size": 20}},
            domain={'y': [0, 1], 'x': [0.25, 0.75]}
        ))
    fig.add_trace(go.Scatter(
        x=monthly_sales["MONTH"],
        y=monthly_sales["Total GM [CAD]"],
        mode="lines",
        fill='tozeroy',
        name="Total Gross Margin",
    ))

    fig.update_xaxes(showticklabels=False, showgrid=False)
    fig.update_yaxes(showticklabels=False, showgrid=False)
    fig = update_hover_layout(fig)
    fig.update_layout(height=250)

    return fig


def summary_rev_sum_card(df):
    fig = go.Figure(
        go.Indicator(
            mode="number",
            value=df["Revenue_2022"].sum() + df["Revenue_2023"].sum(),
            number={"prefix": "C$", "font": {"size": 32}},
            title={"text": "Sum of Revenue", "font": {"size": 20}},
            domain={'y': [0, 1], 'x': [0.25, 0.75]}
        ))

    fig.update_xaxes(showticklabels=False, showgrid=False)
    fig.update_yaxes(showticklabels=False, showgrid=False)
    fig = update_hover_layout(fig)
    fig.update_layout(height=250)

    return fig


def summary_delta_price_sum_card(df):
    fig = go.Figure(
        go.Indicator(
            mode="number",
            value=df["Delta Price [CAD]"].sum(),
            number={"prefix": "C$", "font": {"size": 32}},
            title={"text": "Sum of Delta Price", "font": {"size": 20}},
            domain={'y': [0, 1], 'x': [0.25, 0.75]}
        ))

    fig.update_xaxes(showticklabels=False, showgrid=False)
    fig.update_yaxes(showticklabels=False, showgrid=False)
    fig = update_hover_layout(fig)
    fig.update_layout(height=250)

    return fig


def summary_delta_volume_sum_card(df):
    fig = go.Figure(
        go.Indicator(
            mode="number",
            value=df["Delta Volume [CAD]"].sum(),
            number={"prefix": "C$", "font": {"size": 32}},
            title={"text": "Sum of Delta Volume", "font": {"size": 20}},
            domain={'y': [0, 1], 'x': [0.25, 0.75]}
        ))

    fig.update_xaxes(showticklabels=False, showgrid=False)
    fig.update_yaxes(showticklabels=False, showgrid=False)
    fig = update_hover_layout(fig)
    fig.update_layout(height=250)

    return fig


def summary_delta_volume_perct_card(df):
    df = df[df['Revenue_2023'] > 0]

    fig = go.Figure(
        go.Indicator(
            mode="number",
            value=df["Delta Volume [CAD]"].sum() / df["Revenue_2022"].sum() * 100,
            number={"suffix": " %", "font": {"size": 32}},
            title={"text": "Sum of Delta Volume%", "font": {"size": 20}},
            domain={'y': [0, 1], 'x': [0.25, 0.75]}
        ))

    fig.update_xaxes(showticklabels=False, showgrid=False)
    fig.update_yaxes(showticklabels=False, showgrid=False)
    fig = update_hover_layout(fig)
    fig.update_layout(height=250)

    return fig


def summary_delta_price_perct_card(df):
    df = df[df['Revenue_2023'] > 0]

    fig = go.Figure(
        go.Indicator(
            mode="number",
            value=df["Delta Price [CAD]"].sum() / df["Revenue_2022"].sum() * 100,
            number={"suffix": " %", "font": {"size": 32}},
            title={"text": "Sum of Delta Price%", "font": {"size": 20}},
            domain={'y': [0, 1], 'x': [0.25, 0.75]}
        ))

    fig.update_xaxes(showticklabels=False, showgrid=False)
    fig.update_yaxes(showticklabels=False, showgrid=False)
    fig = update_hover_layout(fig)
    fig.update_layout(height=250)

    return fig


def delta_qty_wrt_channel_category(df):
    melted_df = df.groupby("Channel Category")[['Delta Price %', 'Delta Volume %']].mean().reset_index()
    fig = go.Figure()
    ind = 0
    for cat in ['Delta Price %', 'Delta Volume %']:
        fig.add_trace(go.Bar(
            x=melted_df["Channel Category"], y=melted_df[cat], name=cat,
            textposition="inside", marker=dict(color=colors[ind]),
            text=round(melted_df[cat], 2).astype(str) + '%'
        ))
        ind += 1
    fig = update_hover_layout(fig)
    fig.update_layout(title="YTD Delta Price and Delta Volume",
                      xaxis_title="Channel Category", yaxis_title="%age")
    return fig


def delta_qty_wrt_product_category(df):
    melted_df = df.groupby("Product Category")[['Delta Price %', 'Delta Volume %']].mean().reset_index()
    fig = go.Figure()
    ind = 0
    for cat in ['Delta Price %', 'Delta Volume %']:
        fig.add_trace(go.Bar(
            x=melted_df["Product Category"], y=melted_df[cat], name=cat,
            textposition="inside", marker=dict(color=colors[ind]),
            text=round(melted_df[cat], 2).astype(str) + '%'
        ))
        ind += 1
    fig = update_hover_layout(fig)
    fig.update_layout(title="YTD Delta Price and Delta Volume",
                      xaxis_title="Product Category", yaxis_title="%age")
    return fig


def rev_sum_wrt_channel_category(df):
    df = df.melt(id_vars='Channel Category', value_vars=['Revenue_2022', 'Revenue_2023'], var_name='YEAR', value_name='Revenue')
    df['YEAR'] = df['YEAR'].str[-4:]

    melted_df = df.groupby('Channel Category')['Revenue'].sum().reset_index()

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=melted_df["Channel Category"], y=melted_df["Revenue"], name="Revenue",
        textposition="inside", text=round(melted_df["Revenue"], 2), marker=dict(color=colors[1:])
    ))
    fig = update_hover_layout(fig)
    fig.update_layout(title="Revenue w.r.t Channel",
                      xaxis_title="Channel Category", yaxis_title="Amount")
    return fig


def rev_wrt_channel_category_and_prod_family(df):
    df = df.melt(id_vars='Product Category', value_vars=['Revenue_2022', 'Revenue_2023'], var_name='YEAR', value_name='Revenue')
    df['YEAR'] = df['YEAR'].str[-4:]

    grouped_df = df.groupby(['Product Category', 'YEAR'])['Revenue'].sum().reset_index()

    fig = px.bar(grouped_df, x='YEAR', y='Revenue', color='Product Category',
                 title='Summed Revenue by Year and Product Category',
                 labels={'Revenue': 'Sum of Revenue'}, color_discrete_sequence=colors,
                 category_orders={'YEAR': sorted(grouped_df['YEAR'].unique())},
                 text=round(grouped_df['Revenue'], 2), barmode='group')
    fig = update_hover_layout(fig)
    fig.update_layout(title="YTD Revenue vs. Previous Year", barmode="group",
                      xaxis_title="Year", yaxis_title="Sum of Revenue")
    fig.update_xaxes(tickmode='linear', dtick=1)
    return fig


def rev_wrt_year_channel_n_product_category(df):
    df = df.melt(id_vars=['Channel Category', 'Product Category'], value_vars=['Revenue_2022', 'Revenue_2023'], var_name='YEAR', value_name='Revenue')
    df['YEAR'] = df['YEAR'].str[-4:]

    fig = px.bar(df, x='Channel Category', y='Revenue', color='Product Category', facet_col='YEAR', barmode='stack',
                category_orders={'YEAR': sorted(df['YEAR'].unique())}, labels={'Revenue': 'Sum of Revenue'},
                color_discrete_sequence=colors,
                title='Revenue by Product and Channel Category for 2022 and 2023',
                facet_col_spacing=0.05, facet_col_wrap=2)
    fig.update_layout(title="YTD Revenue vs Prior Year",barmode="stack",
                      xaxis_title='Channel Category', yaxis_title='Sum of Revenue')
    fig.update_xaxes(tickmode='linear', dtick=1)
    fig.update_traces(marker_line_width=0)
    fig = update_hover_layout(fig)
    return fig


def performance_mtd(df):
    # Filter data for Appliances and Electronics
    filtered_df = df[df['Product Category'].isin(['Appliances', 'Electronics'])]

    # Group data by Year, Channel Category, and Product Category, and calculate total revenue
    grouped_df = filtered_df.groupby(['YEAR', 'Channel Category', 'Product Category'])['Revenue'].sum().unstack().reset_index()

    # Get the top 2 years for comparison
    top_years = grouped_df['YEAR'].nlargest(2)

    # Create column charts for each of the top 2 years
    charts = {}
    for year in top_years:
        # Filter data for the current year
        year_data = grouped_df[grouped_df['YEAR'] == year]

        # Melt the DataFrame to have one row per combination of Channel Category and Product Category
        melted_df = year_data.melt(id_vars=['Channel Category'], var_name='Product Category', value_name='Revenue')

        # Create column chart
        chart = px.bar(melted_df, x='Channel Category', y='Revenue', color='Product Category',
                       barmode='group', title=f'Revenue by Channel Category and Product Category for {year}')

        charts[year] = chart

    return charts


def unit_sold_wrt_campaign(df):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fin_data = df.groupby("MONTH").agg({'QTY [Units]':'sum', 'Promo Campaign [DPR%]':'mean'})
    fin_data = fin_data.reindex(MONTHS_ORDER).reset_index()

    fig.add_trace(
        go.Bar(x=fin_data['MONTH'], y=fin_data['QTY [Units]']
        ),
        secondary_y=False
    )
    fig.add_trace(
        go.Scatter(
            x=fin_data['MONTH'],
            y=fin_data['Promo Campaign [DPR%]'],
            name="Avg Promo Campaign",
            mode='lines+markers'
        ),
        secondary_y=True
    )

    fig.update_traces(name="Units Sold", selector=dict(type="bar"))
    fig.update_traces(name="Avg Promo Campaign", selector=dict(type="scatter"))
    fig.update_yaxes(title_text="Units Sold", secondary_y=False)
    fig.update_yaxes(title_text="Avg Promo Campaign", secondary_y=True)
    fig.update_layout(
    title_text="Unit Sold w.r.t Promo Campaign", xaxis_title="Month"
    )

    return fig

def avg_unit_prc(df):
    fig = make_subplots()
    fin_data = df.groupby("MONTH")[['Net Price [CAD]', 'List Price [CAD]']].mean()
    fin_data = fin_data.reindex(MONTHS_ORDER).reset_index()
    fig.add_trace(
    go.Line(
        x=fin_data['MONTH'],
        y=fin_data['Net Price [CAD]'],
        name="Avg Net Price"
    )
    )
    fig.add_trace(
    go.Line(
        x=fin_data['MONTH'],
        y=fin_data['List Price [CAD]'],
        name="AVG Gross Price"
    )
    )
    fig.update_layout(
    title_text="Avg Unit Price"
    )

    return fig

def discount_evo(df):
    fin_data = df.groupby("MONTH")[['Standard Discount [SD1][CAD]', 'Standard Discount [SD2][CAD]', 'Special Discount [DSP][CAD]', 'Promo Campaign [DPR][CAD]']].sum()
    fin_data = fin_data.reindex(MONTHS_ORDER).reset_index()
    fig = px.bar(fin_data, x="MONTH", y=['Standard Discount [SD1][CAD]', 'Standard Discount [SD2][CAD]', 'Special Discount [DSP][CAD]', 'Promo Campaign [DPR][CAD]'], barmode = 'stack')
    newnames={'Standard Discount [SD1][CAD]': 'Std. Discount1', 'Standard Discount [SD2][CAD]':'Std. Discount2', 'Special Discount [DSP][CAD]':'Special Discount', 'Promo Campaign [DPR][CAD]':'Campaign'}
    fig.for_each_trace(lambda t: t.update(name = newnames[t.name],
                                      legendgroup = newnames[t.name],
                                      hovertemplate = t.hovertemplate.replace(t.name, newnames[t.name])
                                     )
                  )
    fig.update_layout(
    title_text="Discount Evolution"
    )
    return fig

def vol_prc_per(df):
    cust_data = df.groupby("Customer Code")['Revenue'].sum()
    prc_data = df.groupby("Customer Code")[['Net Price [CAD]', 'List Price [CAD]']].mean()

    fig = px.scatter(x=cust_data, y=[prc_data['Net Price [CAD]'], prc_data['List Price [CAD]']], trendline="ols")

    fig.update_layout(
    title_text="Volume Price Performance"
    )
    return fig
