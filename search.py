import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os
from anagramModel import Anagram
from myuser import MyUser
import itertools
import logging


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class SearchAnagram(webapp2.RequestHandler):
    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        url = ''
        url_string = ''

        user = users.get_current_user()
        if user is None:
            url = users.create_login_url(self.request.uri)
            url_string = 'login'
            welcome = 'Welcome to Anagram Engine'

            template_values = {
                'url': url,
                'url_string': url_string,
                'user': user,
                'welcome': welcome
            }

            template = JINJA_ENVIRONMENT.get_template('main.html')
            self.response.write(template.render(template_values))

        else:
            url = users.create_logout_url(self.request.uri)
            url_string = 'logout'

            myuser_key = ndb.Key('MyUser', user.email())
            myuser = myuser_key.get()

            if myuser is None:
                welcome = 'Welcome back to the application'
                myuser = MyUser(id=user.email(), emailAddress=user.email())
                myuser.email_address = user.email()
                myuser.put()

            if self.request.get('button') == 'Search':
                searchWord = self.request.get('input_text')
                if searchWord.isalpha():
                    lex = Anagram.processWord(searchWord)

                    anagram_key = ndb.Key('Anagram', lex)
                    anagram = anagram_key.get()

                    if anagram:
                        template_values = {
						'url': url,
						'url_string': url_string,
						'user': user,
						'myuser': myuser,
                        'anagrams' : anagram.words
                        }

                    else:
                        template_values = {
                            'error' : 'No Anagrams Found'
                        }
                else:
                    template_values = {
                        'error' : 'Invalid Search'
                    }

                template = JINJA_ENVIRONMENT.get_template('search.html')
                self.response.write(template.render(template_values))