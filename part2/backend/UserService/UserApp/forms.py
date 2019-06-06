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