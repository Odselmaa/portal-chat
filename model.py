from bson import json_util
from mongoengine import *
import datetime


class CustomQuerySet(QuerySet):
    def to_json(self):
        return "[%s]" % (",".join([doc.to_json() for doc in self]))


class Chat(Document):
    participants = ListField(ObjectIdField())
    created_when = DateTimeField(default=datetime.datetime.now())
    modified_when = DateTimeField()

    meta = {'queryset_class': CustomQuerySet}

    def to_json(self):
        data = self.to_mongo()
        data['_id'] = str(self.id)
        if 'created_when' in data:
            data['created_when'] = self.created_when.timestamp()
        if 'author' in data:
            data['author'] = str(self.author.id)
        if 'modified_when' in data:
            data['modified_when'] = self.modified_when.timestamp()
        data["last_msg"] = Message.objects(conversation=self.id).order_by('-created_when').first().to_mongo()

        for i, p in enumerate(self.participants):
            data['participants'][i] = {"id": str(self.participants[i])}

        return json_util.dumps(data)


class Message(Document):
    conversation = ReferenceField(Chat)
    author = ObjectIdField()
    body = StringField()
    created_when = DateTimeField(default=datetime.datetime.now())
    meta = {'queryset_class': CustomQuerySet}

    def to_json(self):
        data = self.to_mongo()
        data['_id'] = str(self.id)
        if 'created_when' in data:
            data['created_when'] = self.created_when.timestamp()


        if 'author' in data:
            data['author'] = str(self.author)
        if 'conversation' in data:
            data['conversation'] = str(self.conversation.id)


        return json_util.dumps(data)