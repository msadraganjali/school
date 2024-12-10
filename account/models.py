from django.db import models
from django.urls import reverse
from django.utils import timezone
from extensions.utils import jalali_converter
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    
    # email = models.EmailField(default="test@test.com" ,verbose_name="آدرس ایمیل", null=True, blank=True)
    phone = models.CharField(max_length=11, unique=True, verbose_name="شماره مبایل")
    
    is_author = models.BooleanField(default= False, verbose_name="وضعیت نویسندگی" )
    special_user = models.DateTimeField(default=timezone.now, verbose_name="کاربر ویژه تا")

    def is_special_user(self):
        if self.special_user > timezone.now():
            return True
        else:
            return False
    is_special_user.boolean = True
    is_special_user.short_description = "وضعیت کاربر ویژه"

class Form_Registeration(models.Model):

    PARENT_CHICES = (
        ("mother", "مادر"),
        ("father", "پدر"),
        ("motherANDfather", "پدرومادر"),
        ("other", "سایر"),
    )

    FORM_TYPE_CHOICES = (
        ("s", "هفتم"),
        ("e", "هشتم"),
        ("n", "نهم"),
    )

    THE_EDUCATION_LEVEL_CHOICES_FATHER = (
        ("dont", "بی سواد"),
        ("five", "پنجم ابتدایی"),
        ("sicle", "سیکل"),
        ("diplom", "دیپلوم"),
        ("udiplom", "فوق دیپلوم"),
        ("lisans", "لیسانس"),
        ("ulisans", "فوق لیسانس"),
        ("doctor", "دکترا"),
    )    

    THE_EDUCATION_LEVEL_CHOICES_MOTHER = (
        ("dont", "بی سواد"),
        ("five", "پنجم ابتدایی"),
        ("sicle", "سیکل"),
        ("diplom", "دیپلوم"),
        ("udiplom", "فوق دیپلوم"),
        ("lisans", "لیسانس"),
        ("ulisans", "فوق لیسانس"),
        ("doctor", "دکترا"),
    )    
    THE_EDUCATION_LEVEL_CHOICES_GHAIM = (
        ("dont", "بی سواد"),
        ("five", "پنجم ابتدایی"),
        ("sicle", "سیکل"),
        ("diplom", "دیپلوم"),
        ("udiplom", "فوق دیپلوم"),
        ("lisans", "لیسانس"),
        ("ulisans", "فوق لیسانس"),
        ("doctor", "دکترا"),
    )    
    
    RELIGION_CHOICES = (
        ("eslam", "اسلام"),
        ("zartoshti", "زرتشتی"),
        ("kalimi", "کلیمی"),
        ("masihi", "مسیحی"),
    )
    
    RELIGION_RELIGION_CHOICES = (
        ("shie", "شیعه"),
        ("soni", "سنی"),
    )
    
    type = models.CharField(max_length=1, choices=FORM_TYPE_CHOICES, verbose_name="کلاس")
    user = models.OneToOneField(User, related_name="form", verbose_name="کاربر", on_delete=models.SET_NULL, null=True)
    # student
    name = models.CharField(max_length=255, verbose_name="نام")
    lastname = models.CharField(max_length=255, verbose_name="نام خانوادگی")
    father_name = models.CharField(max_length=255, verbose_name="نام پدر")
    nid = models.CharField(max_length=255, verbose_name="کد ملی")
    creation_certificate = models.CharField(max_length=100, verbose_name="محل ثبت شناسنامه")
    birth_localtion = models.CharField(max_length=100, verbose_name="محل تولد")
    date_of_birth_day = models.CharField(max_length = 18, verbose_name="تاریخ تولد")
    the_name_of_privous_school = models.CharField(max_length=300,verbose_name="نام مدرسه قبلی")
    religion = models.CharField(max_length=100, choices=RELIGION_CHOICES, verbose_name="دین")
    religion_of_religion = models.CharField(max_length=100, choices=RELIGION_RELIGION_CHOICES, default="shie", verbose_name="مذهب", null=True)
    # father
    student_parent = models.CharField(max_length=100,verbose_name="سرپرست", choices=PARENT_CHICES)
    father_first_name = models.CharField(max_length=255,verbose_name="نام کوچک پدر", null=True)
    father_last_name = models.CharField(max_length=255,verbose_name="نام خانوادگی پدر", null=True)
    father_date_of_birth_day = models.CharField(max_length = 18, verbose_name="تاریخ تولد پدر", null=True)
    level_of_education_father = models.CharField(max_length=100, choices=THE_EDUCATION_LEVEL_CHOICES_FATHER, verbose_name="میزان تحصیلات پدر")
    job_father = models.CharField(max_length=255,verbose_name="شغل پدر", null=True)
    telephone_number_work_location_father = models.CharField(max_length=11,verbose_name="شماره تلفن محل کار پدر", null=True)
    work_location_adderss_father = models.CharField(max_length=10000000000000000 ,verbose_name="ادرس محل کار پدر", null=True)
    father_phone_number = models.CharField(max_length=11,verbose_name="شماره تلفن پدر", null=True)
    father_live = models.BooleanField(verbose_name="ایا پدر زنده است")
    # mother
    mother_first_name = models.CharField(max_length=255,verbose_name="نام کوچک مادر")
    mother_last_name = models.CharField(max_length=255,verbose_name="نام خانوادگی مادر")
    mother_date_of_birth_day = models.CharField(max_length = 18, verbose_name="تاریخ تولد مادر")
    level_of_education_mother = models.CharField(max_length=100, choices=THE_EDUCATION_LEVEL_CHOICES_MOTHER, verbose_name="میزان تحصیلات مادر")
    job_mother = models.CharField(max_length=255,verbose_name="شغل مادر", null=True)
    telephone_number_work_location_mother = models.CharField(max_length=11,verbose_name="شماره تلفن محل کار مادر")
    work_location_adderss_mother = models.CharField(max_length=100000000000000000000 ,verbose_name="ادرس محل کار مادر")
    mother_phone_number = models.CharField(max_length=11,verbose_name="شماره تلفن مادر")
    mother_live = models.BooleanField(verbose_name="ایا مادر زنده است")
    # ghaim

    ghaim_first_name = models.CharField(max_length=255,verbose_name="نام کوچک سرپرست", null=True, blank=True)
    ghaim_last_name = models.CharField(max_length=255,verbose_name="نام خانوادگی سرپرست", null=True, blank=True)
    ghaim_date_of_birth_day = models.CharField(max_length = 18, verbose_name="تاریخ تولد سرپرست", null=True, blank=True)
    level_of_education_ghaim = models.CharField(max_length=100, choices=THE_EDUCATION_LEVEL_CHOICES_GHAIM, verbose_name="میزان تحصیلات سرپرست", null=True, blank=True)
    job_ghaim = models.CharField(max_length=255,verbose_name="شغل سرپرست", null=True, blank=True)
    telephone_number_work_location_ghaim = models.CharField(max_length=11,verbose_name="شماره تلفن محل کار سرپرست", null=True, blank=True)
    work_location_adderss_ghaim = models.CharField(max_length=100000000000000000000 ,verbose_name="ادرس محل کار سرپرست", null=True, blank=True)
    ghaim_phone_number = models.CharField(max_length=11,verbose_name="شماره تلفن سرپرست", null=True, blank=True)
    # location
    street = models.CharField(max_length=100000000,verbose_name="خیابان")
    alley = models.CharField(max_length=100000000,verbose_name="کوی")
    alley_alley = models.CharField(max_length=100000000,verbose_name="کوچه")
    plaque = models.CharField(verbose_name="پلاک", max_length=5)
    floor = models.CharField(verbose_name="طبقه", max_length=3)
    postal_code = models.CharField(max_length=22,verbose_name="کد پستی")
    telephone_number = models.CharField(max_length=11,verbose_name="تلفن")
    number_of_shad = models.CharField(max_length=11,verbose_name="شماره متصل به شبکه شاد")
    emergensy_phone = models.CharField(max_length=11,verbose_name="شماره اضتراری")

    def get_absolute_url(self):
        return reverse("auth:home")

    class Meta:
        verbose_name = "فرم ثبت‌نام"
        verbose_name_plural = "فرم‌های ثبت‌نام"

    def __str__(self):
        return f"{self.name} {self.lastname}"

class Reserve(models.Model):
    datetime = models.DateTimeField(default = timezone.now)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name="reserve")

    def __str__(self):
        return f"{self.datetime}"
    
    def jrpublish(self):
        return jalali_converter(self.datetime)
    jrpublish.short_description = "زمان رزرو"

    class Meta:
        verbose_name = "نوبت رزرو"
        verbose_name_plural = "نوبت های رزرو"
    