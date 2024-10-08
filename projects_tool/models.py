from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, ValidationError, RegexValidator


# Validators
def divisible_by_five(value):
    if value % 5 != 0:
        raise ValidationError(f'{value} is not divisble by 5')

# Create your models here.


class Project(models.Model):
    title = models.CharField(blank=False, unique=True, max_length=64)
    description = models.CharField(max_length=256, blank=True)
    imageField = models.ImageField(upload_to="media/", blank=True)
    slugField = models.SlugField(null=False, blank=True)

    def save(self, *args, **kwargs):
        if not self.slugField:
            self.slugField = self.title.lower().replace(' ', '-')
        super(Project, self).save(*args, **kwargs)


class Board(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(blank=False, max_length=64)

    class Meta():
        unique_together = ("project", "title")


class List(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, null=False)
    title = models.CharField(blank=False, null=False, max_length=64)
    position = models.IntegerField(validators=[MinValueValidator(0)])

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
    class Priorities(models.TextChoices):
        HIGH = 'HIGH', 'High'
        MEDIUM = 'MEDIUM', 'Medium'
        LOW = 'LOW', 'Low'

    task_no = models.IntegerField(primary_key=True)
    list = models.ForeignKey(List, on_delete=models.CASCADE)
    title = models.CharField(blank=False, max_length=64)
    description = models.CharField(max_length=512, blank=True)

    priority = models.CharField(
        choices=Priorities.choices, default=Priorities.MEDIUM, max_length=6)

    story_points = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100), divisible_by_five])
    labels = models.ManyToManyField(Label)
