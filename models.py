import uuid

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save


# Create your models here.
from django.dispatch import receiver


class Event(models.Model):
    VENUE_LIST = (
        ('s', 'New Sports Complex'),
        ('i', 'IEM Auditorium'),
        ('m', 'Mini Canteen'),
        ('c', 'CSE Department'),
        ('m', 'Mathematics Department')
    )
    EventId = models.UUIDField(primary_key=True, default=uuid.uuid4)
    Name = models.CharField(max_length=20, unique=True, help_text="Event Name")
    Date = models.DateField()
    Time = models.TimeField()
    Venue = models.CharField(max_length=15, choices=VENUE_LIST, default='s')
    RegistrationFee = models.IntegerField(default=0)
    Prize = models.IntegerField(default=0)
    Judge = models.ForeignKey('Faculty', on_delete=None, blank=True, null=True, default=None)
    Winner = models.ForeignKey('Participant', on_delete=None, blank=True, null=True, default=None)

    class Meta:
        ordering = ["-Date"]

    def __str__(self):
        return self.Name


class Faculty(models.Model):
    FacultyId = models.UUIDField(primary_key=True, default=uuid.uuid4)
    Name = models.CharField(max_length=20, help_text="Name of the Faculty")
    PhoneNo = models.IntegerField(unique=True)
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
    PhoneNo = models.IntegerField()
    MailId = models.EmailField(unique=True)
    Password = models.CharField(max_length=25)

    class Meta:
        ordering = ["Name"]

    def __str__(self):
        return self.Name


class Participant(models.Model):
    ID = models.UUIDField(primary_key=True, default=uuid.uuid4())
    Name = models.CharField(max_length=20)
    Password = models.CharField(max_length=25)
    City = models.CharField(max_length=20)
    PhoneNo = models.IntegerField()
    College = models.CharField(max_length=20, blank=True, null=True)
    MailId = models.EmailField(unique=True)
    RegNo = models.CharField(unique=True, max_length=10, blank=True, null=True)

    def __str__(self):
        return self.Name

    class Meta:
        ordering = ["Name"]


class SpecialGuest(models.Model):
    GuestID = models.UUIDField(primary_key=True, default=uuid.uuid4)
    Name = models.CharField(max_length=20, help_text="Name of the Guest")
    PhoneNo = models.IntegerField(default=None, null=False)
    MailId = models.EmailField(default=None, null=False, unique=True)
    Events = models.OneToOneField(Event, on_delete=None, default=None, blank=None, null=True, help_text="Hosted by")

    def __str__(self):
        return self.Name

    class Meta:
        ordering = ["Name"]


class EventParticipates(models.Model):
    Event = models.ForeignKey(Event)
    Participant = models.ForeignKey(Participant)

    class Meta:
        unique_together = ('Event', 'Participant')


class EventCoordinates(models.Model):
    Event = models.ForeignKey(Event)
    Coordinator = models.ForeignKey(Coordinator)

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


