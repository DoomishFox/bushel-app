from flask import Blueprint, g, redirect, request, jsonify
from flask.helpers import stream_with_context

from bushelapp.api_results import LeafDetailsResult, LeafListResult
from bushelapp.edit import branch
from bushelapp.markdown import getLeafContent
from .database import db_session
from .models import AuthToken, Backlink, Branch, Leaf, Root

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/backlinks/<leaf_uri>', strict_slashes=False)
def backlinks(leaf_uri):
    ''' get all backlinks for a leaf '''

    leaf_obj = db_session.query(Leaf).filter(Leaf.uri == leaf_uri).first()

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

@api.route('/leaves/<leaf_uri>', strict_slashes=False)
def leaves(leaf_uri):
    ''' get leaf data '''
    
    leaf_obj = db_session.query(Leaf).filter(Leaf.uri == leaf_uri).first()

    if leaf_obj is not None:
        branch_obj = db_session.query(Branch).filter(Branch.id == leaf_obj.parent_id).first()
        root_obj = db_session.query(Root).filter(Root.id == branch_obj.parent_id).first()
        # this means a leaf exists so let return its data
        return jsonify(LeafDetailsResult(leaf_obj, branch_obj, root_obj, getLeafContent(leaf_obj)).serialize())

@api.route('/branches/<branch_uri>/leaves', strict_slashes=False)
def branches_list(branch_uri):
    ''' get leaves for branch '''

    branch_id = db_session.query(Branch).filter(Branch.uri == branch_uri).first().id

    if branch_id is not None:
        leaves = db_session.query(Leaf).filter(Leaf.parent_id == branch_id).all()
        return jsonify(LeafListResult(leaves).serialize())