import message_templates as msg

COMMAND_START = (["start"], msg.START_DESC)
COMMAND_HELP = (["help"], msg.HELP_DESC)
COMMAND_ABOUT = (["whoareyou"], msg.ABOUT_DESC)
COMMAND_POKE = (["poke", "check"], msg.POKE_DESC)
COMMAND_BUSY = (["busy"], msg.BUSY_DESC)
COMMAND_FREE = (['free', 'end', 'done'], msg.FREE_DESC)
COMMAND_CHANGELOG = (['changelog', 'version'], msg.CHANGELOG_DESC)

privileged_commands_info = [
    COMMAND_BUSY,
    COMMAND_FREE,
]

user_commands_info = [
    COMMAND_HELP,
    COMMAND_ABOUT,
    COMMAND_POKE,
    COMMAND_CHANGELOG,
]
