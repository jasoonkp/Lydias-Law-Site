# forms.py holds the form classes for data input

from django import forms
from sitecontent.models import WebsiteContent


class WebsiteContentForm(forms.ModelForm):
    """
    Form for editing website content in the admin editor.
    CKEditor5 widgets are provided automatically by the CKEditor5Field on the model.
    Regina is my goat, the ckeditor version i was using was SO MUCH MORE WORK
    """

    class Meta:
        model = WebsiteContent
        fields = [
            # home Page
            'frontPageHeader',
            'frontPageDescription',
            # about Page
            'nameTitle',
            'aboutMeDescription',
            'officeLocation',
            # practice Areas
            'stepParentAdoptionDescription',
            'adultAdoptionDescription',
            'guardianshipDescription',
            'guardianshipToAdoptionDescription',
            'independentAdoptionDescription',
            # footer
            'footerDescription',
        ]
        widgets = {
            # CharFields - plain text inputs (CKEditor5 fields get their widget from the model)
            'frontPageHeader': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': '140',
                'placeholder': 'Enter homepage header text'
            }),
            'nameTitle': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': '120',
                'placeholder': 'Enter name/title'
            }),
            'officeLocation': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': '200',
                'placeholder': 'Enter office location'
            }),
        }
        labels = {
            'frontPageHeader': 'Homepage Header',
            'frontPageDescription': 'Homepage Description',
            'nameTitle': 'Name/Title',
            'aboutMeDescription': 'About Me Description',
            'officeLocation': 'Office Location',
            'stepParentAdoptionDescription': 'Step-Parent Adoption',
            'adultAdoptionDescription': 'Adult Adoption',
            'guardianshipDescription': 'Guardianship',
            'guardianshipToAdoptionDescription': 'Guardianship to Adoption',
            'independentAdoptionDescription': 'Independent Adoption',
            'footerDescription': 'Footer Description',
        }
        help_texts = {
            'frontPageHeader': 'Displayed as the main headline on the homepage (max 140 characters)',
            'frontPageDescription': 'Displayed in the green banner below the hero image',
            'officeLocation': 'Address displayed on the Contact page',
            'footerDescription': 'Displayed in the website footer across all pages',
        }
