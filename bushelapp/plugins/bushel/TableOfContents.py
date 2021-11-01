from flask.globals import g
from ..plugins import Plugin
import uuid

class TableOfContents(Plugin):
    """This plugin is a Table of Contents parser module. It will add
    a table of contents object to the leaf that lists all leaves
    in the same branch as clickable URLs.
    """
    def __init__(self):
        super().__init__()
        self.name = 'table of contents'
        self.func = 'toc'
        self.description = 'Table of contents module'

    def build_result(self):
        guid = uuid.uuid4()
        return f'<div class="block">\
<ul id="{guid}" class="element-list"></ul>\
<script>\
newItem = function(leaf) {{\
let arrow = document.createElement("span");\
arrow.innerText = ">";\
let link = document.createElement("a");\
link.classList.add("highlight-link");\
link.href = `/{{{{ root.uri }}}}/{{{{ branch.uri }}}}/${{leaf.uri}}`;\
link.innerText = leaf.name;\
link.appendChild(arrow);\
let li = document.createElement("li");\
li.appendChild(link);\
return li;\
}};\
window.onload = async function() {{\
let list = document.getElementById("{guid}");\
let result = await fetch("/api/branches/{{{{ branch.uri }}}}/leaves")\
.then(response => response.json());\
result.leaves.map(leaf => list.appendChild(newItem(leaf)));\
}}\
</script>\
</div>'

    def parse(self, context):
        """The actual implementation of the table of contents plugin is to return a generated 
        table of contents for the leaf's branch.
        """
        return self.build_result()