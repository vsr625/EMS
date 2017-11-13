import uuid

from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator, RegexValidator
from django.db import models
from django.db.models.signals import post_save, post_delete
# Create your models here.
from django.dispatch import receiver

phone_regex = RegexValidator(regex=r'^\d{10}$', message='Phone number must be 10 digits.')
register_regex = RegexValidator(regex=r'^1(RV|rv)\d{2}[a-zA-Z]{2}\d{3}$', message='Register Number is Invalid')


class Event(models.Model):
    VENUE_LIST = (
        ('s', 'New Sports Complex'),
        ('i', 'IEM Auditorium'),
        ('m', 'Mini Canteen'),
        ('c', 'CSE Department'),
        ('m', 'Mathematics Department')
    )
    EventId = models.UUIDField(primary_key=True, default=uuid.uuid4)
    Name = models.CharField(max_length=20, unique=True)
    Date = models.DateField()
    Time = models.TimeField()
    Venue = models.CharField(max_length=15, choices=VENUE_LIST, default='s')
    RegistrationFee = models.IntegerField(default=0)
    Prize = models.IntegerField(default=0)
    Judge = models.ForeignKey('Faculty', on_delete=None, blank=True, null=True, default=None)
    Winner = models.ForeignKey('Participant', on_delete=None, blank=True, null=True, default=None)
    SpecialGuest = models.OneToOneField('SpecialGuest', related_name='special_guest', on_delete=None, default=None,
                                        blank=True, null=True)

    class Meta:
        ordering = ["-Date"]

    def __str__(self):
        return self.Name


class Faculty(models.Model):
    FacultyId = models.UUIDField(primary_key=True, default=uuid.uuid4)
    Name = models.CharField(max_length=20)
    PhoneNo = models.CharField(max_length=15, validators=[phone_regex])
    MailId = models.EmailField(unique=True)
    RegNo = models.CharField(unique=True, max_length=10, blank=True, null=True)

    class Meta:
        ordering = ["Name"]

    def __str__(self):
        return self.Name


class Coordinator(models.Model):
    CoordinatorId = models.UUIDField(primary_key=True, default=uuid.uuid4)
    Name = models.CharField(max_length=20)
    RegNo = models.CharField(unique=True, max_length=10)
    PhoneNo = models.CharField(max_length=15, validators=[phone_regex])
    MailId = models.EmailField(unique=True)
    Password = models.CharField(max_length=25, validators=[MinLengthValidator(8)])

    class Meta:
        ordering = ["Name"]

    def __str__(self):
        return self.Name


@receiver(post_save, sender=Coordinator)
def save_co_user(sender, instance, created, **kwargs):
    if created:
        user = User.objects.create_user(username=instance.MailId, email=instance.MailId, password=instance.Password)
        user.profile.type = 'c'
        user.save()


@receiver(post_delete, sender=Coordinator)
def delete_co_user(sender, instance, **kwargs):
    User.objects.filter(username=instance.MailId).delete()


class Participant(models.Model):
    ID = models.UUIDField(primary_key=True, default=uuid.uuid4)
    Name = models.CharField(max_length=20)
    Password = models.CharField(max_length=25, validators=[MinLengthValidator(8)])
    City = models.CharField(max_length=20)
    PhoneNo = models.CharField(validators=[phone_regex], max_length=15)
    College = models.CharField(max_length=20, blank=True, null=True)
    MailId = models.EmailField(unique=True)
    RegNo = models.CharField(unique=True, max_length=10, blank=True, null=True, validators=[register_regex])

    def __str__(self):
        return self.Name

    class Meta:
        ordering = ["Name"]


@receiver(post_save, sender=Participant)
def save_p_user(sender, instance, created, **kwargs):
    if created:
        user = User.objects.create_user(username=instance.MailId, email=instance.MailId, password=instance.Password)
        user.profile.type = 'p'
        user.save()


@receiver(post_delete, sender=Participant)
def delete_p_user(sender, instance, **kwargs):
    User.objects.filter(username=instance.MailId).delete()


class SpecialGuest(models.Model):
    GuestID = models.UUIDField(primary_key=True, default=uuid.uuid4)
    Name = models.CharField(max_length=20)
    PhoneNo = models.CharField(max_length=15, validators=[phone_regex])
    MailId = models.EmailField(default=None, null=False, unique=True)

    def __str__(self):
        return self.Name

    class Meta:
        ordering = ["Name"]


class EventParticipates(models.Model):
    Event = models.ForeignKey(Event, on_delete=models.CASCADE)
    Participant = models.ForeignKey(Participant, on_delete=models.CASCADE)

    def __str__(self):
        return self.Participant.Name + '-' + self.Event.Name

    class Meta:
        unique_together = ('Event', 'Participant')


class EventCoordinates(models.Model):
    Event = models.ForeignKey(Event, on_delete=models.CASCADE)
    Coordinator = models.ForeignKey(Coordinator, on_delete=models.CASCADE)

    def __str__(self):
        return self.Coordinator.Name + '-' + self.Event.Name

    class Meta:
        unique_together = ('Event', 'Coordinator')


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    type = models.CharField(default='p', max_length=1)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
