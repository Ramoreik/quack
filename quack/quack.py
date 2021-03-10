#!/usr/bin/python3
import os
import sys
import time
import json
import pyfiglet
from pprint import pprint
from threading import Thread
from colorama import Fore, Back, Style

RESET_CHARS = Fore.RESET + Back.RESET + Style.RESET_ALL
PATH = os.path.dirname(os.path.realpath(__file__))
SPINNER_JSON = os.path.join(PATH, "data", "spinners.json")
SPINNERS = json.load(open(SPINNER_JSON))
STYLES_JSON = os.path.join(PATH, "data", "styles.json")
STYLES = json.load(open(STYLES_JSON))
STYLE_FIELDS = {
    "background": "Back",
    "foreground": "Fore",
    "style": "Style"
}


def spin(spinner: str, fn, *args):
    timer = 0
    idx = 0
    frames = SPINNERS[spinner]["frames"]
    interval = SPINNERS[spinner]["interval"]
    action = Thread(target=fn, args=args)
    action.start()
    while action.is_alive():
        timer += (interval / 1000)
        sys.stdout.write(
            f"[{str(timer).split('.')[0]}s][ {frames[idx]} ]\r"
        )
        sys.stdout.flush()
        time.sleep(interval / 1000)
        if idx == len(frames) - 1:
            idx = 0
        else:
            idx += 1


def ask(prompt: str, style: str):
    chars = __get_style_chars(style)
    if chars:
        answer = input(''.join(chars) + prompt + RESET_CHARS)


def talk(msg: str, style: str):
    chars = __get_style_chars(style)
    if chars:
        print(''.join(chars) + msg + RESET_CHARS)


def eloquate(data: dict, style: str):
    chars = __get_style_chars(style)
    if chars:
        sys.stdout.write(''.join(chars))
        pprint(data, indent=2)
        sys.stdout.write(RESET_CHARS)
        sys.stdout.flush()


def title(msg: str, style: str):
    chars = __get_style_chars(style)
    if chars:
        print(__wrap(msg, "="))


def list_styles():
    for s in STYLES.keys():
        print(s)


def __get_style_chars(style: str):
    s = __get_style(style)
    chars = []
    if s:
        for key in s.keys():
            if key in STYLE_FIELDS:
                chars.append(__get_char(STYLE_FIELDS[key], s[key]))
    return chars


def __get_style(style):
    s = STYLES.get(style, None)
    if s:
        return s
    else:
        raise Exception("Style did not exist in styles.json.")


def __get_char(category: str, choice: str):
    try:
        char = getattr(globals()[category], choice)
        return char
    except AttributeError as e:
        print("Color or Style unavailable in colorama.")
        raise e


def __wrap(msg: str, s: str):
    d = s * len(msg)
    return f"{d}\n{msg}\n{d}"
