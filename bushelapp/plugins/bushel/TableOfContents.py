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
        guid = f"g{uuid.uuid4()}"
        return f'<div class="block">\n\
<ul id="{guid}" class="element-list"></ul>\n\
<script>\n\
    "use strict";\n\
    (async function() {{\n\
      const list = document.querySelector("#{guid}");\n\
      let request = await fetch("/api/branches/{{{{ branch.uri }}}}/leaves");\n\
      let data = await request.json();\n\
      let markup = [];\n\
      data.leaves.forEach(leaf => {{\n\
        markup.push(`<li><a class="highlight-link" href="/{{{{ root.uri }}}}/{{{{ branch.uri }}}}/${{leaf.uri}}">${{leaf.name}}<span>&gt</span></a></li>`);\n\
      }});\n\
      list.insertAdjacentHTML("beforeend", markup.join(""))\n\
    }}());\n\
    </script>\n\
</div>'

    def parse(self, context):
        """The actual implementation of the table of contents plugin is to return a generated 
        table of contents for the leaf's branch.
        """
        return self.build_result()