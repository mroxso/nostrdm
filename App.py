# import tkinter as tk
from tkinter import *
from tkinter import ttk
from nostr.key import PrivateKey
import json
import ssl
import time
from nostr.filter import Filter, Filters
from nostr.event import Event, EventKind
from nostr.relay_manager import RelayManager
from nostr.message_type import ClientMessageType

class App():
    def __init__(self, relay, pubkey):
        self.relay = relay
        self.pubkey = pubkey

        # private_key = PrivateKey()
        # public_key = private_key.public_key
        # print(f"Private key: {private_key.bech32()}")
        # print(f"Public key: {public_key.bech32()}")

        self.root = Tk()
        self.root.title("nostrdm")

        self.tree = ttk.Treeview(self.root, columns="Name", show="headings")
        # self.tree.grid(column=0, row=0)
        self.tree.pack()

        self.loadDMs()

        self.root.mainloop()

    def loadDMs(self):
        filters = Filters([Filter(kinds=[EventKind.ENCRYPTED_DIRECT_MESSAGE], pubkey_refs=[self.pubkey], limit=100)])
        # generate a random uuid
        subscription_id = "12345678-1234-5678-1234-567812345678"
        request = [ClientMessageType.REQUEST, subscription_id]
        request.extend(filters.to_json_array())

        relay_manager = RelayManager()
        relay_manager.add_relay(self.relay)
        relay_manager.add_subscription(subscription_id, filters)
        relay_manager.open_connections({"cert_reqs": ssl.CERT_NONE}) # NOTE: This disables ssl certificate verification
        time.sleep(1.25) # allow the connections to open

        message = json.dumps(request)
        relay_manager.publish_message(message)
        time.sleep(1) # allow the messages to send

        while relay_manager.message_pool.has_events():
            event_msg = relay_manager.message_pool.get_event()
            # check if tree already has this item in it
            if(not self.tree.exists(event_msg.event.public_key)):
                self.tree.insert("", "end", id=event_msg.event.public_key, text=event_msg.event.public_key, values=(event_msg.event.public_key))
                name = self.loadNameForPubkey(event_msg.event.public_key)


        relay_manager.close_connections()
        pass
    def loadNameForPubkey(self, pubkey):
        filters = Filters([Filter(kinds=[EventKind.SET_METADATA], authors=[pubkey], limit=1)])
        # generate a random uuid
        subscription_id = "12345678-1234-5678-1234-567812345677"
        request = [ClientMessageType.REQUEST, subscription_id]
        request.extend(filters.to_json_array())

        relay_manager = RelayManager()
        relay_manager.add_relay(self.relay)
        relay_manager.add_subscription(subscription_id, filters)
        relay_manager.open_connections({"cert_reqs": ssl.CERT_NONE}) # NOTE: This disables ssl certificate verification
        time.sleep(1.25) # allow the connections to open

        message = json.dumps(request)
        relay_manager.publish_message(message)
        time.sleep(1) # allow the messages to send

        while relay_manager.message_pool.has_events():
            event_msg = relay_manager.message_pool.get_event()
            json_content = json.loads(event_msg.event.content)
            # print(event_msg.event.content)
            name = json_content["display_name"]
            if(name == ""):
                name = json_content["name"]
            if(name == ""):
                name = json_content["username"]
            print(json_content["display_name"])
            self.tree.item(item=event_msg.event.public_key, text=event_msg.event.public_key, values=(name))
            

        relay_manager.close_connections()
        pass