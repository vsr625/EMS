from django.contrib import admin

from EMS.models import Event, Participant, Coordinator, Faculty, SpecialGuest, EventParticipates, EventCoordinates


class EventAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Venue', 'Date', 'Time')


class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('Name', 'PhoneNo', 'City', 'College', 'MailId')


class FacultyAdmin(admin.ModelAdmin):
    list_display = ('Name', 'PhoneNo', 'MailId')


class CoordinatorAdmin(admin.ModelAdmin):
    list_display = ('Name', 'RegNo', 'PhoneNo', 'MailId')


class SpecialGuestAdmin(admin.ModelAdmin):
    list_display = ('Name', 'MailId', 'PhoneNo')


admin.site.site_header = "Event Management System Administration"
admin.site.site_url = None
admin.site.register(Event, EventAdmin)
admin.site.register(Participant, ParticipantAdmin)
admin.site.register(Coordinator, CoordinatorAdmin)
admin.site.register(Faculty, FacultyAdmin)
admin.site.register(SpecialGuest, SpecialGuestAdmin)
admin.site.register(EventParticipates)
admin.site.register(EventCoordinates)
