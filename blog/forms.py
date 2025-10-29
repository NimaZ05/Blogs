from django import forms
from .models import Post, Category, Tag


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'category', 'tags', 'status', 'published_date', 'image')
        widgets = {
            'published_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'content': forms.Textarea(attrs={'rows': 15}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
        if 'status' in self.fields:
            self.fields['status'].widget.attrs.update({'class': 'select-pill'})
        if 'category' in self.fields:
            self.fields['category'].widget.attrs.update({'class': 'select-pill'})





