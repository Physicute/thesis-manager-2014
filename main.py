import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

DEFAULT_GUESTBOOK_NAME = 'default_guestbook'

def guestbook_key(guestbook_name=DEFAULT_GUESTBOOK_NAME):
    return ndb.Key('Guestbook', guestbook_name)


class Greeting(ndb.Model):
    author = ndb.UserProperty()
    content = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)


class MainPage(webapp2.RequestHandler):
    def get(self):
        guestbook_name = self.request.get('guestbook_name',
                                          DEFAULT_GUESTBOOK_NAME)
        greetings_query = Greeting.query(
            ancestor=guestbook_key(guestbook_name)).order(-Greeting.date)
        greetings = greetings_query.fetch(10)

        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'greetings': greetings,
            'guestbook_name': urllib.quote_plus(guestbook_name),
            'url': url,
            'url_linktext': url_linktext,
            'user_name': users.get_current_user()
        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))

class Guestbook(webapp2.RequestHandler):

    def post(self):
        guestbook_name = self.request.get('guestbook_name',
                                          DEFAULT_GUESTBOOK_NAME)
        greeting = Greeting(parent=guestbook_key(guestbook_name))

        if users.get_current_user():
            greeting.author = users.get_current_user()

        greeting.content = self.request.get('content')
        greeting.put()

        query_params = {'guestbook_name': guestbook_name}
        self.redirect('/?' + urllib.urlencode(query_params))

class Student(ndb.Model):
    stu_first = ndb.StringProperty(indexed=False)
    stu_last = ndb.StringProperty(indexed=False)
    stu_mail = ndb.StringProperty(indexed=False)
    stu_numb = ndb.StringProperty(indexed=False)

class StudentSuccessPageHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('stusuccess.html')
        self.response.write(template.render())

class StudentIdHandler(webapp2.RequestHandler):
    def get(self, students_id):
        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        students = Student.query().fetch()
        students_id = int(students_id)
        template_values={
            'url': url,
            'url_linktext': url_linktext,
            'user_name': users.get_current_user(),
            'id': students_id,
            'all_students': students
        }
        template = JINJA_ENVIRONMENT.get_template('stuid.html')
        self.response.write(template.render(template_values))

class StudentListHandler(webapp2.RequestHandler):
    def get(self):
        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        students = Student.query().fetch()
        template_values = {
            'url': url,
            'url_linktext': url_linktext,
            'user_name': users.get_current_user(),
            "all_students": students
        }
        template = JINJA_ENVIRONMENT.get_template('stulist.html')
        self.response.write(template.render(template_values))

class StudentNewHandler(webapp2.RequestHandler):
    def get(self):
        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'url': url,
            'url_linktext': url_linktext,
            'user_name': users.get_current_user()
        }
        template = JINJA_ENVIRONMENT.get_template('stureg.html')
        self.response.write(template.render(template_values))

    def post(self):
        students = Student()
        students.stu_first = self.request.get('stu_first')
        students.stu_last = self.request.get('stu_last')
        students.stu_mail = self.request.get('stu_mail')
        students.stu_numb = self.request.get('stu_numb')
        students.put()  
        self.redirect('/student/success') 

class StudentEditHandler(webapp2.RequestHandler):
    def get(self, students_id):
        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        students = Student.query().fetch()
        students_id = int(students_id)
        template_values={
            'url': url,
            'url_linktext': url_linktext,
            'user_name': users.get_current_user(),
            'id': students_id,
            'all_students': students
        }
        template = JINJA_ENVIRONMENT.get_template('stuedit.html')
        self.response.write(template.render(template_values))
    
    def post(self, students_id):
        students_id = int(students_id)
        students = Student.get_by_id(students_id)
        students.stu_first = self.request.get('stu_first')
        students.stu_last = self.request.get('stu_last')
        students.stu_mail = self.request.get('stu_mail')
        students.stu_numb = self.request.get('stu_numb')
        students.put()  
        self.redirect('/student/success')          

class Thesis(ndb.Model):
    thesis_title = ndb.StringProperty(indexed=False)
    thesis_desc = ndb.StringProperty(indexed=False)
    thesis_year = ndb.StringProperty(indexed=False)
    stat = ndb.StringProperty(indexed=False)

class ThesisSuccessPageHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('thesuccess.html')
        self.response.write(template.render())

class ThesisIdHandler(webapp2.RequestHandler):
    def get(self, thesis_id):
        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        thesis = Thesis.query().fetch()
        thesis_id = int(thesis_id)
        template_values={
            'url': url,
            'url_linktext': url_linktext,
            'user_name': users.get_current_user(),
            'id': thesis_id,
            'all_thesis': thesis
        }
        template = JINJA_ENVIRONMENT.get_template('thesisid.html')
        self.response.write(template.render(template_values))

class ThesisListHandler(webapp2.RequestHandler):
    def get(self):
        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        thesis = Thesis.query().fetch()
        template_values = {
            'url': url,
            'url_linktext': url_linktext,
            'user_name': users.get_current_user(),
            "all_thesis": thesis    
        }
        template = JINJA_ENVIRONMENT.get_template('thesislist.html')
        self.response.write(template.render(template_values))

