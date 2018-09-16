# from django.core.exceptions import ObjectDoesNotExist
# from django.core.management import BaseCommand
#
# from modulevieasso.models import Structure
# from modulevieasso.models import Region
# from modulevieasso.models import Individu
# from modulevieasso.models import Fonction
# # from pytz import UTC
# import re
#
# ALREADY_LOADED_ERROR_MESSAGE = """
# If you need to reload the pet data from the CSV file,
# first delete the db.sqlite3 file to destroy the database.
# Then, run `python manage.py migrate` for a new empty
# database with tables"""
#
#
# class Command(BaseCommand):
#     # Show this when the user types help
#     help = "Loads data from structure.csv into our structure model"
#
#     def handle(self, *args, **options):
#         print("Reading data")
#
#         fonction = Fonction.objects.get(id=2)
#         sla_by_region = open('tout.txt')
#         for line in sla_by_region:
#             print("Région = {} structure = {}".format(line.split(";")[0], line.split(";")[1]))
#             region = Region.objects.get(nomRegion=line.split(";")[0])
#             if line.split(";")[1].upper() == 'REGION':
#                 structure = Structure(nomStructure='REGION', region=region)
#                 structure.save()
#             else:
#                 try:
#                     structure = Structure.objects.get(nomStructure=line.split(";")[1].upper())
#                 except ObjectDoesNotExist:
#                     print("erreur : {} ".format(NameError))
#                     structure = Structure(nomStructure=line.split(";")[1])
#                     structure.save()
#
#             print("structure saved")
#             individu = Individu(nom=line.split(";")[4].upper(),
#                                 prenom=line.split(";")[5].upper(),
#                                 email=line.split(";")[9].upper(),
#                                 structure=structure, fonction=fonction,
#                                 adresse=line.split(";")[6],
#                                 codepostal=line.split(";")[7],
#                                 tel=line.split(";")[8])
#             individu.save()
#             print("individu saved")
#
#         print("Fin du chargement")
#
#     """ for line in sla_by_region:
#          region, sla, nom, prenom, email = line.split(";")[0].strip("ï»¿"), line.split(";")[1], line.split(";")[2], \
#                                            line.split(";")[3], line.split(";")[4]
#          slaRegion[sla] = [region, nom, prenom, email]
#
#      sla_by_region.close()
#
#      slabyCode = {}
#      for line in f:
#          code, nom = re.split('\t', line)[0].strip(), re.split('\t', line)[1].strip()
#          slabyCode[nom] = code
#
#      keys = slaRegion.keys()
#
#      for key in keys:
#          print("nom structure  {}".format(slaRegion.get(key)))
#          #if slaRegion.get(key,'Unknown')!='Unknown':
#              #print('la region trouvé = {}'.format(slaRegion.get(key)[0]))
#          nomregion = '{}'.format(slaRegion.get(key)[0])
#          region = Region.objects.get(nomRegion=nomregion)
#          #print("region {} pour sla {}".format(region.nomRegion, slaRegion.get(key)[1]))
#          print("Enregistrement des structure")
#          structure = Structure()
#          structure.codeStructure = 0#slabyCode[key]
#          structure.nomStructure = key
#          structure.region = region
#          structure.save()
#          print("Enregistrement individu RESLA")
#          fonction = Fonction.objects.get(codeFonction='RESLA')
#          individu = Individu()
#          individu.nom=slaRegion.get(key)[1]
#          individu.prenom=slaRegion.get(key)[2]
#          individu.email = slaRegion.get(key)[3]
#          individu.structure=structure
#          individu.fonction = Fonction.objects.get(codeFonction='RESLA')
#          individu.save()
#
#      print("Regions enregistrées {}  structures enregistrées{} individu enregistrés {}".format(Region.objects.count(),Structure.objects.count(),Individu.objects.count()))
#      f.close()
#
#      # print('Enregistrement de la fonction RESLA')
#      # Fonction(nomFonction="Responsable Structure Locale d'activité", codeFonction='RESLA').save()
#
#
#      for row in sla_by_region:
#          s = structure.objects.get(nomStructure=row.split(";")[1])
#          individu = Individu()
#          individu.nom=row.split(";")[2]
#          individu.prenom=row.split(";")[3]
#          individu.email=row.split(";")[4]
#          individu.structure=s,
#          individu.fonction=Fonction.objects.get(codeFonction='RESLA')
#          Individu.save()
#
#      #individu.objects.bulk_create(individus)
#      sla_by_region.close()
#      #structure.objects.bulk_create(structures)
#
#      #for row in DictReader(open('sla_by_region.csv')):
#       #   struc = Structure.objects.get(nomStructure="EEDF {}".format(row.split(";")[1]) + row["sla"])
#
#
#      # print("Loading pet data for pets available for adoption")
#
#      for row in DictReader(open('./pet_data.csv')):
#          pet = Pet()
#          pet.name = row['Pet']
#          pet.submitter = row['Submitter']
#          pet.species = row['Species']
#          pet.breed = row['Breed']
#          pet.description = row['Pet Description']
#          pet.sex = row['Sex']
#          pet.age = row['Age']
#          raw_submission_date = row['submission date']
#          submission_date = UTC.localize(
#              datetime.strptime(raw_submission_date, DATETIME_FORMAT))
#          pet.submission_date = submission_date
#          pet.save()
#          raw_vaccination_names = row['vaccinations']
#          vaccination_names = [name for name in raw_vaccination_names.split('| ') if name]
#          for vac_name in vaccination_names:
#              vac = Vaccine.objects.get(name=vac_name)
#              pet.vaccinations.add(vac)
#          pet.save()
# """
