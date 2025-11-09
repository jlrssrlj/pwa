from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email','username','password1','password2') 
        
    def save(self, commit = True):
        user = super(RegistrationForm,self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.is_staff = True
        
        if commit:
            user.save()
        return user