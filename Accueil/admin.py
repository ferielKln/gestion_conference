from django.contrib import admin

# Register your models here.
from .models import *






class articleInLine(admin.TabularInline):
    model = article
    extra=0



class conferenceAdmin(admin.ModelAdmin):
    list_display= ["__str__","chair","organisateur","date","lieu","description"]

    class meta:
        model = conference

class articleAdmin(admin.ModelAdmin):

    list_display= ["__str__","conférence","date_publication","résumé"]
    list_filter=("titre","date_publication","conférence")
    class meta:
        model = article



admin.site.site_header='Page Administrateur'
admin.site.register(conference,conferenceAdmin) 
admin.site.register(article,articleAdmin)  
admin.site.register(MotCle)
admin.site.register(Auteur)

