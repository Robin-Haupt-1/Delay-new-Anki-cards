import datetime
from aqt.qt import QAction
from aqt.utils import showInfo, tooltip

from .constants import *
from .utils import *
from aqt import mw
from aqt import gui_hooks
import datetime
from anki.consts import *


def suspend_service(conf: ConfigManager):
    """Delay new cards for a few days (with specific settings for different decks) and activate them again after the specified time has passed"""

    deck_config = [{"deck": "All::1) Sprachen::💬 Begriffe", "delay": 3}, {"deck": "All::1) Sprachen::🇺🇸 Englisch::_New", "delay": 6}, {"deck": "All::1) Sprachen::🇺🇸 Englisch::_New (rare)", "delay": 3}, {"deck": "*", "delay": 1}]
    seen_cards = []
    # process decks with specific delay settings
    for deck in deck_config:
        # suspend new cards
        all_cards=mw.col.find_cards(f'"deck:{deck["deck"]}" is:new -is:suspended')
        suspend_ids = [mw.col.get_card(card_id) for card_id in all_cards if card_id not in conf.get(SUSPENDED_CARDS) and card_id not in seen_cards]
        suspend = [card for card in suspend_ids if ((datetime.datetime.now().timestamp() // 86400) - (card.mod // 86400)) < deck["delay"]]

        # save suspended card ids to config
        conf.set(SUSPENDED_CARDS, conf.get(SUSPENDED_CARDS) + [card.id for card in suspend])
        for card in suspend:
            card.queue = anki.consts.QUEUE_TYPE_SUSPENDED
            card.flush()

        if suspend:
            log(f"{len(suspend)} cards to suspend in deck {deck['deck']}")
        seen_cards += all_cards


        # reactivate old cards
        all_cards=mw.col.find_cards(f'"deck:{deck["deck"]}" is:new is:suspended')
        reactivate_ids = [mw.col.get_card(card_id) for card_id in all_cards if
                          card_id in conf.get(SUSPENDED_CARDS) and card_id not in conf.get(REACTIVATED_CARDS) and card_id not in seen_cards]
        reactivate = [card for card in reactivate_ids if ((datetime.datetime.now().timestamp() // 86400) - (card.mod // 86400)) >= deck["delay"]]

        # save reactivated card ids to config
        conf.set(REACTIVATED_CARDS, conf.get(REACTIVATED_CARDS) + [card.id for card in reactivate])

        for card in reactivate:
            card.queue = anki.consts.QUEUE_TYPE_NEW
            card.flush()

        if reactivate:
            log(f"{len(reactivate)} cards to reactivate in deck {deck['deck']}")
        seen_cards += all_cards

        #print("seen cards",seen_cards)

    return
    """suspend new cards and unsuspend new cards that are old enough to be learned"""

    # suspend other new cards
    new_other_cards_ids = [mw.col.get_card(card_id) for card_id in mw.col.find_cards('is:new -is:suspended') if should_suspend(card_id)]
    new_other_cards = [card for card in new_other_cards_ids if too_young(card)]

    # save suspended card ids to config
    conf.set(SUSPENDED_CARDS, conf.get(SUSPENDED_CARDS) + [card.id for card in new_other_cards])
    for card in new_other_cards:
        card.queue = anki.consts.QUEUE_TYPE_SUSPENDED
        card.flush()

    if new_other_cards:
        log(f"{len(new_other_cards)} cards to suspend in miscellaneous decks")

    # reactivate other cards after one day
    old_other_cards = [mw.col.get_card(card_id) for card_id in mw.col.find_cards('is:new is:suspended') if should_reactivate(card_id)]
    old_other_cards = [card for card in old_other_cards if old_enough(card)]
    conf.set(REACTIVATED_CARDS, conf.get(REACTIVATED_CARDS) + [card.id for card in old_other_cards])

    for card in old_other_cards:
        card.queue = anki.consts.QUEUE_TYPE_NEW
        card.flush()

    if old_other_cards:
        log(f"{len(old_other_cards)} cards to reactivate in miscellaneous decks")
