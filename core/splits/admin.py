from django.contrib import admin
# from .models import Question, Choice
from .models import Split, Participant, Expense


# class ChoiceInline(admin.TabularInline):
#     model = Choice
#     extra = 1


# class QuestionAdmin(admin.ModelAdmin):
#     list_display = ["question_text", "created_date", "was_created_recently"]
#     fields = ["question_text", "created_date"]
#     list_filter = ["created_date"]
#     search_fields = ["question_text"]
#     inlines = [ChoiceInline]


# admin.site.register(Question, QuestionAdmin)
admin.site.register(Split)
admin.site.register(Participant)
admin.site.register(Expense)
