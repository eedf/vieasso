from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from .forms import LoginForm, NominationForm
from .models import User, DemandeNominationRedaction, Structure, Individu, Nomination, Fonction, CompteRendu
from .helper import ConnectHelper
from hashlib import sha1
from dateutil import parser
from datetime import datetime
import pytz

"""
affiche la page de login seulement ne fait pas d'authentification
elle réinitialise la session
"""


def index(request):
    request.session.flush()
    loginform = LoginForm()
    return render(request, "index.html", {'form': loginform})


"""
affiche la page home ou se trouve le menu
"""


def home(request):
    context = request.session.get('context')
    if context is None:
        return redirect("/", permanent=True)
    print(context)
    if context['user']['is_connected']:
        return render(request, "home.html", {'context': context})
    else:
        return redirect("/", permanent=True)


"""
affiche la page de login et gére l'authentification
"""


def login(request):
    if request.method == 'POST':
        context = {}
        form = LoginForm(request.POST)
        if form.is_valid():
            # traitement de données
            login = form.cleaned_data["login"]
            password = form.cleaned_data["password"]
            passwordhash = sha1(password.encode('utf-8')).hexdigest()
            try:
                user = User.objects.filter(login__exact=login).get()
                # connexion de l'admin
                if user.role == "SUPERADMIN" and user.password == passwordhash:
                    context = {
                        'user': {
                            'name': user.name,
                            'login': user.login,
                            'role': user.role,
                            'nomine': True,
                            'sla': "SIEGE NATIONAL",
                            'region': "SIEGE NATIONAL",
                            'is_connected': True, }
                    }
                    request.session['context'] = context
                    return redirect('/home/', permanent=True)
            except:
                user = None
            # recherche dans la base de données d'abord
            if user:
                if user.password == passwordhash:
                    # mot de passe correct
                    if user.nomination and user.nomination.reponseAdmin:
                        nomine = True
                        sla = user.nomination.structure.nomstructure
                        region = user.nomination.structure.region
                    else:
                        nomine = False
                        sla = ""
                        region=""
                    context = {
                        'user': {
                            'name': user.name,
                            'login': user.login,
                            'role': user.role,
                            'nomine': nomine,
                            'sla': sla,
                            'region': region,
                            'is_connected': True, }
                    }
                    request.session['context'] = context
                    return redirect('/home/', permanent=True)
                else:
                    # mot de passe erroné
                    error = "Mot de passe erroné"
                    return render(request, 'index.html', {'message': error, 'form': LoginForm()})
            else:
                # recherche dans le site web car n'existe pas en local
                name = ConnectHelper(login, password)
                if name != 'unknown':
                    # authentificaton établie
                    user = User(login=login, password=passwordhash, name=name)
                    user.save()
                    context = {
                        'user': {
                            'name': name,
                            'role': 'unknown',
                            'nomine': False,
                            'login': user.login,
                            'is_connected': True, }
                    }
                    # fin traitement
                    request.session['context'] = context
                    return redirect('/home/', permanent=True, )
                else:
                    # echec d'authentification
                    error = 'Echec de connexion'
                    request.session.flush()
                    return render(request, 'index.html', {'message': error, 'form': LoginForm()})
    else:
        form = LoginForm()
        request.session.flush()
        return render(request, 'index.html', {'form': form})


"""
pour éditer un compte rendu
"""


