import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from utils import *



colors = ["#2a9d8f", "#264653", "#e9c46a", "#f4a261", "#e76f51", "#ef233c", "#f6bd60", "#84a59d", "#f95738"]
# colors = ["#880d1e", "#f26a8d", "#dd2d4a", "#f49cbb", "#cbeef3", "#880d1e"]

def sales_revenue_card(df):
    sales_by_month = df.groupby("MONTH")["Revenue"].sum()
    sales_by_month = sales_by_month.reindex(MONTHS_ORDER).reset_index()
    fig = go.Figure(
        go.Indicator(
            mode="number",
            value=sales_by_month["Revenue"].sum(),
            number={"prefix": "$"},
            title={"text": "Total Sales Revenue", "font": {"size": 20}},
            domain={'y': [0, 1], 'x': [0.25, 0.75]}
        ))

    fig.add_trace(go.Scatter(
        x=sales_by_month["MONTH"],
        y=sales_by_month["Revenue"],
        mode="lines",
        fill='tozeroy',
        name="Total Revenue",
    ))
    fig.update_xaxes(showticklabels=False, showgrid=False)
    fig.update_yaxes(showticklabels=False, showgrid=False)
    fig = update_hover_layout(fig)
    fig.update_layout(height=250)
    return fig

def list_price_sales_card(df):
    sales_by_month = df.groupby("MONTH")["List Price [CAD]"].mean()
    sales_by_month = sales_by_month.reindex(MONTHS_ORDER).reset_index()
    fig = go.Figure(
        go.Indicator(
            mode="number",
            value=sales_by_month["List Price [CAD]"].mean(),
            number={"prefix": "$"},
            title={"text": "List Price Avg", "font": {"size": 20}},
            domain={'y': [0, 1], 'x': [0.25, 0.75]}
        ))

    fig.add_trace(go.Scatter(
        x=sales_by_month["MONTH"],
        y=sales_by_month["List Price [CAD]"],
        mode="lines",
        fill='tozeroy',
        name="Avg List Price",
    ))
    fig.update_xaxes(showticklabels=False, showgrid=False)
    fig.update_yaxes(showticklabels=False, showgrid=False)
    fig = update_hover_layout(fig)
    fig.update_layout(height=250)
    return fig

def net_sales_card(df):
    sales_by_month = df.groupby("MONTH")["Net Price [CAD]"].mean()
    sales_by_month = sales_by_month.reindex(MONTHS_ORDER).reset_index()
    fig = go.Figure(
        go.Indicator(
            mode="number",
            value=sales_by_month["Net Price [CAD]"].mean(),
            number={"prefix": "$"},
            title={"text": "Net Sales", "font": {"size": 20}},
            domain={'y': [0, 1], 'x': [0.25, 0.75]}
        ))

    fig.add_trace(go.Scatter(
        x=sales_by_month["MONTH"],
        y=sales_by_month["Net Price [CAD]"],
        mode="lines",
        fill='tozeroy',
        name="Net Sales",
    ))
    fig.update_xaxes(showticklabels=False, showgrid=False)
    fig.update_yaxes(showticklabels=False, showgrid=False)
    fig = update_hover_layout(fig)
    fig.update_layout(height=250)
    return fig

def units_sold_card(df):
    qty_sold = df.groupby("MONTH")["QTY [Units]"].sum()
    qty_sold = qty_sold.reindex(MONTHS_ORDER).reset_index()
    fig = go.Figure(
        go.Indicator(
            mode="number",
            value=qty_sold["QTY [Units]"].sum(),
            number={"suffix": " units"},
            title={"text": "Total Units Sold", "font": {"size": 20}},
            domain={'y': [0, 1], 'x': [0.25, 0.75]}
        ))

    fig.add_trace(go.Scatter(
        x=qty_sold["MONTH"],
        y=qty_sold["QTY [Units]"],
        mode="lines",
        fill='tozeroy',
        name="Qty Sold",
    ))
    fig.update_xaxes(showticklabels=False, showgrid=False)
    fig.update_yaxes(showticklabels=False, showgrid=False)
    fig = update_hover_layout(fig)
    fig.update_layout(height=250)
    return fig

