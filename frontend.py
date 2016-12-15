from flask import Flask, Response, request
from flask import render_template, url_for, jsonify

from flask_sqlalchemy import SQLAlchemy

from settings import connection_str

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = connection_str
# set SQLALCHEMY_POOL_RECYCLE to 10 (seconds?) less than mysql
# wait_timeout which is currently 600
# hopefully this will eleminate the connection error encounter
# after the database sits idle
app.config['SQLALCHEMY_POOL_RECYCLE'] = 590
db = SQLAlchemy(app)


class ClAd(db.Model):
    __tablename__ = 'cl_ad'
    ad_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    state = db.Column(db.String(64))
    city = db.Column(db.String(64))
    title = db.Column(db.String(255))
    description = db.Column(db.Text())
    link = db.Column(db.String(255))
    link_key = db.Column(db.String(25), primary_key=True, unique=True)
    date_str = db.Column(db.String(128))
    dt = db.Column(db.DateTime(timezone=True))
    new = db.Column(db.Boolean)

    def __init__(self, ad_id, state, city, title,
                description, link, link_key,
                date_str, dt, new):
        self.ad_id = ad_id
        self.state = state
        self.city = city
        self.title = title
        self.description = description
        self.link = link
        self.link_key = link_key
        self.date_str = date_str
        self.dt = dt
        self.new = new


@app.route('/cl_ads_table', methods=['GET'])
def cl_table_main():
    return render_template('cl_ads_tbl.html')

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
            'dt': e.dt,
            'new_rec': e.new}
        result['Records'].append(row)

    return jsonify(result)

if __name__ == '__main__':
    app.run(host = '0.0.0.0',
            debug = True,
            port=9191)

