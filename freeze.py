from flask_frozen import Freezer
from app import app

freezer = Freezer(app)

app.config['FREEZER_DESTINATION'] = 'gh-pages'
app.config['FREEZER_DESTINATION_IGNORE'] = ['.git*', 'CNAME', '.gitignore', 'readme.md']

if __name__ == '__main__':
    freezer.freeze()
