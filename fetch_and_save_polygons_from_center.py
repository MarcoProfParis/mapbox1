def fetch_and_save_polygons_from_center(center_lon, center_lat, radius, geojson_path= None):
    """
    Fetch polygons within a bounding box defined by a center and radius and save as GeoJSON.
    
    Parameters:
    - center_lon, center_lat: Coordinates of the center point.
    - radius: Radius around the center point in degrees.
    - tags: Dictionary of OSM tags to filter specific features (e.g., {'building': True}).
    - geojson_path: Path to save the GeoJSON file.
    """
    tags = {'amenity': 'parking'}
    feature_tags = {
    'service': True,
     'highway':True
    #service=parking_aisle
    }
    # Calculate the bounding box coordinates based on the center and radius
    bbox = ox.utils_geo.bbox_from_point((center_lat, center_lon), dist=radius)
    north, south, west, east = bbox
    # Fetch polygons from OSM
    polygons = ox.geometries_from_bbox(north=north, south=south, east=east, west=west, tags=tags)
    polygons = polygons[polygons.geometry.notnull()]  # Ensure valid geometries

    features = ox.geometries_from_bbox(north, south, east, west, tags=feature_tags)
    
    # Find features within parking areas
    features_within = features[
        features.geometry.apply(
            lambda geom: any(geom.within(poly) for poly in polygons.geometry)
        )
    ]

    # Save polygons to GeoJSON
    if geojson_path != None:
        polygons.to_file(geojson_path, driver="GeoJSON")
        print(f"Polygons saved to {geojson_path}")
    #filter(west,south,east,north,geojson_path)
    return polygons,features_within,bbox
