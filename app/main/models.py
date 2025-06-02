from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


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
