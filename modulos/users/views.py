from django.contrib import messages
from django.shortcuts import render
from django.views.generic import TemplateView, View, ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.views.generic.edit import ModelFormMixin
from .forms import UsersForm, MunicipioForm, RegionForm
from .models import Users, Municipio, Region
from modulos.auditor.views import log_actualizado, log_registro
from django.urls import reverse_lazy

from .serializers import UsersSerializer, MunicipioSerializer, ListMunicipioSerializer, RegionSerializer
from .serializers import ListRegionSerializer
from liderpythondjango.permission import ModelPermission
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404


class Panel(TemplateView):
    template_name = "base.html"

    def dispatch(self, *args, **kwargs):
        return super(Panel, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(Panel, self).get_context_data(**kwargs)
        return context


class Login(View):
    @staticmethod
    def get(request):
        if request.user:
            if request.user.is_active:
                return HttpResponseRedirect(reverse_lazy('users:base'))
        return render(request, 'inicio.html')

    @staticmethod
    def post(request):
        if request.method == 'POST':
            username = request.POST['usu']
            password = request.POST['passwd']
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    messages.success(request, "Login exitoso")
                    return HttpResponseRedirect(reverse_lazy('users:base'))
                else:
                    messages.warning(request, "Usuario invalido")
                    return HttpResponseRedirect(reverse_lazy('users:login'))
            else:
                messages.warning(request, "Login invalido")
                return HttpResponseRedirect(reverse_lazy('users:login'))
        else:
            return HttpResponseRedirect(reverse_lazy('users:login'))


def exit(request):
    if request.user:
        messages.success(request, "We will wait for you.")
        logout(request)
    return HttpResponseRedirect('/')


# User
class Rus(CreateView):
    template_name = 'formadmin.html'
    form_class = UsersForm
    model = Users

    def get_form_kwargs(self):
        kwargs = super(ModelFormMixin, self).get_form_kwargs()
        kwargs.update({'instance': self.object})
        kwargs.update({'request': self.request})
        return kwargs

    def get_success_url(self):
        messages.success(self.request, "User created")
        return reverse_lazy('users:base')

    def get_context_data(self, **kwargs):
        context = super(Rus, self).get_context_data(**kwargs)
        context['tit_cont'] = 'Create'
        context['sub_tit_cont'] = ' user'
        return context

    def form_valid(self, form):
        form.instance.set_password(form.instance.password)
        form.instance.pro = self.request.user
        if form.has_changed:
            log_registro(form.instance, self.request.user, {"fields": form.changed_data})
        return super(Rus, self).form_valid(form)


# Municipio
class LisMun(ListView):
    template_name = 'municipio/lis.html'
    model = Municipio
    paginate_by = 30

    def get_queryset(self):
        qs = Municipio.objects.all()
        nom = self.request.GET.get('nom', None)
        if nom:
            qs = qs.filter(nombre__icontains=nom)
        return qs

    def get_context_data(self, **kwargs):
        context = super(LisMun, self).get_context_data(**kwargs)
        tot = len(self.get_queryset())
        context["tot"] = tot
        context['tit_cont'] = 'Listado'
        context['sub_tit_cont'] = ' de municipios'
        nom = self.request.GET.get('nom', None)
        if nom:
            context["nom"] = nom
        return context


class RegMun(CreateView):
    template_name = 'formadmin.html'
    form_class = MunicipioForm
    model = Municipio

    def get_form_kwargs(self):
        kwargs = super(ModelFormMixin, self).get_form_kwargs()
        kwargs.update({'instance': self.object})
        kwargs.update({'request': self.request})
        return kwargs

    def get_success_url(self):
        messages.success(self.request, "Municipio registrado")
        return reverse_lazy('users:lis_mun')

    def get_context_data(self, **kwargs):
        context = super(RegMun, self).get_context_data(**kwargs)
        context['tit_cont'] = 'Crear'
        context['sub_tit_cont'] = ' municipio'
        return context

    def form_valid(self, form):
        form.instance.nombre = form.instance.nombre.upper()
        if form.has_changed:
            log_registro(form.instance, self.request.user, {"fields": form.changed_data})
        return super(RegMun, self).form_valid(form)


class UpdMun(UpdateView):
    template_name = 'formadmin.html'
    form_class = MunicipioForm
    model = Municipio

    def get_form_kwargs(self):
        kwargs = super(ModelFormMixin, self).get_form_kwargs()
        kwargs.update({'instance': self.object})
        kwargs.update({'request': self.request})
        return kwargs

    def get_object(self, queryset=None):
        qs = Municipio.objects.get(pk=self.kwargs['pk'])
        return qs

    def get_success_url(self):
        messages.success(self.request, "Municipio Actualizado")
        return reverse_lazy('users:lis_mun')

    def get_context_data(self, **kwargs):
        context = super(UpdMun, self).get_context_data(**kwargs)
        context['tit_cont'] = 'Editar'
        context['sub_tit_cont'] = ' municipio'
        return context

    def form_valid(self, form):
        form.instance.nombre = form.instance.nombre.upper()
        if not form.instance.estado:
            for reg in Region.objects.filter(municipios=form.instance):
                print('----> ', reg, flush=True)
                reg.municipios.remove(form.instance)
        if form.has_changed:
            log_actualizado(form.instance, self.request.user, {"fields": form.changed_data})
        return super(UpdMun, self).form_valid(form)


class DelMun(DeleteView):
    template_name = 'del.html'
    model = Municipio

    def get_success_url(self):
        messages.success(self.request, "Municipio Eliminado")
        return reverse_lazy('users:lis_mun')

    def get_context_data(self, **kwargs):
        context = super(DelMun, self).get_context_data(**kwargs)
        context['tit_cont'] = 'Eliminar'
        context['sub_tit_cont'] = ' municipio'
        return context


# Region
class LisReg(ListView):
    template_name = 'region/lis.html'
    model = Region
    paginate_by = 30

    def get_queryset(self):
        qs = Region.objects.all()
        nom = self.request.GET.get('nom', None)
        if nom:
            qs = qs.filter(nombre__icontains=nom)
        return qs

    def get_context_data(self, **kwargs):
        context = super(LisReg, self).get_context_data(**kwargs)
        tot = len(self.get_queryset())
        context["tot"] = tot
        context['tit_cont'] = 'Listado'
        context['sub_tit_cont'] = ' de regiones'
        nom = self.request.GET.get('nom', None)
        if nom:
            context["nom"] = nom
        return context


class RegReg(CreateView):
    template_name = 'formadmin.html'
    form_class = RegionForm
    model = Region

    def get_form_kwargs(self):
        kwargs = super(ModelFormMixin, self).get_form_kwargs()
        kwargs.update({'instance': self.object})
        kwargs.update({'request': self.request})
        return kwargs

    def get_success_url(self):
        messages.success(self.request, "Region registrado")
        return reverse_lazy('users:lis_reg')

    def get_context_data(self, **kwargs):
        context = super(RegReg, self).get_context_data(**kwargs)
        context['tit_cont'] = 'Crear'
        context['sub_tit_cont'] = ' region'
        return context

    def form_valid(self, form):
        form.instance.nombre = form.instance.nombre.upper()
        if form.has_changed:
            log_registro(form.instance, self.request.user, {"fields": form.changed_data})
        return super(RegReg, self).form_valid(form)


class UpdReg(UpdateView):
    template_name = 'formadmin.html'
    form_class = RegionForm
    model = Region

    def get_form_kwargs(self):
        kwargs = super(ModelFormMixin, self).get_form_kwargs()
        kwargs.update({'instance': self.object})
        kwargs.update({'request': self.request})
        return kwargs

    def get_object(self, queryset=None):
        qs = Region.objects.get(pk=self.kwargs['pk'])
        return qs

    def get_success_url(self):
        messages.success(self.request, "Region actualizada")
        return reverse_lazy('users:lis_reg')

    def get_context_data(self, **kwargs):
        context = super(UpdReg, self).get_context_data(**kwargs)
        context['tit_cont'] = 'Editar'
        context['sub_tit_cont'] = ' region'
        return context

    def form_valid(self, form):
        form.instance.nombre = form.instance.nombre.upper()
        if form.has_changed:
            log_actualizado(form.instance, self.request.user, {"fields": form.changed_data})
        return super(UpdReg, self).form_valid(form)


class DelReg(DeleteView):
    template_name = 'del.html'
    model = Region

    def get_success_url(self):
        messages.success(self.request, "Region Eliminada")
        return reverse_lazy('users:lis_reg')

    def get_context_data(self, **kwargs):
        context = super(DelReg, self).get_context_data(**kwargs)
        context['tit_cont'] = 'Eliminar'
        context['sub_tit_cont'] = ' region'
        return context


# RESTFULAPI
class ApiLogin(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        if not user.is_active:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        if Token.objects.filter(user=user).exists():
            Token.objects.get(user=user).delete()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
        })


