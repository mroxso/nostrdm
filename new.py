import tkinter as tk
import json
import ssl
import time
from nostr.filter import Filter, Filters
from nostr.event import Event, EventKind
from nostr.relay_manager import RelayManager
from nostr.message_type import ClientMessageType

pubkey = "82341f882b6eabcd2ba7f1ef90aad961cf074af15b9ef44a09f9d2a8fbfbe6a2"

def loadNameForPubkey(pubkey):
    filters = Filters([Filter(kinds=[EventKind.SET_METADATA], authors=[pubkey], limit=1)])
    # generate a random uuid
    subscription_id = "12345678-1234-5678-1234-567812345677"
    request = [ClientMessageType.REQUEST, subscription_id]
    request.extend(filters.to_json_array())

    relay_manager = RelayManager()
    relay_manager.add_relay("wss://relay.damus.io")
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

        name = json_content["username"]
        if(name == ""):
            name = json_content["name"]
        if(name == ""):
            name = json_content["display_name"]

        print(json_content["display_name"])
        # self.tree.item(item=event_msg.event.public_key, text=event_msg.event.public_key, values=(name))
        # find item with pubkey and update it
        for i in range(listbox.size()):
            if(listbox.get(i) == event_msg.event.public_key):
                listbox.delete(i)
                listbox.insert(i, name)
                break
        

    relay_manager.close_connections()

def loadConversations():
    filters = Filters([Filter(kinds=[EventKind.ENCRYPTED_DIRECT_MESSAGE], pubkey_refs=[pubkey])])
    subscription_id = "12345678-1234-5678-1234-567812345678"
    request = [ClientMessageType.REQUEST, subscription_id]
    request.extend(filters.to_json_array())

    relay_manager = RelayManager()
    relay_manager.add_relay("wss://relay.damus.io")
    relay_manager.add_subscription(subscription_id, filters)
    relay_manager.open_connections({"cert_reqs": ssl.CERT_NONE}) # NOTE: This disables ssl certificate verification
    time.sleep(1.25) # allow the connections to open

    message = json.dumps(request)
    relay_manager.publish_message(message)
    time.sleep(1) # allow the messages to send

    while relay_manager.message_pool.has_events():
        event_msg = relay_manager.message_pool.get_event()
    #   print(event_msg.event.content)
        if event_msg.event.public_key not in listbox.get(0, tk.END):
            listbox.insert(tk.END, event_msg.event.public_key)

    # for i in range(listbox.size()):
    #     loadNameForPubkey(listbox.get(i))

    relay_manager.close_connections()



root = tk.Tk()
root.title("nostrdm")
root.geometry("500x500")

listbox = tk.Listbox(root)
listbox.config(width=500, height=500)
listbox.pack()

loadConversations()

root.mainloop()