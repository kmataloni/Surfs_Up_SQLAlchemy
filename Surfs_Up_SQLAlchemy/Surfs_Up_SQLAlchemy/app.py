from flask import Flask, jsonify

app = Flask(__name__)

#route to home page
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return "Welcome to my Home page!"

#List all available api routes.
@app.route("/welcome")
def welcome():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"


@app.route("/api/v1.0/precipitation")
def precipitation():
    
    session = Session(engine)
    
    results = session.query(measurement.date, measurement.prcp).all()
    
    precipitation_data = []
    
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = precipitation
        precipitation_data.append(precipitation_dict)
    
    return jsonify(precipitation_data)

@app.route("/api/v1.0/stations")
def stations():
    
    session = Session(engine)
    
    results = session.query(station.name).all()
    
    stations_data = list(np.ravel(results))
    
    return jsonify (stations_data)

@app.route("/api/v1.0/tobs")
def tobs():
    
    session = Session(engine)
    
    #most recent data
    query_1 = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   
    #data from last 12 months
    prcp_results = session.query(measurement.date, measurement.prcp).\
    filter(measurement.date >= query_1).\
    order_by(measurement.date).all()
    
    last_twelve = list(np.ravel(prcp_results))
    
    return jsonify(last_twelve)

@app.route("/<start>")
def start_day(start): 
    start_day = session.query(measurement.date, func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
        filter(measurement.date>=start).\
        group_by(measurement.date).all()
        
        start_day_data = list(np.ravel(start_day))
        
        return jsonify(start_day_data)

@app.route("/<start>/<end>")
def start_day(start, end): 
    start_end_day = session.query(measurement.date, func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
        filter(measurement.date>=start).\
        filter(measurement.date<=end).\
        group_by(measurement.date).all()
        
        start_end_day_data = list(np.ravel(start_end_day))
        
        return jsonify(start__end_day_data)

if __name__ == '__main__':
    app.run(debug=True)