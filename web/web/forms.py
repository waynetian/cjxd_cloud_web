#coding=utf-8
from django import forms


class RegisterForm(forms.Form):
    email = forms.EmailField(label='邮箱')
    password = forms.CharField(widget=forms.PasswordInput, label='密码')
    password2 = forms.CharField(widget=forms.PasswordInput, \
                               label="确认")

    def pwd_validate(self, p1, p2):
        return p1==p2


class RegisterCompanyForm(forms.Form):
    name = forms.CharField(max_length=64, label='公司名')
    short_name = forms.CharField(max_length=20, label='公司简称')
    org_code = forms.CharField(max_length=10, label='机构代码')
    stand_type = forms.CharField(max_length=10, label='公司类别')
    address = forms.CharField(max_length=256, label='公司地址')
    certificate_number = forms.CharField(max_length=30, label='认证号')
    business_type_code = forms.CharField(max_length=5, label='业务类别')
    business_tag = forms.CharField(max_length=256, label='业务tag')
    legal_person_id = forms.CharField(max_length=18, label='法人身份证号')


class RegisterDeptForm(forms.Form):
    name = forms.CharField(max_length=64, label='部门名')
    parent_id = forms.CharField(max_length=64, label='上级')


 
class RegisterUserForm(forms.Form):
    user_name = forms.CharField(max_length=64, label='真实姓名')
    id_number = forms.CharField(max_length=18, label='身份证号')
    mobile_number = forms.CharField(max_length=12, label='手机号')
    job_title = forms.CharField(max_length=12, label='职务名称')


 
class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class CompanyForm(forms.Form):
    company_name = forms.CharField(max_length=64)
    company_sname = forms.CharField(max_length=20)
    organization_code = forms.CharField(max_length=10)
    company_stand_type = forms.CharField(max_length=10)
    company_address = forms.CharField(max_length=256)
    certificate_number = forms.CharField(max_length=30)
    business_type_code = forms.CharField(max_length=5)
    business_tags = forms.CharField(max_length=256)
 

