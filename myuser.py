from google.appengine.ext import ndb


class MyUser(ndb.Model):
    name = ndb.StringProperty()
    emailAddress = ndb.StringProperty()
    userWordCount = ndb.IntegerProperty(default=0)
    userAnagramCount = ndb.IntegerProperty(default=0)
