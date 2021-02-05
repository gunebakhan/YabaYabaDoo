from .models import Comment
from django import forms
from django.utils.translation import ugettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from crispy_forms.layout import Layout, Field, Fieldset, ButtonHolder, Submit
from crispy_forms.bootstrap import InlineRadios

class CommentForm(forms.ModelForm):
    # CHOICES = (
    #     (0, 'صفر'),
    #     (1, 'یک'),
    #     (2, 'دو'),
    #     (3, 'سه'),
    #     (4, 'چهار'),
    #     (5, 'پنج')
    # )
    # rate = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    class Meta:
        model = Comment
        fields = ['title', 'body', 'rate']
        widgets = {
            'body': forms.Textarea(attrs={'rows': 10, 'style': 'resize:none;', 'placeholder': 'نظر خود را بنویسید'}),
        }
    
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['placeholder'] = 'عنوان نظر'
        self.helper = FormHelper(self)