class ThesisNewHandler(webapp2.RequestHandler):
    def get(self):
        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'url': url,
            'url_linktext': url_linktext,
            'user_name': users.get_current_user()
        }
        template = JINJA_ENVIRONMENT.get_template('thesisreg.html')
        self.response.write(template.render(template_values))

    def post(self):
        thesis = Thesis()
        thesis.thesis_title = self.request.get('thesis_title')
        thesis.thesis_desc = self.request.get('thesis_desc')
        thesis.thesis_year = self.request.get('thesis_year')
        thesis.stat = self.request.get('stat')
        thesis.put()  
        self.redirect('/thesis/success')  

class ThesisEditHandler(webapp2.RequestHandler):
    def get(self, thesis_id):
        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        thesis = Thesis.query().fetch()
        thesis_id = int(thesis_id)
        template_values={
            'url': url,
            'url_linktext': url_linktext,
            'user_name': users.get_current_user(),
            'id': thesis_id,
            'all_thesis': thesis
        }
        template = JINJA_ENVIRONMENT.get_template('thesisedit.html')
        self.response.write(template.render(template_values))

    def post(self, thesis_id):
        thesis_id = int(thesis_id)
        thesis = Thesis.get_by_id(thesis_id)
        thesis.thesis_title = self.request.get('thesis_title')
        thesis.thesis_desc = self.request.get('thesis_desc')
        thesis.thesis_year = self.request.get('thesis_year')
        thesis.stat = self.request.get('stat')
        thesis.put()  
        self.redirect('/thesis/success')

class Adviser(ndb.Model):
    ad_title = ndb.StringProperty(indexed=False)
    ad_first = ndb.StringProperty(indexed=False)
    ad_last = ndb.StringProperty(indexed=False)
    ad_mail = ndb.StringProperty(indexed=False)
    ad_numb = ndb.StringProperty(indexed=False)
    ad_dept = ndb.StringProperty(indexed=False)

class AdSuccessPageHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('adsuccess.html')
        self.response.write(template.render())

class AdIdHandler(webapp2.RequestHandler):
    def get(self, ad_id):
        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        advise = Adviser.query().fetch()
        advise_id = int(ad_id)
        template_values={
            'url': url,
            'url_linktext': url_linktext,
            'user_name': users.get_current_user(),
            'id': advise_id,
            'all_advise': advise
        }
        template = JINJA_ENVIRONMENT.get_template('adid.html')
        self.response.write(template.render(template_values))

class AdListHandler(webapp2.RequestHandler):
    def get(self):
        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        advise = Adviser.query().fetch()
        template_values = {
            'url': url,
            'url_linktext': url_linktext,
            'user_name': users.get_current_user(),
            "all_advise": advise
        }
        template = JINJA_ENVIRONMENT.get_template('adlist.html')
        self.response.write(template.render(template_values))

class AdNewHandler(webapp2.RequestHandler):
    def get(self):
        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'url': url,
            'url_linktext': url_linktext,
            'user_name': users.get_current_user()
        }
        template = JINJA_ENVIRONMENT.get_template('adreg.html')
        self.response.write(template.render(template_values))

    def post(self):
        advise = Adviser()
        advise.ad_title = self.request.get('ad_title')
        advise.ad_first = self.request.get('ad_first')
        advise.ad_last = self.request.get('ad_last')
        advise.ad_mail = self.request.get('ad_mail')
        advise.ad_numb = self.request.get('ad_numb')
        advise.ad_dept = self.request.get('ad_dept')
        advise.put()  
        self.redirect('/adviser/success')

class AdEditHandler(webapp2.RequestHandler):
    def get(self, advise_id):
        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        advise = Adviser.query().fetch()
        advise_id = int(advise_id)
        template_values={
            'url': url,
            'url_linktext': url_linktext,
            'user_name': users.get_current_user(),
            'id': advise_id,
            'all_advise': advise
        }
        template = JINJA_ENVIRONMENT.get_template('adedit.html')
        self.response.write(template.render(template_values))

    def post(self,advise_id):
        advise_id = int(advise_id)
        advise = Adviser.get_by_id(advise_id)
        advise.ad_title = self.request.get('ad_title')
        advise.ad_first = self.request.get('ad_first')
        advise.ad_last = self.request.get('ad_last')
        advise.ad_mail = self.request.get('ad_mail')
        advise.ad_numb = self.request.get('ad_numb')
        advise.ad_dept = self.request.get('ad_dept')
        advise.put()  
        self.redirect('/adviser/success')

application = webapp2.WSGIApplication([
	('/', MainPage),
	('/sign', Guestbook),
    ('/thesis/view/(\d+)',ThesisIdHandler),
    ('/thesis/new', ThesisNewHandler),
    ('/thesis/list', ThesisListHandler),
    ('/thesis/success', ThesisSuccessPageHandler),
    ('/adviser/view/(\d+)', AdIdHandler),
    ('/adviser/new', AdNewHandler),
    ('/adviser/list', AdListHandler),
    ('/adviser/success', AdSuccessPageHandler),
    ('/student/view/(\d+)', StudentIdHandler),
    ('/student/new', StudentNewHandler),
    ('/student/list', StudentListHandler),
    ('/student/success', StudentSuccessPageHandler),
    ('/student/edit/(\d+)', StudentEditHandler),
    ('/adviser/edit/(\d+)', AdEditHandler),
    ('/thesis/edit/(\d+)', ThesisEditHandler)
], debug=True)