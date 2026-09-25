from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator


# =========================
# CHOICES
# =========================

BLOOD_GROUP_CHOICES = [
    ('A+', 'A+'),
    ('A-', 'A-'),
    ('B+', 'B+'),
    ('B-', 'B-'),
    ('O+', 'O+'),
    ('O-', 'O-'),
    ('AB+', 'AB+'),
    ('AB-', 'AB-'),
]

GENDER_CHOICES = [
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Other', 'Other'),
]

SECURITY_QUESTION_CHOICES = [
    ("pet", "What is your first pet's name?"),
    ("school", "What is your first school name?"),
    ("city", "Which city were you born in?"),
    ("friend", "Who is your childhood best friend?"),
]


# =========================
# VALIDATORS
# =========================

phone_validator = RegexValidator(
    regex=r'^\d{10}$',
    message="Phone number must be exactly 10 digits."
)


# =========================
# DONOR MODEL
# =========================

class Donor(models.Model):

    name = models.CharField(max_length=100)

    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)

    age = models.IntegerField(
        validators=[MinValueValidator(18), MaxValueValidator(65)]
    )

    blood_group = models.CharField(
        max_length=5,
        choices=BLOOD_GROUP_CHOICES
    )

    weight = models.FloatField(validators=[MinValueValidator(45)])

    phone = models.CharField(max_length=10, validators=[phone_validator])

    hemoglobin = models.FloatField(validators=[MinValueValidator(12.5)])

    city = models.CharField(max_length=100)

    state = models.CharField(max_length=100)

    last_donation_date = models.DateField()

    health_issues = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.blood_group})"


# =========================
# USER SECURITY MODEL
# =========================

class UserSecurity(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    security_question = models.CharField(
        max_length=30,
        choices=SECURITY_QUESTION_CHOICES
    )

    security_answer = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username


# =========================
# BLOOD REQUEST MODEL
# =========================

class BloodRequest(models.Model):

    patient_name = models.CharField(max_length=100)

    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUP_CHOICES)

    units_required = models.IntegerField(validators=[MinValueValidator(1)])

    hospital_name = models.CharField(max_length=150)

    city = models.CharField(max_length=100)

    contact_number = models.CharField(max_length=10, validators=[phone_validator])

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.patient_name} - {self.blood_group}"