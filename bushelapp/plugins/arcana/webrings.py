from ..plugins import Plugin
import uuid

class Webrings(Plugin):
    """This plugin is an implementation of Webrings 2.0 for bushel's
    parser module system. It adds a dynamic set of webring links from
    Arcana Labs' Webrings 2.0 server.
    """
    def __init__(self):
        super().__init__()
        self.name = 'webrings'
        self.func = 'webring'
        self.description = 'Webrings 2.0 integration'

    def build_result(self):
        guid = f"g{uuid.uuid4()}"
        return f'<div class="block">\n\
<ul id="{guid}" class="url-list"></ul>\n\
<script>\n\
    "use strict";\n\
    (async function() {{\n\
      const list = document.querySelector("#{guid}");\n\
      let request = await fetch("https://webring.arcanalabs.ca");\n\
      let webring = await request.json();\n\
      let markup = [];\n\
      webring.forEach(item => {{\n\
      if (item.id !== "5f9d9a8b-b2be-4bf5-a33e-ecd49ddd1fd1")\n\
        markup.push(`<li><a href="${{item.url}}">${{item.title}}</a><span>: ${{item.description}}</span></li>`);\n\
      }});\n\
      list.insertAdjacentHTML("beforeend", markup.join(""))\n\
    }}());\n\
    </script>\n\
</div>'

    def parse(self, context):
        """The webrings plugin will return block that can be inserted into 
        the document that will dynamically list links fetched from Arcana 
        Labs' webring.
        """
        return self.build_result()