@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
class ApiLogout(APIView):

    def get(self, request):
        request.user.auth_token.delete()
        return Response({'detail': 'Logout is success'}, status=HTTP_200_OK)


# User
@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated, ModelPermission])
class ApiRus(CreateAPIView):
    serializer_class = UsersSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.pro = self.request.user
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        log_registro(serializer, self.request.user, {"fields": []})
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


# Municipio
@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated, ModelPermission])
class ApiLisMun(ListAPIView):
    serializer_class = ListMunicipioSerializer

    def get_queryset(self):
        qs = Municipio.objects.all()
        nom = self.request.query_params.get('nom', None)
        if nom:
            qs = qs.filter(nombre__icontains=nom)
        return qs


@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated, ModelPermission])
class ApiRegMun(CreateAPIView):
    queryset = Municipio.objects.all()
    serializer_class = MunicipioSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        print(serializer.instance, dir(serializer.instance), flush=True)

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        serializer.instance.nombre = str(serializer.instance.nombre).upper()
        serializer.instance.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated, ModelPermission])
class ApiUpdMun(UpdateAPIView):
    queryset = Municipio.objects.all()
    serializer_class = MunicipioSerializer

    def get_object(self):
        qs = Municipio.objects.get(pk=self.kwargs['pk'])
        return qs

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        serializer.instance.nombre = str(serializer.instance.nombre).upper()

        if not serializer.instance.estado:
            for reg in Region.objects.filter(municipios=serializer.instance):
                print('----> ', reg, flush=True)
                reg.municipios.remove(serializer.instance)
        serializer.instance.save()

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        log_actualizado(instance, self.request.user, {"fields": []})
        return Response(serializer.data)


