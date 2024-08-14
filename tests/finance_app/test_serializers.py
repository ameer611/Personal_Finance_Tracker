import uuid

from django.test import TestCase
from rest_framework.test import APIRequestFactory

from finance_app.models import Transaction, Category
from finance_app.serializers import TransactionSerializer, CategorySerializer
from user_app.models import CustomUser


class TestTransactionSerializer(TestCase):
    def setUp(self):
        unique_email = f"test_{uuid.uuid4()}@hi.com"
        self.user = CustomUser.objects.create(
                last_name='test last',
                first_name='test first',
                email=unique_email,
                password='1'
        )

        self.category = Category.objects.create(
            name='food',
            user=self.user
        )

    def test_is_valid_amount(self):
        data = {
            'title': 'test1',
            'user': self.user,
            'category': self.category,
            'amount': 500000,
            "date": '2016-12-19'
        }
        serializer = TransactionSerializer(data)
        self.assertEqual(float(serializer.data['amount']), 500_000.00)


    def test_is_not_valid_amount(self):
        data = {
            'title': 'test1',
            'user': self.user.id,
            'category': self.category.id,
            'amount': "hello",
            "date": '2016-12-19'
        }
        factory = APIRequestFactory()
        request = factory.get('/')
        request.user = self.user

        serializer = TransactionSerializer(data=data, context={'request': request})
        self.assertFalse(serializer.is_valid())
        self.assertEqual(str(serializer.errors['amount'][0]), 'A valid number is required.')

    def test_is_valid_date(self):
        data = {
            'title': 'test1',
            'user': self.user,
            'category': self.category,
            'amount': 500000,
            "date": '2016-12-19'
        }
        serializer = TransactionSerializer(data)
        self.assertEqual(serializer.data['date'], '2016-12-19')


    def test_is_not_valid_date(self):
        data = {
            'title': 'test1',
            'user': self.user,
            'category': self.category.id,
            'amount': 500000,
            "date": '1999-12-19'
        }
        factory = APIRequestFactory()
        request = factory.get('/')
        request.user = self.user

        serializer = TransactionSerializer(data=data, context={'request': request})
        self.assertFalse(serializer.is_valid())
        self.assertEqual(str(serializer.errors['date'][0]), 'Date must be after 2000-01-01')

        data['date'] = '2120-12-15'
        serializer = TransactionSerializer(data=data, context={'request': request})
        self.assertFalse(serializer.is_valid())
        self.assertEqual(str(serializer.errors['date'][0]), 'Date must be before 2100-01-01')

    def test_is_valid_transaction_type(self):
        data = {
            'title': 'test1',
            'user': self.user,
            'category': self.category,
            'amount': 500000,
            "date": '2016-12-19',
            'transaction_type': 'expense'
        }

        serializer = TransactionSerializer(data)
        self.assertEqual(serializer.data['transaction_type'], 'expense')

        data['transaction_type'] = 'income'
        serializer = TransactionSerializer(data)
        self.assertEqual(serializer.data['transaction_type'], 'income')

    def test_not_is_valid_transaction_type(self):
        data = {
            'title': 'test1',
            'user': self.user.id,
            'category': self.category.id,
            'amount': 500000,
            "date": '2016-12-19',
            'transaction_type': 'hello'
        }
        factory = APIRequestFactory()
        request = factory.get('/')
        request.user = self.user

        serializer = TransactionSerializer(data=data, context={'request': request})
        self.assertFalse(serializer.is_valid())
        # self.assertEqual(str(serializer.errors['transaction_type'][0]), f'"{data['transaction_type']}" is not a valid choice.')

    def test_is_valid_category(self):
        data = {
            'title': 'test1',
            'user': self.user,
            'category': self.category,
            'amount': 500000,
            "date": '2016-12-19'
        }
        serializer = TransactionSerializer(data)
        self.assertEqual(serializer.data['category'], self.category.id)


    def test_not_is_valid_category(self):
        data = {
            'title': 'test1',
            'user': self.user.id,
            'category': 2,
            'amount': 500000,
            "date": '2016-12-19'
        }
        factory = APIRequestFactory()
        request = factory.get('/')
        request.user = self.user

        serializer = TransactionSerializer(data=data, context={'request': request})
        self.assertFalse(serializer.is_valid())
        # self.assertEqual(str(serializer.errors['category'][0]), f'Invalid pk "{data['category']}" - object does not exist.')

class TestCategorySerializer(TestCase):
    def setUp(self):
        unique_email = f"test_{uuid.uuid4()}@hi.com"
        self.user = CustomUser.objects.create(
            last_name='test last',
            first_name='test first',
            email=unique_email,
            password='1'
        )
        self.factory = APIRequestFactory()
        self.request = self.factory.get('/')
        self.request.user = self.user

    def test_is_valid_name(self):
        data = {
            'name':'food',
            'user':self.user
        }
        serializer = CategorySerializer(data)
        self.assertEqual(serializer.data['name'], 'food')


    def test_is_not_valid_name(self):
        data1 = {
            'name': 'food',
        }
        serializer1 = CategorySerializer(data=data1, context={'request': self.request})
        serializer1.is_valid(raise_exception=True)
        serializer1.save(user=self.user)

        data2 = {
            'name': 'food',
        }
        serializer2 = CategorySerializer(data=data2, context={'request': self.request})

        self.assertFalse(serializer2.is_valid())
        self.assertEqual(str(serializer2.errors['name'][0]), "Such category already exists!")