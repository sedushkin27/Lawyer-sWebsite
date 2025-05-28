from django.db import models

# Create your models here.
class Services(models.Model):

    title = models.CharField(("Назва"), max_length=50, unique=True)
    slug = models.SlugField(('Url'), unique=True, blank=True, null=True)
    image = models.ImageField(("Зображення"), upload_to='services/service_images', blank=True, null=True)
    price = models.DecimalField(("Ціна"), max_digits=7, decimal_places=2, default=0.00)
    description = models.TextField(("Опис"), blank=True, null=True)

    class Meta:
        db_table = 'service'
        verbose_name = ("послугу")
        verbose_name_plural = ("Послуги")

    def __str__(self):
        return self.title

    # def get_absolute_url(self):
    #     return reverse("Services_detail", kwargs={"pk": self.slug})

class ServiceSection (models.Model):

    service = models.ForeignKey(Services, related_name=('sections'), verbose_name=("До якої послуги відноситися"), on_delete=models.CASCADE)
    title = models.CharField(("Заголовок блоку"), max_length=50, unique=True)

    class Meta:
        db_table = 'serviceSection'
        verbose_name = "блок з інформацією"
        verbose_name_plural = "Блоки з інформацією"

    def __str__(self):
        return self.title

class SectionItem(models.Model):
    section = models.ForeignKey(ServiceSection, on_delete=models.CASCADE, verbose_name=("До якої блоку відноситися"), related_name=('items'))
    text = models.TextField("Елемент списку")

    class Meta:
        db_table = 'sectionItem'
        verbose_name = "пункт в блок"
        verbose_name_plural = "Пункти в блоці"

    def __str__(self):
        return self.text