from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.mail import send_mail

from .models import Post, Comment

from allauth.account.forms import SignupForm
import secrets

class ConfirmSignupForm(SignupForm):

    def save(self, request):
        user = super().save(request)
        user.is_active = False
        code = secrets.token_urlsafe()[:10]
        user.code = code
        user.save()

        send_mail(
            subject= 'Активация аккаунта',
            message= f'Активируйте свой аккаунт по коду:{code}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list= [user.email],
        )

        return user

class PostForm(forms.ModelForm):

    class Meta:
       model = Post
       fields = ['title', 'content', 'category']

    def clean(self):
        cleaned_data = super().clean()
        content = cleaned_data.get("content")
        title = cleaned_data.get("title")
        if title == content:
            raise ValidationError(
                "Описание не должно быть идентично названию."
            )
        return cleaned_data

class CommentForm(forms.ModelForm):
    class Meta:
       model = Comment
       fields = ['content']
       widgets = {
           'content': forms.Textarea(attrs={'class': 'form-text', 'cols': 40, 'rows': 1}),
       }