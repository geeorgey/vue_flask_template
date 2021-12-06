from flask import Blueprint, render_template, request, jsonify, make_response, redirect
from sqlalchemy.sql.elements import Null
from .models import SlackInstallations, InstalledWorkSpace
from .bolt import bolt_app,SESSION
from . import db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func, Date, cast

from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler
from slack_bolt.error import BoltUnhandledRequestError
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_bolt.oauth.oauth_settings import OAuthSettings
from slack_sdk.oauth.installation_store.sqlalchemy import SQLAlchemyInstallationStore
from slack_sdk.oauth.state_store.sqlalchemy import SQLAlchemyOAuthStateStore
from slack_bolt.oauth.callback_options import CallbackOptions, SuccessArgs, FailureArgs
from slack_bolt.response import BoltResponse

import re
import time
import asyncio
import json
import os

import datetime
from datetime import datetime as dt
from datetime import date
from dateutil.tz import gettz
from dateutil.relativedelta import relativedelta
import calendar
from pytz import timezone

@bolt_app.command(os.environ["SLACK_FEEDBACK_COMMAND"])
def SLACK_FEEDBACK_COMMAND(ack,client, body, say, logger, view):
    print('SLACK_FEEDBACK_COMMAND')
    ack()
    start_Feedback(client, body, logger)

@bolt_app.action("contact_us")
def contact_us(ack, body, logger, client, view):
    print('contact_us ■□■□■□■□■□■□■□■□■□■□■□')
    ack()
    try:
        start_Feedback(client, body, logger)
    except Exception as e:
        print(e)

def start_Feedback(client, body, logger):
    print('start_Feedback')
    """利用する変数一覧
    #チャンネルから呼び出される場合
    channel_id: body['channel_id']
    locale: userinfo['user']['locale']
    """
    user_id = Null
    if body.get('user_id') is not None:#チャンネルから呼び出される場合
        user_id = body.get('user_id')
    if body.get('user') is not None and body.get('user').get('id') is not None:#ホーム画面から呼び出される場合
        user_id = body.get('user').get('id') 
    try:
        userinfo = client.users_info(
            user=user_id,
            include_locale=True
        )
    except SlackApiError as e:
        print("Error fetching conversations: {}".format(e))


    """
    print(userinfo)
    print(userinfo['user']['profile']['email'])
    print(userinfo['user']['id'])
    print(userinfo['user']['team_id'])
    print(userinfo['user']['real_name'])
    print(userinfo['user']['tz'])
    print(userinfo['user']['tz_label'])
    print(userinfo['user']['profile']['image_512'])
    """
    locale = userinfo['user']['locale']

    channel_id = Null
    if body.get('channel_id') is not None: #チャンネルからコマンドで呼び出す場合
        channel_id = body['channel_id']
        print('channel_id: ' + body['channel_id'])
    else:#ホーム画面から呼び出す場合はDMで返すのでuseridを使う
        channel_id = userinfo['user']['id']

    if locale == 'ja-JP':
        text_title = os.environ["APP_NAME"] + "へのフィードバック"
        msg1 = os.environ["APP_NAME"] + " 開発者へのフィードバックをお寄せください。"
        text_label = "メッセージ入力欄"
        text_close = "閉じる"
        text_submit = "送信する"
    else:
        text_title = "Feedback on " + os.environ["APP_NAME"]
        msg1 = "Please send your feedback to the developers."
        text_label = "message input field"
        text_close = "Close"
        text_submit = "Submit"

    blocks = [
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": msg1
			}
		},
		{
			"type": "input",
            "block_id": "feedback_message",
			"element": {
				"type": "plain_text_input",
				"multiline": True,
				"action_id": "plain_text_input-action"
			},
			"label": {
				"type": "plain_text",
				"text": text_label,
				"emoji": True
			}
		}
    ]

    #Messageの送信者情報を送信するのでユーザー情報を取得する
    #Get the user information as we send the Message sender information.
    private_metadata = {
        "email": userinfo['user']['profile']['email'],
        "user_id": userinfo['user']['id'],
        "team_id": userinfo['user']['team_id'],
        "real_name": userinfo['user']['real_name'],
        "tz": userinfo['user']['tz'],
        "tz_label": userinfo['user']['tz_label'],
        "image_512": userinfo['user']['profile']['image_192'],
        "is_admin": userinfo['user']['is_admin'],
        "is_owner": userinfo['user']['is_owner'],
        "channel_id": channel_id,
        "locale": userinfo['user']['locale']
    }

    local_session = SESSION()
    #送信者のWorkspace Nameを取得する
    #Get the sender's Workspace Name
    try:
        slack_installations = local_session.query(SlackInstallations).filter_by(team_id=userinfo['user']['team_id']).order_by(SlackInstallations.id.desc()).first()
    finally:
        print('finish find slack_installations--')
        print(slack_installations)
    private_metadata['team_name'] = slack_installations.team_name 

    try:
        client.views_open(
            trigger_id=body["trigger_id"],
            # ビューのペイロード
            view={
                "type": "modal",
                "callback_id": "send_App_feedback",
                "title": {"type": "plain_text", "text": text_title},
                "submit": {"type": "plain_text", "text": text_submit},
                "close": {"type": "plain_text", "text": text_close},
                "private_metadata": json.dumps(private_metadata),
                "blocks": blocks
            }
        )
    except SlackApiError as e:
        print("Error views_open: {}".format(e))    
    local_session.close()


