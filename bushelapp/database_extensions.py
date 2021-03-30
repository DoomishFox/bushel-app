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

@click.command('scan-content')
@with_appcontext
def scan_content_command():
    ''' Scan content files and create db objects. '''
    content_path = pathlib.Path("bushelapp/templates/content/") #.mkdir(parents=True, exist_ok=True)

    for root_dir in content_path.iterdir():
        # for each root directory create a db object
        root_obj = Root().create(root_dir.name)
        db_session.add(root_obj)
        db_session.commit()
        click.echo('Created root ' + root_obj.uri)
        
        for branch_dir in content_path.joinpath(root_dir.name).iterdir():
            # for each branch directory create a branch object
            branch_obj = Branch().create(branch_dir.name, branch_dir.name, root_obj)
            db_session.add(branch_obj)
            db_session.commit()
            click.echo('Created branch ' + branch_obj.uri)

            # scan for leaves (this will be more difficult hmm)
            for leaf_file in content_path.joinpath(root_dir.name).joinpath(branch_dir.name).iterdir():
                if '.html' in leaf_file.name:
                    leaf_obj = Leaf().create(leaf_file.name.replace('.html', ''), leaf_file.name.replace('.html', ''), branch_obj)
                    db_session.add(leaf_obj)
                    db_session.commit()
                    click.echo('Created leaf ' + leaf_obj.uri)

@click.command('init-content')
@with_appcontext
def init_content_command():
    ''' Initialize base database content. '''
    base_path = pathlib.Path("bushelapp/store/")
    content_path = pathlib.Path("bushelapp/templates/content/").mkdir(parents=True, exist_ok=True)

    # initialize base root
    root_obj = Root().create('root')
    db_session.add(root_obj)
    db_session.commit()
    click.echo('Created root "root"')
    
    # initialize introduction page parent
    branch_obj = Branch().create('introduction', 'Introduction to Bushel', root_obj)
    db_session.add(branch_obj)
    db_session.commit()
    click.echo('Created branch "introduction"')

    # initialize introduction page
    leaf_obj = Leaf().create('an-introduction', 'An Introduction', branch_obj)
    db_session.add(leaf_obj)
    db_session.commit()
    click.echo('Created leaf "an-introduction"')

    # save the page html
    # this also acts as a test of the html to markdown system :D
    formatMarkdown(leaf_obj, User("system", "Bushel"))


def init_app_database(app):
    app.teardown_appcontext(shutdown_session)
    app.cli.add_command(init_db_command)
    app.cli.add_command(register_user_command)
    app.cli.add_command(scan_content_command)
    app.cli.add_command(init_content_command)