from django import forms
from libapp.models import Suggestion, Libuser,User


class SuggestionForm(forms.ModelForm):
    class Meta:
        model= Suggestion
        fields=['title','pubyr','type','cost','comments']
    choice = [('2','Dvd'),('1','Book')]
    title = forms.CharField(label='Title',max_length=100)
    pubyr = forms.IntegerField(label='Publication Year')
    type = forms.ChoiceField(label='Type',choices = choice,widget=forms.RadioSelect)
    cost = forms.IntegerField(label='Estimated Cost in Dollars')
    comments = forms.CharField(label='Comments')

class SearchlibForm(forms.Form):


    class Meta:
        fields = ['title','author']
    title = forms.CharField(label='Title',max_length=100)
    author = forms.CharField(label='Author')

class newuserForm(forms.ModelForm):
    class Meta:

        model = Libuser
        fields = ['username','first_name','last_name','email','password','address', 'city', 'province', 'phone', 'postalcode']

    PROVINCE_CHOICES = (
            ('AB', 'Alberta'),
            ('MB', 'Manitoba'),
            ('ON', 'Ontario'),
            ('QC', 'Quebec'),
        )

    address = forms.CharField(label='Address')
    city = forms.CharField(label='City')
    province = forms.ChoiceField(label='Province', choices = PROVINCE_CHOICES)
    phone = forms.IntegerField(label='Phone')
    postalcode = forms.CharField(label='Postal Code')

