from bushelapp.main import leaf
import requests
import simplejson
import re
import time

from .database import db_session, docdb_session
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
        for e in r['errors']:
            details += '{}.{}: {}.'.format(e['resource'], e['field'], e['code'])
        print('[ERROR][HTTP {}] {} - {}'.format(r.status_code, r['message'], details))
        return None

def formatMarkdown(leaf_obj, user_obj):
    """Convert a leaf's markdown file to HTML"""
    # all we want to do here is send the text to the github api
    # and store the result
    # we provide the uri all we need to do is create and save
    # the html

    md_dict = docdb_session.leafmd.find_one({ "_id": leaf_obj.uri })

    creation_success = False
    # attempt to format markdown
    content = gitHubPost(str(md_dict["content"]), "markdown", None).decode('utf-8')
    # if its successful prepare html
    if content is not None:
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

        # write the final content to aurora
        html_key = { "_id": leaf_obj.uri }
        html_dict = { "content": writable_content }
        docdb_session.leafhtml.update(html_key, html_dict, upsert=True)
        creation_success = True
    
    if creation_success:
        return True
    else:
        return False

def getLeafContent(leaf_obj):
    """Get text of leaf markdown file"""
    md_dict = docdb_session.leafmd.find_one({ "_id": leaf_obj.uri })
    
    return md_dict["content"]

def setLeafContent(leaf_obj, user_obj, leaf_content):
    """Set text of leaf markdown file"""
    # normalize line endings and format content as a dictionary/json
    md_key = { "_id": leaf_obj.uri }
    md_dict = { "content": leaf_content.replace('\r\n', '\n').replace('\r', '\n') }
    # insert normalized leaf_content into aurora
    docdb_session.leafmd.update(md_key, md_dict, upsert=True)
    
    # update the leaf in the db
    db_session.flush()
    leaf_obj.date = int(int.time())
    db_session.commit()

    # format the markdown into html on save for speed
    formatMarkdown(leaf_obj, user_obj)
    
    return leaf_obj
