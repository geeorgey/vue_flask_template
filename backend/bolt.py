from flask import Blueprint, request
from sqlalchemy.sql.elements import Null
from .models import User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_bolt.oauth.oauth_settings import OAuthSettings
from slack_sdk.oauth.installation_store.sqlalchemy import SQLAlchemyInstallationStore
from slack_sdk.oauth.state_store.sqlalchemy import SQLAlchemyOAuthStateStore
from slack_bolt.oauth.callback_options import CallbackOptions, SuccessArgs, FailureArgs
from slack_bolt.response import BoltResponse
from slack_sdk.oauth.installation_store.installation_store import InstallationStore

import os

import logging
logging.basicConfig(level=logging.DEBUG)

from slack_bolt.adapter.flask import SlackRequestHandler

import sqlalchemy
from sqlalchemy.engine import Engine
logger = logging.getLogger(__name__)
client_id, client_secret, signing_secret = (
    os.environ["SLACK_CLIENT_ID"],
    os.environ["SLACK_CLIENT_SECRET"],
    os.environ["SLACK_SIGNING_SECRET"],
)
database_url = os.environ.get("SQLALCHEMY_DATABASE_URI")
engine: Engine = sqlalchemy.create_engine(database_url)
installation_store = SQLAlchemyInstallationStore(
    client_id=client_id, engine=engine, logger=logger,
)
oauth_state_store = SQLAlchemyOAuthStateStore(
    expiration_seconds=120, engine=engine, logger=logger,
)
#slack_oauth_statesテーブルにレコードがなければapp.py起動時にテーブルを初期化
try:
    engine.execute("select count(*) from slack_oauth_states")
except Exception as e:
    installation_store.metadata.create_all(engine)
    oauth_state_store.metadata.create_all(engine)

database_url = os.environ.get("SQLALCHEMY_DATABASE_URI")
ENGINE = create_engine(database_url)
SESSION = sessionmaker(ENGINE)

bolt_app = App(
    logger=logger,
    signing_secret=os.environ.get("SIGNING_SECRET"),
    installation_store=installation_store,
    raise_error_for_unhandled_request=True,
    oauth_settings=OAuthSettings(
        client_id=client_id,
        client_secret=client_secret,
        state_store=oauth_state_store,
        scopes=os.environ.get("SLACK_SCOPES"),
        user_scopes=os.environ.get("SLACK_USER_SCOPES"),
    ),
)
bolt_app.enable_token_revocation_listeners()


@bolt_app.event("app_home_opened")
def app_home_opened(client, event, body, logger):
    print('app_home_opened■□■□■□■□■□■□■□■□■□')

@bolt_app.message("Hello")
def hello(body, say, logger):
    logger.info(body)
    say("What's up?")

@bolt_app.error
def handle_errors(error):
    if isinstance(error, BoltUnhandledRequestError):
        # You may want to have debug/info logging here
        return BoltResponse(status=200, body="")
    else:
        # other error patterns
        return BoltResponse(status=500, body="Something wrong")

handler = SlackRequestHandler(bolt_app)

bolt = Blueprint('bolt', __name__)

@bolt.route("/slack/events", methods=["POST"])
def slack_events():
    print('■□■□■□■□■□/slack/events')
    print(vars(request))
    return handler.handle(request)

@bolt.route("/slack/install", methods=["GET"])
def install():
    return handler.handle(request)

@bolt.route("/slack/oauth_redirect", methods=["GET"])
def oauth_redirect():
    return handler.handle(request)