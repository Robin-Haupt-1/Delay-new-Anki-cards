import requests
import re
import urllib.parse
import time
import socket
import os
import urllib.parse
import urllib.request
from .constants import  REACTIVATED_CARDS, SUSPENDED_CARDS
from .lib import termcolor
import datetime
from aqt import mw
import anki.consts
from .config import ConfigManager


def log(text, start=None, end="\n", color="cyan", start_color="cyan"):
    """Print colorful log to stdout"""
    if start is None:
        start = "{:<10} {:<13}\t".format(datetime.datetime.now().strftime('%H:%M:%S'), f"[DELAY NEW CARDS]")
    print(f"{termcolor.colored(start, start_color)}{termcolor.colored(text, color)}", end=end)


def load_url(url, silent=False):
    """Load a URL while sending an user-agent string to circumvent bot protection measures
    :param silent: whether to print about the event to stdout
    """
    try:
        if not silent:
            print(f'Downloading {url}')
        return requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'}, timeout=120)

    except Exception as e:
        print("❌❌❌ Fehler in load_url!", e, url)


def has_internet_connection(host="8.8.8.8", port=53, timeout=3):
    """Try connecting to the Google DNS server to check internet connectivity"""
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error:
        return False


def wait_for_internet_connection():
    """Try connecting to the Google DNS server to check internet connectivity. Wait until there is connectivity"""
    while not has_internet_connection():
        print("Waiting for internet connection")
        time.sleep(1)
    return True


