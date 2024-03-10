# Import the dependencies.
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func

from flask import Flask, jsonify


# # Database Setup
# #################################################

# # Create engine using the `hawaii.sqlite` database filecle
engine = create_engine("sqlite:///hawaii.sqlite")
# engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# # Declare a Base using `automap_base()`
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Assign the measurement class to a variable called `Measurement` and
# the station class to a variable called `Station`

Measurement = Base.classes.measurement
# Station = Base.classes.station

# # Create a session
# session = Session(engine)

# #################################################
# # Flask Setup
# #################################################
# app = Flask(__name__)



# #################################################
# # Flask Routes
# #################################################
# @app.route("/")
# def home():
#     return (
#         f"Welcome to the Hawaii Climate App<br/>"
#         f"ALOHA!!<br/>"
#         f" <br/>"
#         f"Available Routes: <br/>"
#         f"/api/v1.0/precipitation<br/>"
#         f"/api/v1.0/stations<br/>"
#         f"/api/v1.0/tobs<br/>"
#         f"<br/>"
#     )

# if __name__ == "__main__":
#     app.run(debug=True)