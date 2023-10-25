from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client, TestCase
from django.contrib.auth.models import User
import pytest
from .utils import make_prediction


class LogoutViewTest(TestCase):
    def test_logout_view(self):
        # Créez un utilisateur de test
        user = User.objects.create_user(
            username='testuser', password='testpassword')

        # Connectez l'utilisateur
        self.client.login(username='testuser', password='testpassword')

        # Accédez à la vue de déconnexion
        response = self.client.get(reverse('logout'))

        # Vérifiez que l'utilisateur est déconnecté (redirigé vers la page d'accueil)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))

        # Vérifiez que l'utilisateur est effectivement déconnecté
        user = get_user_model().objects.get(username='testuser')
        self.assertFalse(user.is_authenticated)


class IndexViewTest(TestCase):
    def test_index_view(self):
        # Assurez-vous que l'utilisateur est connecté
        self.client.login(username='testuser', password='testpassword')

        # Accédez à la vue index
        response = self.client.get(reverse('index'))

        # Vérifiez que la page s'affiche correctement
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')


@pytest.mark.django_db
def test_good_prediction():
    good_input = {'Year_Built': 1800,
                  '1st_Flr_SF': 1800,
                  'Gr_Liv_Area': 5,
                  'Garage_Area': 4,
                  'Overall_Qual': 4,
                  'Full_Bath': 4,
                  'Exter_Qual': 'Ex',
                  'Kitchen_Qual': 'Ex',
                  'Foundation': 'BrkTil',
                  'Neighborhood': 'Blmngtn'
                  }

    prediction = make_prediction(good_input)
    assert prediction != 0


@pytest.mark.django_db
def test_wrong_prediction():
    wrong_input = {'Year_Built': 1800,
                   '1st_Flr_SF': 1800,
                   'Gr_Liv_Area': 5,
                   'Garage_Area': 4,
                   'Overall_Qual': 4,
                   'Full_Bath': 4,
                   'Exter_Qual': 'Ex',
                   'Kitchen_Qual': 'Ex',
                   'Foundation': '5',
                   'Neighborhood': 'Blmngtn'
                   }

    prediction = make_prediction(wrong_input)
    assert prediction == 0


@pytest.mark.django_db
def test_index_view(client):
    url = reverse('index')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_predict_view_post_method_good_input(client):
    url = reverse('predict')
    data = {
        'Year_Built': '1990',
        'Total_Bsmt_SF': '1000',
        '1st_Flr_SF': '1200',
        'Gr_Liv_Area': '1800',
        'Garage_Area': '500',
        'Overall_Qual': '8',
        'Full_Bath': '2',
        'Exter_Qual': 'TA',
        'Kitchen_Qual': 'Gd',
        'Neighborhood': 'CollgCr'
    }
    response = client.post(url, data)
    assert response.status_code == 200
    assert int(response.context['data']) == 220863


@pytest.mark.django_db
def test_predict_view_post_method_wrong_input(client):
    url = reverse('predict')
    data = {'Year_Built': 1800,
            '1st_Flr_SF': 1800,
            'Gr_Liv_Area': 5,
            'Garage_Area': 4,
            'Overall_Qual': 4,
            'Full_Bath': 4,
            'Exter_Qual': 'Ex',
            'Kitchen_Qual': 'Ex',
            'Foundation': 'BrkTil',
            'Neighborhood': 'Blmngtn'
            }
    response = client.post(url, data)
    assert response.status_code == 200
    assert response.content == b"The Input is not Correct"


@pytest.mark.django_db
def test_predict_view_get_method(client):
    url = reverse('predict')
    response = client.get(url)
    assert response.status_code == 200
    assert response.content == b"Method Not Allowed"
