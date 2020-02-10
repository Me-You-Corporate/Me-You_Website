import json
import requests
from bs4 import BeautifulSoup
from .models import User
from .models import Email


class linkerAPI():
    @staticmethod
    def login(email, password):
        data = {
            'email': email,
            'password': password
        }

        email = None
        # retrieve email
        try:
            email = Email.objects.get(address=data["email"])
        except Email.DoesNotExist:
            print("email does not exist")
            return {"response": "ko", "message": "Wrong credentials."}
        # retrieve user
        try:
            user = User.objects.get(id=email.user_id, password=password)
        except User.DoesNotExist:
            print("user does not exist")
            return {"response": "ko", "message": "Wrong credentials."}

        return {"response": "ok", "message": "Successfully logged in."}

    @staticmethod
    def signup(form_infos):
        print(json.dumps(form_infos))
        first_name = form_infos["first_name"]
        last_name = form_infos["last_name"]
        email = form_infos["email"]
        password = form_infos["password"]
        zipcode = form_infos["zipcode"]

        #validate following id format
        #USER ID BE LIKE : [ZIPCODE][LASTNAME:1][FIRSTNAME:1][COUNTER{2}]
        user_id = zipcode + last_name[0] + first_name[0]

        count_id = User.objects.filter(id__contains=user_id).count()
        count_id = str(count_id)
        if len(count_id) == 1:
            count_id = '0' + count_id

        user_id += count_id

        user_exist = Email.objects.all().filter(address=email).count()
        if user_exist == 0:

            user = User(id=user_id, first_name=first_name, last_name=last_name, password=password)
            email = Email(user_id=user_id, address=email)

            email.save()
            user.save()

            return {"response": "ok", "message": "You've been registered, you can now login into your account"}

        return {"response": "ko", "message": "User email already exists."}

    @staticmethod
    def verifynumcardpro(card_infos):
        # need to check return status for each request.
        r = requests.post("http://eapspublic.sports.gouv.fr/CarteProRecherche/RechercherEducateurCartePro",
                          data=card_infos)
        soup = BeautifulSoup(r.content, features="html.parser")
        # look if there's any error while validating form. if not : Then must be registered
        # cannot test without valid sport card pro
        print(card_infos)
        try:
            table_body = soup.find('tbody')
            rows = table_body.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                cols = [x.text.strip() for x in cols]
                card_infos = [
                    card_infos['Nom'],
                    card_infos['Prenom'],
                    card_infos['NumCartePro'],
                ]
                if cols == card_infos:
                    return {"response": "NumCardPro validated"}
        except AttributeError as e:
            return {"response": "NumCardPro doesn't match any data on the EAPS public website."}
        return {"response": "NumCardPro doesn't match any data on the EAPS public website."}


