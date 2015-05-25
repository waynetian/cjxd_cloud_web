from django.conf.urls import include, url
#from django.contrib import admin

from .views import *

urlpatterns = [
    # Examples:
    # url(r'^$', 'web.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),


    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^register/', RegisterView.as_view(), name='register'),
    url(r'^logout/', LogoutView.as_view(), name='logout'),
    url(r'^login/', LoginView.as_view(), name='login'),
 

    url(r'^welcome/', WelcomeView.as_view(), name='welcome'),
    url(r'^try_user/', TryUserView.as_view(), name='try_user'),
    url(r'^work/', WorkView.as_view(), name='work'),
    url(r'^admin/', AdminView.as_view(), name='admin'),



    url(r'^create_department/', CreateDepartmentView.as_view(), name='create_department'),
    url(r'^delete_department/', DeleteDepartmentView.as_view(), name='delete_department'),
    url(r'^update_department/', UpdateDepartmentView.as_view(), name='update_department'),

    url(r'^create_orguser/', CreateOrgUserView.as_view(), name='create_orguser'),
    url(r'^delete_orguser/', DeleteOrgUserView.as_view(), name='delete_orguser'),
    url(r'^update_orguser/', UpdateOrgUserView.as_view(), name='update_user'),
 

    url(r'^get_department_set/', GetDepartmentSetView.as_view(), name='get_department_set'),

    url(r'^get_department_user_set/', GetDepartmentUserSetView.as_view(), name='get_department_user_set'),

    url(r'^get_first_level_org_user_set/', GetFirstLevelOrgUserSetView.as_view(), name='get_first_level_user_set'),






    url(r'^contact/', ContactMainView.as_view(), name='contact_main')


]
