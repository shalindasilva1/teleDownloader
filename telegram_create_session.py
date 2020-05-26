#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from telethon.sync import TelegramClient
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon import functions, types, utils
from telethon.tl.types import PeerUser, PeerChat, PeerChannel
from secret import *

def callback(current, total):
    print('Downloaded', current, 'out of', total,
          'bytes: {:.2%}'.format(current / total))

with TelegramClient(entity, api_id, api_hash) as client:
    message_id_list = []
    my_channel = client.get_entity(PeerChannel(channel_id))
    for message in client.iter_messages(my_channel):
        message_id_list.append(message.id)
    my_channel_message_list = client(functions.channels.GetMessagesRequest(
        channel=my_channel,
        id=message_id_list
    )).messages
    
    for message in my_channel_message_list:
        if type(message.media) != type(None):
            file_name = message.media.document.attributes[0].file_name
            client.download_media(message, progress_callback=callback, file='storage/'+file_name)
            client(functions.channels.DeleteMessagesRequest(
                channel = my_channel,
                id = [message.id]
            ))
            
    client.log_out()
    
