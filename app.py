from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func

engine = create_engine("sqlite:///hawaii.sqlite", echo=False)

Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()

Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

query1 = session.query(Measurement.date,Measurement.station,Measurement.prcp).\
filter(Measurement.date >= '2016-08-01').\
filter(Measurement.date <= '2017-08-01').\
order_by(Measurement.date).all()

query2 = session.query(Station.station,Station.name).all()

query5 = session.query(Measurement.date,Measurement.station,Measurement.tobs).\
filter(Measurement.date >= '2016-08-01').\
filter(Measurement.date <= '2017-08-01').\
order_by(Measurement.date).all()

d = [date[0] for date in query1]
p = [prcp[2] for prcp in query1]
s = [station[0] for station in query2]
n = [name[1] for name in query2]
to = [obs[2] for obs in query5]

app = Flask(__name__)
dict1 = dict(zip(d,p))
dict2 = dict(zip(s,n))
dict3 = dict(zip(d,to))

@app.route("/")
def home():
    return (
        f"Welcome to the Hawaii Weather API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    return jsonify(dict1)

@app.route("/api/v1.0/stations")
def stations():
    return jsonify(dict2)

@app.route("/api/v1.0/tobs")
def observations():
    return jsonify(dict3)

if __name__ == "__main__":
    app.run(debug=True)