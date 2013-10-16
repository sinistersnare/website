import sys

from flask import Flask, render_template
from flask.ext.flatpages import FlatPages, pygments_style_defs
from flask_frozen import Freezer

DEBUG = True
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = '.md'

app = Flask(__name__)
app.config.from_object(__name__)
pages = FlatPages(app)
freezer = Freezer(app)


##### Index #####

@app.route("/")
def index():
    return render_template('index.html',pages=reversed(sorted(pages, 
                                        key=lambda page: page.meta['epoch'])))
    #that key was really awkward, but it works!



##### Static Pages i.e. About, Contact #####
"""
Im hardcoding the static pages in jinja because why not.
"""

@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/contact/')
def contact():
    return render_template('contact.html')

##### Dynamic Pages #####

@app.route('/<path:path>/')
def page(path):
    page = pages.get_or_404(path)
    return render_template('page.html', page=page)

@app.route('/tag/<string:tag>/')
def tag(tag):
    tagged = [p for p in pages if tag in p.meta.get('tags', [])]
    return render_template('tag.html', pages=tagged, tag=tag)


##### Initializer #####
if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        freezer.freeze()
    else:
        app.run(port=8000)