def profit_margin_card(df):
    monthly_financials = df.groupby("MONTH").agg({"Revenue": "sum", "Total GM [CAD]": "sum"})
    monthly_financials = monthly_financials.reindex(MONTHS_ORDER).reset_index()
    monthly_financials['Profit Margin'] = (monthly_financials['Total GM [CAD]'] / monthly_financials['Revenue']) * 100
    total_revenue = monthly_financials['Revenue'].sum()
    total_gross_margin = monthly_financials['Total GM [CAD]'].sum()
    overall_profit_margin = (total_gross_margin / total_revenue) * 100
    # delta_ref = overall_profit_margin * 100 - np.mean(monthly_financials['Profit Margin'])
    fig = go.Figure(
        go.Indicator(
            mode="number+delta",
            value=overall_profit_margin,
            number={"suffix": "%"},
            title={"text": "Profit Margin", "font": {"size": 20}},
            domain={'y': [0, 1], 'x': [0.25, 0.75]}
        ))

    fig.add_trace(go.Scatter(
        x=monthly_financials["MONTH"],
        y=monthly_financials["Profit Margin"],
        mode="lines",
        fill='tozeroy',
        name="Profit Margin",
    ))

    fig.update_xaxes(showticklabels=False, showgrid=False)
    fig.update_yaxes(showticklabels=False, showgrid=False)
    fig = update_hover_layout(fig)
    fig.update_layout(height=250)
    return fig

def average_discount_rate_card(df):
    # Calculate the weighted discount rates, assuming discounts are stored as proportions (e.g., 20% is stored as 0.20)
    df['Weighted SD1'] = df['Standard Discount [SD1 %]'] * df['Revenue']
    df['Weighted SD2'] = df['Standard Discount [SD2 %]'] * df['Revenue']
    df['Weighted DSP'] = df['Special Discount [DSP %]'] * df['Revenue']
    df['Weighted DPR'] = df['Promo Campaign [DPR%]'] * df['Revenue']

    # Aggregate these weighted discounts and sum of revenue by month
    monthly_discounts = df.groupby('MONTH').agg({
        'Weighted SD1': 'sum',
        'Weighted SD2': 'sum',
        'Weighted DSP': 'sum',
        'Weighted DPR': 'sum',
        'Revenue': 'sum'
    })
    monthly_discounts = monthly_discounts.reindex(MONTHS_ORDER).reset_index()

    # Calculate the overall average discount rate by month
    monthly_discounts['Avg Discount Rate'] = (
            monthly_discounts[['Weighted SD1', 'Weighted SD2', 'Weighted DSP', 'Weighted DPR']].sum(axis=1)
            / monthly_discounts['Revenue'])

    # Calculate the overall average discount rate
    total_discounts = monthly_discounts[['Weighted SD1', 'Weighted SD2', 'Weighted DSP', 'Weighted DPR']].sum().sum()
    total_revenue = monthly_discounts['Revenue'].sum()
    overall_avg_discount_rate = total_discounts / total_revenue

    fig = go.Figure(
        go.Indicator(
            mode="number+delta",
            value=overall_avg_discount_rate * 100,  # Convert proportion to percentage
            number={"suffix": "%"},
            title={"text": "Average Discount Rate", "font": {"size": 20}},
            domain={'y': [0, 1], 'x': [0.25, 0.75]}
        ))

    fig.add_trace(go.Scatter(
        x=monthly_discounts["MONTH"],
        y=monthly_discounts["Avg Discount Rate"] * 100,  # Convert proportion to percentage for plotting
        mode="lines",
        fill='tozeroy',
        name="Avg Discount Rate",
    ))

    fig.update_xaxes(showticklabels=False, showgrid=False)
    fig.update_yaxes(showticklabels=False, showgrid=False)
    fig = update_hover_layout(fig)
    fig.update_layout(height=250)
    return fig

