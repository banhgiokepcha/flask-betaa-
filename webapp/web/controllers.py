from sqlalchemy import desc, func
from flask import render_template, Blueprint, flash, redirect, url_for, current_app #flask_login, flask_required
from .models import db, Markers, Activity
from flask_login import current_user, login_required
from folium.map import Marker
from jinja2 import Template
import json
from flask import jsonify
from flask import request

import folium

app_blueprint = Blueprint(
    'web',
    __name__,
    template_folder='./templates',
    #url_prefix="/main"
    )

@app_blueprint.route('/getmap')
@login_required
def getMap():
    return redirect(url_for('web.mapView'))

@app_blueprint.route('/map')
@login_required
def mapView():
    map = folium.Map(width=1800, height=800,location=[21.0278, 105.8342] , zoom_start=12)

    #load json file
    with open('places.json', encoding='utf-8') as places: 
        file_contents = places.read()
    print(file_contents)
    content=json.loads(file_contents)
    places=content["outdoor recreation places"]
    for place in places:
     name=place["name"]
     popup_html = "<span>Name: {} </span>".format(name)
     print(f"This is {name}")
     folium.Marker(
        location=[float(place["latitude"]), float(place["longitude"])],
        popup = folium.Popup(
        html=popup_html,
        max_width=200,
        show=False,
        sticky=False,        
        lazy=True
    )).add_to(map)


    iframe = map.get_root()._repr_html_()
    return render_template("mainmap.html", iframe=iframe)

@app_blueprint.route('/mymap', methods=['GET', 'POST'])
@login_required
def get_user_map():
   return render_template('mymap.html', current_user=current_user)

@app_blueprint.route('/getmarker', methods=['GET'])
@login_required
def get_markers():
   markers = Markers.query.all()
   markers_data = []

   for marker in markers:
      marker_data = {
         'id': marker.id,
         'name': marker.title,
         'lat': marker.lat,
         'lon': marker.lon
      }
      markers_data.append(marker_data)
      print(markers_data)
   return json.dumps(markers_data)

@app_blueprint.route('/addmarker', methods=['POST'])
@login_required
def add_marker():
 #retrieve from database
 name = request.form["Name"]
 description = request.form["Activity"]
 lat = request.form.get('lat')
 lon = request.form.get('lon')
 new_marker = Markers(title=name, description=description, lat=lat, lon=lon, user_id = current_user.id)
 try: 
    db.session.add(new_marker)
    db.session.commit()
 except Exception as e:
    print(str(e))
    db.session.rollback()
    print({'error': 'Failed to add marker'})

 else:
    print(new_marker)
    return redirect(url_for('.get_user_map'))

@app_blueprint.route('/delete', methods=['POST'])
@login_required
def delete():
   data=request.json.get('marker_id')
   marker = Markers.query.filter_by(id=data).first()
   if marker is None:
      print("can't delete marker")
      return "False"
   print(marker)
   db.session.delete(marker)
   db.session.commit()
   print("deleted")
   return "True"







