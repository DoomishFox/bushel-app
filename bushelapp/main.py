from flask import Blueprint, render_template, abort
from .database import db_session
from .models import Root, Branch, Leaf

main = Blueprint('main', __name__)

@main.route('/', strict_slashes=False)
def index():
    return render_template('index.html')

@main.route('/<root_name>/<branch_name>/<page_name>', strict_slashes=False)
def leaf(root_name, branch_name, page_name):
    root_obj = db_session.query(Root).filter(Root.uri == root_name).first()
    if root_obj is not None:
        # root object found, check for branch object
        branch_obj = db_session.query(Branch).filter(Branch.parent_id == root_obj.id).filter(Branch.uri == branch_name).first()
        if branch_obj is not None:
            # branch object found, go ahead and allow template to complete
            leaf_obj = db_session.query(Leaf).filter(Leaf.parent_id == branch_obj.id).filter(Leaf.uri == page_name).first()
            if leaf_obj is not None:
                return render_template("leaf.html", root=root_obj, branch=branch_obj, page=leaf_obj)
    abort(404)

@main.route('/<root_name>/<branch_name>', strict_slashes=False)
def branch_home(root_name, branch_name):
    root_obj = db_session.query(Root).filter(Root.uri == root_name).first()
    if root_obj is not None:
        # root object found, check for branch object
        branch_obj = db_session.query(Branch).filter(Branch.parent_id == root_obj.id).filter(Branch.uri == branch_name).first()
        if branch_obj is not None:
            # branch object found, go ahead and allow template to complete
            leaves = db_session.query(Leaf).filter(Leaf.parent_id == branch_obj.id).all()
            return render_template("branch.html", root_name=root_name, branch_name=branch_name, leaves=leaves)
    abort(404)

@main.route('/<root_name>', strict_slashes=False)
def root_home(root_name):
    root_obj = db_session.query(Root).filter(Root.uri == root_name).first()
    if root_obj is not None:
        # root object found, go ahead and allow template to complete
        branches = db_session.query(Branch).filter(Branch.parent_id == root_obj.id).all()
        return render_template("root.html", root_name=root_name, branches=branches)
    abort(404)