def average_selling_price_card(df):
    # Calculate the Average Selling Price (ASP) by dividing total revenue by total units sold
    # Group by month to get monthly ASP
    monthly_sales = df.groupby("MONTH").agg({"Revenue": "sum", "QTY [Units]": "sum"})
    monthly_sales = monthly_sales.reindex(MONTHS_ORDER).reset_index()
    monthly_sales['ASP'] = monthly_sales['Revenue'] / monthly_sales['QTY [Units]']

    # Calculate the total Average Selling Price across all months
    total_revenue = monthly_sales['Revenue'].sum()
    total_units_sold = monthly_sales['QTY [Units]'].sum()
    overall_asp = total_revenue / total_units_sold

    fig = go.Figure(
        go.Indicator(
            mode="number",
            value=overall_asp,
            number={"prefix": "$"},
            title={"text": "Average Selling Price", "font": {"size": 20}},
            domain={'y': [0, 1], 'x': [0.25, 0.75]}
        ))

    fig.add_trace(go.Scatter(
        x=monthly_sales["MONTH"],
        y=monthly_sales["ASP"],
        mode="lines",
        fill='tozeroy',
        name="Average Selling Price",
    ))

    fig.update_xaxes(showticklabels=False, showgrid=False)
    fig.update_yaxes(showticklabels=False, showgrid=False)
    fig = update_hover_layout(fig)
    fig.update_layout(height=250)
    return fig

def income_statement(df):
    df['CoGS'] = df['Total Cost [CAD]']
    df['Total Expense'] = df['Standard Discount [SD1][CAD]'] + df['Standard Discount [SD2][CAD]'] + df[
        'Special Discount [DSP][CAD]'] + df['Promo Campaign [DPR][CAD]']
    df['Net Profit'] = df['Revenue'] - df['Total Expense'] - df['CoGS']

    fin_data = df.groupby("MONTH")[['Total Expense', 'CoGS', 'Revenue', 'Net Profit']].sum()
    fin_data = fin_data.reindex(MONTHS_ORDER).reset_index()
    fig = go.Figure()
    fig.add_trace(
        go.Bar(x=fin_data["MONTH"], y=fin_data["Total Expense"], name="Total Expense",
               marker=dict(color=colors[0]))
    )
    fig.add_trace(
        go.Bar(x=fin_data["MONTH"], y=fin_data["CoGS"], name="CoGS",
               marker=dict(color=colors[1]))
    )
    fig.add_trace(
        go.Bar(x=fin_data["MONTH"], y=fin_data["Revenue"], name="Revenue",
               marker=dict(color=colors[2]))
    )
    fig.add_trace(
        go.Bar(x=fin_data["MONTH"], y=fin_data["Net Profit"], name="Net Profit",
               marker=dict(color=colors[3]))
    )
    fig.update_layout(barmode="group", title="Income Statement", xaxis_title="Month",
                      yaxis_title="Amount", height=450)
    fig = update_hover_layout(fig)
    fig.update_xaxes(type='category')
    return fig

def expenses_pie(df):
    summed_discounts = df[['Standard Discount [SD1][CAD]', 'Standard Discount [SD2][CAD]',
                           'Special Discount [DSP][CAD]', 'Promo Campaign [DPR][CAD]',
                           'Rebates [DREB][CAD]']].sum()
    fig = go.Figure(data=[
        go.Pie(labels=summed_discounts.index, values=summed_discounts.values, hole=.4,
               marker_colors=colors)
    ])
    fig.update_layout(
        title_text='Discounts and Promos Analysis',
        annotations=[dict(text='Expenses', x=0.5, y=0.5, font_size=15, showarrow=False)]
    )
    fig = update_hover_layout(fig)
    return fig

def monthly_rev_gm(filtered_data):
    revenue_data = filtered_data.groupby("MONTH")[["Revenue", "Total GM [CAD]"]].sum()
    revenue_data = revenue_data.reindex(MONTHS_ORDER).reset_index()
    revenue_data['Profit Margin [%]'] = (revenue_data['Total GM [CAD]'] / revenue_data['Revenue']) * 100
    revenue_data['Profit Margin (M)'] = revenue_data['Total GM [CAD]'] / 1e6
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=revenue_data["MONTH"], y=revenue_data["Revenue"], mode="lines+markers+text",
        marker=dict(color="#e76f51"), line=dict(color="#e76f51"), textposition="top center", name="Revenue"))
    fig.add_trace(go.Scatter(
        x=revenue_data["MONTH"], y=revenue_data["Total GM [CAD]"], mode="lines+markers",
        marker=dict(color="#264653"), line=dict(color="#264653"), textposition="top center", name='', hovertemplate='<b>Month:</b> %{x}<br><b>Profit Margin in M:</b> %{customdata:.2f}M<br><b>Profit Margin in %:</b> %{text}',
        customdata=revenue_data['Profit Margin (M)'],  # Custom data for hover template (Total GM in M)
        text=[f"{val:.2f}%" for val in revenue_data['Profit Margin [%]']]))
    fig.update_layout(title="Revenue/G.Profit Over Time", xaxis_title="Month", yaxis_title="Amount")
    fig = update_hover_layout(fig)
    return fig

