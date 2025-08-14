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

class LegalDocument(models.Model):
    DOCUMENT_TYPE_CHOICES = (
        ('privacy_policy', 'Політика конфіденційності'),
        ('public_offer', 'Публична оферта'),
    )
    document_type = models.CharField(
        "Тип документа",
        max_length=20,
        choices=DOCUMENT_TYPE_CHOICES,
        default='privacy_policy'
    )
    content = RichTextField("Содержимое", blank=True, null=True)
    file = models.FileField("Файл (.docx или .txt)", upload_to="privacy_policies/", blank=True, null=True)
    updated_at = models.DateTimeField("Дата обновления", auto_now=True)

    class Meta:
        db_table = "legal_document"
        verbose_name = "Документ"
        verbose_name_plural = "Документы"

    def __str__(self):
        return self.get_document_type_display()

class AboutMe(models.Model):
    name = models.CharField("ім'я", max_length=100)
    sername = models.CharField("прізвище", max_length=100, blank=True, null=True)

    phone = models.CharField("Телефон", max_length=20, blank=True, null=True)
    email = models.EmailField("Електронна пошта", blank=True, null=True)
    address = models.CharField("Адреса офісу", max_length=255, blank=True, null=True)

    viber = models.CharField("viber", max_length=100, blank=True, null=True)
    messenger = models.CharField("messenger", max_length=100, blank=True, null=True)
    telegram = models.CharField("telegram", max_length=100, blank=True, null=True)
    whatsapp = models.CharField("whatsapp", max_length=100, blank=True, null=True)
    
    facebook = models.CharField("facebook", max_length=100, blank=True, null=True)
    instagram = models.CharField("instagram", max_length=100, blank=True, null=True)
    tiktok = models.CharField("tiktok", max_length=100, blank=True, null=True)

    years_of_experience = models.PositiveIntegerField("роки досвіду", blank=True, null=True)
    winning_cases_count = models.PositiveIntegerField("Кількість виграних справ", blank=True, null=True)
    client_count = models.PositiveIntegerField("кількість клієнтів", blank=True, null=True)
    
    first_photo = models.ImageField("фото на головній сторінці", upload_to="about_me", blank=True, null=True)
    second_photo = models.ImageField("друга фотографія на сторінці \"Про мене\"", upload_to="about_me", blank=True, null=True)
    third_photo = models.ImageField("третя фотографія в контактний блок на головній сторінці", upload_to="about_me", blank=True, null=True)
    
    main_about_me_text = RichTextField("Короткий опис про мене на головній сторінці", blank=True, null=True)
    other_about_me_text = RichTextField("Детальний опис про мене на сторінці \"Про мене\"", blank=True, null=True)

    class Meta:
        db_table = "about_me"
        verbose_name = "о себе"
        verbose_name_plural = "О себе"

    def __str__(self):
        return "О себе"
    
class AdvantagesWorkingWithMe(models.Model):

    title = models.CharField("Заголовок", max_length=100)
    text = models.TextField("Текст")
    about_me = models.ForeignKey(AboutMe, on_delete=models.CASCADE, related_name='advantages', verbose_name="Кому относится")
    
    class Meta:
        db_table = "Advantages_working_with_me"
        verbose_name = ("Переваги роботи зі мною")
        verbose_name_plural = ("Переваги роботи зі мною")

    def __str__(self):
        return self.title