from django.db import models


class Banner(models.Model):
    name = models.CharField(blank=True, null=True, max_length=255)
    image = models.ImageField(blank=True, null=True, upload_to="image_banner/")

    class Meta:
        verbose_name = "Banner"
        verbose_name_plural = "Banners"

    def __str__(self):
        return self.name


class ContentTranslate(models.Model):
    lang = models.CharField(blank=True, null=True, max_length=255)
    tag_data = models.TextField(blank=True, null=True)
    tag_value = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Content Translate"
        verbose_name_plural = "Content Translate"

    def __str__(self):
        return self.tag_data or "-"


class Pengumuman(models.Model):
    text_pengumuman = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Pengumuman Website"
        verbose_name_plural = "Pengumuman Website"

    def __str__(self):
        return self.text_pengumuman


class Page(models.Model):
    COICHE_PAGE = [
        (1, "Aggrement"),
        (2, "Privacy and Policy"),
    ]
    page_for = models.IntegerField(choices=COICHE_PAGE, default=1, unique=True)
    content = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Page"
        verbose_name_plural = "Page"
    
    def __str__(self):
        return self.COICHE_PAGE