@bolt_app.view("send_App_feedback")
def send_App_feedback(ack, body, payload, client, view, logger):
    ack()
    print('Start send_App_feedback')
    #メッセージの内容
    #print(view["state"]["values"]['feedback_message']['plain_text_input-action']['value'])
    msg = view["state"]["values"]['feedback_message']['plain_text_input-action']['value']
    #private_metadata にはフィードバックを書いたユーザーの情報が入っている
    #private_metadata contains the information of the user who wrote the feedback.
    #print(json.loads(body['view']['private_metadata']))
    private_metadata = json.loads(body['view']['private_metadata'])
    local_session = SESSION()
    app_owner_ws_id = os.environ.get("APP_OWNER_WS_ID")
    owner_channel_id = os.environ.get("APP_OWNER_CONTACT_CHANNEL_ID")
    app_owner_id = os.environ.get("APP_OWNER_ID")
    try:
        slack_installations_owner = local_session.query(SlackInstallations).filter_by(user_id = app_owner_id,team_id=app_owner_ws_id).order_by(SlackInstallations.id.desc()).first()
    finally:
        print('finish find slack_installations_owner')
    client = WebClient(token=slack_installations_owner.bot_token)
    try:
        owner_userinfo = client.users_info(
            user=app_owner_id,
            include_locale=True
        )
    except SlackApiError as e:
        print("Error fetching users_info: {}".format(e))
    owner_locale = owner_userinfo['user']['locale']
    if owner_locale == "ja-JP":
        header_text = ":newspaper:  " + os.environ["APP_NAME"] +" にフィードバックが届きました  :newspaper:"
    else:
        header_text = ":newspaper:  Feedback has been received on " + os.environ["APP_NAME"] +" :newspaper:"

    params={
        "team_id": private_metadata.get("team_id"),
        "user_id": private_metadata.get("user_id"),
    }
    blocks = create_feedback_blocks(header_text,msg,private_metadata,params,owner_locale)

    owner_client = WebClient(token=os.environ.get("APP_OWNER_TOKEN"))
    try:
        owner_client.chat_postMessage(
            channel=owner_channel_id,
            text=msg,
            blocks=blocks
        )
    except SlackApiError as e:
        print("Error fetching chat_postMessage: {}".format(e))
    #フィードバック送信者に送信完了メッセージを送信する
    #Send a send complete message to the feedback sender.
    try:
        slack_installations = local_session.query(SlackInstallations).filter_by(team_id=private_metadata['team_id']).order_by(SlackInstallations.id.desc()).first()
    finally:
        print('finish find slack_installations')
    client = WebClient(token=slack_installations.bot_token)
    if private_metadata['locale'] == 'ja-JP':
        sent_msg = "フィードバックが開発者に届きました。\nお返事はDMで届きます。"
    else:
        sent_msg = "Your feedback has been received by the developers.\nYou will receive a reply via DM."
    #chat_postEphemeralを送るチャンネルにbotが入っていないと送れないのでjoinする
    #You can't send chat_postEphemeral unless the bot is in the channel where you send it, so join it.
    try:#https://api.slack.com/methods/conversations.history/test
        client.conversations_join(
            channel=private_metadata['channel_id']
        )
    except SlackApiError as e:
        print("Error fetching conversations: {}".format(e))
    #chat_postEphemeralで送信完了メッセージを送る
    #Send a send completion message with chat_postEphemeral
    try:#https://api.slack.com/methods/conversations.history/test
        client.chat_postEphemeral(
            channel=private_metadata['channel_id'],
            user=body['user']['id'],
            text=sent_msg
        )
    except SlackApiError as e:
        print("Error chat_postEphemeral: {}".format(e))
    local_session.close()

