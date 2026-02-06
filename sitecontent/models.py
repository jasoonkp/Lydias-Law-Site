from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

class WebsiteContent(models.Model):
    versionNumber = models.AutoField(primary_key=True)
    frontPageHeader = models.CharField(max_length=140, blank=True)
    frontPageDescription = CKEditor5Field(blank=True, config_name='default')

    stepParentAdoptionDescription = CKEditor5Field(blank=True, config_name='default')
    adultAdoptionDescription = CKEditor5Field(blank=True, config_name='default')
    guardianshipDescription = CKEditor5Field(blank=True, config_name='default')
    guardianshipToAdoptionDescription = CKEditor5Field(blank=True, config_name='default')
    independentAdoptionDescription = CKEditor5Field(blank=True, config_name='default')

    nameTitle = models.CharField(max_length=120, blank=True)
    aboutMeDescription = CKEditor5Field(blank=True, config_name='default') 
    officeLocation = models.CharField(max_length=200, blank=True)

    footerDescription = CKEditor5Field(blank=True, config_name='default')

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
         return f"Website content version {self.versionNumber}"
