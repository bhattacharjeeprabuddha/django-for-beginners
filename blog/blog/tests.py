from django.test import TestCase
from .models import Post
from django.contrib.auth import get_user_model
from django.urls import reverse

# Create your tests here.

class BlogTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(username="test_user", 
                                                        email="test@email.com", 
                                                        password="secret")
        
        cls.post = Post.objects.create(
            title = "test title",
            body = "test body",
            author = cls.user,
        )

    def test_post_model(self):
        self.assertEqual(self.post.title, "test title")
        self.assertEqual(self.post.body, "test body")
        self.assertEqual(self.post.author.username, "test_user")
        self.assertEqual(self.post.author.email, "test@email.com")
        self.assertEqual(self.post.author.password, "secret")
        self.assertEqual(self.post.get_absolute_url(), "/post/1")

    def test_url_exists_at_correct_location_listview(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        
    def test_url_exists_at_correct_location_detailview(self):
        response = self.client.get("/post/1")
        self.assertEqual(response.status_code, 200)

    def test_post_listview(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "test body")
        self.assertTemplateUsed(response, "home.html")

    def test_post_detailview(self):
        response = self.client.get(reverse("post_detail", kwargs={"pk":self.post.pk}))
        no_response = self.client.get("/post/1000")
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, "test body")
        self.assertTemplateUsed(response, "post_detail.html")