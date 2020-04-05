from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from .models import Custom_User_Model

class customuserform(UserCreationForm):
    class Meta:
        model = Custom_User_Model
        fields = {'username','password1','password2'}


