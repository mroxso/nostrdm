import tkinter as tk
from pynostr.relay_manager import RelayManager
from pynostr.filters import FiltersList, Filters
from pynostr.event import EventKind
from pynostr.encrypted_dm import EncryptedDirectMessage
import uuid

class ChatWindow():
    def __init__(self, receiverpubkey, name, relay, pubkey, privkey):
        self.privkey = privkey
        root = tk.Tk()
        root.title("Chat with " + name)
        root.geometry("500x500")

        self.loadMessages(relay=relay, pubkey=pubkey, privkey=privkey)
    
    def loadMessages(self, relay, pubkey, privkey):
        print("Loading messages..")

        relay_manager = RelayManager(timeout=2)
        relay_manager.add_relay(relay)
        filters = FiltersList([Filters(kinds=[EventKind.ENCRYPTED_DIRECT_MESSAGE], pubkey_refs=[pubkey])])
        subscription_id = uuid.uuid1().hex
        relay_manager.add_subscription_on_all_relays(subscription_id, filters)
        relay_manager.run_sync()
        while relay_manager.message_pool.has_notices():
            notice_msg = relay_manager.message_pool.get_notice()
            print(notice_msg.content)
        while relay_manager.message_pool.has_events():
            event_msg = relay_manager.message_pool.get_event()
            dm = EncryptedDirectMessage.from_event(event_msg.event)
            # dm.decrypt(privkey)
            print(dm)


        print("Done")
        pass