def edit(request):
    context = request.session.get('context')
    if context is None:
        return redirect("/", permanent=True)
    if request.method == 'POST':
        sla = request.POST["sla"].upper()
        sla = Structure.objects.filter(nomstructure__exact=sla).get()
        nominant, _ = Individu.objects.get_or_create(codeadherent=context['user']['login'], structure=sla)
        region = request.POST["region"].upper()
        lieu = request.POST["lieu"].upper()
        dateapl = parser.parse(request.POST["dateapl"])
        nbpresent = int(request.POST["nbpresent"])
        nbvotant = int(request.POST["nbvotant"])
        representantnational = request.POST["representantNational"].upper()
        representantregional = request.POST["representantregional"].upper()
        votepour = int(request.POST["votepour"])
        votecontre = int(request.POST["votecontre"])
        voteabstention = int(request.POST["voteabstention"])
        presentationbudget = bool(request.POST["presentationbudget"])
        pointfinancier = float(request.POST["pointfinancier"] if request.POST["pointfinancier"] != "" else 0)
        corpscr = request.POST["comments"].upper()
        signataire = request.POST["signataire"].upper()
        resla = {"codeadherent": request.POST["coderesla"].upper(),
                 "nom": request.POST["nomresla"].upper(),
                 "prenom": request.POST["prenomresla"].upper(),
                 "tel": request.POST["telresla"].upper(),
                 "mail": request.POST["mailresla"].upper(),
                 "adresse": request.POST["adresseresla"].upper()
                 }

        # TODO verifier si l'individu existe avant de l'enregistrer de nouveau
        # vérification dans la base de données
        resladb, _ = Individu.objects.get_or_create(codeadherent=resla['codeadherent'])
        resladb.nom = resla['nom']
        resladb.prenom = resla['prenom']
        resladb.tel = resla['tel']
        resladb.mail = resla['mail']
        resladb.adresse = resla['adresse']
        resladb.structure = sla
        resladb.save()
        # fonction, _ = Fonction.objects.get_or_create(
        #     codefonction="RESLA",
        #     nomfonction="RESPONSABLE SLA"
        # )
        # nominant n'est pas de la meme structure car doit être nomé par la région
        # nominant,_=Individu.objects.get_or_create(
        #     codeadherent=context['user']['login'],
        # )
        # nomination = Nomination(
        #     dateNomination=datetime.now(),
        #     fonction=fonction,
        #     commentaire="En codant",
        #     structure=sla,
        # )
        # nomination.save()
        # resladb.nomination.add(nomination)
        # resladb.save()
        tresla = {'codeadherent': request.POST["codetresla"].upper(),
                  'nom': request.POST["nomtresla"].upper(),
                  'prenom': request.POST["prenomtresla"].upper(),
                  'tel': request.POST["teltresla"].upper(),
                  'mail': request.POST["mailtresla"].upper(),
                  'adresse': request.POST["adressetresla"].upper(),
                  }
        # TODO verifier si l'individu existe avant de l'enregistrer de nouveau
        tresladb, _ = Individu.objects.get_or_create(codeadherent=tresla['codeadherent'])
        tresladb.nom = tresla['nom']
        tresladb.prenom = tresla['prenom']
        tresladb.tel = tresla['tel']
        tresladb.mail = tresla['mail']
        tresladb.adresse = tresla['adresse']
        tresladb.structure = sla
        tresladb.save()
        # fonction, _ = Fonction.objects.get_or_create(
        #     codefonction="TRESLA",
        #     nomfonction="TRESORIER SLA"
        # )
        # nominant n'est pas de la meme structure car doit être nomé par la région
        # nominant, _ = Individu.objects.get_or_create(
        #     codeadherent=context['user']['login'],
        # )
        # nomination = Nomination(
        #     dateNomination=datetime.now(),
        #     fonction=fonction,
        #     commentaire="En codant",
        #     structure=sla,
        # )
        # nomination.save()
        # tresladb.nomination.add(nomination)
        # tresladb.save()
        delegueag = {'codeadherent': request.POST["codedelegueag"].upper(),
                     'nom': request.POST["nomdelegueag"].upper(),
                     'prenom': request.POST["prenomdelegueag"].upper(),
                     'tel': request.POST["teldelegueag"].upper(),
                     'mail': request.POST["maildelegueag"].upper(),
                     'adresse': request.POST["adressedelegueag"].upper()}

        # TODO verifier si l'individu existe avant de l'enregistrer de nouveau
        delegueagdb, _ = Individu.objects.get_or_create(codeadherent=delegueag['codeadherent'])
        delegueagdb.nom = delegueag['nom']
        delegueagdb.prenom = delegueag['prenom']
        delegueagdb.tel = delegueag['tel']
        delegueagdb.mail = delegueag['mail']
        delegueagdb.adresse = delegueag['adresse']
        delegueagdb.structure = sla
        delegueagdb.save()
        fonction, _ = Fonction.objects.get_or_create(
            codefonction="DAG",
            nomfonction="DELEGUE AG"
        )
        # nominant est de la meme structure
        nominant, _ = Individu.objects.get_or_create(
            codeadherent=context['user']['login'],
            structure=sla
        )
        nomination = Nomination(
            dateNomination=datetime.now(),
            fonction=fonction,
            nominant=nominant,
            commentaire="En codant",
            structure=sla,
        )
        nomination.save()
        delegueagdb.nomination.add(nomination)
        delegueagdb.save()
        suppdelegueag = {'codeadherent': request.POST["codesuppdelegueag"].upper(),
                         'nom': request.POST["nomsuppdelegueag"].upper(),
                         'prenom': request.POST["prenomsuppdelegueag"].upper(),
                         'tel': request.POST["telsuppdelegueag"].upper(),
                         'mail': request.POST["mailsuppdelegueag"].upper(),
                         'adresse': request.POST["adressesuppdelegueag"].upper()
                         }
        # TODO verifier si l'individu existe avant de l'enregistrer de nouveau
        suppdelegueagdb, _ = Individu.objects.get_or_create(codeadherent=suppdelegueag['codeadherent'])
        suppdelegueagdb.nom = suppdelegueag['nom']
        suppdelegueagdb.prenom = suppdelegueag['prenom']
        suppdelegueagdb.tel = suppdelegueag['tel']
        suppdelegueagdb.mail = suppdelegueag['mail']
        suppdelegueagdb.adresse = suppdelegueag['adresse']
        suppdelegueagdb.structure = sla
        suppdelegueagdb.save()
        fonction, _ = Fonction.objects.get_or_create(
            codefonction="SUPDAG",
            nomfonction="SUPPLEANT DELEGUE AG"
        )
        # nominant est de la meme structure
        nominant, _ = Individu.objects.get_or_create(
            codeadherent=context['user']['login'],
            structure=sla,
        )
        nomination = Nomination(
            dateNomination=datetime.now(),
            fonction=fonction,
            nominant=nominant,
            commentaire="En codant",
            structure=sla,
        )
        nomination.save()
        suppdelegueagdb.nomination.add(nomination)
        suppdelegueagdb.save()
        cr = CompteRendu(
            sla=sla,
            dateCreation=datetime.now(),
            dateapl=dateapl,
            lieuApl=lieu,
            nbPresent=nbpresent,
            nbVotant=nbvotant,
            representantNational=representantnational,
            representantRegional=representantregional,
            nbPour=votepour,
            nbContre=votecontre,
            nbAbstention=voteabstention,
            budgetPresente=presentationbudget,
            bilanFinancier=pointfinancier,
            corpsCr=corpscr,
            signataireCr=signataire,
            delegueAg=delegueagdb,
            supDelegueAg=suppdelegueagdb,
            resla=resladb,
            tresla=tresladb,
        )
        cr.save()
        return redirect("/listcr/",permanent=True)
    else:
        return render(request, "crapl.html", {'context': context})


