from django.contrib import admin

from .models import Campaign, Candidates

admin.site.site_header = "Suffrage Admin"
admin.site.site_title = "Suffrage Admin Area"
admin.site.index_title = "Welcome to the Suffrage Admin Area"


class ChoiceInLine(admin.TabularInline):
	model = Candidates	
	extra = 3


class CampaignAdmin(admin.ModelAdmin):
	fieldsets = [(None, {'fields': ['organization_name']}), ('Date Information', {
		'fields': ['pub_date'], 'classes': ['collapse']}), ]
	inlines = [ChoiceInLine]


admin.site.register(Campaign, CampaignAdmin)

