# Import dependencies
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Setup engine connection
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect = True)

Measurement = Base.classes.measurement
Station = Base.classes.station

# Declare API initial setup
app = Flask(__name__)

@app.route("/")
def home():
    "List all available API routes."
    return(
        f"Welcome to the Hawaii API!<br/>"
        f"Here you can retrieve weather data to plan your surfing trip.<br/>"
        f"Available routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start/2017-03-15<br/>"
        f"/api/v1.0/start/2016-03-15/end/2017-03-15"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    # Return last date
    end_date_query = session.query(Measurement.date).order_by(Measurement.date.desc()).first()

    for date in end_date_query:
        date_str = date
        
    year = int(date_str[:4])
    day = int(date_str[-2:])
    month = int(date_str[5:7])
    end_date = dt.date(year, month, day)

    # Calculate the date 1 year ago from the last data point in the database
    start_date = end_date - dt.timedelta(days = 365)

    # Perform a query to retrieve the data and precipitation scores
    prcp_results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= start_date).\
        filter(Measurement.date <= end_date).\
        order_by(Measurement.date).all()
    
    session.close()

    # Return jsonified list of date and precipitation
    all_prcp = []
    for date, prcp in prcp_results:
        prcp_dict = {}
        prcp_dict['date'] = date
        prcp_dict['prcp'] = prcp
        all_prcp.append(prcp_dict)

    return(jsonify(all_prcp))

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    # Perform a query to count each station's measurements
    stations_ordered = session.query(Measurement.station, func.count(Measurement.station)).\
        group_by(Measurement.station).\
        order_by(func.count(Measurement.station).desc()).\
        all()
    session.close()

    # Return jsonified list of stations and measurements
    stations_list = []
    for station, measurements in stations_ordered:
        station_dict = {}
        station_dict['id'] = station
        station_dict['measurements'] = measurements
        stations_list.append(station_dict)
    
    return(jsonify(stations_list))
    

@app.route("/api/v1.0/tobs")
def temperatures():
    session = Session(engine)

    # Query station with most measurements
    most_active_station = session.query(Measurement.station, func.count(Measurement.station)).\
        group_by(Measurement.station).\
        order_by(func.count(Measurement.station).desc()).\
        first()

    most_active_id, most_active_count = most_active_station

    # Query temperatures of most active station
    temp_summary = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == most_active_id)

    session.close()

    # Return jsonified list of stations and measurements
    temp_list = []
    for date, temp in temp_summary:
        temp_dict = {}
        temp_dict['date'] = date
        temp_dict['temp'] = temp
        temp_list.append(temp_dict)

    return(jsonify(temp_list))

@app.route("/api/v1.0/start/<start>")
def startDate(start):
    session = Session(engine)

    # Query min, avg and minimum temperatures after start date
    temp_summary = session.query(func.min(Measurement.tobs),
        func.max(Measurement.tobs),
        func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start)

    session.close()
    
    for record in temp_summary:
        min_temp, max_temp, avg_temp = record

    # Return jsonified temperature summary
    temp_dict = {'Min T': min_temp, 'Max T': max_temp, 'Avg T': avg_temp}
    
    return jsonify(temp_dict)

@app.route("/api/v1.0/start/<start>/end/<end>")
def startEndDate(start, end):
    session = Session(engine)

    # Query min, avg and minimum temperatures after start date and before end date
    temp_summary = session.query(func.min(Measurement.tobs),
        func.max(Measurement.tobs),
        func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end)

    session.close()

    for record in temp_summary:
        min_temp, max_temp, avg_temp = record

    # Return jsonified temperature summary
    temp_dict = {'Min T': min_temp, 'Max T': max_temp, 'Avg T': avg_temp}
    
    return jsonify(temp_dict)

if __name__ == '__main__':
    app.run(debug = True)
