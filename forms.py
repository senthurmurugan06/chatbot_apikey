from django import forms

class ChatForm(forms.Form):
    text = forms.CharField(required=False, widget=forms.Textarea(attrs={'placeholder': 'Type your message here...'}))
    image = forms.ImageField(required=False)