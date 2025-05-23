from django.forms import ModelForm
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.
class ComicBookManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by('title', 'issue_number')


class comicbooks(models.Model):
    title = models.CharField(max_length=150)
    issue_number = models.PositiveIntegerField()
    grade = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)],
    )
    significance = models.TextField(blank=True, help_text="Significance of issue")
    writer_name = models.CharField(max_length=150)
    artist_name = models.CharField(max_length=150)
    publisher = models.CharField(max_length=75)
    cover_image = models.ImageField(upload_to='comic_covers/', blank=True, null=True)
    class Meta:
        ordering = ['title', 'issue_number']

    objects = ComicBookManager()

def __str__(self):
     return f"{self.title} #{self.issue_number}"

