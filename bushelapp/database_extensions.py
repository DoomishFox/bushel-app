import click
import pathlib
from flask.cli import with_appcontext
from .database import init_db, destroy_db, shutdown_session, db_session
from .models import User, Root, Branch, Leaf
from .markdown import formatMarkdown

@click.command('init-db')
@with_appcontext
def init_db_command():
    ''' Clear the existing data and create new tables. '''
    click.echo('Destroying previous database...')
    destroy_db()
    init_db()
    click.echo('Initialized the database.')

@click.command('register-user')
@click.argument('username')
@click.argument('password')
@with_appcontext
def register_user_command(username, password):
    ''' Setup a db user. '''
    from werkzeug.security import generate_password_hash
    u = User(username)
    u.password = generate_password_hash(password)
    db_session.add(u)
    db_session.commit()
    click.echo('Initialized user.')

@click.command('register-user-alias')
@click.argument('username')
@click.argument('alias')
@with_appcontext
def register_user_alias_command(username, alias):
    ''' Add an alias to a db user. '''
    db_session.flush()
    db_session.query(User).filter(User.username == username).update({'alias': alias.encode('utf-8')})
    db_session.commit()
    #user_obj = db_session.query(User).filter(User.username == username).first()
    click.echo('Added alias "' + alias + '" to user "' + username + '".')

@click.command('init-content')
@with_appcontext
def init_content_command():
    ''' Initialize base database content. '''
    base_path = pathlib.Path("bushelapp/store/")
    content_path = pathlib.Path("bushelapp/templates/content/").mkdir(parents=True, exist_ok=True)

    # initialize base root
    root_obj = db_session.query(Root).filter(Root.uri == 'root').first()
    if root_obj is None:
        root_obj = Root().create('root')
        db_session.add(root_obj)
        db_session.commit()
        click.echo('Created root "root"')
    
    # initialize introduction page parent
    branch_obj = db_session.query(Branch).filter(Branch.parent_id == root_obj.id).filter(Branch.uri == 'introduction').first()
    if branch_obj is None:
        branch_obj = Branch().create('introduction', 'Introduction to Bushel', root_obj)
        db_session.add(branch_obj)
        db_session.commit()
        click.echo('Created branch "introduction"')

    # initialize introduction page
    leaf_obj = db_session.query(Leaf).filter(Leaf.parent_id == branch_obj.id).filter(Leaf.uri == 'an-introduction').first()
    if leaf_obj is None:
        leaf_obj = Leaf().create('an-introduction', 'An Introduction', branch_obj)
        db_session.add(leaf_obj)
        db_session.commit()
        click.echo('Created leaf "an-introduction"')

    # save the page html
    # this also acts as a test of the html to markdown system :D
    formatMarkdown(leaf_obj, User("system", "Bushel".encode('utf-8')))


def init_app_database(app):
    app.teardown_appcontext(shutdown_session)
    app.cli.add_command(init_db_command)
    app.cli.add_command(register_user_command)
    app.cli.add_command(register_user_alias_command)
    app.cli.add_command(init_content_command)