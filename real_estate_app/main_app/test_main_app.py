import pytest
from django.urls import reverse
from .utils import make_prediction


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
