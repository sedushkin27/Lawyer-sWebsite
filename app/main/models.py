from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from ckeditor.fields import RichTextField


# Create your models here.
class Review(models.Model):

    name = models.CharField(("Ім'я та призвіще"), max_length=50)
    stars = models.DecimalField(
        ("Оцінка"), 
        max_digits=7, 
        decimal_places=2, 
        default=0.00,
        validators=[
            MinValueValidator(1.00, message="Оцінка повинна бути не менше 1.00"),
            MaxValueValidator(5.00, message="Оцінка повинна бути не більше 5.00"),
            ]
        )
    text = models.TextField(("Текст"))

    class Meta:
        db_table = ("review")
        verbose_name = ("коментар")
        verbose_name_plural = ("Коментарі")

    def __str__(self):
        return f"Відгук від {self.name} з оцінкою {self.stars}"

    # def get_absolute_url(self):
    #     return reverse("review_detail", kwargs={"pk": self.pk})

class PrivacyPolicy(models.Model):
    title = models.CharField("Название", max_length=255, default="Політика конфіденційності")
    content = RichTextField("Содержимое", blank=True, null=True)
    file = models.FileField("Файл (.docx или .txt)", upload_to="privacy_policies/", blank=True, null=True)
    updated_at = models.DateTimeField("Дата обновления", auto_now=True)

    class Meta:
        db_table = "privacy_policy"
        verbose_name = "политику конфиденциальности"
        verbose_name_plural = "Политики конфиденциальности"

    def __str__(self):
        return self.title