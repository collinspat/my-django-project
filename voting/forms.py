from django import forms
from django.forms import ModelForm
from .models import Voter, Position, Candidate

class VoterForm(ModelForm):
    class Meta:
        model = Voter
        fields = ['admin', 'phone', 'otp', 'verified', 'voted', 'otp_sent']

class PositionForm(ModelForm):
    class Meta:
        model = Position
        fields = ['name', 'max_vote', 'priority']

class CandidateForm(ModelForm):
    class Meta:
        model = Candidate
        fields = ['fullname', 'photo', 'bio', 'position']