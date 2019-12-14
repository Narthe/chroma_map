from pathlib import Path
import json
import pprint
import random
import folium

chroma_color_scheme = ['#002A49', '#18617C', '#E23200', '#F29311']

# read export file from OpenStreetMap and parse it as json
def export_polygons(input_json_file, output_filename):

    d = json.loads(open(input_json_file.read()))
    d2 = dict(type='FeatureCollection', features=list())

    # Removing markers, streets, etc, keeping only polygons
    for feature in d['features']:
        if feature['geometry']['type'] == 'Polygon':
            d2['features'].append(feature)

    # Saving to output file to be cleaned
    try:
        Path.mkdir(Path.cwd() / Path('output'))
    except:
        pass
    output_path = Path('output', output_filename)

    with open(str(output_path), 'w') as outfile:
        json.dump(d2, outfile)

    return output_path

def create_choropleth(input_json_file, output_html_filename):

    geo_json_data = json.loads(open(input_json_file).read())

    try:
        Path.mkdir(Path.cwd() / Path('output'))
    except:
        pass
    output_html_path = Path('output', output_html_filename)

    # Creating empty map centered on zone of interest
    m = folium.Map([48.4550, -2.0500], zoom_start=15, tiles=None)

    # creating the Choropleth
    folium.GeoJson(
        geo_json_data,
        style_function=lambda feature: {
            'fillColor': random.choice(chroma_color_scheme),
            'fillOpacity': 1,
            'color': 'black',
            'weight': 0,
            'stroke': False
        }
    ).add_to(m)

    # Saving choropleth to html
    m.save(str(output_html_path))

    return output_html_path


if __name__ == '__main__':

    input_json = f'D:/dev/chroma_map/dinan.json'

    # cleaned_json = export_polygons(input_json, 'dinan_only_polygon.json')

    # Manual cleaning at this point if needed using http://geojson.io/ just for artistic reasons

    cleaned_json = str(Path("D:/dev/chroma_map/dinan_cleaned.json"))
    print(create_choropleth(cleaned_json, "output.html"))