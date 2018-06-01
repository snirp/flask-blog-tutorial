from flask import Flask, render_template, url_for
from flask_flatpages import FlatPages
from werkzeug.contrib.atom import AtomFeed

DOMAIN = "<name>.github.io/<repo>"

app = Flask(__name__)
blogs = FlatPages(app, "BLOG")

app.config['FLATPAGES_BLOG_ROOT'] = 'pages/blog'
app.config['FLATPAGES_BLOG_EXTENSION'] = '.md'


# helper functions
def page_list(pages, publish_filter=None, limit=None, meta_sort='', reverse=False):
    """Basic sorting and limiting for flatpage objects"""
    if publish_filter is True:
        # Only published
        pages = [p for p in pages if p.meta['published']]
    elif publish_filter is False:
        # Only unpublished
        pages = [p for p in pages if not p.meta['published']]
    else:
        # All pages
        pages = [p for p in pages]
    if meta_sort:
        pages = sorted(pages, reverse=reverse, key=lambda p: p.meta[meta_sort])
    return pages[:limit]

# controllers
@app.route("/")
def index():
    blog_list = page_list(blogs, True, 3, 'date', True)
    return render_template('index.html', blog_list=blog_list)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/404.html')
def static_404():
    return render_template('404.html')

@app.route('/blog/')
def blog_index():
    blog_list = page_list(blogs, True, None, 'date', True)
    return render_template('blog-index.html', blog_list=blog_list)

@app.route('/blog/<path:path>/')
def blog_detail(path):
    blog = blogs.get_or_404(path)
    return render_template('blog-detail.html', blog=blog)

@app.route('/draft/')
def draft_index():
    blog_list = page_list(blogs, False, None, 'date', True)
    return render_template('blog-index.html', blog_list=blog_list)

@app.route('/blog/atom.xml')
def blog_feed():
    feed = AtomFeed('My recent blog postings',
                    feed_url=DOMAIN+url_for('blog_feed'),
                    url=DOMAIN)
    blog_list = page_list(blogs, 'published', 10, 'date', True)
    for b in blog_list:
        feed.add(b.meta['title'],
                 content_type='html',
                 url=DOMAIN + url_for('blog_detail', path=b.path),
                 author=b.meta['author'],
                 updated=b.meta['lastmod'],
                 published=b.meta['date'],
                 summary=b.meta['excerpt'])
    return feed.get_response()

@app.route('/sitemap.xml')
def sitemap():
    routes = [
        (url_for('index'),      '2018-05-30'),
        (url_for('blog_index'), '2018-05-30'),
        (url_for('blog_feed'),  '2018-05-30'),
    ]
    urls = [ {"loc": DOMAIN + r[0], "lastmod": r[1]} for r in routes ] + \
            [ {"loc": DOMAIN + url_for('blog_detail', path=b.path), "lastmod": b.meta['lastmod']} for b in blogs]
    return render_template('sitemap.xml', urls=urls)

if __name__ == "__main__":
    app.run(debug=True)
