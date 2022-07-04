import unittest
import os
import json
os.environ['TESTING'] = 'true'

from app import app

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home(self):
        response = self.client.get("/")
        assert response.status_code == 200
        html = response.get_data(as_text = True)
        # assert "<title>MLH Fellow</title>" in html : Our page does not have MLH Fellow as Title

        assert '<p style="margin-bottom: 0">Oscar Miranda Escalante</p>' in html
        assert '<nav class="menu-bar">' in html
        assert '</nav>' in html
        # home has image
        assert '<img ' in html

    def test_timeline(self):
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json_r = response.get_json()
        assert "timeline_posts" in json_r
        assert len(json_r["timeline_posts"]) == 0

        post_response = self.client.post("/api/timeline_post",data={"name": "Jane", "email":
            "jane_doe@gmail.com",
                                                                             "content": "hello"})
        assert post_response.status_code == 200
        response_2 = self.client.get("/api/timeline_post")
        assert len(response_2.get_json(["timeline_posts"])) == 1


    def test_malformed_timeline_post(self):
        response = self.client.post("/api/timeline_post", data={"email": "john@example.com", "content": "Hello world, I'm John!"})

        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid name" in html


        response = self.client.post("/api/timeline_post", data={"name": "John Doe","email": "john@example.com", "content": ""})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid content" in html

        response = self.client.post("/api/timeline_post", data={"name": "John Doe", "email": "not-an-email", "content":
            "Hello world, I'm John!"})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid email" in html



