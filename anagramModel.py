from google.appengine.ext import ndb
from google.appengine.api import users

class Anagram(ndb.Model):
    letterCount = ndb.IntegerProperty()
    words = ndb.StringProperty(repeated=True)

    @staticmethod
    def processWord(newWord):
        user = users.get_current_user()
        word = newWord.lower()
        word = ''.join(sorted(word))
        userid = user.email()[:user.email().index('@')]
        lex = userid + '$' + word
        return lex
