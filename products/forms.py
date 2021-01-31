from .models import Comment
from django import forms
from django.utils.translation import ugettext_lazy as _
from crispy_forms.helper import FormHelper


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['title', 'body']
    
        widgets = {
            'body': forms.Textarea(attrs={'rows': 10, 'style': 'resize:none;', 'placeholder': 'نظر خود را بنویسید'}),
        }
    
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['placeholder'] = 'عنوان نظر'
        self.helper = FormHelper(self)
        self.helper.form_show_labels = False
