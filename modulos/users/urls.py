from django.urls import path
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .views import Login, Panel, exit
from .views import Rus, LisMun, RegMun, UpdMun, DelMun, LisReg, RegReg, UpdReg, DelReg
from .views import ApiLogin, ApiRus, ApiLisMun, ApiRegMun, ApiUpdMun, ApiDelMun, MunicipioDetail

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
    path('restfulapi/login/', ApiLogin, name='api_login'),
    path('restfulapi/salir/', exit, name='api_salir'),
    path(r'restfulapi/reg/usu/', login_required(ApiRus.as_view(), login_url=reverse_lazy('users:login')),
         name='api_rus'),
    # MODULOS
    path('restfulapi/lis/mov/', login_required(ApiLisMun.as_view(), login_url=reverse_lazy('users:login')),
         name='api_lis_mov'),
    path('restfulapi/reg/mov/', login_required(ApiRegMun.as_view(), login_url=reverse_lazy('users:login')),
         name='api_reg_mov'),
    path('restfulapi/upd/<int:pk>/mov/', login_required(ApiUpdMun.as_view(), login_url=reverse_lazy('users:login')),
         name='api_upd_mov'),
    path('restfulapi/del/<int:pk>/mov/', login_required(ApiDelMun.as_view(), login_url=reverse_lazy('users:login')),
         name='api_del_mov'),
    path('restfulapi/det/<int:pk>/mov/', login_required(MunicipioDetail.as_view(), login_url=reverse_lazy('users:login')),
         name='api_det_mov'),

]