"""
affiche la page des documents
"""


def docs(request):
    context = request.session.get('context')
    if context is None:
        return redirect("/", permanent=True)
    return render(request, "docs.html", {'context': context})


"""
pour créer une liste d'émargement en pdf
"""


def listemargement(request):
    context = request.session.get('context')
    if context is None:
        return redirect("/", permanent=True)
    return render(request, "listemargement.html", {'context': context})


"""
affiche la liste des cr pour validation
"""


def listcr(request):
    context = request.session.get('context')
    if context is None:
        return redirect("/", permanent=True)
    context = request.session.get('context')
    listcr = []
    if not context['user']['sla'] == "SIEGE NATIONAL":
        try:
            sla = Structure.objects.filter(nomstructure__exact=context['user']['sla']).get()
        except:

            return render(request, "listcr.html", {'context': context, 'listcr': None});
        comptesrendus = CompteRendu.objects.filter(sla__exact=sla).all()
    else:
        comptesrendus = CompteRendu.objects.all()
    i = 0
    for c in comptesrendus:
        i += 1

        try:
            datenominationresla=c.resla.nomination.filter(fonction__codefonction__exact="RESLA").filter(nominant__isnull=True).get().dateNomination.strftime("%d/%m/%Y")
        except:
            datenominationresla = ""

        try:
            datenominationtresla=c.resla.nomination.filter(fonction__codefonction__exact="TRESLA").filter(nominant__isnull=True).get().dateNomination.strftime("%d/%m/%Y")
        except:
            datenominationtresla=""

        listcr.append({"ordre": i,
                       "id": c.id,
                       "dateapl": c.dateapl.strftime("%d/%m/%Y"),
                       "lieuapl": c.lieuApl,
                       "sla": c.sla,
                       "resla": c.resla,
                       "datenominationresla": datenominationresla,
                       "tresla": c.tresla,
                       "datenominationtresla":datenominationtresla,
                       "delegueag": c.delegueAg,
                       "supdelegueag": c.supDelegueAg,
                       "datecreationcr": c.dateCreation.strftime("%d/%m/%Y"),
                       "signatairecr": c.signataireCr,
                       "corpscr": c.corpsCr,
                       })
    return render(request, "listcr.html", {'context': context, 'listcr': listcr});


