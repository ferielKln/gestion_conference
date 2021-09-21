from django.contrib import admin
from django.urls import path,re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url 
from django.views.static import serve

urlpatterns = [
    path('',views.home, name='home'),
    path('recherche/',views.recherche, name='recherche'), 
    path('contact/',views.contact,name='contact'),
    path('resultat/',views.resultat,name='resultat'),
    path('resultat/',views.resultatAccueil,name='resultatAccueil'),
    path('article/<int:pk>/',views.ArticleDetailView,name='detail_article'),
    path('conference/<str:conf>/',views.conferenceView,name='detail_conference'),
    path('conference/<str:conf>/articles',views.conferenceArticles,name='conference_articles'),
    path('conferences/<str:lettre>/',views.conferenceResultat,name='resultat_conference'),
    path('conferences/',views.conferenceFilter,name='conferencedate'),
    path('conference/',views.conferencePage,name='conference'),
    path('view_pdf/<int:pk>/',views.pdf_view,name='view_pdf'), 
    path('inscrire/',views.new_user,name='register'),
    url(r'^download/(?P<path>.*)$',serve,{'document_root':settings.MEDIA_ROOT}),

]

if settings.DEBUG:
    urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