def product_performance(df):
    df["Unit GM [%]"] = pd.to_numeric(df['Unit GM [%]'], errors='coerce')
    prod_data = df.groupby("Product Range").agg(
        {"Unit GM [%]": "mean",
         "QTY [Units]": "sum"}
    ).reset_index()
    prod_data = prod_data.sort_values(by="QTY [Units]", ascending=False)
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Bar(
            x=prod_data["Product Range"], y=df["QTY [Units]"], name="Quantity Sold",
            marker=dict(color="#264653")
        ), secondary_y=False
    )
    fig.add_trace(
        go.Scatter(
            x=prod_data["Product Range"], y=df["Unit GM [%]"], name="Unit GM [%]",
            marker=dict(color="#e76f51"), mode="markers+lines",
            hovertemplate='%{y:.2f}',
        ), secondary_y=True
    )
    fig.update_layout(title="Product Selling Performance", xaxis_title="Product Range", yaxis_title="Units")
    fig = update_hover_layout(fig)
    return fig

def customer_distribution(df):
    prod_data = df.groupby('Customer Name').agg({'Revenue':'sum'}).sort_values(by='Customer Name', ascending=False).reset_index()
    fig = go.Figure(data=[go.Pie(labels=prod_data["Customer Name"], values=prod_data["Revenue"], name="Revenue", marker_colors=colors, title="Revenue", hole=.4, hoverinfo="label+percent+name")])
    fig.update_layout(title_text='Customer Distribution of Revenue')
    fig = update_hover_layout(fig)
    return fig

def channel_distribution(df):
    # Group data by 'Channel Sub-Category' instead of 'Channel Category'
    prod_data = df.groupby('Channel Sub-Category').agg({'QTY [Units]':'sum'}).reset_index()

    # Assuming 'colors' is a predefined list of colors
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']

    # Create the pie chart using 'Channel Sub-Category'
    fig = go.Figure(data=[
        go.Pie(
            labels=prod_data["Channel Sub-Category"],
            values=prod_data["QTY [Units]"],
            name="Qty Sold",
            marker_colors=colors,
            title="Quantity",
            hole=.4,
            hoverinfo="label+percent+name"
        )
    ])

    # Update the layout to include a title and possibly other stylistic choices
    fig.update_layout(title_text='Channel Distribution of Quantity Sold')

    # This function call 'update_hover_layout' is not shown in your snippet.
    # Ensure it's correctly defined elsewhere in your codebase, or remove this line if not needed.
    fig = update_hover_layout(fig)

    return fig

def rev_by_customer(df):
    prod_data = df.groupby("Customer Name")[["Revenue", "Total GM [CAD]", "QTY [Units]"]].sum().reset_index()
    fig = make_subplots(rows=1, cols=3, specs=[[{'type': 'domain'}, {'type': 'domain'}, {'type': 'domain'}]])
    fig.add_trace(
        go.Pie(labels=prod_data["Customer Name"], values=prod_data["Revenue"], name="Revenue",
               marker_colors=colors, title="Revenue"), 1, 1)
    fig.add_trace(
        go.Pie(labels=prod_data["Customer Name"], values=prod_data["Total GM [CAD]"], name="Profit Margin",
               marker_colors=colors, title="Profit Margin"), 1, 2)
    fig.add_trace(
        go.Pie(labels=prod_data["Customer Name"], values=prod_data["QTY [Units]"], name="Qty Sold",
               marker_colors=colors, title="Quantity"), 1, 3)
    fig.update_traces(hole=.4, hoverinfo="label+percent+name")
    fig.update_layout(title_text='Customers Distribution')
    fig = update_hover_layout(fig)
    return fig