def create_feedback_blocks(header_text,msg,private_metadata,params,target_locale):
    print('create_feedback_blocks :::::::')
    #private_metadataは送信元ユーザの情報
    #private_metadata is the information of the sender user
    """
    print(private_metadata)
    print(private_metadata['email'])
    print(private_metadata['real_name'])
    print(private_metadata['team_name'])
    print(private_metadata['tz_label'])
    """
    about = "Email: " + private_metadata['email']
    if target_locale == 'ja-JP':
        about = about + "\n名前： " + private_metadata['real_name']
        about = about + "\n組織名： " + private_metadata['team_name']
        about = about + "\nタイムゾーン： " + private_metadata['tz_label']
        text_box_label = "返信内容を入力"
    else:
        about = about + "\nName： " + private_metadata['real_name']
        about = about + "\nTeam Name： " + private_metadata['team_name']
        about = about + "\nTime zone： " + private_metadata['tz_label']
        text_box_label = "Enter your reply."

    """
    print('header_text: ' + header_text)
    print('msg: ' + msg)
    print('about: ' + about)
    print('image_512: ' + private_metadata['image_512'])
    print('real_name: ' + private_metadata['real_name'])
    print('params')
    print(params)
    """
    if params is Null:
        params = {
            "user_id": private_metadata['user_id'],
            "team_id": private_metadata['team_id'],
        }
    blocks = [
		{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": header_text
			}
		},
		{
			"type": "divider"
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": ":speech_balloon:\n\n" + msg
			},
		},
		{
			"type": "divider"
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": ":bust_in_silhouette:\n\n" + about
			},
			"accessory": {
				"type": "image",
				"image_url": private_metadata['image_512'],
				"alt_text": private_metadata['real_name']
			}
		},
		{
			"type": "input",
            "block_id": "dm_text",
			"element": {
				"type": "plain_text_input",
				"multiline": True,
				"action_id": "dm_text"
			},
			"label": {
				"type": "plain_text",
				"text": text_box_label,
				"emoji": True
			}
		},
		{
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "送信",
						"emoji": True
					},
					"value": "button_action",
					"action_id": "send_replies|" + json.dumps(params)
				}
			]
		}
    ]
    return blocks

@bolt_app.action("send_dm_to_users")
def send_dm_to_users(ack, body, logger, client, view):
    print('send_dm_to_users ■□■□■□■□■□■□■□■□■□■□■□ ')
    ack()
    local_session = SESSION()
    try:
        userinfo = client.users_info(
            user=body['user']['id'],
            include_locale=True
        )
    except SlackApiError as e:
        print("Error fetching conversations: {}".format(e))
    locale = userinfo['user']['locale']
    if locale == 'ja-JP':
        text_admintool = "送信先を選択\n未選択の場合はインストールした人全員に送信されます"
        text_label = "選択する"
        text_input_label = "送信内容を入力"
    else:
        text_admintool = "Select a recipient\nIf not selected, the message will be sent to everyone who has installed the software." 
        text_label = "Select Target"
        text_input_label = "Enter the content to be sent via DM"

    try:
        slack_installations_all = local_session.query(SlackInstallations).all()
    finally:
        print('finish find slack_installations')
    options = []
    for slack_installation in slack_installations_all:
        text = ""
        if slack_installation.user_email is not None:
            text = slack_installation.team_name + ' : ' + slack_installation.user_email
        else:
            text = slack_installation.team_name

        add_option = [
                {
                    "text": {
                        "type": "plain_text",
                        "emoji": True,
                        "text": text
                    },
                    "value": str(slack_installation.id)
                },
        ]
        options = options + add_option
    blocks = [
		{
			"type": "section",
            "block_id": "target",
			"text": {
				"type": "mrkdwn",
				"text": text_admintool
			},
			"accessory": {
				"type": "static_select",
                "action_id": "selected_target",
				"placeholder": {
					"type": "plain_text",
					"emoji": True,
					"text": text_label
				},
				"options": options
			}
		},
		{
			"type": "input",
            "block_id": "dm_text",
			"element": {
				"type": "plain_text_input",
				"multiline": True,
				"action_id": "dm_text"
			},
			"label": {
				"type": "plain_text",
				"text": text_input_label,
				"emoji": True
			}
		}
    ]
    client.views_open(
        trigger_id=body["trigger_id"],
        # ビューのペイロード
        view={
            "type": "modal",
            "callback_id": "dm_for_installed_users_confirm",
            "title": {"type": "plain_text", "text":"ユーザーDM送信"},
            "submit": {"type": "plain_text", "text":"確認"},
            "blocks": blocks
        }
    )

    local_session.close()

