#coding=utf-8
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.views.generic import TemplateView
from django.shortcuts import render_to_response 
from django.template.response import TemplateResponse
from django.db import transaction
import json

from .forms import *
from .sdk import APIServer
from .settings import ORG_TYPE_COMPANY, ORG_TYPE_DEPARTMENT

class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        import time 
        context['current_time'] = time.ctime()
        #context['latest_articles'] = Article.objects.all()[:5]
        return context


 
class RegisterView(TemplateView):
    def get(self, request):
        user_id = request.session.get('user_id', None)
        if None != user_id:
            return HttpResponseRedirect('/work/') 
        t = TemplateResponse(request, 'register.html')
        return t

    def post(self, request):
        form = RegisterForm(request.POST) 
        form.is_valid()
        data = form.cleaned_data 
           
        result = APIServer.create_user(\
                           email=data['email'], \
                           password=data['password'])
        if result is None:
            return HttpResponse(status=201, content="fail") 
        request.session['user_id'] = result['id']
        request.session['user_email'] = result['email']
        return HttpResponse(status=200, content="success") 


class WelcomeView(TemplateView):
    template_name = 'welcome.html'



class TryUserView(TemplateView):

    def get(self, request):
        user_id = request.session.get('user_id', None)
        if user_id is None:
            return HttpResponseRedirect('/register/')

        user = APIServer.retrieve_user(user_id)
        if user is None:
            return HttpResponseRedirect('/register/')


        # company 
        org_name = u'公司' 
        short_name = u''
        org_type = ORG_TYPE_COMPANY
        parent_id = 0
        org = APIServer.create_org(name=org_name.encode('utf8'),\
                             short_name=short_name.encode('utf8'), \
                             type=org_type, \
                             parent_id=parent_id)

        if org is None:
            return HttpResponse(status=400, \
                    content="create organization fail") 

        # org-user info
        user_name = u'试用用户'
        email = request.session.get('user_email', None)
        mobile_number = u''
        id_number = u''
        org_id = org['id']
        job_type = 0 
        job_title = u''
        role_id = 1
        domain_id = org_id
        orguser = APIServer.create_orguser(
                   user_name=user_name.encode('utf8'),\
                   email=email, \
                   mobile_number=mobile_number, \
                   id_number=id_number,\
                   org_id=org_id, \
                   job_title=job_title.encode('utf8'), \
                   job_type=job_type, \
                   role_id = role_id, \
                   user_id = user_id, \
                   domain_id = org_id)

        if orguser is None:
            return HttpResponse(status=400, \
                    content="create organization user fail") 

        request.session['orguser'] = orguser
        return HttpResponseRedirect('/work/') 
         
 

    
class RegisterCompanyView(TemplateView):
    template_name = 'register.html'

    def post(self, request):
        form = RegisterCompanyForm(request.POST) 
        form.is_valid()
        data  = form.cleaned_data
        data['user_id'] = request.session.get('user_id', None)
        name = data['name']
        #if 'short_name' in data:
        short_name = data['short_name']
        #else:
        #    short_name = u''
        #if 'org_code' in data:
        org_code = data['org_code']
        #else:
        #    org_code = u''
        stand_type = data['stand_type']
        address = data['address']
        certificate_number = data['certificate_number']
        business_type_code = data['business_type_code']
        business_tag = data['business_tag']
        legal_person_id = data['legal_person_id']
        
        org = APIServer.org_create(name=name.encode('utf8'),\
                             short_name=short_name.encode('utf8'), \
                             type=0, \
                             parent_id=0)
        org_info = APIServer.org_info_create(org_code=org_code,\
                             stand_type=stand_type, \
                             address=address.encode('utf8'), \
                             certificate_number=certificate_number,\
                             business_type_code = business_type_code,\
                             business_tag = business_tag, \
                             legal_person_id=legal_person_id, \
                             org=org['id'])

        request.session['org_id'] = org['id']
        return HttpResponseRedirect('/register_user/') 



    def get_context_data(self, **kwargs):
        context = super(RegisterCompanyView, self).get_context_data(**kwargs)
        context['form']= RegisterCompanyForm()
        context['sub_title'] = u'填写公司信息'
        return context



