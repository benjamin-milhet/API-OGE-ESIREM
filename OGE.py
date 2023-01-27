from flask import Flask, request
import sys
import requests
import re
import json
import smtplib

app = Flask(__name__)

OGE_ESIREM = "https://casiut21.u-bourgogne.fr/cas-esirem/login?service=https%3A%2F%2Fiutdijon.u-bourgogne.fr%2Foge-esirem%2F"
OGE_DETAILS = "https://iutdijon.u-bourgogne.fr/oge-esirem/stylesheets/etu/detailsEtu.xhtml"
session = requests.session()

@app.route("/connexion/<login>/<password>", methods=['POST'])
def connexion(login, password):
    dataConnexion = {"username": login,
            "password": password,
            "execution": "e236c444-5ef9-4a35-a7dd-1afcb6a444d2_ZXlKaGJHY2lPaUpJVXpVeE1pSXNJblI1Y0NJNklrcFhWQ0o5LlZvQ3lkdlE3YlhiUFAybXBCay80Ylptait0K1BNK2phTmNwUUM3TmxiazRKUXZmaUFKVS8wM2p1SytHRVd6cUlDQU1SUTNBQmgzQkhXeEFqRmx4MWtLQWxNVmxOUEIrVVlja05NSm9MK090bnlWRWszRmQ3OUJhQXB3bExYQUloaTZaTTIxcWNJV2dvd1l3ZEhUajNvYVhjMVFRRW5GMXNDdlh2bW0ydDVLN0tFdm9CV0ZKY1l0bk90Z3ZPR0dmRFVUamE1RldYbndaaTAvNmVLdTNxaGFKbTdlQ05zTytjd21KS3cwWEVoSlM0Z0lGYXJuOW1UMFFoTm0xb0lOYVRCR0FpeWM3akRIUG8wSTY5aFN0TWtWdjVFMk1UY0N3U3NVTEF1ODVoL2lMYWJLb0pzTzExNkMxaGZneGRDckoraUR2a3hPMlhFRkdvLzdUeDNldUxVSUZCUFpHTUNjVlhsdjVGUHA5SllmK0lVUlhXTzI1T2hrVWdQalV2Q0Urb0hERGdtNVkxdTUyTkFxc04xUlZUV1U0RUVZT092T0VyREFyOWtBREpmZ3daMnRndjVWOGhzNU5ndEdHWFNYRW1VS1ZiWFM2c0pBVW42RGs0Y292V0g5OUdhdGg5cEdsRVJ3OU54TVd2MFNyRGZWdzhDSzhJblVlZ1p1elBqSUhOQ0k4bnFRb09aa1NQcW1kTEp2S2p6Nk5yZHZ2cFJ1WHgybjJWWnExV044Wk5IRlRpZjRIWlVvMnJwcWQxZWxhYWpFNGVxWTlvazF4TVJmNEpreTdwWkV0S0c5NmNjL2pXWlNKeTVsOUVkNzZZNW5WVnk2N1JDSm1oV1o3bUpFZ2VRdzlKdnEyVUxtRi81TVMvaTRBUncvTFFMNGFNVFRWSVdRdUFLZVg1cmN4YUJVVUsvQnJVRjNYRlUyZnk5THFQejRSRWttY1p2VU1GTnhKeERvcUNxWDUxR0tvMEdtU3MwclVIRkRVOFp2TzV1ckc1N3JHenJ6eXF1ZHVmbjhZejBudmUrU29SNkJ6azVUU2NMYjRSSVd0eDJEZitYRWpObGtxMTdTcWJrOExSbHpSUkoza2F0ckZ6WTBGKzI2UFBlR3p4aS9Ucmg2bk5neElidkdVbGJFWStZVTUzd3RDemRFVEZBNDM5SWtnVS9SaDVRUHpNNlh0OW5DUkZFVDRwelFQK25raVNyaFZjOFdOVVRNdllocUcxbjJ5SzdxMHJmS3lFNkhCcnN2OVNMQVFFaEtOYkZydVAvZU85QVFCUGdCaEw4M0ZVV1JhbXdRY1dUWHUzcXpmQk9aU2ZyNHFabzhoWEdxOEtYbzJJNVU5eldRNUJsRzF3dnl2TjBqelFVWnQ4L2hXNnhPVkFyZnAwVXdLVHk3NHgxOGY2RE83WTFTd3ZPQkZqVEN1M0J1cFB6ZkhnWlREUStmMUxqNHlOMEFGcyt6Y2lJaEJnZ05ld0Q0YW9TdHE2OUN4cHdQT0w2Tkhnbm1nTE1meUkrcmZlTmx3Q1BtaktjcjZlSTZYRFROS0tyZHcrdkNic3FETGxueHZ4Z1VrWk1sejJyN0d4UTdqaTVnOHcvMjlxVXJSOUJsajZwYlR4U2s2cFlEMU9Tc3lCK1FNRjQwWXV0dVRLZzVuZUdGcXBobzBUWW9WUmZTWlVIWHQvTVhvUlVsaXZDeEIrSXBNWGFLeUhQN1p0MnhoZ1d6YTdxOTZJTk1qWFR0UGw1WXBseXlaVWlPYlVNVS8wSHJmM0x3bXl3NW1GZkJVczhrWVd3TjU3S3g4VkNWV3U3VFNnV3dHVStWaEg4UmpMOWhxVHcwVEhrTS9WNEZmT1NzbXd0S0FaZ2hVNmF2WmdOcGFLU25qb1BOZFk4N25hQUJPR25yb21lQ1dJV2ZWdGt5YmJGU3pTRVByWXdoeElmZVBEYzJEV3ZOa0NxbmU4UWdNM29pNEpZKzRnYUNGNmNxajVmWlFqTGxJblVPbnFNZXV4ait5NlZscCtsMXFMd1JYVXUzU0VXYXhpR25TaW1FNko3ZERsVVZRTVhmcGFPcmc5Q0NFR2ZtUXkvVXpSaFMvSVIxZWt6NllXZFVRNXp6S1dWU3RtVTNVZnpaK2d5YlpCbkNsNUw2aVJOQjFYRzU3WkhZdktVRitNU2lIVUtvWVRmakJ1S0RobVdjMUR1RDY0QWVBTnJmLzhtWWRrcy81bXpyeE1xRzB4S3dDd250WERvZ2VYZUdMWjhEOWNCZUpnOEJITVdkRGx3dTlrL3pjVFY0aUVaeUloV25aT0RVM0sxS2hkRGxTd3RBemRhQUU3KzhtRFJIZTZjR0tobVBOSEtFYWZoaGJVZnErbDE0Zy9PREM3aWpEWkRIbmVHTExMRVlxbHZhYjBqVktoUE1QL1dsOEEyYmxpR0RCNDFiWDBtSFpIQkx1ejJLTzJvOWFwS0k1MktzaTZ3SlpLdWx4dDVmcG8xVVVEWGd5T2VOeVZuVUZXMXU0S2RBa3MxeVl0dVdPZFoxa3BkdE5WVE9ZU1U0di9jZEFSc0hlbWFVRGNoYUo0WFl6ZGxadXdOamEyQTZGbmtIZjk4U3F0ZHdrTCs2SXpGVlZsUElZVmQrdGFsNTl5ZXBoaWpLUEhjQktnYlRMVlFzQVFlVVVNTzZ6TmZoSENMQmRXcWVoSGJFbnMrM1NOZzVtRDVGVnBjL0Rqcy9mc3IrVlZVV2paQWhXTWxqaTVnNTAvZzlLVytFVzdBN1VlenB6dzZWanQzTEsyd05DaUtjQzlOQllnQ1JkYldNMU5rQ1J2SE5HbmUwNU1Ld3ZubjI1R2YvSzJVeVIrZ1lqMEg3cE1rcWhOY2FteFFaS3FpY0ZMcDJlN2F6UVVnR1NuUXRCWjZTOE14azVzUWlSTDg3SHVWampHVDZXbENHd1VrSXdFTUIyMjhWQytEb0RYcWQ2QUNIUCtjOFE1RFJjdUZRMmUwQ2RLZi9rbjFGTjZaRjZ1ZS9hZWlLYk9IK0szYzZEcE8yVlRxMFNrRzJPcVVJNExWY3ZsL0x6di9WOWFJZWM3ZE1xU3FEY3U2SmFWaDNNWnRKdmdwMHZsNitSTk9zQjFaNlJ0MGd1UldRRG5TMldtQXVOKy8zRHBDamhvTGdLTGV3ZHc3cUR1dGhQQkFNdmpSWUxVT3RYNWtMNThrMHNPeEtGRzBnOEdDSmMzektKbklxMDlDaFhHZ1IxN2pWZFBuaFdhcCtLaWZJZjRrZ2M2UDdQTzdrMXJZcjkvWkVJeFVoSFRaWXk1V3dDZiszT3ZzRXVkY0N6akN6ZmlqNnE3dHlGYnpFNSthWEVtaCtQZXdFR25JSkZ0MG9xYWp2eHBhUklRYWtlVVNNYmJNVVlSbkhVU09QanU5aFNUSTBzbGxaTWxlMEdTa1N3Zk15NEZ3b25nTTZRRktoelFka1A3WGU0MnFwUGdiM0w1a1pvajhNQVhDb21yTFJoLzNJSUFWa2NtMzNiaStHbENjL0lGU3E4U0RpMDVPazJyMmExSFZsYm1sUTAzOHBPT0ZtcnNlOWdDM3Y2L0RNYUUzQTB6b0Jvdm9SUXJMWkVPazUwN0p6VzVKMXNRNkdOa2JjUGhEMGFtbk5UaS8zSko2RzE2VGxFRFlIb2FYcnZJbVBKemw3T0N4WUNCa1RvTjA4S0liaHJHSkVsZzFucnA3bFZkK2pXYVo4VHhreEgrU0F2TmJGUHpWeEcrWHcrMThQRnZ0cjkwdjF1UXowbGNMZS8waW85WVlHVkw4THp1akpGQmtFeVBQaVRMK3RPd3pQOGl3bGtCVmJTQlRNQkZOUDk5L2EvWkkrTk5ZTy9QeUw0TkcwNERmSE5uU1ZtRUFjbmxXcmxNQ1RFRmc5TndrWDBMbEZLcE83NEZZOW1NaklpcmZPbjBLaWw2VGZmbFpRZnlJYkgvVyt4ZzZkd0xFMTErWjhaTXdUNXpDYWUvSHZKMXVXRzFwSWpaVitKeUNieW5ZSWxlUUZ6RGl1RHJ0OE5MMkhwc28wQjdrcG9GcWQ2ZURkR01qa00rOFRBdEVzNTUxbUQ1YzkwUlYvYWIwVnNYWWRaQldmanZERkFsYWJ3QnVENThrWUVLcTExclJsUnRuWXcremUwbVRHWDRsNmtYZWl5YlBYTDFCdjFHbk5QeE8xTm9FbFF2VXIrajE2QzJJSmlkUVNsRjRLRmZFOHprTGFHdkJod2JxamVDN3pzbGowbUZBR3ZadllwZXdCaUNhUXVUQno1NTY0amRSZWdSZ0kzYU5jZTBqaUdVM0RMZXRmY0ZvV2lVaDF1dWMyclkwZEYyQkpMSkZab3YwRmZhY2cvcTB3dGhtT3EycGxJK21ab0VEU2lBY0hiR1N3czdhYXFlbTJyaVNTQW0rWVlJVUtXTkU2WFlvMFp2OHREbC9qK1IrV1Z5SEd5OVNSQlBFVHZ5SW0vMkhKVjNUcDU3UzhSbTMxOG9tem12UDR3MmdWNHZsaDBDY0xKUnYzRWpVVGdmZnZqN04ySTBzWGZYeHVsOVdLVUZaMDdpbnJtOE5wTVJvbTZhUWRsNmNPRGN2NG42VHlFNytHbHIwN3VOeERQSU94VUFhaitXeW9YTmsyNFNKZVM1azB4ZGhrUlRjYmExa1FubjNLUUdLMHUrRE9QM2UxQldaaVlFbitia29RamhiYUlPbnZnYmh1UFcuVmVNbGt2SlNhQWxZaUVhYnpCWUF4MVdONHJ4eGM5VnN4Q2txVTlPamE0ZEhZVHRuNFJZOWQzSEV0Q2hjZk9rN2pLVWJTMEVtWENCWThqOUNQM1ZrNkE=",
            "service": "https://iutdijon.u-bourgogne.fr/oge-esirem/",
            "_eventId": "submit"
        }
    response = session.post(OGE_ESIREM, data = dataConnexion)
    return str(response.status_code)

