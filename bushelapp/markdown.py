import requests
import simplejson
import pathlib
import re
import time

from .database import db_session
from .models import Leaf

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
    with open(base_path / md_name, 'r') as md_file:
        # attempt to format markdown
        content = gitHubPost(md_file.read(), "markdown", None).decode('utf-8')
        # if its successful create html file
        if content is not None:
            with open(content_path / html_name, 'w') as html_file:
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
                        header_metadata += user_obj.alias
                    else:
                        header_metadata += user_obj.username
                    header_metadata += '</li>\n</ul>'

                    # add header metadata
                    header_content += '\n' + header_metadata + '\n'

                    # assemble entire content
                    writable_content = content[:match.start()] + header_content + content[match.end():]
                else:
                    writable_content = content

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
    
    # update the leaf in the db
    db_session.flush()
    db_session.query(Leaf).filter(Leaf.id == leaf_obj.id).update({'date': int(time.time())})
    # refresh just in case, i cant find anything on if this would refresh or not
    # so i doubt it
    leaf_obj = db_session.query(Leaf).filter(Leaf.id == leaf_obj.id).first()

    formatMarkdown(leaf_obj, user_obj)
    
    return leaf_obj
