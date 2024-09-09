from django import forms
from .import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class Online_Booking_form(forms.ModelForm):
    class Meta:
        model = models.Online_Booking
        fields = "__all__"

class offline_Booking_form(forms.ModelForm):
    class Meta:
        model = models.Offline_Booking
        fields = "__all__"
class Add_Employee_form(forms.ModelForm):
    class Meta:
        model = models.Add_Employee
        fields = "__all__"

class Add_Room_form(forms.ModelForm):
    class Meta:
        model = models.Add_Room
        fields = "__all__"

class Add_salary_form(forms.ModelForm):
    class Meta:
        model = models.Add_Salarys
        fields = "__all__"


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
