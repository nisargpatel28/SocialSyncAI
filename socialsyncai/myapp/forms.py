from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)

    def send_email(self):
        print(
            f"Sending email with message: {self.cleaned_data['message']}")
