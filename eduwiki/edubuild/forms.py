from django import forms
from eduprototype.models import Review, PrereqFeedback, DistractorFeedback

class ReviewForm(forms.Form):
    class Meta:
        model = Review

class PrereqForm(forms.Form):
    class Meta:
        model = PrereqFeedback

class DistractorForm(forms.Form):
    class Meta:
        model = DistractorFeedback