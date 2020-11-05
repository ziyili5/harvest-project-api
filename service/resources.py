import json
import traceback
from datetime import datetime

import psycopg2
import psycopg2.extras
from flask import jsonify, request, abort
from flask_restful import Resource
from flask_sqlalchemy import SQLAlchemy

from response import BasicResponse
from models import User, UserField
from utils import generate_geo_json, get_db

postgresql = SQLAlchemy()

class UserResource(Resource):
    """user login"""

    def post(self):

        # This could probably all be obtained from Kong X-Userinfo header when it's added
        userjson = request.json
        userquery = postgresql.session.query(User).filter_by(userid=userjson['email']).all()
        try:
            if len(userquery) > 0:
                user = userquery[0]
                user.lastlogin = datetime.now()
                postgresql.session.commit()
                return BasicResponse.create_basic_response(200, "Welcome back, " + user.firstname)
            else:

                user = User(userid=userjson["email"], firstname=userjson["firstName"], lastname=userjson["lastName"],
                            lastlogin=datetime.now())
                postgresql.session.add(user)
                postgresql.session.commit()
                return BasicResponse.create_basic_response(200, "Hello new user, " + userjson["firstName"])
        except Exception as e:
            status_code = 500
            msg = "Cannot add user: " + str(e)
            return BasicResponse.create_basic_response(status_code, msg)


class UserFieldResource(Resource):
    """add user field"""

    def post(self):
        try:
            # Some of this can come from the X-Userinfo header
            userid = request.get_json()['userid']
            clu = request.get_json()['clu']
            cluname = request.get_json()['cluname']
            lat = request.get_json()['lat']
            lon = request.get_json()['lon']

            # Should we add a user if they don't exist?
            userfieldquery = postgresql.session.query(UserField).filter_by(userid=userid, clu=clu).all()
            # user already add this field, update with new cluname
            if len(userfieldquery) > 0:
                userfield = userfieldquery[0]
                userfield.cluname = cluname
                userfield.lat = lat
                userfield.lon = lon

            else:
                # TODO: check if lat/lon within clu
                userfield = UserField(userid=userid, clu=clu, cluname=cluname, lat=lat, lon=lon)
                postgresql.session.add(userfield)
            postgresql.session.commit()
            return BasicResponse.create_basic_response(200, "Add CLU")
        except Exception:
            status_code = 403
            msg = "Cannot add CLU: " + str(traceback.format_exc())
            return BasicResponse.create_basic_response(status_code, msg)

    """get user field"""

    def get(self):
        all_args = request.args.to_dict()
        if "userid" not in all_args:
            return BasicResponse.create_basic_response(403, "You must provide userid.")
        rows = postgresql.session.query(UserField).filter_by(userid=all_args['userid']).all()
        return jsonify([x.as_dict() for x in rows])

    """delete one user field"""

    def delete(self):
        all_args = request.args.to_dict()
        if "userid" not in all_args:
            return BasicResponse.create_basic_response(400, "You must provide userid.")
        if "clu" not in all_args:
            return BasicResponse.create_basic_response(400, "You must provide clu.")
        try:
            userfield = postgresql.session.query(UserField).filter_by(userid=all_args['userid'], clu=all_args["clu"]).first()
            if userfield:
                postgresql.session.delete(userfield)
                postgresql.session.commit()
                msg = "Delete CLU: " + str(userfield.clu)
                return BasicResponse.create_basic_response(200, msg)
            else:
                msg = "Cannot Delete CLU: Not Found"
                return BasicResponse.create_basic_response(404, msg)
        except Exception:
            status_code = 403
            msg = "Cannot delete CLU: " + str(traceback.format_exc())
            return BasicResponse.create_basic_response(status_code, msg)


class CLUResource(Resource):
    """get CLU from database."""

    def get(self, clu_id=None):

        # Query parameters:
        # lat
        # lon
        all_args = request.args.to_dict()

        # Check if either CLU ID or Lat and Long values are provided. If not, abort with 400 error
        # (Bad request).
        if clu_id is None and ("lat" not in all_args or "lon" not in all_args):
            abort(400)

        db = get_db()
        cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)

        # If input CLU ID is not provided
        if clu_id is None:
            # sql for getting CLU id with lat and lon
            # the following is safe way to avoid sql injection attack
            # refer to http://initd.org/psycopg/docs/usage.html#the-problem-with-the-query-parameters
            sql = """
            SELECT clu.gid, ST_AsGeoJSON(clu.geom) as geojson FROM clu WHERE
            ST_Contains(clu.geom,ST_SetSRID(ST_MakePoint(%s,%s),4326)) and
            st_intersects(clu.geom,ST_SetSRID(ST_MakePoint(%s,%s),4326));
            """
            data = (all_args['lon'], all_args['lat'], all_args['lon'], all_args['lat'])
        # If input CLU ID is provided
        else:
            # sql for getting CLU GeoJSON given CLU ID
            # the following is safe way to avoid sql injection attack
            # refer to http://initd.org/psycopg/docs/usage.html#the-problem-with-the-query-parameters
            # SELECT clu.gid, ST_AsGeoJSON(clu.geom) as geojson FROM clu WHERE clu.gid = (665516);
            sql = """
            SELECT clu.gid, st_asgeojson(clu.geom) as geojson FROM clu WHERE clu.gid = (%s);

            """
            data = (clu_id,)

        # Execute SQL command and get result rows
        cur.execute(sql, data)
        rows = cur.fetchall()

        # If there are no rows in the result, return resource not found error
        if len(rows) == 0:
            abort(404)

        # Obtain specific fields from the result
        clu_id = rows[0][0]
        clu_geojson = rows[0][1]

        # If soil information is not requested, return the current geoJSON
        properties = {'clu_id': clu_id}
        geojson = generate_geo_json(json.loads(clu_geojson), properties)
        return jsonify(geojson)
