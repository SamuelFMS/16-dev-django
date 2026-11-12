from typing import ClassVar

from django.contrib import admin

from polls.models import Choice, Question


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    list_display: ClassVar[list[str]] = [
        "question_text",
        "pub_date",
        "was_published_recently",
    ]
    list_filter: ClassVar[list[str]] = ["pub_date"]
    ordering: ClassVar[list[str]] = ["-pub_date", "question_text"]
    search_fields: ClassVar[list[str]] = ["question_text", "pub_date"]
    fieldsets: ClassVar[list] = [
        (None, {"fields": ["question_text"]}),
        ("Date information", {"fields": ["pub_date"]}),
    ]
    inlines: ClassVar[list] = [ChoiceInline]


class ChoiceAdmin(admin.ModelAdmin):
    list_display: ClassVar[list[str]] = ["question", "choice_text", "votes"]
    list_filter: ClassVar[list[str]] = ["question", "votes"]
    ordering: ClassVar[list[str]] = ["question", "votes", "choice_text"]
    search_fields: ClassVar[list[str]] = ["question", "choice_text", "votes"]


admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)
