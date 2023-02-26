import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'posts.settings')
django.setup()



from django.test import TestCase, Client
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from posts.api.models import Post
from posts.api.serializers import PostSerializer
from posts.api.utils.jwt_utils import get_token_for_user

# initialize the APIClient app
client = APIClient()

class PostTest(TestCase):
    """ Test module for Posts """

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        self.post = Post.objects.create(
            title='Test Post',
            content='This is a test post.',
            author=self.user
        )
        self.token = get_token_for_user(self.user)

    def test_get_all_posts(self):
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        # get API response
        response = client.get('/api/posts')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        expected_data = {
            'status': 'success',
            'message': 'Posts retrieved successfully',
            'data': serializer.data
        }
        self.assertEqual(response_data, expected_data)


    def test_create_post(self):
        # get API response
        data = {
            'title': 'New Post',
            'content': 'This is a new test post.',
        }
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = client.post('/api/posts', data, format='json')
        # get data from db
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'success')
        self.assertEqual(response.data['message'], 'Post created successfully')
        self.assertEqual(response.data['data']['title'], data['title'])
        self.assertEqual(response.data['data']['content'], data['content'])
        self.assertEqual(response.data['data']['author'], self.user.id)
        self.assertIsNotNone(response.data['data']['createdAt'])
        self.assertIsNotNone(response.data['data']['updatedAt'])


    def test_get_post_detail(self):
        # get API response
        response = client.get('/api/posts/{}'.format(self.post.pk))
        print(response)
        # get data from db
        post = Post.objects.get(pk=self.post.pk)
        serializer = PostSerializer(post)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'success')
        self.assertEqual(response.data['message'], 'Post retrieved successfully')
        self.assertEqual(response.data['data'], serializer.data)


    def test_update_post(self):
        # get API response
        data = {'content': 'This is updated test post.'}
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = client.patch(f'/api/posts/{self.post.pk}', data, format='json')
        # get data from db
        post = Post.objects.get(pk=self.post.pk)
        serializer = PostSerializer(post)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'success')
        self.assertEqual(response.data['message'], 'Post updated successfully')
        self.assertEqual(response.data['data']['id'], self.post.pk)
        self.assertEqual(response.data['data']['title'], self.post.title)
        self.assertEqual(response.data['data']['content'], data['content'])
        self.assertEqual(response.data['data']['author'], self.user.id)
        self.assertIsNotNone(response.data['data']['createdAt'])
        self.assertIsNotNone(response.data['data']['updatedAt'])



    def test_delete_post(self):
        # get API response
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = client.delete(f'/api/posts/{self.post.pk}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


    def test_like_post(self):
        # get API response
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = client.post(f'/api/posts/{self.post.pk}/like')
        # get data from db
        post = Post.objects.get(pk=self.post.pk)
        self.assertIn(self.user, post.likes.all())
        self.assertEqual(response.data, {'message': 'Post liked.'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_like_post(self):
        # get API response
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = client.post(f'/api/posts/{self.post.pk}/unlike')
        # get data from db
        post = Post.objects.get(pk=self.post.pk)
        self.assertNotIn(self.user, post.likes.all())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'message': 'You have not liked this post.'})
