import os
from autoslug import AutoSlugField
from autoslug.settings import slugify
from django.db import models
from django.urls import reverse

# Create your models here.
def get_path(instance, filename):
    ext = filename.split('.')[-1]
    return os.path.normcase(
        os.path.join(
            'uploads',
            slugify(instance.name[:60]) + '.' + ext))


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(u'Breve Descrição do Produto', max_length=115, blank=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'id': self.id})


class Product(models.Model):
    name = models.CharField(u'Nome do Produto', max_length=20)
    description = models.CharField(u'Breve Descrição do Produto', max_length=115, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Categorias')
    price = models.DecimalField(u'Preço', decimal_places=2, max_digits=6)
    photo = models.ImageField(u'Foto do produto', default='produtos/sem-img.png', blank=True, upload_to=get_path)
    slug = AutoSlugField(u'Slug', populate_from='name', unique=True, max_length=100)

    class Meta:
        verbose_name = u'Produto'
        verbose_name_plural = u'Produtos'
        ordering = ['-name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})
