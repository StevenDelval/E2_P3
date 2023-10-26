from django.shortcuts import render
from django.http import HttpResponse
from .utils import make_prediction
from . import forms
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect
from .models import RealEstate


def logout_view(request):
    logout(request)  # Log the user out
    return redirect('index')


@login_required
def index(request):
    context = {
        "form": forms.RealEstateForm()
    }
    return render(request, 'index.html', context=context)


@login_required
def historique(request):
    trad_label = {
        "Year_Built": "Année de construction",
        "First_Flr_SF": "Superficie au 1er étage",
        "Gr_Liv_Area": "Superficie habitable",
        "Garage_Area": "Superficie du garage",
        "Overall_Qual": "Qualité générale",
        "Full_Bath": "Salles de bains complètes",
        "Exter_Qual": "Qualité de l'extérieur",
        "Kitchen_Qual": "Qualité de la cuisine",
        "Foundation": "Fondation",
        "Neighborhood": "Quartier",
        "Created_at": "Predit le",
        "Pred": "Prix predit"
    }
    user = request.user  # Obtenez l'utilisateur actuellement connecté
    # Récupérez les 10 dernières prédictions de l'utilisateur
    user_predictions = RealEstate.objects.filter(
        User=user).order_by('-Created_at')[:10]
    predictions_data = []
    for prediction in user_predictions:

        prediction_data = {
            trad_label[field.name]: getattr(prediction, field.name)
            for field in prediction._meta.fields
            if field.name not in ["id", "User"]
        }
        predictions_data.append(prediction_data)
    return render(request,
                  'historique.html',
                  {'user_predictions': predictions_data})


@login_required
def predict(request):
    if request.method == 'POST':
        X_predict = {}
        try:
            for var in [
                "Year_Built", "First_Flr_SF", "Gr_Liv_Area", "Garage_Area",
                "Overall_Qual", "Full_Bath", "Exter_Qual",  "Kitchen_Qual",
                "Foundation", "Neighborhood"
            ]:
                if var in ["Exter_Qual", "Kitchen_Qual",
                           "Foundation", "Neighborhood"
                           ]:
                    X_predict[var] = request.POST.get(var)
                elif var == "First_Flr_SF":
                    X_predict["1st_Flr_SF"] = float(request.POST.get(var))
                else:
                    X_predict[var] = float(request.POST.get(var))
        except (ValueError, TypeError):
            return HttpResponse("The Input is not Correct")
        pred = make_prediction(X_predict)
        if pred != 0:
            current_user = request.user
            real_estate_instance = RealEstate(
                Year_Built=request.POST['Year_Built'],
                First_Flr_SF=request.POST['First_Flr_SF'],
                Gr_Liv_Area=request.POST['Gr_Liv_Area'],
                Garage_Area=request.POST['Garage_Area'],
                Overall_Qual=request.POST['Overall_Qual'],
                Full_Bath=request.POST['Full_Bath'],
                Exter_Qual=request.POST['Exter_Qual'],
                Kitchen_Qual=request.POST['Kitchen_Qual'],
                Foundation=request.POST['Foundation'],
                Neighborhood=request.POST['Neighborhood'],
                User=current_user,
                Pred=pred
            )
            real_estate_instance.save()
            return render(request, 'index.html',
                          {'data': float("{:.2f}".format(pred))}
                          )
        else:
            return HttpResponse("The Input is not Correct")
    else:
        return redirect('index')


class SignupPage(CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy('login')
    template_name = './registration/signup.html'
