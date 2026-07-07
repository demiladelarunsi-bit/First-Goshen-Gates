from django import forms
from .models import StudentResult

class StudentResultForm(forms.ModelForm):
    class Meta:
        model = StudentResult
        fields = ['exam_number', 'student_name', 'year', 'term', 'subject', 'score', 'grade', 'remarks']
        widgets = {
            'year': forms.TextInput(attrs={'placeholder': 'e.g. 2024'}),
        }