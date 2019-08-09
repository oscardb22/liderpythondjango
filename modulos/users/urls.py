from django.urls import path
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .views import Login, Panel, exit
from .views import Rus, LisMun, RegMun, UpdMun, DelMun, LisReg, RegReg, UpdReg, DelReg
from .views import ApiLogin, ApiRus, ApiLisMun, ApiRegMun, ApiUpdMun, ApiDelMun, MunicipioDetail
from .views import ApiLisReg, ApiRegReg, ApiUpdReg, ApiDelReg, RegionDetail, ApiLogout

urlpatterns = [
    path('', Login.as_view(), name='login'),
    path('salir/', exit, name='salir'),
    path('start/',
         login_required(Panel.as_view(), login_url=reverse_lazy('users:login')), name='base'),
    path('reg/usu/', login_required(Rus.as_view(), login_url=reverse_lazy('users:login')), name='rus'),
    # Municipios
    path('lis/mun/', login_required(LisMun.as_view(), login_url=reverse_lazy('users:login')), name='lis_mun'),
    path('reg/mun/', login_required(RegMun.as_view(), login_url=reverse_lazy('users:login')), name='reg_mun'),
    path('upd/<int:pk>/mun/', login_required(UpdMun.as_view(), login_url=reverse_lazy('users:login')), name='upd_mun'),
    path('del/<int:pk>/mun/', login_required(DelMun.as_view(), login_url=reverse_lazy('users:login')), name='del_mun'),
    # Regiones
    path('lis/reg/', login_required(LisReg.as_view(), login_url=reverse_lazy('users:login')), name='lis_reg'),
    path('reg/reg/', login_required(RegReg.as_view(), login_url=reverse_lazy('users:login')), name='reg_reg'),
    path('upd/<int:pk>/reg/', login_required(UpdReg.as_view(), login_url=reverse_lazy('users:login')), name='upd_reg'),
    path('del/<int:pk>/reg/', login_required(DelReg.as_view(), login_url=reverse_lazy('users:login')), name='del_reg'),

    # RESTful API
    path('restfulapi/login/', ApiLogin.as_view()),
    path('restfulapi/salir/', ApiLogout.as_view()),
    path(r'restfulapi/reg/usu/', ApiRus.as_view()),
    # Municipio
    path('restfulapi/lis/mun/', ApiLisMun.as_view()),
    path('restfulapi/reg/mun/', ApiRegMun.as_view()),
    path('restfulapi/upd/<int:pk>/mun/', ApiUpdMun.as_view()),
    path('restfulapi/del/<int:pk>/mun/', ApiDelMun.as_view()),
    path('restfulapi/det/<int:pk>/mun/', MunicipioDetail.as_view()),
    # Region
    path('restfulapi/lis/reg/', ApiLisReg.as_view()),
    path('restfulapi/reg/reg/', ApiRegReg.as_view()),
    path('restfulapi/upd/<int:pk>/reg/', ApiUpdReg.as_view()),
    path('restfulapi/del/<int:pk>/reg/', ApiDelReg.as_view()),
    path('restfulapi/det/<int:pk>/reg/', RegionDetail.as_view()),
    # LOGICA
    path('restfulapi/logica/<int:pk>/respuesta/', RegionDetail.as_view()),
]
