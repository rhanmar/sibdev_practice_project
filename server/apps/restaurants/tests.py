from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.restaurants.models import Restaurant, Dish, Ingredient
from django.contrib.auth.models import User


class APITests(APITestCase):
    def setUp(self):
        # create users
        self.client.post(reverse('users-list'),
                                {'username': 'first_user', 'password': '123'})
        self.client.post(reverse('users-list'),
                                {'username': 'second_user', 'password': '456'})

        # create ingredients
        ing1 = Ingredient.objects.create(name='first_ingredient', food_energy=111)
        ing2 = Ingredient.objects.create(name='second_ingredient', food_energy=222)
        ing3 = Ingredient.objects.create(name='third_ingredient', food_energy=333)

        # create dishes
        dish1 = Dish.objects.create(name='first_dish',
                                    price=1234)
        dish1.ingredients.add(ing1)
        dish1.ingredients.add(ing2)

        dish2 = Dish.objects.create(name='second_dish',
                                    price=4567)
        dish2.ingredients.add(ing2)
        dish2.ingredients.add(ing3)

        # create restaurant
        rest1 = Restaurant.objects.create(name='first_rest',
                                          address='Moscow',)
        rest1.dishes.add(dish1)
        rest1.owner = User.objects.get(username='first_user')
        rest1.save()

    def test_get_request(self):
        """
        Test that GET works with unauthorized users
        """
        response = self.client.get(reverse('restaurants-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(reverse('dishes-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(reverse('ingredients-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        rest = Restaurant.objects.get(name='first_rest')
        dish = Dish.objects.get(name='first_dish')
        ingr = Ingredient.objects.get(name='first_ingredient')
        response = self.client.get(reverse('restaurants-detail', args=(rest.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(reverse('dishes-detail', args=(dish.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(reverse('ingredients-detail', args=(ingr.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_auth_restaurants(self):
        """
        Test that only authorized users are allowed to send PUT, PATCH and DELETE requests
        and that only owners are allowed to change and delete restaurants
        """
        obj = Restaurant.objects.get(name='first_rest')
        owner = obj.owner
        another_user = User.objects.get(username='second_user')
        header_owner = {'HTTP_AUTHORIZATION': f"Token {owner.auth_token}"}
        header_another_user = {'HTTP_AUTHORIZATION': f"Token {another_user.auth_token}"}
        url = reverse('restaurants-detail', args=(obj.id,))

        dish = Dish.objects.get(name='second_dish')
        put_data = {'name': 'put_new_name_for_restaurant',
                    'address': 'Sochi',
                    'dishes': [dish.id]}
        patch_data = {'name': 'patch_new_name_for_restaurant'}

        # PATCH, PUT, DELETE without token
        response = self.client.patch(url, patch_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.client.put(url, put_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # PATCH WITH OWNER
        response = self.client.patch(url, patch_data, **header_owner)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # PATCH WITH ANOTHER USER
        response = self.client.patch(url, patch_data, **header_another_user)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # PUT WITH OWNER
        response = self.client.put(url, put_data, **header_owner)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # PUT_WITH_ANOTHER_USER
        response = self.client.put(url, put_data, **header_another_user)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # DELETE WITH ANOTHER USER
        response = self.client.delete(url, **header_another_user)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # DELETE WITH OWNER
        response = self.client.delete(url, **header_owner)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_token_return(self):
        """
        Test that POST request on /api/users and on /api/auth/token returns token
        """
        # Test /api/auth/token
        data = {'username': 'first_user', 'password': '123'}
        response = self.client.post(reverse('auth/token'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Test /api/users
        response = self.client.post(reverse('users-list'),
                                 {'username': 'test_user', 'password': '123'})
        self.assertEqual(response.data['token'],
                         User.objects.get(username='test_user').auth_token.key)

    def test_creating_rest_and_dish(self):
        """
        Test that only authorized users are allowed to create restaurants and dishes
        and test that POST is not allowed for ingredients
        """
        user = User.objects.get(username='second_user')
        dish = Dish.objects.get(name='first_dish')
        ingredient = Ingredient.objects.get(name='third_ingredient')

        header = {'HTTP_AUTHORIZATION': f"Token {user.auth_token}"}
        rest_data = {'name': 'rest_name', 'address': 'Riga', 'dishes': [dish.id]}
        dish_data = {'name': 'dish_name', 'price': 222, 'ingredients': [ingredient.id]}
        ingr_data = {'name': 'ing_name', 'food_energy': 10}

        # Test restaurants
        # Without token
        response = self.client.post(reverse('restaurants-list'), rest_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # With token
        response = self.client.post(reverse('restaurants-list'), rest_data, **header)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Test dish
        # Without token
        response = self.client.post(reverse('dishes-list'), dish_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # With token
        response = self.client.post(reverse('dishes-list'), dish_data, **header)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Test ingredients
        # Without token
        response = self.client.post(reverse('ingredients-list'), ingr_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # Without token
        response = self.client.post(reverse('ingredients-list'), ingr_data, **header)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
