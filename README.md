# Bushel
this is a heavy wip, lots is gonna change. so far this file is mostly just my notes about the project, but im going to clean it up soon.

#### Try it Out
its hosted on [bushel-app.com](https://bushel-app.com)!

#### Data Structure
so everythings gonna be in flat files. specifically, flat md files. flask is going to grab them, render them to html using githubs markdown api, then insert them into a template or two and serve that. each page will have an edit link like ms docs which will route you through an auth page to an edit page for the specified uri which maps to a flat file. on save it will save your md file along with its acompanying html file to disk.
NOTE: the md -> html conversion happens on page save, not on page load.

landing pages will be dynamically using the sqlite db generated. searching inside pages will be unsupported, use google or find-on-page cause its just flat files. search of page title can be accomplished with the sqlite db but im not sure i want that.

#### Tables
so theres users of course

there are roots. roots are the base containers. branches and leaves can belong to a single root to prevent cross contamination. roots are part of the url.

there are branches. branches are purely organizaional. they have a name and ran link to other branches and leaves.

there are leaves. leaves are the actual content rendered from md files.

oh and the whole tokens thing is... interesting. i might change that but for the level of security i care about i think itll be fine.

## Running
activate the python venv and then `set FLASK_DEBUG=1`, `set FLASK_APP=bushelapp` (I have this set in my env activate). then you can just run `flask run`