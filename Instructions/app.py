import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

app = Flask(__name__)


#################################################
# Flask Routes
#################################################

#################################################
# API ROUTES
#################################################

@app.route("/")
def Home():
    """List all available api routes."""
    return (
        f"Welcome to the API!<br/><br/>"
        f"Available Routes:<br/>"
        f"Date range available: 2010-01-01 to 2017-08-23<br/><br/>"
        f"Precipitation information from last year<br/>"
        f"/api/v1.0/precipitation <br/><br/>"
        f"Available Stations<br/>"
        f"/api/v1.0/stations <br/><br/>" 
        f"Temperature information from last year<br/>" 
        f"/api/v1.0/tobs <br/><br/>"
        f"Enter a start date in yyyy-mm-dd format to obtain temperature min,max,avg:<br/>"
        f"/api/v1.0/<start> <br/><br/>"
        f"Enter a start/end date in yyyy-mm-dd format to obtain temperature min,max,avg:<br/>"
        f"/api/v1.0/<start>/<end> <br/>"
    )
#################################################
# API PRECIPITATION
#################################################

@app.route("/api/v1.0/precipitation")
def pcrp():
    """Return precipitation query"""
#Building query
    precipitation = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= '2016-08-23').order_by(Measurement.date)
    
    rain = []
    for result in precipitation:
        prcp_dict = {}
        prcp_dict["date"] = result.date
        prcp_dict["precipitation"] = result.prcp
        rain.append(prcp_dict)

    return jsonify(rain)

#################################################
# API STATIONS
#################################################

@app.route("/api/v1.0/stations")
def stations():
    """Return a list of all stations from the dataset"""
    # Query all stations
    results = session.query(Station.name).all()

    # Convert list of tuples into normal list
    station_list = list(np.ravel(results))

    return jsonify(station_list)

#################################################
# API TEMPS
#################################################

@app.route("/api/v1.0/tobs")
def temperature():
    """Return precipitation query"""
#Building query
    temp = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= '2016-08-23').order_by(Measurement.date)
# Create dictionary
    temps = []
    for result in temp:
        temp_dict = {}
        temp_dict["date"] = result.date
        temp_dict["Temperature"] = result.tobs
        temps.append(temp_dict)

    return jsonify(temps)

#################################################
# API START DATE
#################################################
@app.route("/api/v1.0/<start>")
def start_date(start):
#Building query
    trip_dates = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
   
    trip = []
    for result in trip_dates:
        trip_dict = {}
        trip_dict["Min Temp"] = result[0]
        trip_dict["Avg Temp"] = result[1]
        trip_dict["Max Temp"] = result[2]
        trip.append(trip_dict)

    return jsonify(trip)

#################################################
# API START DATE - END DATE
#################################################

@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start,end):
#Building query
    tripr_dates = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start, Measurement.date <= end).all()
   
    trip_r = []
    for result in tripr_dates:
        trip_r_dict = {}
        trip_r_dict["Start Date"] =start
        trip_r_dict["End Date"] = end
        trip_r_dict["Average Temperature"] = result[0]
        trip_r_dict["Highest Temperature"] = result[1]
        trip_r_dict["Lowest Temperature"] = result[2]
        trip_r .append(trip_r_dict)
    return jsonify(trip_r )

if __name__ == '__main__':
    app.run(debug=True)