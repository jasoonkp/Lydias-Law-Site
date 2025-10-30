from django.db import models

class WebsiteContent(models.Model):
    versionNumber = models.AutoField(primary_key=True)
    frontPageHeader = models.CharField(max_length=140, blank=True)
    frontPageDescription = models.TextField(blank=True)

    stepParentAdoptionDescription = models.TextField(blank=True)
    adultAdoptionDescription = models.TextField(blank=True)
    guardianshipDescription = models.TextField(blank=True)
    guardianshipToAdoptionDescription = models.TextField(blank=True)
    independentAdoptionDescription = models.TextField(blank=True)

    nameTitle = models.CharField(max_length=120, blank=True)
    aboutMeDescription = models.TextField(blank=True) 
    officeLocation = models.CharField(max_length=200, blank=True)

    footerDescription = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
         return f"Website content version {self.versionNumber}"
