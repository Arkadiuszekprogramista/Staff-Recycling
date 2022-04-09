import django.forms as forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from clothesresourcing_app.models import Category, Institution

def validation_email(value):
    if User.objects.filter(username=value):
        raise ValidationError('Ten logi/email jest już zajęty')


class RegisterUserForm(forms.Form):
    password1 = forms.CharField(max_length=128, widget=forms.PasswordInput(attrs={'placeholder': 'Hasło'}), required=True)
    password2 = forms.CharField(max_length=128, widget=forms.PasswordInput(attrs={'placeholder': 'Powtórz hasło'}), required=True)
    email = forms.EmailField(validators=[validation_email], required=True, widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    name = forms.CharField(max_length=128, required=True, widget=forms.TextInput(attrs={'placeholder': 'Imię'}))
    surname = forms.CharField(max_length=128, required=True, widget=forms.TextInput(attrs={'placeholder': 'Nazwisko'}))

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data['password1']
        password2 = cleaned_data['password2']
        if password1 != password2:
            raise ValidationError('Passwords are different')
        return cleaned_data


class LoginForm(forms.Form):
    username = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(max_length=128, widget=forms.PasswordInput(attrs={'placeholder': 'Hasło'}))


class AddDonationForm(forms.Form):
    categories = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), widget=forms.CheckboxSelectMultiple,
                                                required=False)
    quantity = forms.IntegerField(min_value=1)
    institution = forms.ModelMultipleChoiceField(queryset=Institution.objects.all())
    street = forms.CharField(max_length=128)
    city = forms.CharField(max_length=128)
    post = forms.CharField(max_length=32)
    phone = forms.CharField(max_length=32)
    data = forms.DateField(widget=forms.DateTimeInput(attrs={'type': 'date'}))
    time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    comments = forms.CharField(widget=forms.Textarea, initial='Brak uwag')


class PickUpForm(forms.Form):
    is_taken = forms.BooleanField(widget=forms.CheckboxInput, required=False, initial=False)


class ContactForm(forms.Form):
    name = forms.CharField(max_length=32, widget=forms.TextInput(attrs={'placeholder': 'Imię'}) )
    surname = forms.CharField(max_length=32, widget=forms.TextInput(attrs={'placeholder': 'Nazwisko'}))
    massage = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Wiadomość', 'rows': 1}))


class MyUserCreation(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        fields = ('username', 'first_name', 'last_name')