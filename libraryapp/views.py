

# Create your views here.

from django.http import HttpResponse,Http404
from datetime import datetime
from libapp.forms import SuggestionForm
from libapp.models import Book, Dvd, Libuser, Libitem, Suggestion
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.forms import ModelForm
from libapp.forms import SuggestionForm,SearchlibForm, newuserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.sessions.models import Session
from random import randint


# def index(request):
#     booklist = Book.objects.all() [:10]
#     dvdlist = Dvd.objects.all() [:5]
#     response = HttpResponse()
#     heading1 = '<p>' + 'List of books: ' + '</p>'
#     response.write(heading1)
#     for book in booklist:
#         para = '<p>' + str(book) + '</p>'
#         response.write(para)
#     heading2 = '<p>' + 'List of DVDs: ' + '</p>'
#     response.write(heading2)
#     sort = Dvd.objects.order_by('-pubyr')
#     for dvd in sort:
#         para = '<p>' + str(dvd) + '</p>'
#
#         response.write(para)
#
#     return response

def index(request):
    itemlist = Libitem.objects.all()
    if request.session.get('luckynum'):
        mynumber = request.session.get('luckynum')
    else:
        mynumber=0
    indexcontext = {'itemlist': itemlist, 'user_request': request.user, 'mynumber':mynumber, 'user_request': request.user}
    return render(request, 'libapp/index.html', indexcontext)

#
# def about(request):
#     response = HttpResponse()
#     para = '<p>' + 'This is a Library APP' + '</p>'
#     response.write(para)
#     return response


def about(request):

    context_dict = {}

    visits = request.session.get('visits')
    if not visits:
        visits = 1
    reset_last_visit_time = False

    last_visit = request.session.get('last_visit')
    if last_visit:
        last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")

        if (datetime.now() - last_visit_time).seconds > 0:
            # ...reassign the value of the cookie to +1 of what it was before...
            visits = visits + 1
            # ...and update the last visit cookie, too.
            reset_last_visit_time = True
    else:
        # Cookie last_visit doesn't exist, so create it to the current date/time.
        reset_last_visit_time = True

    if reset_last_visit_time:
        request.session['last_visit'] = str(datetime.now())
        request.session['visits'] = visits
        context_dict['visits'] = visits

    if request.session.get('visits'):
        count = request.session.get('visits')
    else:
        count = 0

    context_dict = {'visits': count, 'user_request': request.user}
    response = render(request, 'libapp/about.html', context_dict)

    return response

# def detail(request,item_id):
#
#     booklist = Book.objects.all()
#     dvdlist = Dvd.objects.all()
#     response = HttpResponse()
#     heading1 = '<p>' + 'List of Books/Dvd\'s' + '</p>'
#     response.write(heading1)
#     isBook = 0
#     isDvd = 0
#
#     for book in booklist:
#         # response.write(book.id)
#         # response.write(item_id)
#         if book.id == int(item_id):
#             para = '<p>' + str(book.title)+' '+str(book.author)+' '+str(book.duedate)+' '+str(book.itemtype)+ '</p>'
#             response.write(para)
#             isBook = 1
#             break
#         else:
#             isBook = 0
#
#
#
#     for dvd in dvdlist:
#         # response.write(isBook)
#         if dvd.id == int(item_id):
#             para = '<p>' + str(dvd.title)+' '+str(dvd.maker)+' '+str(dvd.duedate)+' '+str(dvd.itemtype)+ '</p>'
#             response.write(para)
#             isDvd = 1
#             break
#         else:
#             isDvd = 0
#
#     if(isBook == 0 and isDvd == 0):
#         raise Http404
#
#     return response

def detail(request,item_id):
    item =  get_object_or_404(Libitem, id=item_id)
    # item = Libitem.objects.get(id=item_id)
    response = HttpResponse()
    if item.itemtype == 'Book':
        data = Book.objects.get(id=item_id)
    else:
        data = Dvd.objects.get(id= item_id)

    #
    # booklist = Book.objects.all()[:10]
    # dvdlist = Dvd.objects.all()[:5]
    mycontext = {'data':data, 'item':item, 'user_request': request.user}
    return render(request, 'libapp/detail.html', mycontext)

def suggestions(request):
    suggestionlist = Suggestion.objects.all()[:10]
    return render(request, 'libapp/suggestions.html', {'itemlist': suggestionlist, 'user_request': request.user})

def newitem(request):
    suggestions = Suggestion.objects.all()
    if request.method == 'POST':
        form = SuggestionForm(request.POST)
        if form.is_valid():
            suggestion = form.save(commit=False)
            suggestion.num_interested = 1
            suggestion.save()
            return HttpResponseRedirect(reverse('libapp:suggestions'))
        else:
            return render(request, 'libapp/newitem.html', {'form':form, 'suggestions':suggestions, 'user_request': request.user})
    else:
        form = SuggestionForm()
        return render(request, 'libapp/newitem.html', {'form':form, 'suggestions':suggestions, 'user_request': request.user})

def searchlib(request):

        form = SearchlibForm()
        if request.method == 'GET':
            return render(request, 'libapp/search.html', {'form': form, 'user_request': request.user})

        else:
            form = SearchlibForm()
            if request.POST.get("title") != '':
                q = request.POST.get("title")
                booklist = Book.objects.filter(title__contains=q)
                dvdlist = Dvd.objects.filter(title__contains=q)
                if request.POST.get("author") != '':
                    r = request.POST.get("author")
                    booklist = booklist.filter(author__contains=r)
                    dvdlist = dvdlist.filter(maker__contains=r)
                return render(request,'libapp/search.html',{'booklist':booklist,'dvdlist':dvdlist,'form':form, 'user_request': request.user})
            elif request.POST.get("author") != '':
                q = request.POST.get("author")
                booklist = Book.objects.filter(author__contains=q)
                dvdlist = Dvd.objects.filter(maker__contains=q)
                return render(request, 'libapp/search.html', {'booklist': booklist, 'dvdlist': dvdlist,'form':form, 'user_request': request.user})
            else:
                return render(request, 'libapp/search.html',{'form': form, 'user_request': request.user})





def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        random_number = randint(1,9)
        request.session['luckynum'] = random_number
        if user:
            if user.is_active:
                login(request, user)
                request.session.set_expiry(3600)
                return HttpResponseRedirect(reverse('libapp:index'))
            else:
                return HttpResponse('Your account is disabled.')
        else:
            return HttpResponse('Invalid login details.')
    else:
        return render(request, 'libapp/login.html', { 'user_request': request.user})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse(('libapp:index')))

def myitems(request):
    if request.user.is_active:
        temp = request.user.email
        mydvd = Dvd.objects.all().filter(user__email= temp).filter(checked_out=True)
        mybook = Book.objects.all().filter(user__email=temp).filter(checked_out=True)
        return render(request, 'libapp/myitems.html', {'mydvd': mydvd, 'temp': temp, 'mybook':mybook, 'user_request': request.user })

    else:
        return HttpResponse('You are not Libuser')


def register(request):
    if request.method == 'POST':
        form = newuserForm(request.POST)
        if form.is_valid():
            suggestion = form.save(commit=False)
            suggestion.num_interested = 1
            suggestion.save()
            return HttpResponseRedirect(reverse('libapp:login'))
        else:
            return render(request, 'libapp/register.html', { 'user_request': request.user})

    else:

        form = newuserForm()
        return render(request, 'libapp/register.html', {'form':form, 'user_request': request.user})

def base(request):
    return render(request, 'libapp/base.html', {'user_request': request.user})