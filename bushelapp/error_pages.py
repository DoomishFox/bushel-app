from flask import render_template

def page_not_found(e):
    return render_template("not_found.html"), 404