def getViewState(url):
    r = session.get(url)
    id = re.findall(r"<li class=\"ui-tabmenuitem(?:.*?)onclick=\"PrimeFaces\.ab\({s:&quot;(.*?)&quot;,f:(?:.*?)</li>", r.text)
    viewState = re.findall(r"id=\"javax\.faces\.ViewState\" value=\"(.*?)\" />", r.text)

    if (len(id) == 0 or len(viewState) == 0):
        print("notCLef")
    else:
        return id[0], viewState[0]

@app.route("/update/<email>", methods=['POST'])
def update(email):
    id, viewState = getViewState(OGE_DETAILS)
    dataNote = {"javax.faces.partial.execute": "@all",
                "javax.faces.partial.render": "mainFormDetailNote",
                id: id,
                id + "_menuid": str(2),
                "mainFormDetailNote_SUBMIT": "1",
                "javax.faces.ViewState": viewState}
    r = session.post(OGE_DETAILS, data=dataNote, headers={'referer':OGE_DETAILS, 'Faces-Request': 'partial/ajax'})
    matieresResult = re.findall(r"request\('(.*?):elpLink',event(?:.*?)>- (.*?)</a>(?:.*?)font-style:italic;(?:.*?)\">\((?:(?:([0-9]+) note(?:s|))|(?:pas de notes))\)</font>", r.text, re.DOTALL)

    listMatiereFichier, listNoteFichier = getNotesMatieres()
    listMatiere = []
    listMatiereBis = []
    nbNote = []
    nbNoteBis = []
    listMatiereNom = []
    totalNote = 0
    i = 0;

    for matiere in matieresResult :
        print(matiere[1], matiere[2])
        listMatiereBis.append(matiere[1])
        nbNoteBis.append(matiere[2])
        for k in range(len(listMatiereBis)) :
            if not (listMatiereBis[k] in listMatiere):
                listMatiere.append(listMatiereBis[k])
                nbNote.append(nbNoteBis[k])

        if (listMatiereFichier[i] == matiere[1]):
            if ((listNoteFichier[i] != "") and (matiere[2] != "")):
                if (int(listNoteFichier[i]) < int(matiere[2])):
                    listMatiereNom.append(listMatiereFichier[i])
            if ((listNoteFichier[i] == "") and (matiere[2] != "")):
                listMatiereNom.append(listMatiereFichier[i])
            i += 1

        if (matiere[2] != ''):
            totalNote += int(matiere[2])

    if (totalNote > getNoteTotal()):
        envoyerMail(listMatiereNom, email)

    write(convertToJSON(listMatiere, nbNote))
    return str(getNoteTotal())

