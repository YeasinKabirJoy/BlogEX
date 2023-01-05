from django.forms import ModelForm
from django import forms
from .models import Blog,Review


class BlogForm(ModelForm):
    required_css_class = 'required'

    class Meta:
        model = Blog
        fields = ['title','image','file','description',]

        # widgets = {
        #     'tags': forms.CheckboxSelectMultiple(),
        # }
        #
    def __init__(self,*args,**kwargs):
        super(BlogForm, self).__init__(*args,**kwargs)
        for label,field in self.fields.items():
            field.widget.attrs.update({"class":"input input--text"})

        # self.fields['title'].widget.attrs.update({"class":"input input--text","placeholder":"Give a Title"})
        # self.fields['title'].widget.attrs['required'] = 'required'
        # self.fields['description'].widget.attrs.update({"class":"input input--text"})
        # self.fields['title'].widget.attrs['class']= "input input--text"
        # self.fields['description'].widget.attrs['class']= "input input--text"


class ReviewForm(ModelForm):
    required_css_class = 'required'

    class Meta:
        model = Review
        fields = ['vote', 'review_text']
        labels = {
            'vote':'Place You Vote',
            'review_text': 'Add a Comment With Your Vote'
        }

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)

        for label, field in self.fields.items():
            field.widget.attrs.update({"class": "input"})