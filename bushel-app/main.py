from flask import Blueprint, render_template
from .database import db_session
from .models import Root, Branch, Leaf

main = Blueprint('main', __name__)

@main.route('/', strict_slashes=False)
def index():
    return render_template('index.html')

@main.route('/<root_name>/<branch_name>/<page_name>', strict_slashes=False)
def leaf(root_name, branch_name, page_name):
    page_exists = True
    return render_template("leaf.html", root_name=root_name, branch_name=branch_name, page_name=page_name, page_exists=page_exists)

@main.route('/<root_name>/<branch_name>', strict_slashes=False)
def branch_home(root_name, branch_name):
    page_exists = False
    leaves = []
    root_obj = db_session.query(Root).filter(Root.uri == root_name).first()
    if root_obj is not None:
        branch_obj = db_session.query(Branch).filter(Branch.parent_id == root_obj.id and Branch.uri == branch_name).first()
        if branch_obj is not None:
            # root object found, go ahead and allow template to complete
            page_exists = True
            leaves = db_session.query(Leaf).filter(Leaf.parent_id == branch_obj.id).all()
    return render_template("branch.html", root_name=root_name, branch_name=branch_name, page_exists=page_exists, leaves=leaves)

@main.route('/<root_name>', strict_slashes=False)
def root_home(root_name):
    page_exists = False
    branches = []
    root_obj = db_session.query(Root).filter(Root.uri == root_name).first()
    if root_obj is not None:
        # root object found, go ahead and allow template to complete
        page_exists = True
        branches = db_session.query(Branch).filter(Branch.parent_id == root_obj.id).all()
    return render_template("root.html", root_name=root_name, page_exists=page_exists, branches=branches)
