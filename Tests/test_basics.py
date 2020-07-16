"""
@auth: cyq
@name: test_basics
@desc: 单元测试
"""

import unittest

from flask import current_app

from App import create_app, db


class TestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.app = create_app("testing")
        self.app_content = self.app.app_context()
        self.app_content.push()
        db.create_all()

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()
        self.app_content.pop()

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_test(self):
        self.assertTrue(current_app.config['TESTING'])

if __name__ == '__main__':
    unittest.main()
