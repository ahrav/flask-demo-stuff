from unittest import TestCase
from blog.blog import Blog


class BlogTest(TestCase):
    def test_create_post_in_blog(self):
        b = Blog('Test', 'Test Author')
        b.create_post('Test Post', 'Test Content')

        self.assertEqual(b.posts[0].title, 'Test Post')
        self.assertEqual(len(b.posts), 1)

    def test_json(self):
        b = Blog('Test', 'Test Author')
        b.create_post('Test Post', 'Test Content')

        expected = {
            'title': 'Test',
            'author': 'Test Author',
            'posts': [{'title': 'Test Post', 'content': 'Test Content'}]
        }

        self.assertDictEqual(b.json(), expected)