# Import the dependencies.
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func

import numpy as np
import pandas as pd
import datetime as dt

from flask import Flask, jsonify


# # Database Setup
# #################################################

# # Create engine using the `hawaii.sqlite` database filecle
engine = create_engine("sqlite:////Users/luisherran/Desktop/sqlalchemy-challenge/SurfsUp/hawaii.sqlite")

# # Declare a Base using `automap_base()`
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Assign the measurement class to a variable called `Measurement` and
# the station class to a variable called `Station`

Measurement = Base.classes.measurement
Station = Base.classes.station

# Create a session
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route("/")
def home():
    return (
        f"Welcome to the Hawaii Climate App<br/>"
        f"ALOHA!!<br/>"
        f" <br/>"
        f"Available Routes: <br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"<br/>"
    )


@app.route("/api/v1.0/precipitation")
def prcp():
    one_yr_before = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    one_yr_query = session.query(Measurement.date, Measurement.prcp).\
            filter(Measurement.date > one_yr_before).\
            order_by(Measurement.date).all()
    
    one_yr_list = [{'date': row.date, \
                   'prcp': row.prcp} for row in one_yr_query]
    return jsonify(one_yr_list)

@app.route("/api/v1.0/stations")
def stations():
    station_query = session.query(Station)
    station_list = [{'id':row.id, 'station': row.station, \
                      'latitude': row.latitude, 'longitude': row.longitude, \
                        'elevation': row.elevation} \
                            for row in station_query]
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def temps():
    most_act_df = pd.DataFrame(session.query(func.min(Measurement.tobs).label('min_temp'), \
             func.max(Measurement.tobs).label('max_temp'), \
             func.avg(Measurement.tobs).label('avg_temp')).filter(Measurement.station == 'USC00519281').all())
    most_act_list = most_act_df.values.tolist()
    labels = ['min_temp', 'max_temp', 'avg_temps']
    most_act_list = [dict(zip(labels, sublist)) for sublist in most_act_list]

    return jsonify(most_act_list)

@app.route("/api/v1.0/<start>")
def start(start):
    temps_query = session.query(Measurement.date, Measurement.tobs).\
            filter(Measurement.date > start).all()
    temps_list = [{'date': row.date, \
                   'temps': row.tobs} for row in temps_query]
    canonicalized = start.replace(" ", "").lower()
    for date in temps_list:
        search_term = date["date"].replace(" ", "").lower()

        if search_term == canonicalized:
            return jsonify(date)



if __name__ == "__main__":
    app.run(debug=True)