@bolt_app.view("dm_for_installed_users_confirm")
def dm_for_installed_users_confirm(ack, body, payload, client, view, logger):
    print('start dm_for_installed_users_confirm')
    try:
        userinfo = client.users_info(
            user=body['user']['id'],
            include_locale=True
        )
    except SlackApiError as e:
        print("Error fetching conversations: {}".format(e))
    locale = userinfo['user']['locale']

    local_session = SESSION()
    """
    print(view["state"]["values"])
    print(view["state"]["values"]["target"]["selected_target"]["selected_option"])
    print(view["state"]["values"]["dm_text"]["dm_text"]["value"])
    """

    slack_installation_id = Null
    if view["state"]["values"]["target"]["selected_target"]["selected_option"] is not None:
        slack_installation_id = view["state"]["values"]["target"]["selected_target"]["selected_option"].get('value')
    print('6666666')
    print(slack_installation_id)
    blocks = []
    targetlist = ''
    slack_installation_id_list = ''
    #Nullの場合は全員に送信する
    #If Null, send to all users.
    if slack_installation_id is Null:
        try:
            slack_installations_all = local_session.query(SlackInstallations).all()
        finally:
            print('finish find slack_installations')
        for slack_installation in slack_installations_all:
            targetlist = targetlist + slack_installation.team_name + ' : ' + slack_installation.user_email + '\n'
            slack_installation_id_list = slack_installation_id_list + str(slack_installation.id) + ','
    else:
        print('not Null')
        try:
            slack_installation = local_session.query(SlackInstallations).filter_by(id = slack_installation_id).first()
        finally:
            print('finish find slack_installations')
            print(slack_installation)
        targetlist = targetlist + slack_installation.team_name + ' : ' + slack_installation.user_email + '\n'
        slack_installation_id_list = str(slack_installation.id)

    if locale == 'ja-JP':
        text_target = "*送信先*\n\n"
        text_message = "*送信内容*\n\n"
    else:
        text_target = "*Send DM to*\n\n"
        text_message = "*Message*\n\n"

    blocks = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": text_target + targetlist
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": text_message + view["state"]["values"]["dm_text"]["dm_text"]["value"]
            }
        }, 
    ]
    private_metadata={
        "slack_installation_id_list": slack_installation_id_list,
        "text": view["state"]["values"]["dm_text"]["dm_text"]["value"]
    }
    view={
        "type": "modal",
        "callback_id": "dm_for_installed_users_send",
        "private_metadata": json.dumps(private_metadata),
        "title": {"type": "plain_text", "text":"DM送信"},
        "submit": {"type": "plain_text", "text": "送信する"},
        "blocks": blocks
    }
    ack(response_action="update", view=view)
    local_session.close()

