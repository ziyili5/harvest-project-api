import json
from datetime import datetime

from db import db
from flask import abort
from flask import jsonify
from flask import make_response
from flask import request
from flask_restful import Resource
from models import CLU
from models import User
from models import UserField
from sqlalchemy import func


def create_basic_response(status_code, message):
    return make_response(
        jsonify({"status_code": status_code, "message": message}), status_code
    )


class UserResource(Resource):
    """user login"""

    def post(self):
        # This could probably all be obtained from Kong X-Userinfo header when it's added
        user_json = request.json
        user_query = db.session.query(User).filter_by(user_id=user_json["email"]).all()
        try:
            if len(user_query) > 0:
                user = user_query[0]
                user.last_login = datetime.now()
                db.session.commit()
                return create_basic_response(200, f"Welcome back, {user.first_name}")
            else:
                user = User(
                    user_id=user_json["email"],
                    first_name=user_json["first_name"],
                    last_name=user_json["last_name"],
                    last_login=datetime.now(),
                )
                db.session.add(user)
                db.session.commit()
                return create_basic_response(
                    200, f"Hello new user, {user_json['first_name']}"
                )
        except Exception as e:
            return create_basic_response(500, f"Cannot add user: {str(e)}")


class UserFieldResource(Resource):
    """add user field"""

    def post(self):
        args = request.get_json()
        try:
            # Some of this can come from the X-Userinfo header
            user_id = args["user_id"]
            clu = args["clu"]
            clu_name = args["clu_name"]

            # Should we add a user if they don't exist?
            user_field_query = (
                db.session.query(UserField).filter_by(user_id=user_id, clu=clu).all()
            )
            # user already add this field, update with new clu_name
            if len(user_field_query) > 0:
                user_field = user_field_query[0]
                user_field.clu_name = clu_name
            else:
                user_field = UserField(user_id=user_id, clu=clu, clu_name=clu_name)
                db.session.add(user_field)
            db.session.commit()
            return create_basic_response(200, "Add CLU")
        except Exception as e:
            return create_basic_response(403, f"Cannot add CLU: {e}")

    """get user field"""

    def get(self):
        all_args = request.args.to_dict()
        user_id = all_args.get("user_id")
        if not user_id:
            return create_basic_response(403, "You must provide user_id.")
        rows = db.session.query(UserField).filter_by(user_id=user_id).all()
        return jsonify([x.as_dict() for x in rows])

    """delete one user field"""

    def delete(self):
        all_args = request.args.to_dict()

        user_id = all_args.get("user_id")
        clu = all_args.get("clu")

        if not user_id:
            return create_basic_response(400, "You must provide user_id.")
        if not clu:
            return create_basic_response(400, "You must provide clu.")

        try:
            user_field = (
                db.session.query(UserField).filter_by(user_id=user_id, clu=clu).first()
            )
            if user_field:
                db.session.delete(user_field)
                db.session.commit()
                return create_basic_response(200, f"Delete CLU: {user_field.clu}")
            else:
                return create_basic_response(404, "Cannot Delete CLU: Not Found")
        except Exception as e:
            return create_basic_response(403, f"Cannot delete CLU: {e}")


class CLUResource(Resource):
    """
    get CLU from database.
    Query parameters:
        - lat
        - lon
    """

    def get(self, clu_id=None):
        all_args = request.args.to_dict()

        lat = all_args.get("lat")
        long = all_args.get("long")

        # Check if either CLU ID or Lat and Long values are provided. If not, abort with 400 error
        # (Bad request).
        if clu_id is None and (not lat or not long):
            abort(400)

        # If input CLU ID is not provided
        if clu_id is None:
            point = (
                db.session.query(
                    func.ST_SetSRID(func.ST_MakePoint(long, lat), 4326).label("point")
                )
                .first()
                .point
            )
            query = db.session.query(
                CLU, CLU.geom.ST_ASGeoJSON().label("geojson")
            ).filter(func.ST_Intersects(CLU.geom, point))
        # If input CLU ID is provided
        else:
            query = db.session.query(
                CLU, CLU.geom.ST_ASGeoJSON().label("geojson")
            ).filter(CLU.gid == clu_id)

        # Execute SQL command and get result rows
        clu = query.first()

        # If there are no rows in the result, return resource not found error
        if not clu:
            abort(404)

        # Obtain specific fields from the result
        clu_id = clu.CLU.gid
        clu_geojson = json.loads(clu.geojson)
        clu_geojson["properties"] = {"clu_id": clu_id}

        return clu_geojson
