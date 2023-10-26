from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client, TestCase
from django.contrib.auth.models import User
from .models import CustomUser
import pytest
from .utils import (make_prediction,
                    get_foundation_categorie,
                    get_neighborhood_categorie)


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
                   'Garage_Area': "ex",
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
def test_get_foundation_categorie():

    resultat_attendus = [
        ('BrkTil', 'Brick & Tile'),
        ('CBlock', 'Cinder Block'),
        ('PConc', 'Poured Concrete'),
        ('Slab', 'Slab'),
        ('Stone', 'Stone'),
        ('Wood', 'Wood')
    ]
    resultat_obtenue = get_foundation_categorie()
    assert resultat_obtenue == resultat_attendus


@pytest.mark.django_db
def test_get_neighborhood_categorie():

    resultat_attendus = [
        ('Blmngtn', 'Bloomington Heights'),
        ('Blueste', 'Bluestem'),
        ('BrDale', 'Briardale'),
        ('BrkSide', 'Brookside'),
        ('ClearCr', 'Clear Creek'),
        ('CollgCr', 'College Creek'),
        ('Crawfor', 'Crawford'),
        ('Edwards', 'Edwards'),
        ('Gilbert', 'Gilbert'),
        ('Greens', 'Greens'),
        ('IDOTRR', 'Iowa DOT and Rail Road'),
        ('MeadowV', 'Meadow Village'),
        ('Mitchel', 'Mitchell'),
        ('NAmes', 'NAmes'),
        ('NPkVill', 'Northpark Villa'),
        ('NWAmes', 'Northwest Ames'),
        ('NoRidge', 'Northridge'),
        ('NridgHt', 'Northridge Heights'),
        ('OldTown', 'Old Town'),
        ('SWISU', 'South & West of Iowa State University'),
        ('Sawyer', 'Sawyer'), ('SawyerW', 'Sawyer West'),
        ('Somerst', 'Somerset'), ('StoneBr', 'Stone Brook'),
        ('Timber', 'Timberland'),
        ('Veenker', 'Veenker')
    ]
    resultat_obtenue = get_neighborhood_categorie()
    assert resultat_obtenue == resultat_attendus


@pytest.mark.django_db
def test_login_view(client):
    url = reverse('login')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_signup_view(client):
    url = reverse('signup')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_index_view(client):
    user = CustomUser.objects.create_user(
        username='testuser', password='testpassword')

    # Connectez l'utilisateur
    client.login(username='testuser', password='testpassword')
    url = reverse('index')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_logout_view(client):
    user = CustomUser.objects.create_user(
        username='testuser', password='testpassword')

    # Connectez l'utilisateur
    client.login(username='testuser', password='testpassword')
    url = reverse('logout')
    response = client.post(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_historique_view(client):
    user = CustomUser.objects.create_user(
        username='testuser', password='testpassword')

    # Connectez l'utilisateur
    client.login(username='testuser', password='testpassword')
    url = reverse('historique')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_predict_view_post_method_good_input(client):

    user = CustomUser.objects.create_user(
        username='testuser', password='testpassword')

    # Connectez l'utilisateur
    client.login(username='testuser', password='testpassword')

    url = reverse('predict')
    data = {'Year_Built': 1800,
            'First_Flr_SF': 1800,
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


@pytest.mark.django_db
def test_index_with_no_user(client):
    url = reverse('index')
    response = client.post(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))


@pytest.mark.django_db
def test_historique_with_no_user(client):
    url = reverse('historique')
    response = client.post(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))


@pytest.mark.django_db
def test_predict_with_no_user(client):
    url = reverse('predict')
    data = {'Year_Built': 1800,
            'First_Flr_SF': 1800,
            'Gr_Liv_Area': 5,
            'Garage_Area': "test",
            'Overall_Qual': 4,
            'Full_Bath': 4,
            'Exter_Qual': 'Ex',
            'Kitchen_Qual': 'Ex',
            'Foundation': 'BrkTil',
            'Neighborhood': 'Blmngtn'
            }
    response = client.post(url, data)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))


@pytest.mark.django_db
def test_predict_view_post_method_wrong_input(client):
    user = CustomUser.objects.create_user(
        username='testuser', password='testpassword')

    # Connectez l'utilisateur
    client.login(username='testuser', password='testpassword')
    url = reverse('predict')
    data = {'Year_Built': 1800,
            'First_Flr_SF': 1800,
            'Gr_Liv_Area': 5,
            'Garage_Area': "test",
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
    user = CustomUser.objects.create_user(
        username='testuser', password='testpassword')

    # Connectez l'utilisateur
    client.login(username='testuser', password='testpassword')
    url = reverse('predict')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == reverse('index')
