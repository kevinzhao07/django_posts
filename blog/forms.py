from django import forms
from .models import Comment, Message, Todo

# each model requires a form (if needed) and a class Meta, which
# specifies the model and fields that will be displayed
# (forms don't always need to be specified (can be manually made))
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['message']

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['due_date', 'todo']
