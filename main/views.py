from main.auth import login
from main.models import Trips,User
from django.contrib import messages
from django.shortcuts import redirect, render
import bcrypt
from .decorators import login_required


@login_required
def index(request):

    triplist = Trips.objects.filter(travellers__id=int(request.session['user']['id'])) | Trips.objects.exclude(travellers__id=int(request.session['user']['id'])).filter(creator=int(request.session['user']['id']))
    finallist = list(set(triplist))
    user = User.objects.get(id=int(request.session['user']['id']))

    context = {
        'my_trips': finallist,
        'other_trips' : Trips.objects.exclude(travellers__id=int(request.session['user']['id'])),
        'user' : user
    }
    #import pdb; pdb.set_trace()
    return render(request, 'index.html', context)

@login_required
def destination(request,tripid):
    trip = Trips.objects.get(id=int(tripid))
    context = {'trip':Trips.objects.get(id=int(tripid)),
                'others':User.objects.filter(others_trips=trip).exclude(my_trip=trip)}
    return render(request,'destination.html',context)

@login_required
def add(request):
    if request.method == 'GET':
        return render(request,'add.html')
    
    errors = Trips.objects.basic_valid(request.POST)
    if len(errors) > 0:
            for key, error_msg in errors.items():
                messages.error(request, error_msg)
            return redirect('/add')
    
    newtrip = Trips.objects.create(dest=request.POST['dest'],plan=request.POST['plan'],date_from=request.POST['date_from'],date_to=request.POST['date_to'],creator=User.objects.get(id=int(request.session['user']['id'])))
    newtrip.travellers.add(User.objects.get(id=int(request.session['user']['id'])))
    messages.success(request,"Trip has been Succesfully created")
    return redirect('/')

@login_required
def join(request,tripid):
    trip = Trips.objects.get(id=tripid)
    trip.travellers.add(User.objects.get(id=int(request.session['user']['id'])))
    messages.success(request,f"Succesfully Joined the Trip")
    return redirect('/')

@login_required
def cancel(request,tripid):
    trip = Trips.objects.get(id=tripid)
    trip.travellers.remove(User.objects.get(id=int(request.session['user']['id'])))
    messages.warning(request,"You Left The Trip")
    return redirect('/')

@login_required
def delete(request,tripid):
    trip = Trips.objects.get(id=tripid)
    trip.delete()
    messages.warning(request,"Trip Deleted")
    return redirect('/')



