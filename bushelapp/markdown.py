from os import pardir
import requests
import simplejson
import pathlib
import re
import time

from .database import db_session
from .models import Backlink, Leaf
from .plugin_handler import PluginHandler, PluginCollection, plugins

def gitHubPost(text, mode, context):
    """Send a POST request to GitHub via API """
    payload = {'text': text, 'mode': mode}
    if context != None:
        payload['context'] = context
           
    r = requests.post('https://api.github.com/markdown', data=simplejson.dumps(payload))

    if r.status_code == 200:
        return r.content
    else:
        details = ''
        for e in res['errors']:
            details += '{}.{}: {}.'.format(e['resource'], e['field'], e['code'])
        print('[ERROR][HTTP {}] {} - {}'.format(r.status_code, res['message'], details))
        return None

def createBacklinks(leaf_obj, leaf_content):
    """Create backlink objects based on links in the leaf"""
    # we just need to regex the text for md style links that go
    # to a page on bushel and create a backlink for them

    # regex for the first headline
    # (i need a way to check for localhost:5000 as well for testing)
    link_re = re.compile(r"(https?:\/\/)?(www\.)?bushel-app\.com\/(.+?\/)(.+?\/)([-a-zA-Z0-9@:%_\+.~#?&=]*)", re.MULTILINE)
    #link_re = re.compile(r"localhost:5000\/(.+?\/)(.+?\/)([-a-zA-Z0-9@:%_\+.~#?&=]*)", re.MULTILINE)
    matches = link_re.finditer(leaf_content)
    for match in matches:
        print(f"Matched backlink: {match.group()}")
        # for each match we want to get the link and attempt to
        # parse the leaf uri from it if available
        if (match.group(5)):
            # we got a match, lets get the target leaf
            print(f"Creating backlink for {match.group(5)}")
            target_obj = db_session.query(Leaf).filter(Leaf.uri == match.group(5)).one()

            backlink_obj = db_session.query(Backlink).filter(Backlink.parent_id == leaf_obj.id).filter(Backlink.target_id == target_obj.id).first()

            if backlink_obj is None:
                # now we can create a backlink if it doesnt exist
                # technically we should be deleting all old backlinks
                backlink_obj = Backlink().create(leaf_obj.id, target_obj.id)
                db_session.add(backlink_obj)
                db_session.commit()

def formatMarkdown(leaf_obj, user_obj):
    """Convert a leaf's markdown file to HTML"""
    # all we want to do here is send the text to the github api
    # and store the result
    # we provide the uri all we need to do is create and save
    # the html
    md_name = leaf_obj.uri + '.md'
    html_name = leaf_obj.uri + '.html'
    base_path = pathlib.Path("bushelapp/store/")
    content_path = pathlib.Path("bushelapp/templates/content/")

    # init path
    content_path.mkdir(parents=True, exist_ok=True)
    
    creation_success = False

    # using the md file get all the text
    with open(base_path / md_name, 'r', encoding='utf-8') as md_file:
        # attempt to format markdown
        content = gitHubPost(md_file.read(), "markdown", None).decode('utf-8')
        # if its successful create html file
        if content is not None:
            with open(content_path / html_name, 'w', encoding='utf-8') as html_file:
                # add the creation date here
                # regex for the first headline
                header_re = re.compile(r"<h1>(.|\n|\n\r)*?<\/h1>", re.MULTILINE)
                match = header_re.search(content)
                if match:
                    header_content = match.group()
                    # we've got our first headline, lets add some stuff after it
                    print("adding post header...")
                    header_metadata = '<ul class="metadata">'
                    header_metadata += '\n<li><time aria-label="Article creation date" datetime="'
                    header_metadata += time.strftime('%Y-%m-%dT00:00:00.000Z', time.gmtime(leaf_obj.date))
                    header_metadata += '">'
                    header_metadata += time.strftime('%m/%d/%y', time.gmtime(leaf_obj.date))
                    header_metadata += '</time></li>'
                    header_metadata += '\n<li class="metadata-user">'
                    if user_obj.alias is not None:
                        header_metadata += user_obj.alias.decode('utf-8')
                    else:
                        header_metadata += user_obj.username
                    header_metadata += '</li>\n</ul>'

                    # add header metadata
                    header_content += '\n' + header_metadata + '\n'

                    # assemble entire content
                    writable_content = content[:match.start()] + header_content + content[match.end():]
                else:
                    writable_content = content
                
                # apply plugins after markdown format
                plugin_re = re.compile(r"\[~:([a-zA-Z]+?):([a-zA-Z]+?)(\.([a-zA-Z0-9].?))?\](\(.*?\))?", re.MULTILINE)
                for plugin_match in reversed(list(plugin_re.finditer(writable_content))):
                    print(f"Finding plugin for match '{plugin_match.group()}'")
                    plugin_collection = plugin_match.group(1)
                    plugin_func = plugin_match.group(2)
                    plugin_arg = plugin_match.group(4)
                    plugin_context = plugin_match.group(5)
                    active_plugin_collection = plugins.get_collection(plugin_collection)
                    if active_plugin_collection is not None:
                        try:
                            result = active_plugin_collection.apply_plugin(plugin_func, plugin_arg, plugin_context)
                            if result is not None:
                                writable_content = writable_content[:plugin_match.start()] + result + writable_content[plugin_match.end():]
                                print(f"Successfully applied plugin!")
                        except:
                            print("WARN: Plugin internal error!")
                    else:
                        print(f"WARN: Could not apply plugin for match '{plugin_match.group()}'!")

                # write the final content to the file
                html_file.write(writable_content)
                creation_success = True
    
    if creation_success:
        return html_name
    else:
        return None

def getLeafContent(leaf_obj):
    """Get text of leaf markdown file"""
    md_name = leaf_obj.uri + '.md'
    base_path = pathlib.Path("bushelapp/store/")
    
    # using the md file get all the text
    with open(base_path / md_name, 'r') as md_file:
        content = md_file.read()
    
    return content

def setLeafContent(leaf_obj, user_obj, leaf_content):
    """Set text of leaf markdown file"""
    md_name = leaf_obj.uri + '.md'
    base_path = pathlib.Path("bushelapp/store/")
    
    # using the md file get all the text
    with open(base_path / md_name, 'w') as md_file:
        # normalize line endings
        md_file.write(leaf_content.replace('\r\n', '\n').replace('\r', '\n'))
    
    # create backlinks from the inputted content
    createBacklinks(leaf_obj, leaf_content)
    
    # update the leaf in the db
    db_session.flush()
    db_session.query(Leaf).filter(Leaf.id == leaf_obj.id).update({'date': int(time.time())})
    db_session.commit()
    # refresh just in case, i cant find anything on if this would refresh or not
    # so i doubt it
    leaf_obj = db_session.query(Leaf).filter(Leaf.id == leaf_obj.id).first()

    formatMarkdown(leaf_obj, user_obj)
    
    return leaf_obj
