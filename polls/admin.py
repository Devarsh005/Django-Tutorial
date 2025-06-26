from django.contrib import admin
from polls.models import Question,Choice
# Register your models here.

# admin.site.register(Question)
# admin.site.register(Choice)

class choice(admin.TabularInline):
    model = Choice
    extra =0

class QuestionsAdmin(admin.ModelAdmin):
    fieldsets =[ ( "Question", {'fields':['question']}),
                 ('Date information',{'fields':['publish_date'],'classes':['collapse']}),
                 ]
    list_display = ['question','publish_date','was_published_recently' ]
    list_filter = ['publish_date']
    search_fields = ['question']
    inlines = [choice]
admin.site.register(Question,QuestionsAdmin)