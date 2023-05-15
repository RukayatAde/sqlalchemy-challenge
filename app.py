# Import the dependencies.

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
engine = create_engine("sqlite:///C:/Users/User/Downloads/Starter_Code (7)/Starter_Code/Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)


# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation:<br/>"
        f"/api/v1.0/stations:<br/>"
        f"/api/v1.0/tobs:<br/>"
        f"/api/v1.0/start:<br/>"
        f"/api/v1.0/start/end"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():

    # Create our session (link) from Python to the DB
    session = Session(engine)
    a_year_ago_date = dt.date(2017,8,23) - dt.timedelta(days = 365)
    precipitation_data = session.query(measurement.date, measurement.prcp).filter(measurement.date >= a_year_ago_date).all()

    prcp_dict = {date: prcp for date, prcp in precipitation_data}
    session.close()
    return jsonify(prcp_dict)

@app.route("/api/v1.0/stations")
def stations():

    session = Session(engine)
    stations = session.query(station.station).all()
    stations_list = list(np.ravel(stations))
    session.close()
    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs():

    session = Session(engine)
    a_year_ago_date = dt.date(2017,8,23) - dt.timedelta(days = 365)
    actv_stations = session.query(measurement.date, measurement.tobs).filter(measurement.station == 'USC00519281').\
                       filter(measurement.date >= a_year_ago_date).all()
    temp_list = list(np.ravel(actv_stations))
    session.close()
    return jsonify(temp_list)

@app.route("/api/v1.0/start")
def start():
       
    start_date = dt.date(2010,1,1)  
    session = Session(engine)
    result = session.query(func.min(measurement.tobs),func.max(measurement.tobs), func.avg(measurement.tobs)).\
                 filter(measurement.date >= start_date).all()
    result_list = list(np.ravel(result))
    session.close()
    return jsonify(result_list)

@app.route("/api/v1.0/start/end")
def date_range():

    start_date = dt.date(2010,1,1)
    end_date = dt.date(2017,8,23)
    session = Session(engine)
    results = session.query(func.min(measurement.tobs),func.max(measurement.tobs), func.avg(measurement.tobs)).\
                 filter(measurement.date >= start_date).filter(measurement.date <= end_date).all()
    results_list = list(np.ravel(results))
    session.close()
    return jsonify(results_list)

if __name__ == '__main__':
    app.run(debug=True)