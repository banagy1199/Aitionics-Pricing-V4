# Aitionics Dashboard

## Overview

Aitionics Dashboard is an interactive, web-based analytics platform designed to deliver insights into sales revenue, customer behavior, and product performance. It is built using Streamlit and integrates various Python packages for data processing and visualization.

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

Use the sidebar filters to refine the data and interact with the visualizations for deeper analysis.

## File Structure

- `app.py`: Main application script.
- `utils.py`: Utility functions for data processing.
- `requirements.txt`: List of Python package dependencies.
- `/assets`: Contains logo image.
- `/css`: Custom CSS for frontend.
- `/plots`: code for Plotly charts.

---
