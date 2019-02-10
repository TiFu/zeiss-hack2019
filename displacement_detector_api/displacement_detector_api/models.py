import cv2
import datetime

from django.contrib.postgres.fields import ArrayField
from django.db import models
from PIL import Image

from displacement_detector_api import settings
from displacement_detector_api.image_processing.image_processing import ImageProcessing
from displacement_detector_api.image_processing.position_change import calculate_position_change


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

    rotation_val_left = models.DecimalField(blank=True, null=True, max_digits=12, decimal_places=4)
    rotation_val_right = models.DecimalField(blank=True, null=True, max_digits=12, decimal_places=4)
    translation_val_left_x = models.DecimalField(blank=True, null=True, max_digits=12, decimal_places=4)
    translation_val_left_y = models.DecimalField(blank=True, null=True, max_digits=12, decimal_places=4)
    translation_val_right_x = models.DecimalField(blank=True, null=True, max_digits=12, decimal_places=4)
    translation_val_right_y = models.DecimalField(blank=True, null=True, max_digits=12, decimal_places=4)

    date_before = models.DateTimeField(null=True, blank=True)
    date_after = models.DateTimeField(null=True, blank=True)

    overlay_left = models.CharField(null=True, blank=True, max_length=256)
    overlay_right = models.CharField(null=True, blank=True, max_length=256)

    DEFECT_CHOICES = (
        ('none', 'none'),
        ('surface', 'surface'),
        ('position', 'position')
    )

    in_spec = models.NullBooleanField(blank=True, null=True)
    defect = models.CharField(choices=DEFECT_CHOICES, blank=True, null=True, max_length=32)
    quality = models.DecimalField(blank=True, null=True, decimal_places=4, max_digits=12)
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

        self.in_spec=quality_score<=0
        self.defect='position'
        self.quality=quality_score
        self.rotation_val_left=displ_left[0]
        self.rotation_val_right=displ_right[0]
        self.translation_val_left_x=displ_left[1][0]
        self.translation_val_left_y=displ_left[1][1]
        self.translation_val_right_x=displ_right[1][0]
        self.translation_val_right_y=displ_right[1][1]

        save_image_as_png(self.picture_left_before.file.file.name, self.picture_left_before.path)
        save_image_as_png(self.picture_right_before.file.file.name, self.picture_right_before.path)
        save_image_as_png(self.picture_left_after.file.file.name, self.picture_left_after.path)
        save_image_as_png(self.picture_right_after.file.file.name, self.picture_right_after.path)

        self.overlay_left = save_npy_as_img(overlay_left, './media/media/' + self.picture_left_before.name.split('_')[0] + '_overlay_left.png' )
        self.overlay_right = save_npy_as_img(overlay_right, './media/media/' + self.picture_left_before.name.split('_')[0] + '_overlay_right.png' )

        self.overlay_left = 'http://localhost:8765/media/media/' + self.picture_left_before.name.split('_')[0] + '_overlay_left.png'
        self.overlay_right = 'http://localhost:8765/media/media/'+ self.picture_left_before.name.split('_')[0] + '_overlay_right.png'


        self.picture_right_after.url.replace('tif', 'png')

        return self

def save_image_as_png(path, path_out):
    im = Image.open(path)
    im.mode = 'I'
    im.point(lambda i:i*(1./256)).convert('L').save(path_out.replace('tif', 'png').replace('media', 'media/media'))

def save_npy_as_img(array, path):
    im = Image.fromarray(array)
    im.save(path)
    return path

