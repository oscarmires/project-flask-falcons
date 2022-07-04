import unittest
from peewee import MySQLDatabase, Model, CharField, TextField, DateTimeField, SqliteDatabase

from app import TimelinePost

MODELS = [TimelinePost]

test_db = SqliteDatabase(':memory:')

class TestTimelinePost(unittest.TestCase):
    def setUp(self):
        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)
        test_db.connect()
        test_db.create_tables(MODELS)

    def tearDown(self):
        test_db.drop_tables(MODELS)
        test_db.close()

    def test_timeline_post(self):

        first_post = TimelinePost.create(name='John Doe', email='john@example.com', content="Hello World, I\'m John!")

        assert first_post.id == 1

        second_post = TimelinePost.create(name='Jane Doe', email='john@example.com', content="Hello World, I\'m Jane!")
        assert second_post.id == 2

        all_posts = TimelinePost.select().order_by(TimelinePost.created_at.desc())
        assert all_posts[0].name == 'Jane Doe'
        assert all_posts[0].email == 'john@example.com'
        assert all_posts[0].content == "Hello World, I\'m Jane!"
        assert len(list(all_posts)) == 2

