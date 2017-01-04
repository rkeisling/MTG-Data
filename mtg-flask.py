import flask
from db import *
from pony.orm import *
app = flask.Flask(__name__)


@app.route('/card/<int:id>')
@db_session
def show_card_by_id(id):
    card = Card.get(id=id)
    if card:
        return flask.render_template('show_card.html', card=card)
    else:
        flask.abort(404)


@app.route('/top/<int:how_many>')
@db_session
def show_top(how_many):
    top = list(select((
        c,
        c.pricings) for c in Card).order_by(-2)[:how_many])
    return flask.render_template('show_top.html',
                                 how_many=how_many,
                                 top=top)


if __name__ == "__main__":
    app.run()
