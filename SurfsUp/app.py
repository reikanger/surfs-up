#!/usr/bin/env python

# Import the dependencies.
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

import datetime as dt

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

##### Precipitation Query #####

# Find the most recent date in the data set.
most_recent_date = session.query(func.max(measurement.date)).scalar()

# Calculate the date one year from the last date in data set.
most_recent_dt = dt.datetime.strptime(most_recent_date, '%Y-%m-%d')
days = 30 * 12
one_year_from_recent_dt = most_recent_dt - dt.timedelta(days=days)

# Perform a query to retrieve the data and precipitation scores
dates_prcps = session.query(measurement).\
    filter(measurement.date >= one_year_from_recent_dt, measurement.date <= most_recent_date)\
    .with_entities(measurement.date, measurement.prcp).all()

precips_dict = dict(dates_prcps)

##### Stations Query #####
unique_stations = session.query(station.station.distinct()).all()
stations_list = [s[0] for s in unique_stations]
stations = {'Stations': stations_list}

##### TOBS Query #####

##### Start Query #####

##### Start End Query #####

# close the database session
session.close()

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    return (
        f"Welcome to the Climate App API!<br/><br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    return jsonify(precips_dict)

@app.route("/api/v1.0/stations")
def stations():
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    return False

@app.route("/api/v1.0/<start>/<end>")
def start_end():
    return False

# Run web server if run directly
if __name__ == "__main__":
    app.run(debug=True)
