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

    def test_list_action(self):
        """
        Test that `list` action works for unauthorized users
        """
        response = self.client.get(reverse('restaurants-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(reverse('dishes-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(reverse('ingredients-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_action(self):
        """
        Test that GET by id works for unauthorized users
        """
        rest = Restaurant.objects.get(name='first_rest')
        dish = Dish.objects.get(name='first_dish')
        ingr = Ingredient.objects.get(name='first_ingredient')
        response = self.client.get(reverse('restaurants-detail', args=(rest.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(reverse('dishes-detail', args=(dish.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(reverse('ingredients-detail', args=(ingr.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_action_without_token(self):
        """
        Test that unauthorized users are not allowed to send PATCH requests
        """
        obj = Restaurant.objects.get(name='first_rest')
        url = reverse('restaurants-detail', args=(obj.id,))
        patch_data = {'name': 'patch_new_name_for_restaurant'}
        response = self.client.patch(url, patch_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_action_with_another_user(self):
        """
        Test that another users are not allowed to change restaurants
        """
        obj = Restaurant.objects.get(name='first_rest')
        another_user = User.objects.get(username='second_user')
        header_another_user = {'HTTP_AUTHORIZATION': f"Token {another_user.auth_token}"}
        url = reverse('restaurants-detail', args=(obj.id,))
        patch_data = {'name': 'patch_new_name_for_restaurant'}
        response = self.client.patch(url, patch_data, **header_another_user)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_action_with_owner(self):
        """
        Test that owners are allowed to change restaurants
        """
        obj = Restaurant.objects.get(name='first_rest')
        owner = obj.owner
        header_owner = {'HTTP_AUTHORIZATION': f"Token {owner.auth_token}"}
        url = reverse('restaurants-detail', args=(obj.id,))
        patch_data = {'name': 'patch_new_name_for_restaurant'}
        response = self.client.patch(url, patch_data, **header_owner)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_action_without_token(self):
        """
        Test that unauthorized users are not allowed to send PUT requests
        """
        obj = Restaurant.objects.get(name='first_rest')
        url = reverse('restaurants-detail', args=(obj.id,))
        dish = Dish.objects.get(name='second_dish')
        put_data = {'name': 'put_new_name_for_restaurant',
                    'address': 'Sochi',
                    'dishes': [dish.id]}
        response = self.client.put(url, put_data)  # without token
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_put_action_with_another_user(self):
        """
        Test that another users are not allowed to send PUT requests
        """
        obj = Restaurant.objects.get(name='first_rest')
        another_user = User.objects.get(username='second_user')
        header_another_user = {'HTTP_AUTHORIZATION': f"Token {another_user.auth_token}"}
        url = reverse('restaurants-detail', args=(obj.id,))
        dish = Dish.objects.get(name='second_dish')
        put_data = {'name': 'put_new_name_for_restaurant',
                    'address': 'Sochi',
                    'dishes': [dish.id]}
        response = self.client.put(url, put_data, **header_another_user)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_action_with_owner(self):
        """
        Test that owners are allowed to change restaurants
        """
        obj = Restaurant.objects.get(name='first_rest')
        owner = obj.owner
        header_owner = {'HTTP_AUTHORIZATION': f"Token {owner.auth_token}"}
        url = reverse('restaurants-detail', args=(obj.id,))
        dish = Dish.objects.get(name='second_dish')
        put_data = {'name': 'put_new_name_for_restaurant',
                    'address': 'Sochi',
                    'dishes': [dish.id]}
        response = self.client.put(url, put_data, **header_owner)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_action_without_token(self):
        """
        Test that unauthorized users are not allowed to send DELETE requests
        """
        obj = Restaurant.objects.get(name='first_rest')
        url = reverse('restaurants-detail', args=(obj.id,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_action_with_another_user(self):
        """
        Test that another users are not allowed to delete restaurants
        """
        obj = Restaurant.objects.get(name='first_rest')
        another_user = User.objects.get(username='second_user')
        header_another_user = {'HTTP_AUTHORIZATION': f"Token {another_user.auth_token}"}
        url = reverse('restaurants-detail', args=(obj.id,))
        response = self.client.delete(url, **header_another_user)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_action_with_owner(self):
        """
        Test that owners are allowed to delete restaurants
        """
        obj = Restaurant.objects.get(name='first_rest')
        owner = obj.owner
        header_owner = {'HTTP_AUTHORIZATION': f"Token {owner.auth_token}"}
        url = reverse('restaurants-detail', args=(obj.id,))
        response = self.client.delete(url, **header_owner)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_token_return_after_creating(self):
        """
        Test that POST request on /api/users returns token
        """
        response = self.client.post(reverse('users-list'),
                                 {'username': 'test_user', 'password': '123'})
        self.assertEqual(response.data['token'],
                         User.objects.get(username='test_user').auth_token.key)

    def test_token_return(self):
        """
        Test that POST request on /api/auth/token returns token
        """
        data = {'username': 'first_user', 'password': '123'}
        response = self.client.post(reverse('auth/token'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_creating_restaurant_without_token(self):
        """
        Test that unauthorized users are not allowed to create restaurants
        """
        dish = Dish.objects.get(name='first_dish')
        rest_data = {'name': 'rest_name', 'address': 'Riga', 'dishes': [dish.id]}
        response = self.client.post(reverse('restaurants-list'), rest_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_creating_restaurant_with_token(self):
        """
        Test that only authorized users are allowed to create restaurants
        """
        user = User.objects.get(username='second_user')
        dish = Dish.objects.get(name='first_dish')
        header = {'HTTP_AUTHORIZATION': f"Token {user.auth_token}"}
        rest_data = {'name': 'rest_name', 'address': 'Riga', 'dishes': [dish.id]}
        response = self.client.post(reverse('restaurants-list'), rest_data, **header)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_creating_dish_without_token(self):
        """
        Test that unauthorized users are not allowed to create dishes
        """
        ingredient = Ingredient.objects.get(name='third_ingredient')
        dish_data = {'name': 'dish_name', 'price': 222, 'ingredients': [ingredient.id]}
        response = self.client.post(reverse('dishes-list'), dish_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_creating_dish_with_token(self):
        """
        Test that only authorized users are allowed to create dishes
        """
        user = User.objects.get(username='second_user')
        ingredient = Ingredient.objects.get(name='third_ingredient')
        header = {'HTTP_AUTHORIZATION': f"Token {user.auth_token}"}
        dish_data = {'name': 'dish_name', 'price': 222, 'ingredients': [ingredient.id]}
        response = self.client.post(reverse('dishes-list'), dish_data, **header)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_creating_ingredient_without_token(self):
        """
        Test that unauthorized users are not allowed to send POST to ingredients
        """
        ingr_data = {'name': 'ing_name', 'food_energy': 10}
        response = self.client.post(reverse('ingredients-list'), ingr_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_creating_ingredient_with_token(self):
        """
        Test that POST is not allowed for ingredients
        """
        user = User.objects.get(username='second_user')
        header = {'HTTP_AUTHORIZATION': f"Token {user.auth_token}"}
        ingr_data = {'name': 'ing_name', 'food_energy': 10}
        response = self.client.post(reverse('ingredients-list'), ingr_data, **header)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