def parametre(request):
    # todo : non encore réalisée
    context = request.session.get('context')
    if context is None:
        return redirect("/", permanent=True)
    return HttpResponse("Paramètrages", {'context': context})



"""
pour demander une nomination afin de rédiger un cr afférent à une sla
"""


def nominationredacteur(request):
    context = request.session.get('context')
    if context is None:
        return redirect("/", permanent=True)
    if request.method == 'POST':
        form = NominationForm(request.POST)
        # print(request.POST)
        if form.is_valid():
            regions = (
                (1, 'CENTRE'),
                (2, 'HAUTS DE FRANCE'),
                (3, 'ILE DE FRANCE'),
                (4, 'BRETAGNE'),
                (5, 'NORMANDIE'),
                (6, 'BOURGOGNE'),
                (7, 'FRANCHE COMTE'),
                (8, 'GRAND EST'),
                (9, 'AQUITAINE'),
                (10, 'MIDI PYRENEES'),
                (11, 'POITOU CHARENTE'),
                (12, 'AUVERGNE'),
                (13, 'RHONE ALPES'),
                (14, 'PAM'),
                (15, 'LANGUEDOC ROUSSILLON'),
                (16, 'GUYANE'),
            )
            # traitement de données
            login = form.cleaned_data["login"]
            name = form.cleaned_data["name"]
            region = regions[int(form.cleaned_data["region"]) - 1][1]
            sla = form.cleaned_data["sla"]
            tel = form.cleaned_data["tel"]
            adresse = form.cleaned_data["adresse"]
            codepostal = form.cleaned_data["codepostal"]
            mail = form.cleaned_data["mail"]
            if login and region and sla and tel and adresse and codepostal and mail:
                # récupération de l'user
                user = User.objects.filter(login__exact=login).get()
                try:
                    # récupération de la structure sur laquelle il a été nommé
                    sla = Structure.objects.filter(nomstructure__exact=sla.upper()).get()
                except:
                    sla = Structure(nomstructure=sla.upper(), region=region)
                    sla.save()
                # création d'une demande de nomination avec les infos récupérées
                demande = DemandeNominationRedaction(
                    dateDemande=datetime.now(), structure=sla)
                demande.save()
                # affectation de la demande à l'utilisateur et mise à jour
                user.nomination=demande
                user.adresse = adresse
                user.tel = tel
                user.codepostal = codepostal
                user.mail = mail
                user.save()
                print('userobject = ',user)
                message = '{} Votre demande de nomination a été prise en considération'.format(name)
                return render(request, "demandenomination.html",
                              {'error': message, 'form': form, 'context': context})
        else:
            print(form.errors)
            form = NominationForm()
            message = "Des renseignements manquent à votre demande de nomination"
            return render(request, "demandenomination.html", {'error': message, 'form': form, 'context': context})
    else:
        # création d'un formulaire de nomination avec les infos de l'user après authentification
        form = NominationForm(initial={'login': context['user']['login'],
                                       'name': context['user']['name']})
        return render(request, "demandenomination.html", {'form': form, 'context': context})


