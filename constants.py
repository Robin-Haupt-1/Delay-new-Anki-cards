import sys
from os.path import join

CONFIG_NAME = "delay-new-cards-config"
SUSPENDED_CARDS = "delayed card ids"
REACTIVATED_CARDS = "reactivated card ids"
CONFIG_DEFAULT_CONFIG = {SUSPENDED_CARDS: [], REACTIVATED_CARDS: []}


def get_os_name():
    """Get the name of the running OS. Returns 'Linux', 'Windows' or 'Mac'"""
    if sys.platform in ['linux', 'linux2']:
        return "Linux"
    if sys.platform in ['Windows', 'win32', 'cygwin']:
        return "Windows"
    if sys.platform in ['Mac', 'darwin', 'os2', 'os2emx']:
        return "Mac"

    raise Exception(f"Unknown OS {sys.platform}")


# save OS name to variable. It doesn't change
os_name = get_os_name()
