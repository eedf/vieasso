# from django.core.exceptions import ObjectDoesNotExist
# from django.core.management import BaseCommand
# import csv
# from modulevieasso.models import Structure
# from modulevieasso.models import Region
# from modulevieasso.models import Individu
# from modulevieasso.models import Fonction
#
#
# class Command(BaseCommand):
#     # Show this when the user types help
#     help = "Loads data from structure.csv into our structure model"
#
#     def handle(self, *args, **options):
#         with open('tout.txt',newline='') as csvfile:
#             file = csv.DictReader(csvfile,delimiter=';')
#             for r in file:
#                 if r['CODE']=='0':
#                     continue
#                 #toutes les régions et les fonctions ont été introduites à la base de données en dur
#                 fonction = Fonction.objects.get(codeFonction=r['FONCTION'])
#                 region = Region.objects.get(nomRegion=r['REGION'])
#                 if r['SLA'].upper()=='REGION':
#                     print('CAS SLA == REGION')
#                     try:
#                         structure=Structure.objects.get(nomStructure="REGION DE {}".format(r['REGION']))
#                         print('SLA REGION TROUVEE')
#                     except ObjectDoesNotExist:
#                         structure=Structure(nomStructure="REGION DE {}".format(r['REGION']),region=region)
#                         print('SLA REGION ENREGISTREE',r['REGION'])
#                         structure.save()
#                 else:
#                     try:
#                         structure = Structure.objects.get(nomStructure=r['SLA'].upper())
#                         print('SLA TROUVEE')
#                     except ObjectDoesNotExist:
#                         structure=Structure(nomStructure=r['SLA'].upper(),region=region)
#                         print('SLA ENREGISTRE =',r['SLA'])
#                         structure.save()
#                 try:
#                     individu = Individu.objects.get(codeadherent=r['CODE'])
#                     print('Individu trouvé ', individu.nom, individu.prenom)
#                 except ObjectDoesNotExist:
#                     individu=Individu(codeadherent=r['CODE'],
#                                       nom=r['NOM'],
#                                       prenom=r['PRENOM'],
#                                       adresse=r['ADRESSE'],
#                                       codepostal=r['CODE POSTAL'],
#                                       tel=r['TEL'],
#                                       email=r['EMAIL'],
#                                   )
#                 individu.save()
#                 individu.fonction.add(fonction)
#                 individu.structure.add(structure)
#                 individu.save()
#                 print('individu enregistré')
#                 print('Fin de traitement')