"""
permet d'exécuter le logout
"""


def sortir(request):
    request.session.clear()
    request.session.flush()
    return redirect("/", permanent=True)


"""
permet de récupérer la liste des demandes de nominations et les affiches pour validation
"""


def listnomination(request):
    context = request.session.get('context')
    if context is None:
        return redirect("/", permanent=True)
    demandants = User.objects.all().exclude(role__exact="SUPERADMIN")
    listdemandants = []
    for d in demandants:
        datereponse=""
        datedemande=""
        if d.nomination.reponseAdmin:
            datereponse=d.nomination.dateReponse.strftime("%d/%m/%Y")
        if d.nomination.dateDemande:
            datedemande=d.nomination.dateDemande.strftime("%d/%m/%Y")
        listdemandants.append({'id': d.id,
                     'login': d.login,
                     'name': d.name,
                     'cp': d.codepostal,
                     'adresse': d.adresse,
                     'tel': d.tel,
                     'mail': d.mail,
                     'datedemande': datedemande,
                     'datereponse':datereponse,
                     'sla': d.nomination.structure.nomstructure,
                     'region': d.nomination.structure.region,
                     'role': d.role})
    return render(request, "listdemandes.html", {'context': context, 'list': listdemandants})


"""
méthode utilisée pour valider la nomination d'un utilisateur pour la redaction cr avec ajax
"""


def validernomination(request):
    #idempotente
    if request.method == "POST":
        id = request.POST['id']
        role = request.POST['role']
        try:
            user = User.objects.get(pk=id)
        except:
            return JsonResponse({"answer": False})
        if not user.nomination.reponseAdmin == "ok":
            user.nomination.reponseAdmin = "ok"
            user.nomination.dateReponse=datetime.now()
            user.nomination.save()
        user.role = role
        user.save()
    return JsonResponse({"answer": True})


"""
asynchrone pour enregistrer les memebres de l'équipe d'animation
"""


def saveanimationteam(request):
    context = request.session.get('context')
    if context is None:
        return redirect("/", permanent=True)
    if request.method == "POST":
        print(request.POST)
        codeadherent = request.POST['codeanimation']
        nom = request.POST['nom'].upper()
        prenom = request.POST['prenom'].upper()
        tel = request.POST['tel']
        mail = request.POST['mail'].upper()
        adresse= request.POST['adresse'].upper()
        fonction, _ = Fonction.objects.get_or_create(nomfonction=request.POST['fonction'].upper())
        sla, _=Structure.objects.get_or_create(nomstructure=context['user']['sla'])
        teammember, _ = Individu.objects.get_or_create(codeadherent=codeadherent, nom=nom, prenom=prenom, tel=tel,
                                                       adresse=adresse, mail=mail,structure=sla)
        nominant, _ = Individu.objects.get_or_create(
            codeadherent=context['user']['login'],
            structure=sla,
        )
        try:
            nomination=teammember.nomination.filter(fonction__nomfonction__exact=fonction.nomfonction).get()
        except:
            nomination=Nomination(dateNomination=datetime.now(),fonction=fonction,nominant=nominant,structure=sla, commentaire="Nominé directement par système")
            nomination.save()
        teammember.nomination.add(nomination)
    return JsonResponse({"answer": True,"teammemberid":teammember.id,"nominationid":nomination.id})


"""
asynchrone pour supprimer nommination à l'équipe d'animation
"""


def removenomination(request):
    if request.method=="POST":
        teammemberid=request.POST['teammemberid']
        nominationid = request.POST['nominationid']
        nomination=Nomination.objects.get(id=nominationid)
        teammember=Individu.objects.get(id=teammemberid)
        teammember.nomination.remove(nomination)
    return JsonResponse({"answer": True,"teammemberid":teammember.id})


#todo verification validation cr
#todo fonction pour nommer resla / tresla
#todo fonction pour exporter compte rendu à l'aide de open doc
#todo liste emargement à réaliser
#todo importer les noms des structures
#todo importer les codes adhérents et les nom prenom
