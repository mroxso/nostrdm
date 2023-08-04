import tkinter as tk
import json
import uuid
from pynostr.relay_manager import RelayManager
from pynostr.filters import FiltersList, Filters
from pynostr.event import EventKind

pubkey = "82341f882b6eabcd2ba7f1ef90aad961cf074af15b9ef44a09f9d2a8fbfbe6a2"
relay = "wss://relay.damus.io"
# cachedContacts = [{"pubkey": "test", "name":"test"}]
cachedContacts = []

def loadNameForPubkey():
    print("Total contact names to load: " + str(cachedContacts.__len__()))
    for i in range(listbox.size()):
        pubkey = listbox.get(i)
        print(str(i+1) + " - Loading name for " + pubkey)
        relay_manager = RelayManager(timeout=2)
        relay_manager.add_relay(relay)
        filters = FiltersList([Filters(kinds=[EventKind.SET_METADATA], authors=[pubkey], limit=1)])
        subscription_id = uuid.uuid1().hex
        relay_manager.add_subscription_on_all_relays(subscription_id, filters)
        relay_manager.run_sync()
        while relay_manager.message_pool.has_notices():
            notice_msg = relay_manager.message_pool.get_notice()
            print(notice_msg.content)
        while relay_manager.message_pool.has_events():
            event_msg = relay_manager.message_pool.get_event()
            json_content = json.loads(event_msg.event.content)
            # print(json_content)

            try: 
                if(json_content['display_name'] != ""):
                    name = json_content["display_name"]
                elif(json_content['name'] != ""):
                    name = json_content["name"]
                elif(json_content['username'] != ""):
                    name = json_content["username"]
            except KeyError:
                name = event_msg.event.pubkey

            # self.tree.item(item=event_msg.event.public_key, text=event_msg.event.public_key, values=(name))
            # find item with pubkey and update it
            for i in range(listbox.size()):
                if(listbox.get(i) == event_msg.event.pubkey):
                    listbox.delete(i)
                    listbox.insert(i, name)
                    for contact in cachedContacts:
                        if(contact["pubkey"] == event_msg.event.pubkey):
                            print("\t-> " + name)
                            contact["name"] = name
                            break
                    break
            # print(event_msg.event.content)
        # relay_manager.close_all_relay_connections()

def loadConversations():
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
        # json_content = json.loads(event_msg.event)
        # print(event_msg.event.pubkey)
        if event_msg.event.pubkey not in listbox.get(0, tk.END):
            cachedContacts.append({"pubkey": event_msg.event.pubkey, "name": event_msg.event.pubkey})
            listbox.insert(tk.END, event_msg.event.pubkey)

    loadNameForPubkey()

    relay_manager.close_all_relay_connections()

def on_listbox_item_click(event):
    selected_index = listbox.curselection()
    # if(selected_index and event.num == 1):
    # TODO: check for double click or enter instead of one click or scroll
    selected_item = listbox.get(selected_index[0])
    print(selected_item)
    print("-> " + cachedContacts[selected_index[0]]["pubkey"])


root = tk.Tk()
root.title("nostrdm")
root.geometry("500x500")

listbox = tk.Listbox(root)
listbox.config(width=500, height=500)
listbox.bind("<<ListboxSelect>>", on_listbox_item_click)
listbox.pack()

loadConversations()
# print(cachedContacts)

root.mainloop()