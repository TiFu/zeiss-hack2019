import cv2
import datetime

from django.db import models

from displacement_detector_api.image_processing.image_processing import ImageProcessing


class EvaluationResult(models.Model):

    DEFECT_CHOICES = (
        ('none', 'none'),
        ('surface', 'surface'),
        ('position', 'position')
    )

    in_spec = models.NullBooleanField(blank=True, null=True)
    defect = models.CharField(choices=DEFECT_CHOICES, blank=True, null=True, max_length=32)
    quality = models.DecimalField(blank=True, null=True, decimal_places=4, max_digits=12)

    top_corner_left = models.CharField(blank=True, null=True, max_length=32)
    top_corner_right = models.CharField(blank=True, null=True, max_length=32)
    bot_corner_left = models.CharField(blank=True, null=True, max_length=32)
    bot_corner_right = models.CharField(blank=True, null=True, max_length=32)
    rotation_val = models.DecimalField(blank=True, null=True, decimal_places=4, max_digits=12)


class AnalysisImage(models.Model):
    picture_id = models.CharField(max_length=64, blank=True, null=True)

    picture_left_before = models.ImageField(upload_to='media/', null=True)
    picture_right_before = models.ImageField(upload_to='media/', null=True)
    picture_left_after = models.ImageField(upload_to='media/', null=True)
    picture_right_after = models.ImageField(upload_to='media/', null=True)

    date_before = models.DateTimeField(null=True, blank=True)
    date_after = models.DateTimeField(null=True, blank=True)

    DEFECT_CHOICES = (
        ('none', 'none'),
        ('surface', 'surface'),
        ('position', 'position')
    )

    in_spec = models.NullBooleanField(blank=True, null=True)
    defect = models.CharField(choices=DEFECT_CHOICES, blank=True, null=True, max_length=32)
    quality = models.DecimalField(blank=True, null=True, decimal_places=4, max_digits=12)

    top_corner_left = models.CharField(blank=True, null=True, max_length=32)
    top_corner_right = models.CharField(blank=True, null=True, max_length=32)
    bot_corner_left = models.CharField(blank=True, null=True, max_length=32)
    bot_corner_right = models.CharField(blank=True, null=True, max_length=32)
    rotation_val = models.DecimalField(blank=True, null=True, decimal_places=4, max_digits=12)

    def save(self, *args, **kwargs):
        # set values for new instance
        if not self.id:
            print(self.picture_left_before)
            self.evaluate_pictures()

            self.picture_id = self.picture_left_before.name.split('_')[0]
            self.date_before = datetime.datetime.strptime(self.picture_left_before.name.split('_')[1], "%Y%m%d-%H%M%S")
            self.date_after = datetime.datetime.strptime(self.picture_left_after.name.split('_')[1], "%Y%m%d-%H%M%S")

        return super(AnalysisImage, self).save(*args, **kwargs)

    def evaluate_pictures(self):
        # TODO create evaluation
        image_processing = ImageProcessing()
        plb=cv2.imread(self.picture_left_before.file.file.name)
        pla=cv2.imread(self.picture_left_after.file.file.name)
        prb=cv2.imread(self.picture_right_before.file.file.name)
        pra=cv2.imread(self.picture_right_after.file.file.name)

        displ_left, displ_right, overlay_left, overlay_right, quality_score =image_processing.determineDisplacement(plb, prb, pla, pra)

        self.in_spec=True
        self.defect='surface'
        self.quality=quality_score
        self.top_corner_left='(2,3)'
        self.top_corner_right='(2,4)'
        self.bot_corner_left='(0,3)'
        self.bot_corner_right='(0,7)'
        self.rotation_val=displ_left[0]

        return self




