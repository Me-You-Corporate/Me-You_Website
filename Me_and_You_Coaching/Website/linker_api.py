import json
import requests
from bs4 import BeautifulSoup


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
        return {"response": "ok"}

    @staticmethod
    def verifynumcardpro(card_infos):
        # need to check return status for each request.
        r = requests.post("http://eapspublic.sports.gouv.fr/CarteProRecherche/RechercherEducateurCartePro",
                          data=card_infos)
        soup = BeautifulSoup(r.content, features="html.parser")
        # look if there's any error while validating form. if not : Then must be registered
        # cannot test without valid sport card pro
        error_message = soup.find("div", {"class", "validation-summary-errors"}).ul.li.string
        # assumption that there's nothing in the error section if the number is registered
        if error_message == "":
            return {"response": "NumCardPro validated"}
        return {"response": "NumCardPro doesn't match any data on the EAPS public website."}
