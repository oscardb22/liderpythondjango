from crispy_forms.layout import Submit, Button, Layout
from django import forms
from crispy_forms.helper import FormHelper
from .models import Users, Municipio, Region


class UsersForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=True, label='Password')
    con_pass = forms.CharField(widget=forms.PasswordInput, required=True, label='Conf. Password')

    def clean(self):
        password = self.cleaned_data.get("password")
        con_pass = self.cleaned_data.get("con_pass")
        username = self.cleaned_data.get("username")

        if Users.objects.filter(username=username).exists():
            self.add_error('username', "This username exist")

        if con_pass != password:
            self.add_error('password', "Passwords dosn't match")

    class Meta:
        model = Users
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(UsersForm, self).__init__(*args, **kwargs)
        lay = Layout(
            'username', 'password', 'con_pass'
        )
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.form_group_wrapper_class = 'row clearfix'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-10 col-md-10 col-sm-8 form-control-label'
        self.helper.field_class = 'col-lg-10 col-md-10 col-sm-8'
        self.helper.add_input(Submit('submit', 'Enviar'))
        self.helper.add_input(Button('cancel', 'Cancel', css_class='btn-default'))
        self.helper.layout = lay


class MunicipioForm(forms.ModelForm):
    def clean(self):
        codigo = self.cleaned_data.get("codigo")
        if self.instance.pk:
            lis = Municipio.objects.filter(codigo=codigo)
            if lis.exists():
                municipio = lis.first()
                if municipio.pk != self.instance.pk:
                    self.add_error('codigo', "Este codigo de municipio ya existe")
        else:
            if Municipio.objects.filter(codigo=codigo).exists():
                self.add_error('codigo', "Este codigo de municipio ya existe")

    class Meta:
        model = Municipio
        fields = ['codigo', 'nombre', 'estado']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(MunicipioForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.form_group_wrapper_class = 'row clearfix'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-10 col-md-10 col-sm-8 form-control-label'
        self.helper.field_class = 'col-lg-10 col-md-10 col-sm-8'
        self.helper.add_input(Submit('submit', 'Enviar'))
        self.helper.add_input(Button('cancel', 'Cancel', css_class='btn-default'))


class RegionForm(forms.ModelForm):
    def clean(self):
        codigo = self.cleaned_data.get("codigo")
        if self.instance.pk:
            lis = Region.objects.filter(codigo=codigo)
            if lis.exists():
                region = lis.first()
                if region.pk != self.instance.pk:
                    self.add_error('codigo', "Este codigo de region ya existe")
        else:
            if Region.objects.filter(codigo=codigo).exists():
                self.add_error('codigo', "Este codigo de municipio ya existe")

    class Meta:
        model = Region
        fields = ['codigo', 'nombre', 'municipios']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(RegionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.form_group_wrapper_class = 'row clearfix'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-10 col-md-10 col-sm-8 form-control-label'
        self.helper.field_class = 'col-lg-10 col-md-10 col-sm-8'
        self.helper.add_input(Submit('submit', 'Enviar'))
        self.helper.add_input(Button('cancel', 'Cancel', css_class='btn-default'))
        self.fields['municipios'].queryset = Municipio.objects.filter(estado=True)
