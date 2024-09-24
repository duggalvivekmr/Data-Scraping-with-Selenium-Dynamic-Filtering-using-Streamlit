

# Redbus Data Scraping with Selenium and Dynamic Filtering using Streamlit

# **Objective:** 

Develop a web scraper to automate the extraction of bus route details, schedules, and relevant information from the RedBus website for multiple states. Store the data in an SQL database and visualize it using a Streamlit app.

## Scope:

* **Data Extraction:** Scrape bus route links, names, and detailed information for each route, including bus name, type, departing time, duration, reaching time, star rating, price, and seat availability.  
* **Automation:** On the RedBus website, automate navigation across multiple pages and states.  
* **Data Storage:** Store the scraped data in an SQL database.  
* **Visualization:** Develop a Streamlit app to visualize and analyze the stored data.

### Solution Overview

The solution involves three main components: web scraping, SQL database integration, and Streamlit app development.

#### 1\. Web Scraping

**Approach:**

* Use Selenium to automate web browsing and data extraction from the RedBus website.  
* Handle dynamic content loading, pagination, and potential pop-ups.

**Steps:**

1) **Initialize the Web Driver:** Open and maximize the browser, then navigate to the RedBus website.  
2) **Load Web Page:** Load the specific URL for the target state, handling any loading delays.  
3) **Scrape Bus Routes:** Identify and extract all bus route links and names on the page, managing pagination to capture all routes.  
4) **Scrape Bus Details:** Navigate to each bus route link and extract detailed information about available buses, such as name, type, departing time, duration, reaching time, star rating, price, and seat availability.  
5) **Handle Errors:** Implement error handling for missing elements or loading failures, logging errors, and continuing the scraping process.

#### 2\. SQL Database Integration

**Approach:**

* Use Python's sqlite3 or another SQL database connector (like mysql-connector-python for MySQL) to store the scraped data.

**Steps:**

1) **Database Setup:** Create a database and define a table structure to store bus route and schedule details.  
2) **Data Insertion:** Insert the scraped data into the SQL database, ensuring data integrity and handling duplicates or errors.

| Column names | Data types |
| :---- | :---- |
| Id | INT PRIMARY KEY AUTO INCREMENT |
| Route Name | TEXT |
| Route Link | TEXT |
| Bus Name | TEXT |
| Bus Type | TEXT |
| Departing Time | TIME (6) |
| Duration | TEXT |
| Reaching Time | TIME (6) |
| Star Rating | FLOAT |
| Price | FLOAT |
| Seat availability  | INT |

#### 3\. Streamlit App Development

**Approach:**

* Develop a Streamlit app to query and visualize the data from the SQL database.

**Steps:**

1) **Database Connection:** Establish a connection to the SQL database.  
2) **Query Data:** Fetch data from the database to be displayed in the app.  
3) **Filtering:** Use Streamlit components to filter the bus route name, price and star rating

##### Streamlit App Features:

* Display a table of bus routes and schedules.  
* Provide filters for searching by route name, bus type, departing time, etc.

###### *Implementation Steps*

###### *1\. Web Scraping*

1. **Initialize Web Driver:**  
   1. Use Selenium to open the browser and navigate to the target URL.  
   2. Handle page loading and pop-ups.  
2. **Scrape Bus Routes and Details:**  
   1. Identify elements containing bus route links and names.  
   2. Navigate to each route link and extract detailed information.

###### *2\. SQL Database Integration*

1. **Setup Database:**  
   1. Use sqlite3 or pymysql-connector-python to create a database and define table structures.  
   2. Whether check datatypes are same.

###### *3\. Streamlit App Development*

1. **Setup Streamlit:**  
   1. Install Streamlit (pip install streamlit).  
   2. Create a Streamlit script (app.py).  
2. **Database Connection:**  
   1. Use sqlite3 or another connector to connect to the database.  
3. **Query and Display Data:**  
   1. Fetch data from the database and use Streamlit components to display it.  
4. **Add Filters and Analysis:**  
   1. Use Streamlit widgets to add filters for route name, bus type, etc.  
   2. Use Streamlit to analyse data

By following this approach, you can automate the scraping of bus route details, store the data in an SQL database, and create an interactive Streamlit app for data analysis.  
