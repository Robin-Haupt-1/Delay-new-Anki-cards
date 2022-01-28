from aqt.qt import QAction
from aqt import gui_hooks

from .utils import *

from .main import suspend_new_cards


def init():

    conf = ConfigManager(mw)

    gui_hooks.sync_will_start.append(lambda *args: suspend_new_cards(conf))



gui_hooks.profile_did_open.append(lambda *args: init())
