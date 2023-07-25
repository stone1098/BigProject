from django import forms
from post.models import Question, Answer


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'image', 'content']
        labels = {
            'title': 'Title',
            'image': 'Image Upload',
            'content': 'Content',
        }
        
class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        labels = {
            'content': '답변내용',
        }