class RegisterUserView(TemplateView):
    template_name = 'register.html'

    def post(self, request):
        form = RegisterUserForm(request.POST) 
        form.is_valid()
        data = form.cleaned_data
        user_id = request.session.get('user_id')
        name = data['user_name']
        id_number = data['id_number']
        email = self.request.session.get('email')
        mobile_number = data['mobile_number']
        

        user_base_info = APIServer.user_base_info_create( \
                                name=name.encode('utf8'), \
                                id_number=id_number,\
                                mobile_number=mobile_number,\
                                user_id=user_id,
                                email=email)
        org_id = request.session.get('org_id')
        role_id = 2   
        job_type = 1
        job_title = data['job_title'].encode('utf8')
        org2user = APIServer.org2user_create(org_id=org_id,\
                   user_id = user_id, \
                   job_title= job_title, \
                   job_type=1, \
                   role_id =role_id)


        return HttpResponseRedirect('/register_finish/') 

                  
    def get_context_data(self, **kwargs):
        context = super(RegisterUserView, self).get_context_data(**kwargs)
        context['form']= RegisterUserForm()
        context['sub_title'] = u'填写个人信息'


        return context


class RegisterFinishView(TemplateView):
    template_name = 'register_finish.html'


    def get_context_data(self, **kwargs):
        context = super(RegisterFinishView, self).get_context_data(**kwargs)
        return context






 
class LoginView(TemplateView):
    template_name = 'login.html'

    def post(self, request):
        
        import logging
        logger = logging.getLogger('django.request')

        form = LoginForm(request.POST) 
        form.is_valid()
        data = form.cleaned_data 
        email = data['email']
        password = data['password']
        orguser = APIServer.user_login(email, password)
        if orguser is not None:
            request.session['orguser'] = orguser
            return HttpResponseRedirect('/work/') 
        return HttpResponseRedirect('/') 

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        context['form']= LoginForm()
        #context['latest_articles'] = Article.objects.all()[:5]
        return context
 

class CompanyView(TemplateView):
    template_name = 'company.html'
     
    def post(self, request):
        #user_login = request.session.get('login', False)
        form = CompanyForm(request.POST) 
        form.is_valid()
        data = form.cleaned_data 
        print type(data['company_name']), data['company_name']
        result = APIServer.company_create( \
                           company_name=data['company_name'].encode('utf8'), \
                           company_sname=data['company_sname'].encode('utf8'),\
                           organization_code=data['organization_code'],\
                           company_stand_type=data['company_stand_type'],\
                           company_address=data['company_address'].encode('utf8'), \
                           certificate_number=data['certificate_number'],\
                           business_type_code=data['business_type_code'],)
        print result
        return HttpResponseRedirect('/department/') 

   
    def get_context_data(self, **kwargs):
        context = super(CompanyView, self).get_context_data(**kwargs)
        context['form']= CompanyForm()
        #context['latest_articles'] = Article.objects.all()[:5]
        return context



class CreateDepartmentView(TemplateView):

    def post(self, request):
        data = request.POST
        name = data['name'].encode('utf8')
        short_name = data['short_name'].encode('utf8')
        org_type = ORG_TYPE_DEPARTMENT
        parent_id = int(data['parent_id'])
        org = APIServer.create_org(name=name,\
                             short_name=short_name, \
                             type=org_type, \
                             parent_id=parent_id)
        import json
        data = json.dumps(org)
        return HttpResponse(data) 



class UpdateDepartmentView(TemplateView):

    def post(self, request):
        data = request.POST
        org_id = int(data['org_id'])
        name = data['name'].encode('utf8')
        short_name = data['short_name'].encode('utf8')
        org_type = ORG_TYPE_DEPARTMENT
        parent_id = int(data['parent_id'])

        if org_id == parent_id:
            return HttpResponse(status=400, \
                content="parent_id is same with org_id") 


        org = APIServer.update_org(org_id, \
                            name=name,\
                            short_name=short_name, \
                            type=org_type, \
                            parent_id=parent_id)
        data = json.dumps(org)
        return HttpResponse(data) 


class UpdateOrgUserView(TemplateView):

    def post(self, request):
        data = request.POST
        user_id = int(data['user_id'])
        user_name = data['user_name'].encode('utf8')
        email = data['email'].encode('utf8')
        mobile_number = data['mobile_number']
        id_number = data['id_number']
        org_id = int(data['org_id'])
        old_org_id = int(data['old_org_id'])
        job_title = data['job_title'].encode('utf8')
        job_type=data['job_type'].encode('utf8')
        role_id = int(data['role_id'])
        org = APIServer.update_orguser(\
                user_id, \
                user_name=user_name,\
                email=email, \
                mobile_number=mobile_number, \
                id_number=id_number,\
                org_id=org_id,\
                old_org_id=old_org_id,\
                job_title=job_title, \
                job_type=job_type, \
                role_id = role_id)

        data = json.dumps(org)
        return HttpResponse(data) 



