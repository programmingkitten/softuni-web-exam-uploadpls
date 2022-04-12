from django import forms
from django.forms import ModelForm

from pyla.manage_profiles.models import Profile, ContactUs
from pyla.user_activity.models import FeedbackReply


class ProfileForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['profile_picture'].label = ""
        self.fields['profile_picture'].text_field = ""
        self.fields['description'].widget.attrs.update({'placeholder': 'Enter your description'})
        self.fields['moto'].widget.attrs.update({'placeholder': 'Enter your moto'})

    class Meta:
        model = Profile
        fields = ("profile_picture", 'description', 'moto')
        widgets = {
            'profile_picture': forms.FileInput(),

        }


class CreateFeedbackForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.fields['description'].widget.attrs.update(
            {
                'placeholder': 'Describe your problem'
            }
        )

        self.fields['title'].widget.attrs.update(
            {
                'placeholder': 'Very short description of your problem (title)'
            }
        )

        self.fields['video'].widget.attrs.update(
            {
                'placeholder': 'Link to a video that describes your question/problem in detail (Best to be on YouTube)'
            }
        )

        for field in self.fields:
            self.fields[f'{field}'].label = ""

    def save(self, commit=True):
        # commit false does not persist to database
        # just returns the object to be created
        feedback = super().save(commit=False)

        feedback.user = self.user
        if commit:
            feedback.save()

        return feedback

    class Meta:
        model = ContactUs
        fields = ('title', 'description', 'image', 'video')
        # widgets = {
        #     'description': forms.TextInput(
        #         attrs={
        #             'placeholder': 'Enter pet name',
        #         }
        #     ),
        # }


class ReplyToFeedbackForm(forms.ModelForm):
    def __init__(self, user, feedback, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.feedback = feedback
        self.fields['description'].widget.attrs.update(
            {
                'placeholder': 'Describe your a solution to the problem'
            }
        )

        self.fields['title'].widget.attrs.update(
            {
                'placeholder': 'Very short introduction to solution'
            }
        )

        for field in self.fields:
            self.fields[f'{field}'].label = ""

    def save(self, commit=True):
        # commit false does not persist to database
        # just returns the object to be created
        feedback_reply = super().save(commit=False)

        feedback_reply.user = self.user
        feedback_reply.feedback = self.feedback
        if commit:
            feedback_reply.save()

        return feedback_reply

    class Meta:
        model = FeedbackReply
        fields = ('title', 'description')
        # widgets = {
        #     'description': forms.TextInput(
        #         attrs={
        #             'placeholder': 'Enter pet name',
        #         }
        #     ),
        # }
