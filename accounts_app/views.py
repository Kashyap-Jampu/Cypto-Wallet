from django.shortcuts import render, HttpResponse,redirect
import binascii
from django.contrib.auth import authenticate,login,logout
from Crypto.PublicKey import RSA
import Crypto.Random
from Crypto.Hash import SHA256
from utility.transaction import Transaction
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import User,Blockchain
from django.http import JsonResponse
from Crypto.Signature import PKCS1_v1_5
from utility.blockchain import *

# Create your views here.
def home(request):
    return render(request,"home.html")


def register_view(request):
    if request.method=='POST':
        username=request.POST['name']
        email=request.POST['email']
        password=request.POST['psw']
        private_key = RSA.generate(1024, Crypto.Random.new().read)
        public_key = private_key.publickey()

        private_key = binascii.hexlify(private_key.exportKey(format='DER')).decode('ascii')
        public_key = binascii.hexlify(public_key.exportKey(format='DER')).decode('ascii')
        while User.objects.filter(public_key=public_key).exists():
            private_key = RSA.generate(1024, Crypto.Random.new().read)
            public_key = private_key.publickey()
            private_key = binascii.hexlify(private_key.exportKey(format='DER')).decode('ascii')
            public_key = binascii.hexlify(public_key.exportKey(format='DER')).decode('ascii')


        if User.objects.filter(email=email).exists():
            #messages.info(request,'EMAIL ALREADY IN USE ')
            return render(request,'signup.html')

        else:
            users=User.objects.create_user(username=username,password=password,
            email=email,public_key=public_key,private_key=private_key)
            users.save()
            return redirect("home")


            # Create and save the png file naming "myqr.png"

        return response
    return render(request,'signup.html')


def login_view(request):
    if request.method=='POST':
        email=request.POST['email']
        password=request.POST['psw']
        users = authenticate(request, email=email, password=password)

        if users is not None:
            login(request, users)
            print(users.id)
            return redirect('add_transaction')

        else:
            messages.info(request,'ERROR IN LOGIN!!!')


    return render(request,'login.html')
@login_required
def logout_view(request):
    logout(request)
    return redirect('home')




@login_required
def add_transaction(request):
    
    if request.method=="POST":

        #receiver=int(request.POST['receiver'])
        sender=request.user
        spk=sender.public_key
        receiver_id=int(request.POST['user_id'])
        receiver=User.objects.get(id=receiver_id).public_key

        blockchain=Blockchainn(sender.public_key)
        amount=int(request.POST['amount'])
        signer = PKCS1_v1_5.new(RSA.importKey(
            binascii.unhexlify(sender.private_key)))
        h = SHA256.new((str(spk) + str(receiver) +
                        str(amount)).encode('utf8'))
        signature = signer.sign(h)
        print(signature)
        sign= binascii.hexlify(signature).decode('ascii')
        print(sign)
        if blockchain.add_transaction(sender.public_key,receiver,amount,sign):
            print("success")
        else:
            print("failure")
    bc=Blockchainn(request.user.public_key)
    users=User.objects.all()
    balance=bc.get_balance(request.user.public_key)
    return render(request,"add_tx.html",{"users":users,"balance":balance})

@login_required
def mine_view(request):
    sender=request.user
    blockchain=Blockchainn(sender.public_key)
    if blockchain.mine():
        print("Blockmined")
        
    else:
        print("Error while mining")

    return redirect("add_transaction")    
    
