import enum
from typing import NamedTuple


class GptModel(enum.Enum):
    # see: https://beta.openai.com/docs/models/gpt-3
    davinci = "text-davinci-003"
    curie = "text-curie-001"
    babbage = "text-babbage-001"
    ada = "text-ada-001"


class Colors(enum.Enum):
    # using RL_PROMPT_START_IGNORE ('\001') and RL_PROMPT_END_IGNORE ('\002') to get the readline module
    # to ignore the color sequences in prompt when calculating cursor position
    black = '\001\033[90m\002'
    red = '\001\033[91m\002'
    green = '\001\033[1;92m\002'
    yellow = '\001\033[93m\002'
    blue = '\001\033[1;94m\002'
    magenta = '\001\033[1;95m\002'
    cyan = '\001\033[96m\002'
    white = '\001\033[97m\002'
    end = '\001\033[0m\002'


class ThemeMode(enum.Enum):
    dark = 0
    light = 1


class ThemeColors(NamedTuple):
    title: str
    info: str   # shell info color
    cinfo: str  # console info color
    prompt: str
    cmessage: str
    cinput: str
    cresponse: str
    end: str = Colors.end.value


class VoiceStop(enum.Enum):
    period = 0
    newline = 1
