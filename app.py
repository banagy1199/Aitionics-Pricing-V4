import streamlit as st
from streamlit_option_menu import option_menu

from utils import *
from plots.plots import *



setup_app()
initialize_session_state()
authenticate()
users, delta, _ = get_mongo_collections()


def main():
    if st.session_state['authenticated']:
        # ------------------------------- Data Fetching -------------------------------
        df = fetch_data(users)
        delta_df = fetch_data(delta)

        # ------------------------------- Menu -------------------------------
        menu = option_menu(menu_title=None, menu_icon=None, orientation="horizontal",
                           options=["Overview","Summary Charts", "Price Analysis", "Customer Insights", "Product Performance"])
        if menu == "Overview":
            # ------------------------------- Welcome Messages -------------------------------
            df_year_1, df_year_2, delta_df_filtered = get_notification_filters(df, delta_df)
            show_dataframe = st.sidebar.checkbox("Show Dataframe", value=False)


            overall_growth, max_growth_channel, min_growth_channel = get_notification_revenue_growth(df_year_1, df_year_2)

            # Notifications for Revenue Growth
            if overall_growth > 0:
                st.success(f"Great news! YTD Revenue has grown this month by {overall_growth:.2f}% vs prior year, thanks to {max_growth_channel['Channel Category']} channel which grew by {max_growth_channel['YTD Revenue Growth']:.2f}%!", icon="🚀")
            elif overall_growth < 0:
                st.error(f"Bad news! YTD Revenue has declined this month by {abs(overall_growth):.2f}% vs prior year, due to {min_growth_channel['Channel Category']} channel which made a loss by {abs(min_growth_channel['YTD Revenue Growth']):.2f}%!", icon="📉")
            else:
                st.info(f"No change in YTD Revenue this month compared to prior year.", icon="�")

            # ------------------------------- Delta Price & Volume -------------------------------
            st.sidebar.markdown("""---""")
            delta_price_threshold = st.sidebar.number_input("Delta Price %", min_value=0, max_value=100, value=5, step=1)
            delta_price_summary = get_notification_delta(delta_df_filtered, 'Delta Price %')

            # Notifications for Delta Price
            if delta_price_summary['overall_delta_pct'] > delta_price_threshold:  # Assuming 5% is your yearly target for Delta Price
                st.success(f"The overall Delta Price is {delta_price_summary['overall_delta_pct']:.2f}% which is above your yearly target. Great job!", icon="☺")
                if show_dataframe: st.dataframe(delta_price_summary['pivot_table'], use_container_width=True)
            else:
                st.error(f"The overall Delta Price is {delta_price_summary['overall_delta_pct']:.2f}%. Please review the pricing strategy.", icon="🚨")
                if show_dataframe: st.dataframe(delta_price_summary['pivot_table'], use_container_width=True)

            # Highlighting the highest and lowest Delta Price
            st.info(f"Highest Delta Price: {delta_price_summary['highest_delta_pct']:.2f}% in {delta_price_summary['highest_channel']} ({delta_price_summary['highest_sub_channel']}), by customer {delta_price_summary['highest_customer']}.", icon="🔼")
            st.info(f"Lowest Delta Price: {delta_price_summary['lowest_delta_pct']:.2f}% in {delta_price_summary['lowest_channel']} ({delta_price_summary['lowest_sub_channel']}), by customer {delta_price_summary['lowest_customer']}. This requires immediate attention.", icon="🔽")

            delta_volume_threshold = st.sidebar.number_input("Delta Volume %", min_value=0, max_value=100, value=1, step=1)
            delta_volume_summary = get_notification_delta(delta_df_filtered, 'Delta Volume %')

            # Notifications for Delta Volume
            if delta_volume_summary['overall_delta_pct'] < delta_volume_threshold:  # Assuming 1% is the minimum acceptable Delta Volume
                st.error(f"The overall Delta Volume is {delta_volume_summary['overall_delta_pct']:.2f}% which is below your yearly target. This is concerning and needs a deep dive.", icon="🚨")
                if show_dataframe: st.dataframe(delta_volume_summary['pivot_table'], use_container_width=True)
            else:
                st.success(f"The overall Delta Volume is {delta_volume_summary['overall_delta_pct']:.2f}%, which is above your yearly target. Excellent performance!", icon="☺")
                if show_dataframe: st.dataframe(delta_volume_summary['pivot_table'], use_container_width=True)

            # Highlighting the highest and lowest Delta Volume
            st.info(f"Highest Delta Volume: {delta_volume_summary['highest_delta_pct']:.2f}% in {delta_volume_summary['highest_channel']} ({delta_volume_summary['highest_sub_channel']}), by customer {delta_volume_summary['highest_customer']}.", icon="🔼")
            st.info(f"Lowest Delta Volume: {delta_volume_summary['lowest_delta_pct']:.2f}% in {delta_volume_summary['lowest_channel']} ({delta_volume_summary['lowest_sub_channel']}), by customer {delta_volume_summary['lowest_customer']}. Critical review required.", icon="🔽")


            # ------------------------------- Quick Analysis -------------------------------
            row_0 = st.columns(2)
            row_0[0].plotly_chart(top_10_customers(df_year_2), use_container_width=True)
            row_0[1].plotly_chart(top_10_products(df_year_2), use_container_width=True)

            row_1 = st.columns(2)
            row_1[0].plotly_chart(delta_qty_wrt_channel_category(delta_df_filtered), use_container_width=True)
            row_1[1].plotly_chart(delta_qty_wrt_product_category(delta_df_filtered), use_container_width=True)

            st.plotly_chart(rev_wrt_year_channel_n_product_category(delta_df_filtered), use_container_width=True)

            # ------------------------------- End Overview -------------------------------

        if menu == "Price Analysis":
            # ------------------------------- Filters -------------------------------
            df_filtered = get_price_filters(df)


            # ------------------------------- KPIs -------------------------------
            kpi_row = st.columns(4)
            kpi_row[0].plotly_chart(sales_revenue_card(df_filtered), use_container_width=True)
            kpi_row[1].plotly_chart(units_sold_card(df_filtered), use_container_width=True)
            kpi_row[2].plotly_chart(profit_margin_card(df_filtered), use_container_width=True)
            kpi_row[3].plotly_chart(average_discount_rate_card(df_filtered), use_container_width=True)

            kpi_row1 = st.columns(3)
            kpi_row1[0].plotly_chart(average_selling_price_card(df_filtered), use_container_width=True)
            kpi_row1[1].plotly_chart(list_price_sales_card(df_filtered), use_container_width=True)
            kpi_row1[2].plotly_chart(net_sales_card(df_filtered), use_container_width=True)


            # ------------------------------- Income & Discounts Analysis -------------------------------
            st.plotly_chart(unit_sold_wrt_campaign(df_filtered), use_container_width=True)
            st.plotly_chart(discount_evo(df_filtered), use_container_width=True)

            # ------------------------------- End Income & Expenses -------------------------------

        if menu == "Customer Insights":
            # ------------------------------- Filters -------------------------------
            df_filtered = get_customer_filters(df)


            # ------------------------------- Product Sales Analysis -------------------------------
            st.plotly_chart(avg_unit_prc(df_filtered), use_container_width=True)
            st.plotly_chart(avg_unit_prc_per_customer(df_filtered), use_container_width=True)

            # ------------------------------- End Customer Insights -------------------------------

        if menu == "Product Performance":
            # ------------------------------- Filters -------------------------------
            df_filtered = get_product_filters(df)


            # ------------------------------- KPIs -------------------------------
            kpi_row = st.columns(4)
            kpi_row[0].plotly_chart(average_list_price_card(df_filtered), use_container_width=True)
            kpi_row[1].plotly_chart(total_prod_qty_card(df_filtered), use_container_width=True)
            kpi_row[2].plotly_chart(total_prod_rev_card(df_filtered), use_container_width=True)
            kpi_row[3].plotly_chart(total_prod_GM_card(df_filtered), use_container_width=True)


            # ------------------------------- Product Sales Analysis -------------------------------
            row_1 = st.columns(2)
            row_1[0].plotly_chart(monthly_rev_gm(df_filtered), use_container_width=True)
            row_1[1].plotly_chart(product_performance(df_filtered), use_container_width=True)

            row_2 = st.columns(2)
            row_2[0].plotly_chart(customer_distribution(df_filtered), use_container_width=True)
            row_2[1].plotly_chart(channel_distribution(df_filtered), use_container_width=True)

            # ------------------------------- End Product Performance -------------------------------

        if menu == "Summary Charts":
            # ------------------------------- Filters -------------------------------
            df_filtered = get_summary_filters(delta_df)


            # ------------------------------- KPIs -------------------------------
            kpi_row = st.columns(5)
            kpi_row[0].plotly_chart(summary_rev_sum_card(df_filtered), use_container_width=True)
            kpi_row[1].plotly_chart(summary_delta_price_sum_card(df_filtered), use_container_width=True)
            kpi_row[2].plotly_chart(summary_delta_price_perct_card(df_filtered), use_container_width=True)
            kpi_row[3].plotly_chart(summary_delta_volume_sum_card(df_filtered), use_container_width=True)
            kpi_row[4].plotly_chart(summary_delta_volume_perct_card(df_filtered), use_container_width=True)


            # ------------------------------- Revenue and Change Analysis -------------------------------
            row_1 = st.columns(2)
            row_1[0].plotly_chart(delta_qty_wrt_channel_category(df_filtered), use_container_width=True)
            row_1[1].plotly_chart(rev_sum_wrt_channel_category(df_filtered), use_container_width=True)

            st.plotly_chart(rev_wrt_channel_category_and_prod_family(df_filtered), use_container_width=True)

            # ------------------------------- End Summary Charts -------------------------------

    elif st.session_state['authenticated'] == None:
        st.info("Login to view data insights", icon="🚨")
    else:
        st.error("Invalid credentials", icon="🚨")

if __name__ == main():
    main()
