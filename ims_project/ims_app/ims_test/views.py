from django.test import TestCase
from django.urls import reverse
from ims_app.models import Category


class CategoryViewTest(TestCase):
    def setUp(self):
        # Set up data for the test views
        self.category = Category.objects.create(category_name='Electronics')

    def test_create_category_view_get(self):
        response = self.client.get(reverse('create_category'))  # Adjust URL name if necessary
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ims/create_category.html')

    def test_create_category_view_post(self):
        response = self.client.post(reverse('create_category'), data={'category_name': 'Books'})
        self.assertEqual(response.status_code, 302)  # Expect redirect after creation
        self.assertTrue(Category.objects.filter(category_name='Books').exists())

    def test_category_detail_view(self):
        response = self.client.get(reverse('category_detail'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ims/category_detail.html')
        self.assertContains(response, 'Electronics')

    def test_category_update_view_get(self):
        response = self.client.get(reverse('category_update', kwargs={'pk': self.category.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ims/category_update.html')

    def test_category_update_view_post(self):
        response = self.client.post(reverse('category_update', kwargs={'pk': self.category.pk}), data={'category_name': 'Updated Name'})
        self.assertEqual(response.status_code, 302)  # Expect redirect after update
        self.category.refresh_from_db()  # Refresh the category from database
        self.assertEqual(self.category.category_name, 'Updated Name')

    def test_category_delete_view_get(self):
        response = self.client.get(reverse('category_delete', kwargs={'pk': self.category.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ims/category_confirm_delete.html')

    def test_category_delete_view_post(self):
        response = self.client.post(reverse('category_delete', kwargs={'pk': self.category.pk}))
        self.assertEqual(response.status_code, 302)  # Expect redirect after deletion
        self.assertFalse(Category.objects.filter(pk=self.category.pk).exists())

