from django import forms
from django.contrib.auth.models import Group
from django.forms import ModelForm
from todo.models import Task, Book


class AddBookForm(ModelForm):
    class Meta:
        model = Book
        exclude = ["created_date", "slug", "author", "editor", "completed"]


class AddEditTaskForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["task_type"].queryset = Task.TYPES_OF_TASK_CHOICES
        # self.fields["task_type"].label_from_instance = lambda obj: "%s (%s)" % (
        #     obj.get_full_name(),
        #     obj.username,
        # )
        self.fields["task_type"].widget.attrs = {
            "id": "id_task_type",
            "class": "custom-select mb-3",
            "name": "task_type",
        }
        self.fields["book_list"].value = kwargs["initial"]["book_list"].id

    due_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}), required=False)
    title = forms.CharField(widget=forms.widgets.TextInput())
    note = forms.CharField(widget=forms.Textarea(), required=False)

    def clean_created_by(self):
        """Keep the existing created_by regardless of anything coming from the submitted form.
        If creating a new task, then created_by will be None, but we set it before saving."""
        return self.instance.created_by

    class Meta:
        model = Task
        exclude = ["assigned_to", "created_date"]


class AddExternalTaskForm(ModelForm):
    """Form to allow users who are not part of the GTD system to file a ticket."""

    title = forms.CharField(widget=forms.widgets.TextInput(attrs={"size": 35}), label="Summary")
    note = forms.CharField(widget=forms.widgets.Textarea(), label="Problem Description")
    priority = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = Task
        exclude = (
            "book_list",
            "created_date",
            "due_date",
            "created_by",
            "assigned_to",
            "completed",
            "completed_date",
        )


class SearchForm(forms.Form):
    """Search."""

    q = forms.CharField(widget=forms.widgets.TextInput(attrs={"size": 35}))
