"""
Vector file helpers for the script entrypoints.

Uses the pure-Python ``pyshp`` package so the repo does not depend on Fiona.
"""
import os

import shapefile
from pyproj import CRS


def _shape_type(geometry_type):
    if geometry_type == 'Point':
        return shapefile.POINT
    if geometry_type == 'LineString':
        return shapefile.POLYLINE
    raise ValueError(f'Unsupported geometry type: {geometry_type}')


def _field_type(value):
    if isinstance(value, bool):
        return ('L', 1, 0)
    if isinstance(value, int):
        return ('N', 18, 0)
    if isinstance(value, float):
        return ('F', 18, 8)
    return ('C', 254, 0)


def _field_names(properties):
    field_names = {}
    used = set()

    for index, name in enumerate(properties):
        safe_name = ''.join(ch if ch.isalnum() else '_' for ch in name).upper()
        safe_name = safe_name[:10] or f'FIELD{index}'

        candidate = safe_name
        suffix = 1
        while candidate in used:
            suffix_text = str(suffix)
            candidate = f'{safe_name[:10 - len(suffix_text)]}{suffix_text}'
            suffix += 1

        used.add(candidate)
        field_names[name] = candidate

    return field_names


def _write_geometry(writer, feature):
    geometry = feature['geometry']
    coordinates = geometry['coordinates']

    if geometry['type'] == 'Point':
        writer.point(*coordinates)
        return

    if geometry['type'] == 'LineString':
        writer.line([list(coordinates)])
        return

    raise ValueError(f"Unsupported geometry type: {geometry['type']}")


def write_shapefile(features, directory, filename, crs):
    """
    Write GeoJSON-like features to an ESRI Shapefile.
    """
    if not features:
        raise ValueError('At least one feature is required')

    os.makedirs(directory, exist_ok=True)

    base_path = os.path.splitext(os.path.join(directory, filename))[0]
    geometry_type = features[0]['geometry']['type']
    field_names = _field_names(features[0]['properties'])

    writer = shapefile.Writer(base_path, shapeType=_shape_type(geometry_type))
    writer.autoBalance = 1

    for original_name, value in features[0]['properties'].items():
        field_type, size, decimal = _field_type(value)
        writer.field(field_names[original_name], field_type, size=size, decimal=decimal)

    for feature in features:
        _write_geometry(writer, feature)
        writer.record(*[feature['properties'][name] for name in field_names])

    writer.close()

    with open(f'{base_path}.prj', 'w', encoding='utf-8') as prj_file:
        prj_file.write(CRS.from_user_input(crs).to_wkt())
