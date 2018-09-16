from django.db import models


class Individu(models.Model):
	codeadherent=models.CharField(max_length=15,null=True)
	civilite=models.CharField(max_length=50,null=True)
	nom=models.CharField(max_length=50,null=True)
	prenom=models.CharField(max_length=50,null=True)
	adresse=models.CharField(max_length=50,null=True)
	mail=models.CharField(max_length=50,null=True)
	tel=models.CharField(max_length=50,null=True)
	codepostal=models.CharField(max_length=50,null=True)
	structure=models.ForeignKey('Structure',on_delete=models.SET_NULL,null=True)
	nomination=models.ManyToManyField('Nomination',related_name="nomination_individu")


""" pour RESLA TRESLA DAG ET SUPPDG """
class Nomination(models.Model):
	dateNomination= models.DateTimeField('datenomination')
	fonction = models.ForeignKey('Fonction',on_delete=models.SET_NULL,null=True)
	nominant = models.ForeignKey('Individu',on_delete=models.SET_NULL,null=True,related_name='nominant')
	commentaire = models.CharField(max_length=200)
	structure=models.ForeignKey('Structure', on_delete=models.SET_NULL,null=True)

""" Pour la rédaction d'un compte rendu"""
class DemandeNominationRedaction(models.Model):
	dateDemande=models.DateTimeField('datenomination', null=True)
	dateReponse=models.DateTimeField('datereponse', null=True)
	structure=models.ForeignKey('Structure', on_delete=models.SET_NULL,null=True)
	reponseAdmin=models.CharField(max_length=50,null=True)

class Region(models.Model):
	nom=models.CharField(max_length=15)


class Structure(models.Model):
	codestructure=models.CharField(max_length=15, null=True)
	nomstructure=models.CharField(max_length=100, null=True)
	region= models.CharField(max_length=100, null=True)


class User(models.Model):
	login=models.CharField(max_length=15, null=True)
	name=models.CharField(max_length=50,  null=True)
	password=models.CharField(max_length=40, null=True)
	role=models.CharField(max_length=50, null=True)
	mail=models.CharField(max_length=50, null=True)
	adresse=models.CharField(max_length=50, null=True)
	codepostal=models.CharField(max_length=50, null=True)
	tel=models.CharField(max_length=50, null=True)
	nomination=models.ForeignKey('DemandeNominationRedaction', on_delete=models.SET_NULL, null=True)


class Fonction(models.Model):
	codefonction=models.CharField(max_length=15)
	nomfonction=models.CharField(max_length=100)


class CompteRendu(models.Model):
	sla = models.ForeignKey('Structure', on_delete=models.SET_NULL,null=True)
	dateCreation = models.DateTimeField('datecreationcr',null=True, blank=True)
	dateapl=models.DateTimeField('dateapl',null=True, blank=True)
	lieuApl=models.CharField('lieuapl', max_length=100,null=True)
	nbPresent = models.IntegerField('nbPresent',null=True)
	nbVotant = models.IntegerField('nbVotant',null=True)
	representantNational = models.CharField('representantnational', max_length=100,null=True)#models.ForeignKey('Individu',on_delete=models.SET_NULL,related_name='representantnational', null=True)
	representantRegional= models.CharField('representantregional', max_length=100, null=True)#models.ForeignKey('Individu',on_delete=models.SET_NULL,related_name='representantregional', null=True)
	nbPour=models.IntegerField('nbPour',null=True)
	nbContre=models.IntegerField('nbContre',null=True)
	nbAbstention = models.IntegerField('nbAbstention',null=True)
	budgetPresente=models.BooleanField('budgetPresente',default=False)
	bilanFinancier=models.DecimalField('bilanFinancier',decimal_places=2,max_digits=8,null=True)
	corpsCr = models.CharField('corpsCr', max_length=500, blank=True,null=True)
	signataireCr = models.CharField('signataireCr', max_length=50, blank=True,null=True)
	delegueAg = models.ForeignKey('Individu',on_delete=models.SET_NULL,related_name='delegueag', null=True)
	supDelegueAg= models.ForeignKey('Individu',on_delete=models.SET_NULL,related_name='supdelegueag', null=True)
	resla= models.ForeignKey('Individu',on_delete=models.SET_NULL,related_name='resla', null=True)
	tresla= models.ForeignKey('Individu',on_delete=models.SET_NULL,related_name='tresla', null=True)
	valide=models.BooleanField('validation',default=False)
	equipeanimation=models.ManyToManyField('Individu')
