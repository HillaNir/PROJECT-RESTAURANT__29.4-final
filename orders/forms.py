from django import forms # מייבא לנו טפסים של גאנגו
from django.contrib.auth.forms import UserCreationForm, UserChangeForm # מייבא לנו טופס חכם של יוזר
from .models import User # מייבאים את מודל יוזר

#  נרחיב את הטופס המובנה של יוזר ביצירת טופס חדש
class NewUserCreationForm(UserCreationForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.CharField()
# הקלאס המקונן הזה נותן לנו עוד יכולות שקשורות לטופס/למודל. במקרה הזה הוספת שדות לתוך מודל יוזר
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email')


class EditUserForm(UserChangeForm):
    password = None
    class Meta(UserChangeForm.Meta):
        fields = ('username', 'first_name', 'last_name', 'email')