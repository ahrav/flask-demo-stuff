from unittest import TestCase
from blog.blog import Blog


class BlogTest(TestCase):
    def test_create_blog(self):
        b = Blog('Test', 'Test Author')

        self.assertEqual('Test', b.title)
        self.assertListEqual([], b.posts)
        self.assertEqual('Test Author', b.author)

    def test_repr(self):
        b = Blog('Test', 'Test Author')

        self.assertEqual((b.__repr__()), 'Test by Test Author (0 posts)')

    def test_repr_multiple_posts(self):
        b = Blog('Test', 'Test Author')
        b.posts = ['test']

        self.assertEqual((b.__repr__()), 'Test by Test Author (1 post)')