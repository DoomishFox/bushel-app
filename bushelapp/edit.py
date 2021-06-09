from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from .database import db_session
from .models import User, AuthToken, Root, Branch, Leaf
from .markdown import getLeafContent, setLeafContent

edit = Blueprint('edit', __name__, url_prefix='/edit')

@edit.before_app_request
def load_logged_in_user():
    token = session.get('token')

    if token is None:
        g.user = None
    else:
        auth_token_obj = db_session.query(AuthToken).filter(AuthToken.token == token).first()
        if auth_token_obj is not None:
            g.user = db_session.query(User).filter(User.id == auth_token_obj.user_id).first()
        else:
            g.user = None

@edit.route('/<root_name>/<branch_name>/<page_name>', methods=('GET', 'POST'), strict_slashes=False)
def leaf(root_name, branch_name, page_name):
    leaf_name = "Untitled Leaf"
    leaf_content = "# Untitled Leaf\n\nSample leaf content."
    if g.user is None:
        # if theres no user session we need to redirect to the login page with a next url
        return redirect(url_for('auth.login', next='/edit/' + root_name + '/' + branch_name + '/' + page_name))
    
    root_obj = db_session.query(Root).filter(Root.uri == root_name).first()
    if root_obj is not None:
        # root object found, check for branch object
        branch_obj = db_session.query(Branch).filter(Branch.parent_id == root_obj.id).filter(Branch.uri == branch_name).first()
        if branch_obj is not None:
            # branch object found
            leaf_obj = db_session.query(Leaf).filter(Leaf.parent_id == branch_obj.id).filter(Leaf.uri == page_name).first()
            if leaf_obj is not None:
                leaf_name = leaf_obj.name
                leaf_content = getLeafContent(leaf_obj)
        
            if request.method == 'POST':
                # then we need to get our form data and do stuff with it
                print('attempting leaf edit')

                leaf_name = request.form.get('leaf_name')
                leaf_content = request.form.get('leaf_content')

                if leaf_obj is None:
                    # create one if it doesnt exist
                    leaf_obj = Leaf().create(page_name, leaf_name, branch_obj)
                    db_session.add(leaf_obj)
                    db_session.commit()
                    
                setLeafContent(leaf_obj, g.user, leaf_content)
                return redirect(url_for('main.leaf', root_name=root_name, branch_name=branch_name, page_name=page_name))
        else:
            flash("Cannot create branch, branch already exists!")
    else:
        flash("Cannot create branch, root does not exist!")
    return render_template("edit/leaf.html", editing=True, root_name=root_name, branch_name=branch_name, page_name=page_name, leaf_name=leaf_name, leaf_content=leaf_content)

@edit.route('/<root_name>/<branch_name>', methods=('GET', 'POST'), strict_slashes=False)
def branch(root_name, branch_name):
    if g.user is None:
        # if theres no user session we need to redirect to the login page with a next url
        return redirect(url_for('auth.login', next='/edit/' + root_name + '/' + branch_name))
    if request.method == 'POST':
        # then we need to get our form data and do stuff with it
        print('creating new branch')
        uri = request.form.get('new_branch_uri')
        name = request.form.get('new_branch_name')
        if uri is not None and name is not None:
            # make sure that theres a root
            duplicate_root = db_session.query(Root).filter(Root.uri == root_name).first()
            if duplicate_root is not None:
                # check db for branches
                duplicate_branch = db_session.query(Branch).filter(Branch.uri == uri).first()
                if duplicate_branch is None:
                    # add to db if there is no branch
                    branch_obj = Branch().create(uri, name, duplicate_root)
                    db_session.add(branch_obj)
                    db_session.commit()

                    return redirect(url_for('main.branch_home', root_name=root_name, branch_name=branch_name))
                else:
                    flash("Cannot create branch, branch already exists!")
            else:
                flash("Cannot create branch, root does not exist!")

    # here we edit a root if it exists, or if it doesnt exist we create it
    return render_template("edit/branch.html", root_name=root_name, branch_name=branch_name)

@edit.route('/<root_name>', methods=('GET', 'POST'), strict_slashes=False)
def root(root_name):
    if g.user is None:
        # if theres no user session we need to redirect to the login page with a next url
        return redirect(url_for('auth.login', next='/edit/' + root_name))
    if request.method == 'POST':
        # then we need to get our form data and do stuff with it
        print('creating new root')
        uri = request.form.get('new_root_name')
        if uri is not None:
            # check db for roots
            duplicate_root = db_session.query(Root).filter(Root.uri == uri).first()
            if duplicate_root is None:
                # add to db
                root_obj = Root().create(uri)
                db_session.add(root_obj)
                db_session.commit()
                return redirect(url_for('main.root_home', root_name=root_name))
            else:
                flash("Cannot create branch, root does not exist!")

    # here we edit a root if it exists, or if it doesnt exist we create it
    return render_template("edit/root.html", root_name=root_name)
