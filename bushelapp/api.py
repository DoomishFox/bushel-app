from flask import Blueprint, g, redirect, request, jsonify
from .database import db_session
from .models import AuthToken, Backlink, Leaf

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/backlinks/<leaf_uri>', strict_slashes=False)
def backlinks(leaf_uri):
    ''' get all backlinks for a leaf '''

    leaf_obj = db_session.query(Leaf).filter(Leaf.uri == leaf_uri).first()
    print(f"Leaf {leaf_obj.name} with ID of {leaf_obj.id}")

    if leaf_obj is not None:
        # this means a leaf exists so we can get all backlinks pointing to it
        backlink_objs = list(db_session.query(Backlink).filter(Backlink.target_id == leaf_obj.id))
        backlinks = []
        for backlink in backlink_objs:
            # iterate through them and get all leaf names and uris
            # this will get passed back as a json list

            # first get the parent leaf info
            parent = db_session.query(Leaf).filter(Leaf.id == backlink.parent_id).first()
            backlinks.append([parent.uri, parent.name])
        # now we want to return this list of backlinks
        return jsonify(backlinks)