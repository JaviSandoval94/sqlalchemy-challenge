# Introduction
After weeks of hard work on Python, we are finally off for our surfing vacation trip to Hawaii! This project aims to explore historic climate data retrieved from weather stations there to help plan our surfing vacation for end-summer 2020. Additionaly, the data will be available from an API that will be developed in this same project in the complementary app.py file! The project will use the SQLAlchemy library to connect to a SQLite database containing weahter data from different stations in Hawaii. The project is divided into two separate analyses:
* Precipitation analysis: Plot precipitation data for the last 12 months
* Station analysis: This includes the total number of stations, a list of the most active stations, and the last 12 months of observed temperatures (TOBS).<br>
In addition, a Flask API with different endpoints is designed to retrieve the data based on the created queries. The code for this API is provided as a separate `.py` file.

# Data set
The data for this project comes from the files `hawaii.sqlite`, `hawaii_measurements.csv`, and `hawaii_stations.csv`, all of which were provided by the Tecnológico de Monterrey Data Analytics and Visualization Bootcamp for the February - August 2020 term.

# Code explanation
Make sure to download the complete folders and open them to run the analyses. Also make sure to download all the necessary libraries and create a connection to the SQLite database. The code to create the API is provided in the 
Routes


/


Home page.


List all routes that are available.




/api/v1.0/precipitation


Convert the query results to a dictionary using date as the key and prcp as the value.


Return the JSON representation of your dictionary.




/api/v1.0/stations

Return a JSON list of stations from the dataset.



/api/v1.0/tobs


Query the dates and temperature observations of the most active station for the last year of data.


Return a JSON list of temperature observations (TOBS) for the previous year.




/api/v1.0/<start> and /api/v1.0/<start>/<end>


Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.


When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.


When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
