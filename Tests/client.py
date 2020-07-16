import unittest
from flask import url_for
from App import create_app, db
from Model.Models import User,Part

class FlaskClientCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_index(self):
        print('start')
        res = self.client.get(url_for(endpoint="testfunc"))
        a = res.get_data(as_text=True)
        print(a)
        assert "o" in a

if __name__ == '__main__':
    unittest.main()
