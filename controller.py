from model import *


def add_message(conversation, user_id, body, created_when):
    message = Message(conversation=conversation, author=user_id, body=body, created_when=created_when)
    chat = Chat(pk=conversation).update(modified_when=created_when)
    return message.save()


def create_chat(users):
    conv = Chat(participants=users)
    return conv.save()


def get_chat(users):
    conv = Chat.objects(__raw__={"participants": {"$all": users}}).first()
    return conv


def get_chats_user(user_id, s=0, l=10):
    l = int(l)
    s = int(s)
    t1 = datetime.datetime.now()
    chats = Chat.objects.filter(participants__contains=user_id).order_by('-modified_when').skip(s).limit(l)
    t2 = datetime.datetime.now()
    print(t2-t1)
    return chats


def get_chat_by_id(chat_id):
    return Chat.objects(pk=chat_id).first()


def get_all_messages(chat_id, fields):
    return Message.objects(conversation=chat_id).only(*fields).order_by('created_when')


def get_all_chats(user_id):
    conv = Chat(participants__contains=user_id).order_by('-modified_when')
    # if limit > len(conv):
    #     limit = len(conv)
    return conv


def get_last_msg(chat_id):
    msg = Message.objects(conversation=chat_id).order_by('-created_when').first()
    return msg

