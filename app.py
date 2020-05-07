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
        f"Welcome to the Hawaii API!\<br/>"
        f"Here you can retrieve weather data to plan your surfing trip.<br/>"
        f"Available routes:</br>"
        f"/api/v1.0/precipitation"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    
    # Return last date
    end_date_query = session.query(Measurement.date).order_by(Measurement.date.desc()).first()

    # Calculate the date 1 year ago from the last data point in the database
    for date in end_date_query:
        date_str = date
        
    year = int(date_str[:4])
    day = int(date_str[-2:])
    month = int(date_str[5:7])
    end_date = dt.date(year, month, day)
    start_date = end_date - dt.timedelta(days = 365)

    # Perform a query to retrieve the data and precipitation scores
    prcp_results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= start_date).\
        filter(Measurement.date <= end_date).\
        order_by(Measurement.date).all()
    
    session.close()

    all_prcp = []
    for date, prcp in prcp_results:
        prcp_dict = {}
        prcp_dict['date'] = date
        prcp_dict['prcp'] = prcp
        all_prcp.append(prcp_dict)

    return(jsonify(all_prcp))


# @app.route("/api/v1.0/stations")

# @app.route("/api/v1.0/tobs")

# @app.route("/api/v1.0/<start>")

# @app.route("/api/v1.0/<start>/<end>")


if __name__ == '__main__':
    app.run(debug = True)
