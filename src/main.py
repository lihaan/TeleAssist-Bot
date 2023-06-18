from dotenv import dotenv_values
import message_templates as msg
import commands as cmd
import telebot
import rest
import re
import time
import os

curr_path = os.path.dirname(__file__)
secret_path = (os.path.abspath(f"{curr_path}/../.env"))
SECRETS = dotenv_values(secret_path)
MY_USER_ID = int(SECRETS["MY_USER_ID"])
bot = telebot.TeleBot(SECRETS["BOT_TOKEN"])


def msg_from_me(msg): return msg.from_user.id == MY_USER_ID


def is_recent(msg): return int(time.time()) - msg.date < 10


def respond_to(user_msg, response):
    bot.send_message(user_msg.chat.id, response)


all_command_words = [word for word_list in ([info[0] for info in cmd.privileged_commands_info] + [
    info[0] for info in cmd.user_commands_info]) for word in word_list]


def show_avail_commands(commands_info):
    output = []
    for commands, description in commands_info:
        line = ""
        line += ", ".join([f"/{command}" for command in commands])
        line += f": {description}"
        output.append(line)

    return "\n".join(output)


@bot.message_handler(func=lambda x: not is_recent(x), commands=all_command_words)
# Extra check to make sure that bot does not attempt to service commands sent while it was offline
def handle_not_recent(message):
    print(f"{time.asctime()}: Not Recent - {message.from_user.username}")
    # ignore messages that are not recent
    # By right, skip_pending=True should prevent the bot from receiving message "updates" while offline, but doesn't seem to work reliably
    pass


@bot.message_handler(func=is_recent, commands=cmd.COMMAND_START[0])
def handle_start(message):
    print(f"{time.asctime()}: Start - {message.from_user.username}")
    respond_to(message, msg.ABOUT_BOT)
    commands_info = cmd.user_commands_info + \
        cmd.privileged_commands_info if msg_from_me(
            message) else [cmd.user_commands_info]
    respond_to(message, show_avail_commands(commands_info))


@bot.message_handler(commands=cmd.COMMAND_HELP[0])
def handle_help(message):
    print(f"{time.asctime()}: Help - {message.from_user.username}")
    commands_info = cmd.user_commands_info + \
        cmd.privileged_commands_info if msg_from_me(
            message) else [cmd.user_commands_info]
    respond_to(message, show_avail_commands(commands_info))


@bot.message_handler(commands=cmd.COMMAND_ABOUT[0])
def handle_about(message):
    print(f"{time.asctime()}: About - {message.from_user.username}")
    respond_to(message, msg.ABOUT_BOT)


@bot.message_handler(commands=cmd.COMMAND_CHANGELOG[0])
def handle_changelog(message):
    print(f"{time.asctime()}: Changelog - {message.from_user.username}")
    respond_to(message, msg.CHANGELOG)


@bot.message_handler(commands=cmd.COMMAND_POKE[0])
def handle_poke(message):
    print(f"{time.asctime()}: POKE - {message.from_user.username}")
    is_free, reason, end_time, duration_mins_remaining = rest.check_assist_session()
    if is_free:
        respond_to(message, msg.POKE["free"])
        return

    duration_units, duration_num = "mins", round(duration_mins_remaining)
    if abs(duration_mins_remaining) > 60:
        duration_units = "hours"
        duration_num = abs(round(duration_mins_remaining / 60, 1))
    if duration_mins_remaining > 0:
        respond_to(message, msg.POKE['busy'].format(
            reason=reason, duration_num=duration_num, duration_units=duration_units, end_time=end_time.strftime('%#I:%M%p, %A')))
    else:
        respond_to(message, msg.POKE['still_busy'].format(
            reason=reason, duration_num=duration_num, duration_units=duration_units, end_time=end_time.strftime('%#I:%M%p, %A')))


@bot.message_handler(func=msg_from_me, commands=cmd.COMMAND_BUSY[0])
def handle_busy(message):
    print(f"{time.asctime()}: Busy - {message.text}")
    msg_txt = message.text
    for command in cmd.COMMAND_BUSY[0]:
        msg_txt = msg_txt.replace(f"/{command}", "")

    HOUR = r"(hour)|(hr)|h"
    MINUTE = r"(minute)|(min)|m"

    var_list = msg_txt.split(",")
    print(var_list, len(var_list))
    if len(var_list) != 2:
        respond_to(message, msg.BUSY['missing_comma'])
        return

    reason = var_list[1].strip()

    duration_float = re.search(r"([0-9]+\.?[0-9]*)", var_list[0])
    if duration_float is None:
        respond_to(message, msg.BUSY['missing_number'])
        return
    else:
        duration_float = float(duration_float.group(0))

    unit_hour = re.search(HOUR, var_list[0])
    unit_minute = re.search(MINUTE, var_list[0])

    if unit_hour is None and unit_minute is None:
        respond_to(message, msg.BUSY['missing_units'])
        return
    else:
        duration_mins = 60 * duration_float if unit_hour else duration_float

    is_success, reason = rest.start_assist_session(reason, duration_mins)
    if is_success:
        respond_to(message, msg.BUSY['success'])
    elif reason == 1:
        respond_to(message, msg.BUSY['existing'])
    elif reason == 2:
        respond_to(message, msg.BUSY['notif_problem']
                   )


@bot.message_handler(func=msg_from_me, commands=cmd.COMMAND_FREE[0])
def handle_end(message):
    print(f"{time.asctime()}: Free - {message.text}")

    result = rest.end_assist_session()

    if result[0]:
        respond_to(message, msg.FREE['success'])
    elif result[1] == 1:
        respond_to(message, msg.FREE['no_session'])
    elif result[1] == 2:
        respond_to(message, msg.FREE['notif_problem'])


print("Bot ready. Polling...")
bot.infinity_polling(
    interval=0,  # default is 0
    timeout=20,  # default is 20 # Not sure what it does
    # Should skip "pending updates" while bot is offline, but doesn't work reliably
    skip_pending=True
)
