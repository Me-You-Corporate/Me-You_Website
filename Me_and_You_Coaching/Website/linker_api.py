import json
import requests
from bs4 import BeautifulSoup
# from .Forms.signup import SignupForm

class linkerAPI():
    @staticmethod
    def login(email, password):
        data = {
            'email': email,
            'password': password
        }
        print(json.dumps(data))
        # call api with values in json (REST API)
        return {"token": "je-suis-un-token"}

    @staticmethod
    def signup(form_infos):
        print(json.dumps(form_infos))
        first_name = form_infos["first_name"]
        last_name = form_infos["last_name"]
        email = form_infos["email"]
        password = form_infos["password"]
        # SignupForm.model.save(instance=SignupForm(data=form_infos))
        print(first_name, ' ', last_name, ' ', password, ' ', email)
        # object = User(first_name=form_infos["first_name"], last_name=form_infos["last_name"])
        return {"response": "ok"}

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


