from unittest import TestCase

from linkedlist.core import db
from .helpers import FlaskTestCaseMixin
from .factories import UserFactory

class LinkedListTestCase(TestCase):
    pass

class LinkedListAppTestCase(LinkedListTestCase, FlaskTestCaseMixin):
    def _create_app(self):
        raise NotImplementedError

    def _create_fixtures(self):
        self.user = UserFactory()

    def setUp(self):
        super(LinkedListAppTestCase, self).setUp()
        self.app = self._create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self._create_fixtures()
        self._create_csrf_token()

    def tearDown(self):
        super(LinkedListAppTestCase, self).tearDown()
        db.drop_all()
        self.app_context.pop()

    def _login(self, email=None, password=None):
        email = email or self.user.email
        password = password or "password"
        return self.post("/login", data=dict(email=email, password=password),
                         follow_redirects=False)
 