class CreateOrgUserView(TemplateView):

    def post(self, request):
        orguser = request.session.get('orguser', None)
        if orguser is None:
            return HttpResponseRedirect('/') 
 
        data = request.POST
        user_name=data['user_name'].encode('utf8')
        email=data['email'].encode('utf8')
        mobile_number=data['mobile_number']
        id_number=data['id_number']
        org_id=data['org_id']
        job_title=data['job_title'].encode('utf8')
        job_type= int(data['job_type'])
        role_id = int(data['role_id'])
        domain_id = orguser['base_info']['domain_id']


        user = APIServer.create_orguser(
                   user_name=user_name,\
                   email=email, \
                   mobile_number=mobile_number, \
                   id_number=id_number,\
                   org_id=org_id,\
                   job_title=job_title, \
                   job_type=job_type, \
                   role_id=role_id, \
                   domain_id=domain_id)

        import json
        data = json.dumps(user)
        return HttpResponse(data) 




class DeleteDepartmentView(TemplateView):
    def get(self, request):
        data = request.GET
        org_id = int(data['org_id'])
        org = APIServer.delete_org(org_id)
        data = json.dumps(org)
        return HttpResponse(data) 


class DeleteOrgUserView(TemplateView):
    def get(self, request):
        data = request.GET
        user_id = int(data['user_id'])
        org = APIServer.delete_orguser(user_id)
        data = json.dumps(org)
        return HttpResponse(data) 





class GetDepartmentSetView(TemplateView):
    def get(self, request):
        data = request.GET
        org_id = int(data['org_id'])
        org_sub_set =  APIServer.retrieve_organization_set(org_id)
        import json
        data = json.dumps(org_sub_set)
        return HttpResponse(data) 


class GetDepartmentUserSetView(TemplateView):

    def get(self, request):
        data = request.GET
        org_id = int(data['org_id'])
        page_num = 1
        try:
            page_num = int(data['page_num'])
        except KeyError:
            pass

        orguser_set =  APIServer.retrieve_orguser_set(org_id,page_num)

        result_list = []
        for i in orguser_set:
            a = {'user_id': i['base_info']['user'],\
                 'name': i['base_info']['name'], \
                 'role': i['role']['role_name'], \
                 'org_id': i['org']['id'], \
                 'org':  i['org']['name'], \
                 'job_title': i['org2user']['job_title'], \
                 'job_type': i['org2user']['job_type'], \
                 'mobile_number': i['base_info']['mobile_number'], \
                 'id_number': i['base_info']['id_number'], \
                 'email': i['base_info']['email'], \
                 'status':i['org2user']['status']}
            result_list.append(a) 
        import json
        data = json.dumps(result_list)
        return HttpResponse(data) 

class GetFirstLevelOrgUserSetView(TemplateView):

    def get(self, request):
        data = request.GET
        org_id = int(data['org_id'])

        orguser_set =  APIServer.retrieve_first_level_orguser_set(org_id)
        import json
        data = json.dumps(orguser_set)
        return HttpResponse(data) 






class WorkView(TemplateView):
    def get(self, request):
        orguser = request.session.get('orguser', None)
        #if None == orguser:
        #    return HttpResponseRedirect('/') 
        try: 
            role_id =  orguser['role']['role_id']
        except:
            role_id = 0
        para = { \
            'role_id': role_id,
            'orguser': orguser,
        }

        t = TemplateResponse(request, 'work.html', para)
        return t

class AdminView(TemplateView):
    def get(self, request):
        orguser = request.session.get('orguser', None)
        if orguser is None:
            return HttpResponseRedirect('/') 
   
        user_name = orguser['base_info']['name']
        domain_id = orguser['org']['domain_id'] 
        company_name = orguser['org']['name']
        role_id = orguser['role']['role_id']
        org2user = orguser['org2user']
        para = { \
            'user_name': user_name,
            'company_name': company_name,
            'company_id': domain_id, 
            'role_id': role_id
        }


        t = TemplateResponse(request, 'admin.html', para)
        return t

 
class LogoutView(TemplateView):
    def get(self, request):
        try:
            del request.session['user_id']
        except KeyError:
            pass
        try:
            del request.session['user_email']
        except KeyError:
            pass
        try:
            del request.session['orguser']
        except KeyError:
            pass
        return HttpResponseRedirect('/') 



class ContactMainView(TemplateView):
    def get(self, request):
        orguser = request.session.get('orguser', None)
        if orguser is None:
            return HttpResponseRedirect('/') 
        data = request.GET
        org_id = data.get('org_id', None)
        if org_id is None:
            org_id = orguser['org']['domain_id'] 
        user_name = orguser['base_info']['name']
        role_id = orguser['role']['role_id']
        org2user = orguser['org2user']
 
        para = { \
            'user_name': user_name,
            'org_id': org_id, 
            'role_id': role_id,
        }


        t = TemplateResponse(request, 'contact_main.html', para)
        return t

 


