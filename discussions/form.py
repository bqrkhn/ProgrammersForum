from django import forms
from .models import Question, Answer


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('title', 'description', )

    title = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'id': 'my_field',
                                                                          'class': 'form-control',
                                                                          'placeholder': 'Question Title'}))
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Question Description'}))


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('description', )

    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Answer'}))
