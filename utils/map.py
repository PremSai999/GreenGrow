import folium
import pandas as pd
import folium.plugins as plugins
from folium.features import LatLngPopup
from jinja2 import Template


data = pd.read_csv('Data/data1.csv')
# Add a feature that displays the nearest attributes when a point is clicked
# def find_nearest(lat, lon):
#     """Find the nearest data point to the given Latitude and Longitude"""
#     distances = ((row["Latitude"] - lat)**2 + (row["Longitude"] - lon)**2 for _, row in data.iterrows())
#     index = min(range(len(distances)), key=distances.__getitem__)
#     return data.loc[index]

# def on_click(e):
#     """Handle a click event on the map"""
#     lat, lon = e.latlng
#     if any((row["Latitude"] == lat and row["Longitude"] == lon) for _, row in data.iterrows()):
#         return
#     nearest = find_nearest(lat, lon)
#     folium.Marker(location=[lat, lon], tooltip="New Point").add_to(m)

def func():
    # Load the data from a CSV file

    # Create a map centered on the mean Latitude and Longitude of the data
    map_center = [15.9129, 79.7400]
    m = folium.Map(location=map_center, zoom_start=7)

    # Add markers for each data point
    for i, row in data.iterrows():
        marker = folium.Marker(location=[row["Latitude"], row["Longitude"]],
                            tooltip=f"{row['District']}")
        marker.add_to(m)
        marker.add_child(folium.Popup(f"<b>Soil Type:</b> {row['Soil type']}"))
        marker.add_child(folium.ClickForMarker(popup="Click to add a new point"))
    folium.plugins.LocateControl().add_to(m)
    m.add_child(GetLatLngPopup())
    m.add_child(folium.plugins.MousePosition())
    m.add_child(folium.LayerControl())
    m.add_child(folium.plugins.MeasureControl())
    m.add_child(folium.plugins.Fullscreen())
    return m

class GetLatLngPopup(LatLngPopup):
    _template = Template(u"""
            {% macro script(this, kwargs) %}
                var {{this.get_name()}} = L.popup();
                function latLngPop(e) {
                parent.parent.document.getElementById("latitude").value = e.latlng.lat.toFixed(4);
                parent.parent.document.getElementById("longitude").value = e.latlng.lng.toFixed(4); 
                $(document).ready(function() {
                $.ajax({
                    type: 'POST',
                    url: '/tech',
                    dataType: 'json',
                    data: {
        "lat": e.latlng.lat.toFixed(4),
        "lng": e.latlng.lng.toFixed(4)
    },
                    success: function(response) {
                    parent.parent.document.getElementById("soil").value = response["Soil type"];
                    parent.parent.document.getElementById("ph").value = response["pH"]; 
                    parent.parent.document.getElementById("p").value = response["Avail-P"]; 
                    parent.parent.document.getElementById("k").value = response["Exch-K"];  
                    parent.parent.document.getElementById("oc").value = response["OC"]; 
                    parent.parent.document.getElementById("s").value = response["Avail-S"];
                    }
                });
                });
                    {{this.get_name()}}
                        .setLatLng(e.latlng)
                        .setContent("Latitude: " + e.latlng.lat.toFixed(4) +
                                    "<br>Longitude: " + e.latlng.lng.toFixed(4) )
                        .openOn({{this._parent.get_name()}});
                    return e.latlng.lat.toFixed(4);
                    } 
                {{this._parent.get_name()}}.on('click', latLngPop);
            {% endmacro %}
            """)

    def __init__(self):
        super(GetLatLngPopup, self).__init__()
        self._name = 'GetLatLngPopup'
