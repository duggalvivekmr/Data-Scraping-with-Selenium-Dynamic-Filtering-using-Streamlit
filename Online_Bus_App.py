import streamlit as st
import pymysql
import pandas as pd
from streamlit_option_menu import option_menu
from sqlalchemy import create_engine
import plotly.express as px
from datetime import datetime, time

# Connect to MySQL database
def get_connection():
    host="localhost"
    username = "root"
    password = "Msd89_rhn"
    database = "redbus"

    connection_string = f"mysql+pymysql://{username}:{password}@{host}/{database}"
    engine = create_engine(connection_string)
    return engine
# Function to fetch route names starting with a specific letter, arranged alphabetically
def fetch_route_names(engine, starting_letter):
    query = f"SELECT DISTINCT Route_Name FROM bus_routes_detail WHERE Route_Name LIKE %s ORDER BY Route_Name"
    route_names = pd.read_sql(query, engine, params=(f'{starting_letter}%',))["Route_Name"].tolist()
    return route_names
# convert the TIME format to a 12-hour AM/PM format 
def convert_to_12_hour_format(time_value): # Attempted this and other logical approaches, but the intended outcome was not attained
    if pd.isna(time_value):
        return "No Time"

    if isinstance(time_value, (datetime.time, str)):
        if isinstance(time_value, str):
        # If time_value is a string, convert it to a datetime object
            try:
                time_value = datetime.strptime(time_value, '%H:%M:%S').time()
            except ValueError:
                return "Invalid time format"
        return time_value.strftime('%I:%M %p')  # Convert to 12-hour format

    return "Invalid time format"
# Function to fetch data from MySQL based on selected Route_Name and price sort order
def fetch_data(engine, route_name, price_sort_order):
    price_sort_order_sql = "ASC" if price_sort_order == "Low to High" else "DESC"
    query = f"SELECT * FROM bus_routes_ WHERE Route_Name = %s ORDER BY Star_Rating DESC, Price {price_sort_order_sql}"
    df = pd.read_sql(query, engine, params=(route_name,))

    # Check if DataFrame is empty before proceeding
    if df.empty:
        return df
    
    # Print original data for debugging
    print("Original Data:")
    print(df[['Departing_Time', 'Reaching_Time', 'Price']])
    
    # Convert timedelta to total hours
    df['departing_time'] = df['Departing_Time'].dt.total_seconds().div(3600).astype(float)
    df['reaching_time'] = df['Reaching_Time'].dt.total_seconds().div(3600).astype(float)
    
    # Convert to HH:MM AM/PM format
    def convert_to_hhmm(hours):
        hh = int(hours) % 24  # Handle hours over 24
        mm = int((hours - int(hours)) * 60)
        period = "AM" if hh < 12 else "PM"
        hh = hh % 12
        hh = 12 if hh == 0 else hh  # Convert 0 hour to 12
        return f"{hh:02}:{mm:02} {period}"
    
    df['Departing_Time_HH:MM'] = df['departing_time'].apply(convert_to_hhmm)
    df['Reaching_Time_HH:MM'] = df['reaching_time'].apply(convert_to_hhmm)
    
    # Print converted data for debugging
    print("Converted Data:")
    print(df[['Departing_Time_HH:MM', 'Reaching_Time_HH:MM']])
    return df[['Route_Link', 'Route_Name', 'Bus_Name', 'Bus_Type', 'Departing_Time_HH:MM', 'Duration', 'Reaching_Time_HH:MM', 'Star_Rating', 'Price', 'Seat_Availability']]

# Function to filter data based on Star_Rating and Bus_Type
def filter_data(df, star_ratings, bus_types):
    filtered_df = df[
        df["Star_Rating"].isin(star_ratings) & df["Bus_Type"].isin(bus_types)
    ]
    return filtered_df
# Setting up streamlit page
st.set_page_config(layout="wide")
# Option menu
web = option_menu(
    menu_title="Welcome to the Online Bus App",
    options=["Home", "Buses & Routes"],
    icons=["house", "info"],
    orientation="horizontal",
)
# Home page setting
if web == "Home":
    st.title(
        ":red[Redbus Data Scraping with Selenium & Dynamic Filtering using Streamlit]"
    )
    st.write("Welcome to the Home page!")
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
    st.markdown("Selenium, Python, MySQL, pymysql.connector-python, sqlalchemy, Streamlit")
    st.subheader(":blue[Developed by]", divider="gray")
    st.markdown("Vivek Duggal on Saturday, 9/29/2024 01:10 AM IST")
    st.markdown("Guvi Geek Netwroks IITM Research Park")
    st.markdown("Batch ID: MD 114")


if web == "Buses & Routes":
    st.write("Here are the available buses and routes.")
    # Main Streamlit app
    def main():

        st.header("Online Bus Tickets Booking")

        connection = get_connection()
        if connection is None:
            st.stop()

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

                       # Add price range slider
                       min_price = float(data['Price'].min())
                       max_price = float(data['Price'].max()) 
                       price_range = st.slider(
                           "Select Price Range",
                            min_value=min_price,
                            max_value=max_price,
                            value=(min_price, max_price),
                            step=1.0 # Change step to a float
                        )
                        
                    # Filter data based on selected price range
                    filtered_data = data[(data['Price']>=price_range[0]) & (data['Price'] <= price_range[1])]
                    
                    # Display filtered data
                    st.write(f"### Data for Route: {selected_route} within price range {price_range[0]} to {price_range[1]}")
                    st.write(filtered_data)
                    # Filter by Star_Rating and Bus_Type
                    star_ratings = filtered_data["Star_Rating"].unique().tolist()
                    selected_ratings = st.multiselect(
                        "Filter by Star Rating", star_ratings
                    )

                    bus_types = filtered_data["Bus_Type"].unique().tolist()
                    selected_bus_types = st.multiselect(
                        "Filter by Bus Type", bus_types
                    )

                    if selected_ratings and selected_bus_types:
                            final_filtered_data = filter_data(
                                filtered_data,
                                selected_ratings,
                                selected_bus_types,
                            )
                            # Display filtered data table with a subheader
                            st.write(
                                f"### Further Filtered Data for Star Rating: {selected_ratings} and Bus Type: {selected_bus_types}"
                            )
                            st.write(final_filtered_data)
                    else:
                        st.write(
                            f"No data found for Route: {selected_route} with the specified price sort order."
                        )
            else:
                st.write("No routes found starting with the specified letter.")
        finally:
            connection.dispose()

    if __name__ == "__main__":
        main()