def write(matieres):
    with open("/home/pi/API-ON/data.json", "w") as fichier:
        fichier.write(matieres)

def read():
    with open('/home/pi/API-ON/data.json') as json_data:
        data_dict = json.load(json_data)
    return data_dict

def convertToJSON(matieres, nbNote):
    dictionnaire = {}
    for i in range(len(matieres)):
        dictionnaire[matieres[i]] = nbNote[i]
    print(dictionnaire)
    cJson = json.dumps(dictionnaire)
    return cJson

def getNoteTotal():
    totalNote = 0

    for cle, valeur in read().items():
        if (valeur != ''):
            totalNote += int(valeur)

    return totalNote

def getNotesMatieres():
    listMatiere = []
    listNote = []
    for cle, valeur in read().items():
        listMatiere.append(cle)
        listNote.append(valeur)
    return listMatiere, listNote


def envoyerMail(matieres, email):
    with open("/home/pi/API-ON/passwordGmail.txt", "r") as fichier:
        SMTP_PASSWORD = fichier.read()
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587
    SMTP_USERNAME = "milhetbenjamin@gmail.com"
    EMAIL_FROM = "milhetbenjamin@gmail.com"
    EMAIL_TO = email
    EMAIL_SUBJECT = "Nouvelle note sur OGE"
    EMAIL_MESSAGE = ""
    for matiere in matieres:
        EMAIL_MESSAGE += "Vous avez une nouvelle note en " + matiere + ".\n"
    EMAIL_MESSAGE = ["\n".join(msg.replace(u'\xe9', u' ')) for msg in EMAIL_MESSAGE]
    EMAIL_MESSAGE = ''.join(EMAIL_MESSAGE)
    s = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    s.starttls()
    s.login(SMTP_USERNAME, SMTP_PASSWORD)
    message = 'Subject: {}\n\n{}'.format(EMAIL_SUBJECT, EMAIL_MESSAGE)
    s.sendmail(EMAIL_FROM, EMAIL_TO, message)
    s.quit()
