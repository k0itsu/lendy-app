import sqlite3, os, lendydata
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

app = Flask(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'lendy.db'),
    DEBUG=True,
    SECRET_KEY='nicknackpaddywhack',
    USERNAME='admin',
    PASSWORD='thisisterrible'
))
app.config.from_envvar('LENDY_SETTINGS', silent=True)


def get_db():
    """Opens a new database connection if one does not exist for our current request
    context (the g object helps with this this task)"""
    if not hasattr(g, 'sqlite_db'):
        lendydata.initDB()
        g.sqlite_db = lendydata.db
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request. Note the 'g'
    object which makes sure we only operate on the current request."""
    if hasattr(g, 'sqlite_db'):
        lendydata.closeDB()


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid Username!'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid Password!'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_inventory'))
    return render_template('login.html', error=error)

@app.route('/inventory')
def show_inventory():
    get_db()
    allItems = lendydata.get_items()
    inventory = [dict(zip(['name', 'description'], [item[1], item[2]]))
                for item in allItems]
    return render_template('items.html', items=inventory)

@app.route('/add', methods=['POST'])
def add_item():
    if not session.get('logged_in'):
        abort(401)
    get_db()
    ownerID = [row[0] for row in lendydata.get_members()
               if row[1] == request.form['owner']]
    try: ownerID = ownerID[0]
    except IndexError:
        # implies no owners match name
        # should raise error/create new member
        ownerID = 1     # use default member for now.

    lendydata.insert_item(request.form['name'],
                          request.form['description'],
                          ownerID,
                          request.form['price'],
                          request.form['condition'])

    flash('New entry was successfully posted')
    return redirect(url_for('show_inventory'))



if __name__ == '__main__':
    app.run(host ='0.0.0.0', port = 5000, debug = True)
