from django.db import models


class Project(models.Model):
    name = models.CharField('Name', max_length=64, blank=True)
    user = models.ForeignKey('users.User', on_delete=models.SET_NULL, verbose_name='User',
                             related_name='projects', null=True)

    def __str__(self):
        return self.name


class Page(models.Model):
    project = models.ForeignKey('Project', on_delete=models.CASCADE, verbose_name='Project',
                                related_name='pages')
    json = models.JSONField('JSON', null=True, default=None)
    template = models.JSONField('Template', null=True, default=None)

    def __str__(self):
        return str(self.id)


class Product(models.Model):
    name = models.CharField('Name', max_length=64, blank=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='Project',
                                related_name='products')

    def __str__(self):
        return self.name