@bolt_app.view("dm_for_installed_users_send")
def dm_for_installed_users_send(ack, body, payload, client, view, logger):
    print('dm_for_installed_users_send')
    ack()
    local_session = SESSION()
    private_metadata = json.loads(body['view']['private_metadata'])
    slack_installation_id_list_text = private_metadata['slack_installation_id_list'].split(',')
    slack_installation_id_list = []
    for slack_installation_id in slack_installation_id_list_text:
        if slack_installation_id != '':
            slack_installation_id_list.append(int(slack_installation_id))
    text = private_metadata['text']
    try:
        slack_installations = local_session.query(SlackInstallations).filter(SlackInstallations.id.in_(slack_installation_id_list)).all()
    finally:
        print('finish find slack_installations')

    owner_client = WebClient(token=os.environ.get("APP_OWNER_TOKEN"))
    try:
        sender_userinfo = owner_client.users_info(
            user=os.environ.get("APP_OWNER_ID"),
            include_locale=True
        )
    except SlackApiError as e:
        print("Error fetching conversations: {}".format(e))
    #送信者のデータ
    private_metadata = {
        "email": sender_userinfo['user']['profile']['email'],
        "user_id": sender_userinfo['user']['id'],
        "team_id": sender_userinfo['user']['team_id'],
        "real_name": sender_userinfo['user']['real_name'],
        "tz": sender_userinfo['user']['tz'],
        "tz_label": sender_userinfo['user']['tz_label'],
        "image_512": sender_userinfo['user']['profile']['image_192'],
        "is_admin": sender_userinfo['user']['is_admin'],
        "is_owner": sender_userinfo['user']['is_owner'],
        "locale": sender_userinfo['user']['locale'],
        "team_name": os.environ.get("APP_OWNER_TEAM_NAME")
    }


    for slack_installation in slack_installations:
        print("ループ" + slack_installation.user_email)
        print(vars(slack_installation))
        client = WebClient(token=slack_installation.bot_token)
        try:
            userinfo = client.users_info(
                user=slack_installation.user_id,
                include_locale=True
            )
        except SlackApiError as e:
            print("Error fetching conversations: {}".format(e))

        locale = userinfo['user']['locale']
        if locale == 'ja-JP':
            header_text = ":mega:" + os.environ.get("APP_NAME") + " よりお知らせ"
            label = "返信はこちらから"
            text_button = "送信する"
        else:
            header_text = ":mega: Announcement from " + os.environ.get("APP_NAME")
            label = "Fill out the reply here."
            text_button = "Send"

        params={
            "team_id": slack_installation.team_id,
            "user_id": slack_installation.user_id,
        }
        blocks = create_feedback_blocks(header_text,text,private_metadata,params,userinfo['user']['locale'])

        client = WebClient(token=slack_installation.bot_token)
        try:
            client.chat_postMessage(
                channel=slack_installation.user_id,
                text=text,
                blocks=blocks
            )
        except SlackApiError as e:
            print("Error chat_postMessage: {}".format(e))

    local_session.close()

