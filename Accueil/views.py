from django.db.models.fields import DateField
from django.db.models.query import QuerySet
from django.http.response import HttpResponseNotFound
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import *
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime
from django.http import HttpResponse,Http404
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from .forms import UserRegisterForm


# Create your views here.
def home(request):
    
    list_conference = conference.objects.all().filter(date__gte= datetime.now())
    context ={"liste_conference":list_conference}
    return render(request,"Accueil.html",context)

def recherche(request):

    conferences=conference.objects.all()
    return render(request,"recherche.html",{'liste_conference':conferences})

def contact(request):
    note=''
    if request.method == 'POST':
        nom = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        data = {
            'nom': nom,
            'email':email,
            'message':message
        }
        mess= '''
         Nom: {}

         Nouvel message: {}

         From: {}
        '''.format(data['nom'],data['message'],data['email'])
        send_mail('Contact Form',mess,settings.EMAIL_HOST_USER,['dzconferencesdjango@gmail.com'],fail_silently=False)
        note="Email envoyée avec succée ,Merci de nous contacter"
        return render(request,"contact.html",{'note':note})
    else:

        return render(request,"contact.html",{'note':note})

    
    
#recherche avancé
def resultat(request):
   erreur=False
   if request.method =='GET':
     titre=request.GET.get('titre')
     auteur = request.GET.get('auteur')
     conf=request.GET.get('conference')
     motcle=request.GET.get('mot')
     dat=request.GET.get('date')
     articles=article.objects.all() 
     recherche=""
    
     if titre!='' and titre is not None:
         articles=articles.filter(titre__icontains=titre)
         recherche="\""+titre+"\""

     if dat !='' and dat is not None:
         
         articles= articles.filter(conférence__date__year=dat)

         if recherche!='':
            recherche="\""+dat+"\"" +" ET \"" +recherche +"\""
         else:
               recherche="\""+dat+"\""

     if auteur !='' and auteur is not None:
           
           articles1=articles.filter(auteurs__nom__icontains=auteur)
           articles2=articles.filter(auteurs__prenom__icontains=auteur)
           articles=articles1.union(articles2)

           if recherche!='':
            recherche="\""+auteur+"\"" +" ET \""+recherche+"\""
           else:
               recherche="\""+auteur+"\""


     if motcle !='' and motcle is not None :
         articles=articles.filter(motsClé__mot__icontains=motcle)
         
         if recherche!='':
            recherche="\""+motcle+"\"" +" ET \"" +recherche +"\""
         else:
               recherche="\""+motcle+"\""


     if conf!='' and conf is not None :
         articles_conf=conference.objects.get(nom=conf).Articles.all()
         articles=articles.intersection(articles_conf)

         if recherche!='':
            recherche="\""+conf+"\"" +" ET \""+ recherche +"\""
         else:
               recherche="\""+conf+"\""

     if titre==''and auteur==''and motcle=='' and conf=='' and dat=='':
         erreur=True
         conferences=conference.objects.all()
         return render(request,"recherche.html",{'erreur':erreur,'liste_conference':conferences})
        

     cpt =len(articles)
     
     return render(request,"resultat.html",{'articles':articles,'cpt':cpt,'recherche':recherche})
          




#recherche dans accueil
def resultatAccueil(request):
    if request.method =='GET':
     
     motcle=request.GET.get('mot')
     if motcle !='' and motcle is not None :
         articles=article.objects.all().filter(motsClé__mot__icontains=motcle)
         recherche=motcle
     
     cpt =len(articles) 
     
     return render(request,"resultat.html",{'articles':articles,'cpt':cpt,'recherche':recherche})



def ArticleDetailView(request,pk):
    art= article.objects.get(pk=pk)
    auteurs= art.auteurs.all()
    motsCle= art.motsClé.all()

    return render(request,"detail_article.html",{'article':art,'auteurs':auteurs,'motsCle':motsCle})


    

def conferenceView(request,conf):
    conf=conference.objects.get(nom=conf)
    return render(request, "detail_conference.html",{'conference':conf})

def conferenceArticles(request,conf):
    conf=conference.objects.get(nom=conf)
    articles=conf.Articles.all()
    cpt =len(articles)
    return render(request, "conference_articles.html",{'conference':conf,'articles':articles,'cpt':cpt})

def conferenceResultat(request,lettre):
    if lettre=='All':
        conferences=conference.objects.all()
    else:
      conferences=conference.objects.all().filter(nom__istartswith=lettre)
    cpt=len(conferences)
    lettre="\""+lettre+"\""
    return render(request, "resultat_conference.html",{"conferences":conferences,"cpt":cpt,"lettre":lettre})
    
def conferencePage(request):
    return render(request,"conference.html",)

def conferenceFilter(request):
 erreur=False
 if request.method =='GET':
    
    dat=request.GET.get('date')
    
    if dat !='' and dat is not None:
         
         conferences=conference.objects.all().filter(date__year=dat)
         cpt=len(conferences)
         return render(request, "resultat_conference_date.html",{"conferences":conferences,"recherche":dat,"cpt":cpt})   
            
    if dat=='':
        erreur=True
        return render(request,"conference.html",{'erreur':erreur})


    

def pdf_view(request,pk):
    art= article.objects.get(pk=pk).fichier.name
    fs=FileSystemStorage()
    filename= art
    if fs.exists(filename) :
      with fs.open(filename) as pdf:  
         response = HttpResponse(pdf,content_type='application/pdf')
         response['Content-Disposition'] = 'inline; filename=some_file.pdf'
         return response
    else:
        return HttpResponseNotFound('the request pdf was not found')



def inscrire(request):
  erreur=""
  note=""
  erreur2=""
  count=""
  if request.method == 'POST':
      nomUtilisateur=request.POST['username'],
      email=request.POST['email'],
      password= request.POST['password']
      passwordconfirm=request.POST['password_confirm']
      #name=get_object_or_404(User,username=nomUtilisateur)
      #count =User.objects.filter(username=nomUtilisateur).count()
      if password!= passwordconfirm :
         erreur= "le mot de passe est incorrect" 
         return render(request,"register.html",{'note':note, 'erreur':erreur, 'erreur2':erreur2})

      print(nomUtilisateur)
      try:
          count= User.objects.get(username=nomUtilisateur)

      except User.DoesNotExist:
         count= None

      print(count)

      if count is not None:
          erreur2 = "le nom d'utilisateur déjà existé"
          return render(request,"register.html",{'note':note, 'erreur':erreur, 'erreur2':erreur2})

      else:
              user=User.objects.create_user(username=request.POST['username'],
                                    email=request.POST['email'],
                                    password= request.POST['password'])

              user.is_staff=True 
              user.save()
              my_group = Group.objects.get(name='utilisateur') 
              my_group.user_set.add(user)
              note="L'inscription est faite avec succée"
              return render(request,"register.html",{'note':note, 'erreur':erreur, 'erreur2':erreur2})
    
  else:  
         return render(request,"register.html",{})


def new_user(request):
 note=""
 if request.method == 'POST':
    form = UserRegisterForm(request.POST)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password1')
        new_user = User.objects.create(username=username, email=email, password=password)
        new_user.set_password(password)
        new_user.is_staff=True 
        new_user.save()
        my_group = Group.objects.get(name='utilisateur') 
        my_group.user_set.add(new_user)
        note="L'inscription est faite avec succée"
        return render(request,"register.html",{'note':note, 'form':form})
       
 else:
    form = UserRegisterForm()

 return render(request, 'register.html', {'form': form})



