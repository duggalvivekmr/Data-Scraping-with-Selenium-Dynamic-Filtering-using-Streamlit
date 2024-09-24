import streamlit as st
import pymysql
import pandas as pd
from streamlit_option_menu import option_menu
import plotly.express as px
from datetime import datetime


# Connect to MySQL database
def get_connection():
    return pymysql.connect(
        host="localhost", user="root", passwd="Vkmd@rhn", database="REDBUS"
    )


# Function to fetch route names starting with a specific letter, arranged alphabetically
def fetch_route_names(connection, starting_letter):
    query = f"SELECT DISTINCT Route_Name FROM busroutes_details WHERE Route_Name LIKE '{starting_letter}%' ORDER BY Route_Name"
    route_names = pd.read_sql(query, connection)["Route_Name"].tolist()
    return route_names


# Function to fetch data from MySQL based on selected Route_Name and price sort order
def fetch_data(connection, route_name, price_sort_order):
    price_sort_order_sql = "ASC" if price_sort_order == "Low to High" else "DESC"
    query = f"SELECT * FROM busroutes_details WHERE Route_Name = %s ORDER BY Star_Rating DESC, Price {price_sort_order_sql}"
    df = pd.read_sql(query, connection, params=(route_name))
    return df

# Function to filter data based on Star_Rating and Bus_Type
def filter_data(df, star_ratings, bus_types):
    filtered_df = df[
        df["Star_Rating"].isin(star_ratings) & df["Bus_Type"].isin(bus_types)
    ]
    return filtered_df

# Setting up streamlit page
st.set_page_config(layout="wide")

web = option_menu(
    menu_title="🚌 Online Bus App",
    options=["Home", "🌐 Buses & Routes"],
    icons=["house", "🌐"],
    orientation="horizontal",
)

# Home page setting
if web == "Home":
    st.title(
        ":red[Redbus Data Scraping with Selenium & Dynamic Filtering using Streamlit]"
    )
    st.subheader(":blue[Transportation]")
    st.subheader(":blue[Objective]")
    st.markdown(
        "The 'Redbus Data Scraping and Filtering with Streamlit Application' aims to revolutionize the transportation industry by providing a comprehensive solution for collecting, analyzing, and visualizing bus travel data. By utilizing Selenium for web scraping, this project automates the extraction of detailed information from Redbus, including bus routes, schedules, prices, and seat availability. By streamlining data collection and providing powerful tools for data-driven decision-making, this project can significantly improve operational efficiency and strategic planning in the transportation industry."
    )
    st.subheader(":blue[Overview]")
    st.markdown(
        "Selenium: Primarily it is for automating web applications for testing purposes, which involves web scraping and extracting data from websites."
    )
    st.markdown(
        """Pandas: Use the powerful Pandas library to transform the dataset from CSV format to structured dataframe """
    )
    st.markdown(
        """MySQL: With the help of SQL establish a connection to a SQL database, enable seamless integration of the transformed dataset, and the data can be efficiently inserted into relevant tables for storage and retrieval. """
    )
    st.markdown(
        "Streamlit: Develop an interactive web application using streamlit, a user friendly framework for data visualization and analysis."
    )
    st.subheader(":blue[Skill-Used]")
    st.markdown("Selenium, Python, MySQL, pymysql.connector-python, Streamlit")
    st.subheader(":blue[Developed by]", divider="gray")
    st.markdown("Vivek Duggal on 9/24/2024 1530 PM IST")


if web == "🌐 Buses & Routes":
    # Main Streamlit app
    def main():
        st.header("Online Bus Tickets Booking")

        connection = get_connection()

        try:
            # Sidebar - Input for starting letter
            starting_letter = st.sidebar.text_input(
                "Enter starting letter of Route Name", "A"
            )

            # Fetch route names starting with the specified letter
            if starting_letter:
                route_names = fetch_route_names(connection, starting_letter.upper())

                if route_names:
                    # Sidebar - Selectbox for Route_Name
                    selected_route = st.sidebar.radio("Select Route Name", route_names)

                if selected_route:
                    # Sidebar - Selectbox for sorting preference
                    price_sort_order = st.sidebar.selectbox(
                        "Sort by Price", ["Low to High", "High to Low"]
                    )

                    # Fetch data based on selected Route_Name and price sort order
                    data = fetch_data(connection, selected_route, price_sort_order)
                    if not data.empty:
                        # Display data table with a subheader
                        st.write(f"### Data for Route: {selected_route}")
                        st.write(data)
                        # Filter by Star_Rating and Bus_Type
                        star_ratings = data["Star_Rating"].unique().tolist()
                        selected_ratings = st.multiselect(
                            "Filter by Star Rating", star_ratings
                        )

                        bus_types = data["Bus_Type"].unique().tolist()
                        selected_bus_types = st.multiselect(
                            "Filter by Bus Type", bus_types
                        )

                        if selected_ratings and selected_bus_types:
                            filtered_data = filter_data(
                                data,
                                selected_ratings,
                                selected_bus_types,
                            )
                            # Display filtered data table with a subheader
                            st.write(
                                f"### Filtered Data for Star Rating: {selected_ratings} and Bus Type: {selected_bus_types}"
                            )
                            st.write(filtered_data)
                    else:
                        st.write(
                            f"No data found for Route: {selected_route} with the specified price sort order."
                        )
            else:
                st.write("No routes found starting with the specified letter.")
        finally:
            connection.close()

    if __name__ == "__main__":
        main()