def avg_disc_given(df):
    df["Total Discount"] = df['Standard Discount [SD1][CAD]'] + df['Standard Discount [SD2][CAD]'] + df['Special Discount [DSP][CAD]']
    df = df.groupby("Customer Name")["Total Discount"].mean().reset_index()

    fig = go.Figure(
        go.Bar(x=df["Customer Name"], y=df["Total Discount"],
               marker=dict(color=colors[0]))
    )
    fig.update_layout(
        title_text='Avg. Discount availed by Customers')
    fig = update_hover_layout(fig)
    return fig

def clv_plot(df):
    # Calculate Customer Lifetime Value approximation
    clv = df.groupby('Customer Name')['Revenue'].sum().sort_values(ascending=False).reset_index()

    # Calculate the cumulative sum of revenue and the cumulative percentage
    clv['Cumulative Revenue'] = clv['Revenue'].cumsum()
    clv['Cumulative Percentage'] = clv['Cumulative Revenue'] / clv['Revenue'].sum() * 100

    # Plot for Customer Lifetime Value
    fig_clv = go.Figure(data=[
        go.Bar(x=clv['Customer Name'], y=clv['Cumulative Percentage'], marker=dict(color=colors[1]))
    ])

    fig_clv.update_layout(
        title_text='Customer Lifetime Value (CLV) Approximation',
        xaxis_title='Customer Name',
        yaxis_title='Cumulative Percentage'
    )
    fig_clv = update_hover_layout(fig_clv)
    return fig_clv

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

def top_10_customers(df):
    top_10_customers = df.groupby('Customer Name')['Revenue'].sum().nlargest(10).reset_index()
    fig = go.Figure(
        go.Bar(x=top_10_customers['Customer Name'], y=top_10_customers['Revenue'],
               marker=dict(color=colors[0]))
    )
    fig.update_layout(barmode='group', xaxis_title="Customer Name", yaxis_title="Revenue", title_text='Top 10 Customers by Revenue')
    fig = update_hover_layout(fig)
    return fig

def top_10_products(df):
    top_10_products = df.groupby('Product Range')['Revenue'].sum().nlargest(10).reset_index()
    fig = go.Figure(
        go.Bar(x=top_10_products['Product Range'], y=top_10_products['Revenue'],
               marker=dict(color=colors[0]))
    )
    fig = update_hover_layout(fig)
    fig.update_layout(barmode='group', xaxis_title="Product Range", yaxis_title="Revenue", title_text='Top 10 Products by Revenue')
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
                 text=round(grouped_df['Revenue'], 2))
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
                title='Revenue by Product and Channel Category for 2022 and 2023')
    fig = update_hover_layout(fig)
    fig.update_layout(title="YTD Revenue vs Prior Year",barmode="stack",
                      xaxis_title='Channel Category', yaxis_title='Sum of Revenue')
    fig.update_xaxes(tickmode='linear', dtick=1)
    fig.update_traces(marker_line_width=0)
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
    print(fin_data['Promo Campaign [DPR%]'])
    fin_data = fin_data.reindex(MONTHS_ORDER).reset_index()
    fig.add_trace(
        go.Bar(x=fin_data['MONTH'], y=fin_data['QTY [Units]']
        ),
        secondary_y=False
    )
    fig.add_trace(
        go.Scatter(
            x=fin_data['MONTH'],
            y=list(map(lambda x: x * 100, fin_data['Promo Campaign [DPR%]'])),
            name="Avg Promo Campaign (%)",
            mode='lines+markers',
            hovertemplate='%{y:.2f}%'
        ),
        secondary_y=True
    )
    fig.update_traces(name="Units Sold", selector=dict(type="bar"))
    fig.update_traces(name="Avg Promo Campaign (%)", selector=dict(type="scatter"))
    fig.update_yaxes(title_text="Units Sold", secondary_y=False)
    fig.update_yaxes(title_text="Avg Promo Campaign (%)", secondary_y=True)
    fig.update_layout(title_text="Unit Sold w.r.t Promo Campaign (%)", xaxis_title="Month")
    return fig

def avg_unit_prc(df):
    fig = make_subplots()
    fin_data = df.groupby("MONTH")[['Net Price [CAD]', 'List Price [CAD]']].mean()
    fin_data = fin_data.reindex(MONTHS_ORDER).reset_index()
    fig.add_trace(
        go.Scatter(
            x=fin_data['MONTH'],
            y=fin_data['Net Price [CAD]'],
            name="Avg Net Price",
            mode="lines+markers"
        )
    )
    fig.add_trace(
        go.Scatter(
            x=fin_data['MONTH'],
            y=fin_data['List Price [CAD]'],
            name="AVG Gross Price",
            mode="lines+markers"
        )
    )
    fig.update_layout(title_text="Avg Unit Price", xaxis_title="Month", yaxis_title="Avg Price", legend_title="Price Type")
    return fig

