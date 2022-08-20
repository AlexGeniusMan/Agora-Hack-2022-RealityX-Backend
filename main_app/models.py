from django.db import models


class Page(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='User',
                             related_name='pages', default=None, null=True)
    json = models.JSONField('JSON', null=True, default=None)
    template = models.JSONField('Template', null=True, default=None)

    def __str__(self):
        return str(self.id)


class Product(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='User',
                             related_name='products', default=None, null=True)
    name = models.CharField('Name', max_length=64, blank=False)
    image = models.ImageField('Image', upload_to='media/products', blank=True)

    def __str__(self):
        return self.name
