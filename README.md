# Aitionics Dashboard

## Overview

Aitionics Dashboard is an interactive, web-based analytics platform designed to deliver insights into sales revenue, customer behavior, and product performance. It is built using Streamlit and integrates various Python packages for data processing and visualization.

## Data Upload and Management
Support for Various File Formats: The dashboard can handle CSV, XLS, and XLSX file formats, allowing users to upload and analyze data from different sources​​.

## Dynamic Filtering
Customizable Data Views: Users can filter data based on attributes such as year, month, channel, and other relevant criteria, enabling them to tailor the analytics to their specific needs. This feature allows for more focused analysis and insight generation​​​​.

## Key Performance Indicators (KPIs) Visualization
Real-time Insights: The dashboard displays key performance indicators (KPIs), offering quick insights into critical metrics like sales performance, revenue growth, and more. These KPIs are essential for tracking business health and making informed decisions​​.

## Interactive Data Visualization
Plotly Integration: Utilizing Plotly, the dashboard provides interactive and responsive charts. This feature enhances the user experience by allowing for dynamic data exploration, including drilling down into specific data points for more detailed analysis​​.

## Advanced Data Processing and Analytics
Data Pre-processing Module: Before analysis, data goes through a pre-processing stage to prepare it for visualization and insights generation. This step ensures data quality and consistency​​.

Revenue Growth Notifications: Users receive notifications about overall revenue growth, including detailed insights into the best and worst-performing channels. This feature is beneficial for quickly identifying trends and areas of concern​​.

Price and Volume Analysis: The dashboard offers in-depth analysis of price and volume changes, highlighting areas where pricing strategies may need adjustment or where volume changes indicate market shifts​​.

Customer Insights: Focused analysis on customer-related data helps businesses understand customer behavior, preferences, and profitability. This feature aids in tailoring products and services to meet customer needs better​​.

Product Performance: Users can analyze product sales and performance metrics, identifying top-performing products and areas for improvement. This aspect is crucial for inventory management and product development strategies​​.

## Customization and Extensibility
Modular Design: The dashboard’s design, including the use of utility functions and the separation of plotting code into a specific module, suggests it is built for customization and extensibility. Users can add new features, analytics capabilities, or data sources as needed​​​​.
T
The Aitionics Dashboard combines data management, advanced analytics, and interactive visualization to provide a robust platform for data-driven decision-making. Its capabilities are suited for businesses looking to gain insights into sales trends, customer behaviors, and product performance to drive growth and improve operational efficiency.

## Features

- **Data Upload**: Supports CSV, XLS, and XLSX file formats.
- **Dynamic Filtering**: Users can filter data based on year, month, channel, and other attributes.
- **KPI Visualization**: Displays key performance indicators for quick insights.
- **Data Processing**: Includes a data pre-processing module to prepare data for analysis.
- **Interactive Charts**: Uses Plotly for responsive, interactive charts.

## Installation

To run the Aitionics Dashboard, you need to have Python installed on your machine along with the required libraries listed in `requirements.txt`.

1. Clone/Get the source code.
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the Streamlit application:
   ```
   streamlit run app.py
   ```

## Usage

Launch the dashboard and upload a data file in the supported format. Navigate through the different sections using the menu tabs:

- **Overview**: General sales and performance metrics.
- **Customer Insights**: Analysis focused on customer-related data.
- **Product Performance**: Metrics about product sales and performance.
- **Price Anylisis**: Product discount and Overall performance
- **Summery Charts**: YTD performance charts

Use the sidebar filters to refine the data and interact with the visualizations for deeper analysis.

## File Structure

- `app.py`: Main application script.
- `utils.py`: Utility functions for data processing.
- `requirements.txt`: List of Python package dependencies.
- `/assets`: Contains logo image.
- `/css`: Custom CSS for frontend.
- `/plots`: code for Plotly charts.

---
