import json
from flask import Flask, render_template, request
import pandas as pd
import requests
import os
import geopandas as gpd

#https://github.com/benalexkeen/d3-flask-blog-post/blob/master/app.py
#http://adilmoujahid.com/posts/2015/01/interactive-data-visualization-d3-dc-python-mongodb/
#http://adilmoujahid.com/posts/2016/08/interactive-data-visualization-geospatial-d3-dc-leaflet-python/
app = Flask(__name__)
#set up route flask ,

#Live Station Data:
url = 'https://feeds.divvybikes.com/stations/stations.json'
r  = requests.get(url)
r_load = json.loads(r.text)
print(r_load['executionTime'])
df = pd.DataFrame.from_records(r_load['stationBeanList'])[['id','availableBikes','availableDocks','totalDocks','status','lastCommunicationTime','is_renting','longitude','latitude']]
chart_data = df.to_dict(orient='records')
chart_data = json.dumps(chart_data, indent=2)
f = 64
#Test CSV Data
df2 = pd.read_csv('data.csv').drop('Open', axis=1)
chart_data2 = df2.to_dict(orient='records')
chart_data2 = json.dumps(chart_data2, indent=2)

#Bike Path GeoJson Data:
df3 = gpd.read_file('Chicago_BikePaths.geojson')
df3 = df3.to_json()

data = {'chart_data': chart_data,'chart_data2': chart_data2,'chart_data3': df3}

@app.route("/")
def index():
    return render_template("index3.html", data=data,f=f)

@app.route("/Suggested_Route", methods=['POST','GET'])
def optimal_path():
	if request.method=='POST':
		s=request.form.get('start_station',None)
		ff=request.form['end_station']
        
		return render_template('index3.html', f=s, last_name=ff,data=data)
	else:
		return render_template('index3.html', data=data,f=f)

if __name__ == "__main__":
    app.run(debug=True)



