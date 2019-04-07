import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os
from anagramModel import Anagram
from myuser import MyUser
import logging


JINJA_ENVIRONMENT = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class Upload(webapp2.RequestHandler):
    def get (self):
        self.response.headers['Content-Type'] = 'text/html'
		
        template = JINJA_ENVIRONMENT.get_template('upload.html')
        self.response.write(template.render())

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'

        user = users.get_current_user()
        url = ''
        url_string = ''
        myuser_key = ndb.Key('MyUser', user.email())
        myuser = myuser_key.get()

        if self.request.get('button') == 'Upload':
            filepath = self.request.get('fileToUpload')
            logging.getLogger('scope.name').info(filepath)
            filedata = filepath.splitlines()
            for addWord in filedata:
                if addWord.isalpha():

                    lex = Anagram.processWord(addWord)

                    anagram_key = ndb.Key('Anagram', lex)
                    anagram = anagram_key.get()

                    if anagram:
                        anagram.words.append(addWord)
                        anagram.put()
                        myuser.userWordCount += 1
                        myuser.put()
                    else:
                        newAnagram = Anagram(
                            id=lex,
                            letterCount=len(addWord),
                            words=[addWord.lower()]
                        )

                        newAnagram.put()
                        myuser.userWordCount += 1
                        myuser.userAnagramCount += 1
                        myuser.put()

            template_values = {
                'url': url,
                'url_string': url_string,
                'user': user,
                'myuser': myuser,
                'message': ''
            }
            template = JINJA_ENVIRONMENT.get_template('upload.html')
            self.response.write(template.render(template_values))