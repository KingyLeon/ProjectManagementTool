from django.db import models
from django.template.defaultfilters import slugify
from django.core.validators import MaxValueValidator, RegexValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# Validators
def divisible_by_five(value):
    if value % 5 != 0:
        raise ValidationError(f'{value} is not divisble by 5')

# Create your models here.


class Project(models.Model):
    title = models.CharField(unique=True, max_length=64)
    description = models.TextField(max_length=256, blank=True, null=True)
    imageField = models.ImageField(upload_to="media", blank=True, null=True)
    slugField = models.SlugField(null=False, unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

class Board(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(blank=False, max_length=64)

    class Meta():
        unique_together = ("project", "title")


class List(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, null=False)
    title = models.CharField(max_length=64)
    position = models.PositiveIntegerField()  

    class Meta:
        unique_together = ("board", "title")

class Label(models.Model):
    title = models.CharField(blank=False, max_length=32)
    colour = models.CharField(blank=False, max_length=7,
                              validators=[RegexValidator(r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$')])
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("title", "project")

class Task(models.Model):
    class Priority(models.TextChoices):
        HIGH = 'H', _('High')
        MEDIUM = 'M', _('Medium')
        LOW = 'L', _('Low')

    def validate_story_points(value):
        if value % 5 != 0 or value > 100:
            raise ValidationError(
                _('%(value)s is not a valid story point value'),
                params={'value': value})

    task_no = models.AutoField(primary_key=True)

    list = models.ForeignKey(List, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=512, blank=True, null=True)
    priority = models.CharField(max_length=1, choices=Priority)
    story_points = models.PositiveIntegerField(
        validators=[validate_story_points])
    labels = models.ManyToManyField('Label')