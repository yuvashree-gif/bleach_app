from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post

class PostTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.post = Post.objects.create(user=self.user, image='test_image.jpg')

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/home.html')

    def test_post_list_view(self):
        response = self.client.get(reverse('post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/post_list.html')
        self.assertContains(response, self.post.image)

    def test_post_create_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('post_create'), {'image': 'test_image.jpg'})
        self.assertEqual(response.status_code, 302)  # Redirects after successful creation
        self.assertTrue(Post.objects.filter(user=self.user).exists())

    def test_register_view(self):
        response = self.client.post(reverse('login'), {'username': 'newuser', 'password': 'newpass'})
        self.assertEqual(response.status_code, 302)  # Redirects after registration
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_login_view(self):
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'testpass'})
        self.assertEqual(response.status_code, 302)  # Redirects after successful login

    def test_react_to_post(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('react_to_post', args=[self.post.id]), {'reaction_type': 'like'})
        self.assertEqual(response.status_code, 302)  # Redirects after reacting
        self.assertTrue(self.post.reaction_set.filter(user=self.user).exists())
