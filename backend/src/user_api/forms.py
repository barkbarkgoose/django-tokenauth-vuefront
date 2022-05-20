from django import forms

from user_api.models import Appointment

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ('title', 'date', 'time', 'notes')