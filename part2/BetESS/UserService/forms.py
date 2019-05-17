from django import forms


class UserForm(forms.Form):
    nome = forms.CharField(max_length=200)
    email = forms.EmailField()
    password = forms.PasswordInput()
    clube = forms.IntegerField()


'''
class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.PasswordInput()
'''

class CriarEventoForm(forms.Form):
    jogo = forms.IntegerField()
    equipa = forms.IntegerField(required=False)
    tipo = forms.IntegerField()
    atleta1 = forms.IntegerField(required=False)
    atleta2 = forms.IntegerField(required=False)
    zonaC = forms.CharField(max_length=5, required=False)
    zonaB = forms.CharField(max_length=5, required=False)
    instante = forms.TimeField()
    novoinst = forms.TimeField(required=False)


class MudarEventoForm(forms.Form):
    idEvento = forms.IntegerField()
    equipa = forms.IntegerField(required=False)
    atleta1 = forms.IntegerField(required=False)
    atleta2 = forms.IntegerField(required=False)
    zonaC = forms.CharField(max_length=5, required=False)
    zonaB = forms.CharField(max_length=5, required=False)
    instante = forms.TimeField()
    novoinst = forms.TimeField(required=False)