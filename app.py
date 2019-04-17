import json
from flask import Flask, render_template
import pandas as pd
import requests

#https://github.com/benalexkeen/d3-flask-blog-post/blob/master/app.py
#http://adilmoujahid.com/posts/2015/01/interactive-data-visualization-d3-dc-python-mongodb/
#http://adilmoujahid.com/posts/2016/08/interactive-data-visualization-geospatial-d3-dc-leaflet-python/
app = Flask(__name__)

@app.route("/")
def index():
    url = 'https://feeds.divvybikes.com/stations/stations.json'
    r  = requests.get(url)
    r_load = json.loads(r.text)
    print(r_load['executionTime'])
    df = pd.DataFrame.from_records(r_load['stationBeanList'])[['id','availableBikes','availableDocks','totalDocks','status','lastCommunicationTime','is_renting','longitude','latitude']]
    chart_data = df.to_dict(orient='records')
    chart_data = json.dumps(chart_data, indent=2)
    data = {'chart_data': chart_data}
    return render_template("index.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)

