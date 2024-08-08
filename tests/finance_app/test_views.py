import uuid

from django.test import TestCase, Client
from rest_framework_simplejwt.tokens import RefreshToken
from finance_app.models import Transaction, Category
from user_app.models import CustomUser


class TestTransactionViewSet(TestCase):
    def setUp(self):
        unique_email = f"test_{uuid.uuid4()}@hi.com"
        self.user = CustomUser.objects.create(
            last_name='test last',
            first_name='test first',
            email=unique_email,
            password='1'
        )
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)

        self.category = Category.objects.create(
            name='food',
            user=self.user
        )

        self.salary = Category.objects.create(
            name='salary',
            user=self.user
        )

        self.transaction = Transaction.objects.create(
            user=self.user,
            title='test title 1',
            amount=500000,
            date='2020-2-15',
            category=self.salary,
            transaction_type='income'
        )

        self.transaction_expense = Transaction.objects.create(
            user=self.user,
            title='test title 2',
            amount=90000,
            date='2019-4-19',
            category=self.category,
            transaction_type='expense'
        )

        self.client = Client()
        self.client.defaults['HTTP_AUTHORIZATION'] = f'Bearer {self.token}'


    def test_get_all_transactions(self):
        response = self.client.get('/api/transactions/transactions/')
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 2)
        self.assertIsNotNone(data[0]['id'])
        self.assertEqual(data[0]['title'], 'test title')


    def test_get_categories(self):
        transaction_id = self.transaction.id
        response = self.client.get(f'/api/transactions/transactions/{transaction_id}/category/')
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['id'], 2)
        self.assertEqual(data['name'], 'salary')

    def test_get_incomes(self):
        response = self.client.get('/api/transactions/transactions/income/')
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(data[0]['id'])
        self.assertEqual(data[0]['amount'], '500000.00')


    def test_get_expenses(self):
        response = self.client.get('/api/transactions/transactions/expense/')
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(data)

    def test_search(self):
        response = self.client.get("/api/transactions/transactions/?search=test&ordering=-amount")
        data = response.json()
        self.assertEqual(len(data), 2)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data[0]['title'], 'test title 1')

