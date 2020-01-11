from django.shortcuts import render, redirect
from django.template import loader
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
from .Forms.login import LoginForm
from .Forms.signup import SignupForm
from .Forms.contact import ContactForm
from Website import linkerAPI
from django.conf import settings
from smtplib import SMTPException

from django.template.loader import render_to_string
from django.utils.html import strip_tags
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
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message, email, [settings.EMAIL_HOST_USER], fail_silently=False)
            except SMTPException:
                return redirect("contact")
    print("email sent")
    context = {'form': form}
    return render(request, "Website/contact.html", context)


def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            # token = linkerAPI.login(email, password)
            print(email)
            print(password)
            # print(token)
    else:
        form = LoginForm()

    return render(request, "Website/login.html", {'form': form})


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form_inputs = {
                'first_name': form.cleaned_data.get('first_name'),
                'last_name': form.cleaned_data['last_name'],
                'email': form.cleaned_data['email'],
                'password': form.cleaned_data['password'],
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
            if response['response'] == "ok":  # change and use real code error
                subject = 'Confirmation de votre adresse e-mail'
                html_message = render_to_string('Website/Mails/MY_Corporate_mail_confirmation.html', {'context': form_inputs})
                plain_message = strip_tags(html_message)
                from_email = settings.EMAIL_HOST_USER
                to = form_inputs['email']
                send_mail(subject, plain_message, from_email, [to], html_message=html_message)
                # messages.success(request,"Votre compte a bien été créé !")
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