@bolt_app.action(re.compile("send_replies"))
def send_replies(ack, body, logger, client, view):
    print('send_replies ■□■□■□■□■□■□■□■□■□■□■□')
    ack()
    try:
        conversations_info = client.conversations_info(
            channel=body["channel"]["id"]
        )
    except SlackApiError as e:
        print("Error fetching conversations_info: {}".format(e))

    to_user = False
    to_developer = False
    #チャンネルからのpostの場合は、開発者からユーザーへのpost
    #If the post is from a channel, the post is from the developer to the user.
    if conversations_info["channel"].get('is_channel') == True:
        to_user = True
    #DMからのpostの場合は、ユーザーから開発者へのpost
    #In the case of post from DM, post from user to developer
    if conversations_info["channel"].get('is_im') == True:
        to_developer = True
    local_session = SESSION()
    #private_metadata にはフィードバックを書いたユーザーの情報が入る

    #ユーザー側のtsを格納する
    message_ts = Null
    dev_message_ts = Null
    params = {}
    if body['actions'][0]['action_id'].split('|')[1] != '':
        print("param有り")
        params = json.loads(body['actions'][0]['action_id'].split('|')[1])
        team_id = params.get('team_id')
        user_id = params.get('user_id')
        if to_developer == True:
            print("to_developer")
            if params.get('message_ts') is None:
                print("add message_ts")
                message_ts = body["container"]["message_ts"]
                params["message_ts"] = message_ts
            else:
                message_ts = params.get('message_ts')
            if params.get('dev_message_ts') is not None:
                print("params.get('dev_message_ts') is not None")
                dev_message_ts = params.get('dev_message_ts')
                print("dev_message_ts:aad " + dev_message_ts)
        if to_user == True:
            print("to_user")
            if params.get('dev_message_ts') is None:
                print("add dev_message_ts")
                dev_message_ts = body["container"]["message_ts"]
                params["dev_message_ts"] = dev_message_ts
            else:
                dev_message_ts = params.get('dev_message_ts')
            if params.get('message_ts') is not None:
                message_ts = params.get('message_ts')
    else:
        print("paramなし")
        if to_developer == True:
            print("to_developer")
            message_ts = body["container"]["message_ts"]
            params["message_ts"] = message_ts
        if to_user == True:
            print("to_user")
            dev_message_ts = body["container"]["message_ts"]
            params["dev_message_ts"] = dev_message_ts

    #組織名を取得したいので、送信者のuserinfoからSlackInstallationsを取得する
    #To get the organization name, so we get SlackInstallations from the sender's userinfo.
    try:
        sender_slack_installations = local_session.query(SlackInstallations).filter_by(team_id=body['team']['id']).order_by(SlackInstallations.id.desc()).first()
    finally:
        print('finish find sender_slack_installations--')
    sender_client = WebClient(token=sender_slack_installations.bot_token)
    try:
        sender_userinfo = sender_client.users_info(
            user=body["user"]["id"],
            include_locale=True
        )
    except SlackApiError as e:
        print("Error fetching conversations: {}".format(e))

    private_metadata = {
        "email": sender_userinfo['user']['profile']['email'],
        "user_id": sender_userinfo['user']['id'],
        "team_id": sender_userinfo['user']['team_id'],
        "real_name": sender_userinfo['user']['real_name'],
        "tz": sender_userinfo['user']['tz'],
        "tz_label": sender_userinfo['user']['tz_label'],
        "image_512": sender_userinfo['user']['profile']['image_192'],
        "is_admin": sender_userinfo['user']['is_admin'],
        "is_owner": sender_userinfo['user']['is_owner'],
    }
    private_metadata['team_name'] = sender_slack_installations.team_name
    sender_locale = sender_userinfo['user']['locale']

    #送信相手のinstallationを取得する
    #Get the installation of the sender.
    try:
        user_slack_installations = local_session.query(SlackInstallations).filter_by(user_id=user_id).first()
    finally:
        print('finish find user_slack_installations--')
    user_client = WebClient(token=user_slack_installations.bot_token)
    try:
        userinfo = user_client.users_info(
            user=user_id,
            include_locale=True
        )
    except SlackApiError as e:
        print("Error fetching conversations: {}".format(e))
    #送信先ユーザのlocaleを入れる
    #Enter the locale of the destination user.
    private_metadata['locale'] = userinfo['user']['locale']

    #メッセージを送信した時にスレッドに送信内容をpostするためのテキストを生成
    #Generate text to post to a thread when a message is sent.
    if sender_locale == 'ja-JP':
        text = "送信者： <@" + sender_userinfo['user']['id'] + '>\n送信内容：\n' + body["state"]["values"]["dm_text"]["dm_text"]["value"]
    else:
        text = "Sender： <@" + sender_userinfo['user']['id'] + '>\nText：\n' + body["state"]["values"]["dm_text"]["dm_text"]["value"]

    #送信者のスレッドに自分のメッセージを追加
    #Add message to the sender's thread
    #to_developer と to_user で使用するthread_tsが違うので注意してください
    #Note that the thread_ts used by to_developer and to_user are different.
    if to_developer == True:
        #送信内容を送信したユーザーのスレッドに追加
        #Add the sent content to the thread of the user who sent it.
        if message_ts is not Null:
            #スレッド元がある場合はthread_tsを設定する
            #If there is a thread source, set thread_ts
            try: 
                client.chat_postMessage(
                    channel=body["container"]["channel_id"],
                    thread_ts=message_ts,
                    text=text
                )
            except SlackApiError as e:
                print("Error chat_postMessage: {}".format(e))
        else:
            try:
                client.chat_postMessage(
                    channel=body["container"]["channel_id"],
                    thread_ts=body["container"]["message_ts"],
                    text=text
                )
            except SlackApiError as e:
                print("Error chat_postMessage: {}".format(e))
    if to_user == True:
        if dev_message_ts is not Null:
            print("dev_message_ts is not Null")
            print(dev_message_ts)
            try: #送信内容を送信したユーザーのスレッドに追加
                client.chat_postMessage(
                    channel=body["container"]["channel_id"],
                    thread_ts=dev_message_ts,
                    text=text
                )
            except SlackApiError as e:
                print("Error fetching conversations: {}".format(e))
        else:
            print("dev_message_ts is Null")
            try: #送信内容を送信したユーザーのスレッドに追加
                client.chat_postMessage(
                    channel=body["container"]["channel_id"],
                    thread_ts=body["container"]["message_ts"],
                    text=text
                )
            except SlackApiError as e:
                print("Error fetching conversations: {}".format(e))


    #相手に向けたメッセージ送信
    #Send a message to the other person.
    if to_user == True:
        print('start to_user')
        try:
            slack_installations_to = local_session.query(SlackInstallations).filter_by(team_id=team_id).order_by(SlackInstallations.id.desc()).first()
        finally:
            print('finish find slack_installations_to')
        client = WebClient(token=slack_installations_to.bot_token)
        try:
            app_userinfo = client.users_info(
                user=user_id,
                include_locale=True
            )
        except SlackApiError as e:
            print("Error fetching users_info: {}".format(e))
        app_user_locale = app_userinfo['user']['locale']
        if app_user_locale == "ja-JP":
            header_text = "開発者より返事が届きました"
        else:
            header_text = "Received a reply from the developer."
        try:
            blocks = create_feedback_blocks(header_text,body["state"]["values"]["dm_text"]["dm_text"]["value"],private_metadata,params,app_user_locale)
        except Exception as e:
            print(e)

        if message_ts is Null:
            print("message_ts is None:::message_ts is None")
            try:
                client.chat_postMessage(
                    channel=user_id,
                    text=body["state"]["values"]["dm_text"]["dm_text"]["value"],
                    blocks = blocks,
                )
            except SlackApiError as e:
                print("Error fetching conversations: {}".format(e))
        else:
            print("message_ts is not None:::")
            try:
                client.chat_postMessage(
                    channel=user_id,
                    thread_ts=message_ts,
                    text=body["state"]["values"]["dm_text"]["dm_text"]["value"],
                    reply_broadcast=True,
                    blocks = blocks
                )
            except SlackApiError as e:
                print("Error fetching conversations: {}".format(e))
    elif to_developer == True:
        print("to_developer")
        client = WebClient(token=os.environ.get("APP_OWNER_TOKEN"))
        app_owner_id = os.environ.get("APP_OWNER_ID")
        app_owner_ws_id = os.environ.get("APP_OWNER_WS_ID")
        try:
            slack_installations_owner = local_session.query(SlackInstallations).filter_by(user_id = app_owner_id,team_id=app_owner_ws_id).order_by(SlackInstallations.id.desc()).first()
        finally:
            print('finish find slack_installations_owner')
        client = WebClient(token=slack_installations_owner.bot_token)
        try:
            owner_userinfo = client.users_info(
                user=app_owner_id,
                include_locale=True
            )
        except SlackApiError as e:
            print("Error fetching users_info: {}".format(e))
        owner_locale = owner_userinfo['user']['locale']
        if owner_locale == "ja-JP":
            header_text = "ユーザーから連絡が入りました"
        else:
            header_text = "A user has contacted us."

        blocks = create_feedback_blocks(header_text,body["state"]["values"]["dm_text"]["dm_text"]["value"],private_metadata,params,owner_locale)
        add_mention_block = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text":  "<@" + os.environ.get("APP_OWNER_ID") + ">"
                },
            },
        ]
        blocks = blocks + add_mention_block
        if dev_message_ts is Null:
            print("dev_message_ts is Null")
            try:#送信完了のお知らせをユーザーにpost
                client.chat_postMessage(
                    channel=os.environ.get("APP_OWNER_CONTACT_CHANNEL_ID"),
                    text=body["state"]["values"]["dm_text"]["dm_text"]["value"],
                    blocks = blocks
                )
            except SlackApiError as e:
                print("Error fetching conversations: {}".format(e))
        else:
            print("dev_message_ts is not Null")
            try:#送信完了のお知らせをユーザーにpost
                client.chat_postMessage(
                    channel=os.environ.get("APP_OWNER_CONTACT_CHANNEL_ID"),
                    thread_ts=dev_message_ts,
                    text=body["state"]["values"]["dm_text"]["dm_text"]["value"],
                    blocks = blocks
                )
            except SlackApiError as e:
                print("Error fetching conversations: {}".format(e))

    local_session.close()

feedback = Blueprint('feedback', __name__)