def avg_unit_prc_per_customer(df):
    # Assuming 'Customer Name' is the name of the column that contains customer names,
    # 'Revenue' is the name of the column that contains revenue data,
    # 'Net Price [CAD]' contains the net unit price per customer, and
    # 'List Price [CAD]' contains the gross unit price per customer.

    # Data preparation
    cust_data = df.groupby("Customer Name")['Revenue'].sum().reset_index()
    prc_data = df.groupby("Customer Name")[['Net Price [CAD]', 'List Price [CAD]']].mean().reset_index()

    # Merge the DataFrames on Customer Name to have Revenue, Net Price, and List Price in one DataFrame
    merged_data = cust_data.merge(prc_data, on="Customer Name")

    # Creating the scatter plot
    fig = go.Figure()

    # Adding Net Price scatter
    fig.add_trace(go.Scatter(
        x=merged_data['Revenue'],
        y=merged_data['Net Price [CAD]'],
        mode='markers',
        name='Avg Net Price',
        text=merged_data['Customer Name'],  # This will show the customer name when hovering
        hoverinfo='text+y+x'  # Show hover info for customer name, y and x values
    ))

    # Adding List Price scatter
    fig.add_trace(go.Scatter(
        x=merged_data['Revenue'],
        y=merged_data['List Price [CAD]'],
        mode='markers',
        name='Avg Gross Price',
        text=merged_data['Customer Name'],  # This will show the customer name when hovering
        hoverinfo='text+y+x'  # Show hover info for customer name, y and x values
    ))

    # Update layout to match the example
    fig.update_layout(
        title_text="Average Unit Price Per Customer",
        xaxis_title="Revenue",
        yaxis_title="Avg Unit Price [CAD]",
        hovermode='closest'  # Highlight the closest point on hover
    )

    # Set the aspect ratio to match the example image
    min_price = min(df['Net Price [CAD]'].min(), df['List Price [CAD]'].min())
    max_price = max(df['Net Price [CAD]'].max(), df['List Price [CAD]'].max())
    padding = (max_price - min_price) * 0.1  # Add 10% of the range as padding
    fig.update_yaxes(range=[min_price - padding, max_price + padding])

    # Update the marker style if needed to match the example
    fig.update_traces(marker=dict(size=10))
    # fig.add_trace(go.Scatter(x=cust_data, y=prc_data['Net Price [CAD]'], mode='lines+markers', name='Avg Net Price'))
    # fig.add_trace(go.Scatter(x=cust_data, y=prc_data['List Price [CAD]'], mode='lines+markers', name='Avg Gross Price'))
    # fig.update_layout(title_text="Avg Unit Price per Customer", xaxis_title="Revenue", yaxis_title="Avg Price", legend_title="Price Type")

    return fig

def discount_evo(df):
    percentage_columns = ['Standard Discount [SD1 %]', 'Standard Discount [SD2 %]', 'Special Discount [DSP %]', 'Promo Campaign [DPR%]']
    fin_data = df.groupby("MONTH")[percentage_columns].mean()
    fin_data = fin_data.reindex(MONTHS_ORDER).reset_index()

    # Iterate over the columns and multiply by 100
    for col in percentage_columns:
        fin_data[col] = fin_data[col] * 100

    fig = px.bar(fin_data, x="MONTH", y=percentage_columns, barmode = 'stack')
    newnames={'Standard Discount [SD1 %]': 'Std. Discount1 %', 'Standard Discount [SD2 %]':'Std. Discount2 %', 'Special Discount [DSP %]':'Special Discount %', 'Promo Campaign [DPR%]':'Campaign %'}
    fig.for_each_trace(lambda t: t.update(name = newnames[t.name],
                                      legendgroup = newnames[t.name],
                                      hovertemplate = t.hovertemplate.replace(t.name, newnames[t.name])
                                     )
                  )
    fig.update_layout(title_text="Discount Evolution")
    return fig
