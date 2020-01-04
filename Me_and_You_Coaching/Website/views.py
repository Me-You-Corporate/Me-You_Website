from django.shortcuts import render, redirect
from django.template import loader
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.contrib import messages
from .Forms.login import LoginForm
from .Forms.signup import SignupForm
from .Forms.contact import ContactForm
from Website import linkerAPI
# Create your views here.


def index(request):
    template = loader.get_template('Website/index.html')

    return HttpResponse(template.render({}, request))


def contact(request):
    template = loader.get_template('Website/contact.html')
    form = ContactForm()
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['password']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
    context = {'form': form}

    return HttpResponse(template.render(context, request))


def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            token = linkerAPI.login(email, password)
    else:
        form = LoginForm()

    return render(request, "Website/login.html", {'form': form})


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form_inputs = {
                'first_name': form.clean_email(),
                'last_name': form.cleaned_data['last_name'],
                'email': form.cleaned_data['email'],
                'password': form.cleaned_data['email'],
            }
            fs = FileSystemStorage()
            if request.FILES and request.FILES['identification_document']:
                id_card = request.FILES['identification_document']
                fs.save(id_card.name, id_card)
                # figure out a path to save relative document to each user : hint : user_id
            if request.FILES and request.FILES['professional_document']:
                pro_card = request.FILES['professional_document']
                fs.save(pro_card.name, pro_card)
                # figure out a path to save relative document to each user : hint : user_id
            # cannot seem to query info from the photo, so use normal input to get them
            coachInfos = {
                "Nom": form_inputs.get('first_name'),
                "Prenom": form_inputs.get('last_name'),
                "NumCartePro": 123456
            }
            # verification using html response from official website : not best solution but only one found
            response = linkerAPI.verifynumcardpro(coachInfos)
            print(response)

            # signup on API make registration on temp_table, ID must be verified manually on the administrator panel
            # during test phases, then when everything seems ok, switch to automatic saves (through e-mail confirmation)
            response = linkerAPI.signup(form_inputs)
            print(response)
            if response == "ok": # change and use real code error
                messages.success(request,"Votre compte a bien été créé !")
                return redirect("login")
            # there on signup response == "OK" use mailing service to send a confirmation e-mail to the new user
            # ATM: just send an e-mail for the visual wait for design
    else:
        form = SignupForm()
    return render(request, "Website/signup.html", {'form': form})


def askresetpassword(request):
    return HttpResponse("Page de demande de réinitialisation de mot de passe")


def resetpasswrod(request):
    return HttpResponse("Page de réinitialisation de mot de passe")


def account(request):
    return HttpResponse("Page mon compte")


def admin(request):
    return HttpResponse("Page connexion panel administrateur")

# set an endpoint to confirm user creation : i.e. : an e-mail redirect on that URL with some info and based on those
# the user proves he's not a spam nor a bot hence we switch him from unconfirmed to confirmed
