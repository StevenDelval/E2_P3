from django.shortcuts import render
from django.http import HttpResponse
from .utils import make_prediction
from . import forms
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect


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
def predict(request):
    if request.method == 'POST':
        X_predict = {}
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
                X_predict["1st_Flr_SF"] = int(request.POST.get(var))
            else:
                X_predict[var] = int(request.POST.get(var))

        pred = make_prediction(X_predict)

        if pred != 0:
            return render(request, 'index.html',
                          {'data': float("{:.2f}".format(pred))}
                          )
        else:
            return HttpResponse("The Input is not Correct")
    else:
        return redirect('index')


@login_required
def historique(request):
    pass


class SignupPage(CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy('login')
    template_name = './registration/signup.html'
