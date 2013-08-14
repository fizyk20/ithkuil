from django.contrib import admin
from morphology.models import *

class CategValueInline(admin.StackedInline):
	model = CategValue
	extra = 1
	
class CategoryAdmin(admin.ModelAdmin):
	fields = ['name', 'description']
	inlines = [CategValueInline]
	
admin.site.register(Category, CategoryAdmin)

admin.site.register(CategValue)
admin.site.register(WordType)
admin.site.register(Slot)
admin.site.register(Morpheme)
