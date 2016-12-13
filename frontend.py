from pprint import pformat, pprint

from flask import Flask, Response, request
from flask import render_template, url_for, jsonify
from flask_login import LoginManager, UserMixin, login_required

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = ('mysql+mysqlconnector://'
                                        'tools:YPrn3Uy8OX61DQlFjinb'
                                        '@localhost/cl_scrape')
db = SQLAlchemy(app)


class ClAd(db.Model):
    __tablename__ = 'cl_ad'
    ad_id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(64))
    city = db.Column(db.String(64))
    title = db.Column(db.String(255))
    description = db.Column(db.Text())
    link = db.Column(db.String(255))
    link_key = db.Column(db.String(25), primary_key=True)
    date_str = db.Column(db.String(128))
    dt = db.Column(db.DateTime(timezone=True))

    def __init__(self, ad_id, state, city, title,
                description, link, link_key,
                date_str, dt):
        self.ad_id = ad_id
        self.state = state
        self.city = city
        self.title = title
        self.description = description
        self.link = link
        self.link_key = link_key
        self.date_str = date_str
        self.dt = dt


login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin):
    # proxy for a database of users
    user_database = {"JohnDoe": ("JohnDoe", "John"),
                   "JaneDoe": ("JaneDoe", "Jane")}

    def __init__(self, username, password):
        self.id = username
        self.password = password

        @classmethod
        def get(cls,id):
            return cls.user_database.get(id)


@login_manager.request_loader
def load_user(request):
    token = request.headers.get('Authorization')
    if token is None:
        token = request.args.get('token')

    if token is not None:
        username,password = token.split(":") # naive token
        user_entry = User.get(username)
        if (user_entry is not None):
            user = User(user_entry[0],user_entry[1])
            if (user.password == password):
                return user

    return None

@app.route('/', methods=['GET'])
def index():
    response = 'Place holder'
    return Response(response=response, status=200)

@app.route('/cl_ads_list', methods=['POST'])
def cl_ad_list():
    try:
        offset = int(request.args.get('jtStartIndex'))
        limit = int(request.args.get('jtPageSize'))
    except (ValueError, TypeError):
        return Response(status=400)

    query_order = {'dt ASC': ClAd.dt.asc, 'dt DESC': ClAd.dt.desc,
            'city ASC': ClAd.city.asc, 'city DESC': ClAd.city.desc,
            'state ASC': ClAd.state.asc, 'state DESC': ClAd.state.desc,
            'title ASC': ClAd.title.asc, 'title DESC': ClAd.title.desc, None: ClAd.ad_id.desc}
    if 'search' in request.form:
        like = '%{}%'.format(request.form['search'])
        ads = ClAd.query.filter( ( ClAd.title.like(like) )|( ClAd.description.like(like) ) ).\
                order_by( query_order[request.args.get('jtSorting')]() ).offset(offset).limit(limit)
    else:
        ads = ClAd.query.order_by( query_order[request.args.get('jtSorting')]() ).offset(offset).limit(limit)

    result = {'Result':'OK', 'Records':[]}
    for e in ads:
        row = {'ad_id': e.ad_id,
            'state': e.state,
            'city': e.city,
            'title': e.title,
            'description': e.description,
            'link': e.link,
            'link_key': e.link_key,
            'date_str': e.date_str,
            'dt': e.dt}
        result['Records'].append(row)

    return jsonify(result)


@app.route('/cl_ads_table', methods=['GET'])
def cl_table_main():
    return render_template('cl_ads_tbl.html')

@app.route('/protected/', methods=['GET'])
@login_required
def protected():
    return Response(response='Hello Protected World', status=200)


if __name__ == '__main__':
    app.run(host = '0.0.0.0',
            debug = True,
            port=9191)

