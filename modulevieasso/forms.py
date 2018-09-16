from django import forms


class LoginForm(forms.Form):
    login = forms.CharField(
        label='Login :',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'type': 'Text',
                'title': 'Entrer votre login',
            },
        )
    )
    password = forms.CharField(
        label='Mot de passe :',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'type': 'password',
                'title': 'Entrer votre mot de passe',
            },
        )
    )


class NominationForm(forms.Form):
    name = forms.CharField(
        label='Nom & prénom :',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'type': 'Text',
                'title': 'Votre nom et prénom',
                'readonly':'readonly',
            },
        )
    )
    login = forms.CharField(
        label='Login:',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'type': 'Text',
                'title': 'Votre login',
                'readonly': 'readonly',
            },
        )
    )
    region=forms.ChoiceField(
        label='Région :',
        choices=(
            (1, 'CENTRE'),
            (2, 'HAUTS DE FRANCE'),
            (3, 'ILE DE FRANCE'),
            (4, 'BRETAGNE'),
            (5, 'NORMANDIE'),
            (6, 'BOURGOGNE'),(7, 'FRANCHE COMTE'), (8, 'GRAND EST'), (9, 'AQUITAINE'), (10, 'MIDI PYRENEES'),
            (11, 'POITOU CHARENTE'),(12, 'AUVERGNE'), (13, 'RHONE ALPES'), (14, 'PAM'), (15, 'LANGUEDOC ROUSSILLON'),
            (16, 'GUYANE')),
        widget=forms.Select(
            attrs={
                'class': 'custom-select',
                'title': 'Sélectionner votre région',
            },
        )
    )
    sla=forms.CharField(
        label='Votre structure :',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'type': 'Text',
                'title': 'Entrer votre structure',
                'placeholder': 'Exemple : PARIS 3',
            },
        )
    )
    mail = forms.CharField(
        label='Adresse mail :',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'type': 'email',
                'title': 'Entrer votre adresse mail',
                'placeholder': 'Exemple : nom@gmail.com',
                'pattern':'[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,3}$',
            },
        )
    )
    adresse = forms.CharField(
        label='Adresse :',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'type': 'Text',
                'title': 'Entrer votre adresse',
                'placeholder': 'Exemple : 15 RUE LIBERTE LYON',
            },
        )
    )
    codepostal = forms.CharField(
        label='Code postal :',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'type': 'Text',
                'title': 'Entrer votre code postal',
                'placeholder': 'Exemple: 92100',
                'pattern': '^\d{5}',
            },
        )
    )
    tel = forms.CharField(
        label='N° Tel :',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'type': 'tel',
                'title': 'Entrer votre structure',
                'placeholder': 'EX : PARIS 3',
                'pattern':'^0\d{9}'
            },
        )
    )


