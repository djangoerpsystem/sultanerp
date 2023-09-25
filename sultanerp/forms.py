from django import forms
from django.core.exceptions import ValidationError
from .models import DocumentData, VacationApplication, Inventory, Deposit


def file_extension_checker(value):
    if value.name.endswith('.csv') is False:
        # https://docs.djangoproject.com/en/4.2/topics/forms/formsets/#custom-formset-validation
        raise ValidationError('Please upload a .csv file')


class UploadCSVForm(forms.Form):
    csv_file = forms.FileField(label='Upload CSV file', 
        # "https://docs.djangoproject.com/en/4.2/ref/validators/#writing-validators"
        validators=[file_extension_checker])


class VacationApplicationForm(forms.ModelForm):
    start_date = forms.DateField(
        widget=forms.SelectDateWidget(),
        label="",
        help_text="Hiermit beantrage ich Urlaub vom"
    )

    end_date = forms.DateField(
        widget=forms.SelectDateWidget(),
        label="",
        help_text="Hiermit beantrage ich Urlaub bis"
    )

    class Meta:
        model = VacationApplication
        fields = ['start_date', 'end_date']

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date and start_date > end_date:
            raise forms.ValidationError(
                "End date should be after the start date.")


class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ['section', 'category', 'name',
                  'boughtOn', 'storedIn', 'value', 'amount']
        widgets = {
            'boughtOn': forms.DateInput(attrs={'type': 'date'}),
        }


class DepositForm(forms.ModelForm):
    class Meta:
        model = Deposit
        exclude = ['user', 'paid_back', 'paid_back_date']


class MessageForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))
