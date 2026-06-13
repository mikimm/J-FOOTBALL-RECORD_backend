from django import forms
from django.contrib.auth.forms import UserCreationForm
from jfootball_record.model_definition.users_models import Users

class SignUpForm(UserCreationForm):

    GENDER_CHOICE={
        1:"男性",
        2:"女性"
    }

    gender=forms.ChoiceField(label="性別", choices=GENDER_CHOICE)

    class Meta:
        model = Users
        fields = ["username", "email", "password1", "password2", "gender"]