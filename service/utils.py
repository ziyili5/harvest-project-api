import flask as g
import psycopg2
import psycopg2.extras
from config import ProdConfig


def generate_geo_json(geom, props=None):
    """Generate geojson according to geom."""
    geojson = {
        'type': 'FeatureCollection',
        'crs': {
            'type': 'name',
            'properties': {
                'name': 'EPSG:4326'
            }
        },
        'features': [{
            'type': 'Feature',
            'geometry': None,
            'properties': None
        }]
    }
    geojson['features'][0]['geometry'] = geom
    geojson['features'][0]['properties'] = props

    return geojson


def get_db():
    """
    Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'psycopg_db'):
        print("No DB connection yet.")
        g.psycopg_db = connect_db()
    return g.psycopg_db


def connect_db():
    """Connects to the specific database."""
    conn = psycopg2.connect(ProdConfig.SQLALCHEMY_DATABASE_URI)
    return conn