@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated, ModelPermission])
class ApiDelMun(DestroyAPIView):
    queryset = Municipio.objects.all()
    serializer_class = MunicipioSerializer

    def get_object(self):
        obj = get_object_or_404(Municipio, id=self.kwargs['pk'])
        return obj


@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated, ModelPermission])
class MunicipioDetail(RetrieveAPIView):
    queryset = Municipio.objects.all()
    serializer_class = ListMunicipioSerializer


# Region
@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated, ModelPermission])
class ApiLisReg(ListAPIView):
    serializer_class = ListRegionSerializer

    def get_queryset(self):
        qs = Region.objects.all()
        nom = self.request.query_params.get('nom', None)
        if nom:
            qs = qs.filter(nombre__icontains=nom)
        return qs


@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated, ModelPermission])
class ApiRegReg(CreateAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        serializer.instance.nombre = str(serializer.instance.nombre).upper()
        serializer.instance.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated, ModelPermission])
class ApiUpdReg(UpdateAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer

    def get_object(self):
        qs = Region.objects.get(pk=self.kwargs['pk'])
        return qs

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        serializer.instance.nombre = str(serializer.instance.nombre).upper()
        serializer.instance.save()
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        log_actualizado(instance, self.request.user, {"fields": []})
        return Response(serializer.data)


@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated, ModelPermission])
class ApiDelReg(DestroyAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer

    def get_object(self):
        obj = get_object_or_404(Region, id=self.kwargs['pk'])
        return obj


@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated, ModelPermission])
class RegionDetail(RetrieveAPIView):
    queryset = Region.objects.all()
    serializer_class = ListRegionSerializer
