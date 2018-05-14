from datetime import datetime, timedelta
import json

import flask
from werkzeug.routing import IntegerConverter as BaseIntegerConverter
from core.texts import MSG_MAIN_READY_TO_BATTLE
from core.types import Order, Session, Squad, SquadMember, OrderCleared

from sqlalchemy.exc import SQLAlchemyError


app = flask.Flask(__name__)


class IntegerConverter(BaseIntegerConverter):
    regex = r'-?\d+'


app.url_map.converters['int'] = IntegerConverter


@app.route('/new_ready_to_battle/<int:chat_id>', methods=['GET'])
def new_ready_to_battle(chat_id):
    session = Session()
    try:
        order = Order()
        order.chat_id = chat_id
        order.confirmed_msg = 0
        order.text = MSG_MAIN_READY_TO_BATTLE
        order.date = datetime.now()
        session.add(order)
        session.commit()
        order = session.query(Order).filter_by(chat_id=chat_id,
                                               date=order.date,
                                               text=MSG_MAIN_READY_TO_BATTLE).first()

        return flask.Response(status=200,
                              mimetype="application/json",
                              response=json.dumps({'order_id': order.id}))
    except SQLAlchemyError:
        Session.rollback()
        return flask.Response(status=400)


@app.route('/ready_to_battle/<int:order_id>/<int:user_id>', methods=['GET'])
def new_order_click(order_id, user_id):
    try:
        session = Session()
        order = session.query(Order).filter_by(id=order_id).first()
        if order is not None:
            squad = session.query(Squad).filter_by(chat_id=order.chat_id).first()
            if squad is not None:
                squad_member = session.query(SquadMember).filter_by(squad_id=squad.chat_id,
                                                                    user_id=user_id,
                                                                    approved=True)

                if squad_member is not None:
                    order_ok = session.query(OrderCleared).filter_by(order_id=order_id,
                                                                     user_id=user_id).first()

                    if order_ok is None and datetime.now() - order.date < timedelta(minutes=10):
                        order_ok = OrderCleared()
                        order_ok.order_id = order_id
                        order_ok.user_id = user_id
                        session.add(order_ok)
                        session.commit()

            else:
                order_ok = session.query(OrderCleared).filter_by(order_id=order_id,
                                                                 user_id=user_id).first()

                if order_ok is None and datetime.now() - order.date < timedelta(minutes=10):
                    order_ok = OrderCleared()
                    order_ok.order_id = order_id
                    order_ok.user_id = user_id
                    session.add(order_ok)
                    session.commit()

        return flask.Response(status=200)

    except SQLAlchemyError:
        Session.rollback()
        return flask.Response(status=400)


@app.route('/ready_to_battle_status/<int:order_id>', methods=['GET'])
def order_status(order_id):
    try:
        session = Session()
        order = session.query(Order).filter_by(id=order_id).first()
        if order is not None:
            users = []
            for order_ok in order.cleared:
                users.append({'username': order_ok.user.username,
                              'id': order_ok.user.id,
                              'attack': order_ok.user.character.attack if order_ok.user.character else 0,
                              'defence': order_ok.user.character.defence if order_ok.user.character else 0})

            return flask.Response(status=200,
                                  mimetype="application/json",
                                  response=json.dumps({'users': users}))

    except SQLAlchemyError:
        Session.rollback()
        return flask.Response(status=400)
