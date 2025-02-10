from flask import Flask, jsonify, request
import osmnx as ox
import geopandas as gpd

app = Flask(__name__)

def fetch_polygons(center_lon, center_lat, radius):
    """
    Fetch polygons within a bounding box defined by a center and radius.
    """
    tags = {'amenity': 'parking'}
    feature_tags = {'service': True, 'highway': True}

    # Compute bounding box
    bbox = ox.utils_geo.bbox_from_point((center_lat, center_lon), dist=radius)
    north, south, west, east = bbox

    # Fetch polygons
    polygons = ox.geometries_from_bbox(north, south, east, west, tags)
    polygons = polygons[polygons.geometry.notnull()]  

    # Fetch features
    features = ox.geometries_from_bbox(north, south, east, west, feature_tags)
    features_within = features[features.geometry.apply(
        lambda geom: any(geom.within(poly) for poly in polygons.geometry)
    )]

    return polygons.to_json(), features_within.to_json(), bbox


@app.route("/get_polygons", methods=["GET"])
def get_polygons():
    """API endpoint to return polygons."""
    center_lon = float(request.args.get("lon", -79.4512))  # Default value
    center_lat = float(request.args.get("lat", 43.6568))
    radius = float(request.args.get("radius", 1000))

    polygons_json, features_json, bbox = fetch_polygons(center_lon, center_lat, radius)

    return jsonify({
        "polygons": polygons_json,
        "features": features_json,
        "bbox": bbox
    })

if __name__ == "__main__":
    app.run(debug=True)
