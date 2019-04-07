import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os
from anagramModel import Anagram
from myuser import MyUser
from add import Add
from search import SearchAnagram
from upload import Upload
import logging

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class MainPage(webapp2.RequestHandler):
    def get(self):

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

                logging.info(myuser)

            template_values = {
                'url': url,
                'url_string': url_string,
                'user': user,
                'myuser': myuser,

            }
        template = JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render(template_values))


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/add', Add),
    ('/search', SearchAnagram),
    ('/upload', Upload)
], debug=True)
