from django import forms
from django.contrib.auth.models import Group
from django.forms import ModelForm
from todo.models import CreditCardInfo, Task, Book, UserInfo, Editor, Designer, PublishedBook, Reader 


class AddBookForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["thematic"].queryset = Book.THEMATIC
        self.fields["thematic"].widget.attrs = {
            "id": "id_thematic",
            "class": "custom-select mb-3",
            "name": "thematic",
        }

    class Meta:
        model = Book
        exclude = ["created_date", "slug", "author", "editor", "completed", "file"]


class AddEditTaskForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["task_type"].queryset = Task.TYPES_OF_TASK_CHOICES
        self.fields["task_type"].widget.attrs = {
            "id": "id_task_type",
            "class": "custom-select mb-3",
            "name": "task_type",
        }
        self.fields["book"].value = kwargs["initial"]["book"].id

    due_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}), required=False)
    title = forms.CharField(widget=forms.widgets.TextInput())
    note = forms.CharField(widget=forms.Textarea(), required=False)

    def clean_created_by(self):
        return self.instance.created_by

    class Meta:
        model = Task
        exclude = ["assigned_to", "created_date"]


class AddExternalBookForm(ModelForm):
    class Meta:
        model = UserInfo
        exclude = (
            "user",
        )

class PublishedBookForm(ModelForm):
    class Meta:
        model = PublishedBook
        exclude = (
            "book","author_text"
        )

class SearchForm(forms.Form):
    q = forms.CharField(widget=forms.widgets.TextInput(attrs={"size": 35}))

class AssignForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["editor"].widget.attrs = {
            #"id": "id_thematic",
            "class": "custom-select mb-3",
            #"name": "thematic",
        }
        self.fields["editor"].label = ""

    editor = forms.ModelChoiceField(queryset=Editor.objects.all())

class AssignFormDesigner(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["designer"].widget.attrs = {
            #"id": "id_thematic",
            "class": "custom-select mb-3",
            #"name": "thematic",
        }
        self.fields["designer"].label = ""

    designer = forms.ModelChoiceField(queryset=Designer.objects.all())

class PaymentSubscriptionForm(ModelForm):
    class Meta:
        model = CreditCardInfo
        exclude = []

class profileForm(forms.ModelForm):
    name1 = forms.CharField(label='Name', widget=forms.PasswordInput)

    class Meta:
        model = UserInfo
        fields = ('full_name', 'user')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        if password1:
            raise forms.ValidationError("Passwords don't match")

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(profileForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        # user.active = False # send confirmation email
        if commit:
            user.save()
        return user