from aqt.qt import QAction
from aqt import gui_hooks

from .utils import *

from .main import suspend_service

unsuspend_timer = None



def init():
    """    # add menu option to import new cards
        options_action = QAction("Import from Cambridge ...", mw)
        options_action.triggered.connect(lambda _, o=mw: start_import())
        mw.form.menuTools.addAction(options_action)
     """

    conf = ConfigManager(mw)

    gui_hooks.sync_will_start.append(lambda *args: suspend_service(conf))


    global unsuspend_timer


gui_hooks.profile_did_open.append(lambda *args: init())
