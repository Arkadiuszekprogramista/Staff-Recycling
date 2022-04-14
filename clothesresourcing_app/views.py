from django.views import View
from django.shortcuts import render, redirect
from clothesresourcing_app.models import Donation, Institution, Category
from clothesresourcing_app.forms import RegisterUserForm, LoginForm, AddDonationForm, MyUserCreation, PickUpForm,\
    ContactForm, UserSettingsForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.core.paginator import Paginator
from django.db.models import Sum
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages



class LandingPageView(View):
    def get(self, request):
        quantity = Donation.objects.all().aggregate(Sum('quantity'))
        quantity = quantity['quantity__sum']
        count = Institution.objects.all().count()
        foundation = list(Institution.objects.filter(type=1))
        organization = list(Institution.objects.filter(type=2))
        local_collection = list(Institution.objects.filter(type=3))

        categories = Category.objects.values('institution')

        paginator = Paginator(foundation, 1)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        paginator_organization = Paginator(organization, 1)
        page_number_organization = request.GET.get('page')
        page_obj_organization = paginator_organization.get_page(page_number_organization)

        paginator_local_collection = Paginator(local_collection, 2)
        page_number_local_collection = request.GET.get('page')
        page_obj_local_collection = paginator_local_collection.get_page(page_number_local_collection)

        return render(request, 'index.html', {
            'quantity': quantity,
            'count': count,
            'foundation': foundation,
            'organization': organization,
            'local_collection': local_collection,
            'page_obj': page_obj,
            'page_obj_organization': page_obj_organization,
            'page_obj_local_collection': page_obj_local_collection,
            'categories': categories,
        })


class AddDonationView(LoginRequiredMixin, View):
    def get(self, request):

        form = AddDonationForm()
        category = Category.objects.all()
        institution = Institution.objects.all()

        return render(request, 'form.html', {
            'category': category,
            'institution': institution,
            'form': form,
        })


@login_required(login_url='/accounts/login/')
def get_institution_by_category(request):
    categories_ids = request.GET.getlist('categories_ids')
    if categories_ids is not None:
        institution = Institution.objects.filter(categories__in=categories_ids).distinct()
    else:
        institution = Institution.objects.all()

    return render(request, "api_institution.html", {
        'institution': institution,
        'categories_ids': categories_ids,
        'form': MyUserCreation,
    })


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            try:
                User.objects.get(username=username) == None
            except ObjectDoesNotExist:
                return redirect('/register/#registration')
            else:
                user = authenticate(username=username, password=password)
                login(request, user)
                return redirect('/')
        else:
            return render(request, 'login.html', {'form': form})


class RegisterView(View):
    def get(self, request):
        form = RegisterUserForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['email']
            email = username
            password = form.cleaned_data['password1']
            first_name = form.cleaned_data['name']
            last_name = form.cleaned_data['surname']
            User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
            )
            return redirect('/login/#login')
        else:
            return render(request, 'register.html', {'form': form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('/')


class ProfilView(LoginRequiredMixin, View):
    def get(self, request):
        form = PickUpForm()
        user = request.user.id
        donation = Donation.objects.filter(user_id=user).order_by('is_taken').order_by('pick_up_date')
        donation_ids = Donation.objects.filter(user_id=user).values('id')
        categories = Category.objects.all().filter(donation__id=donation_ids)
        return render(request, 'profile.html', {
            'donation': donation,
            'categories': categories,
            'donation_ids': donation_ids,
            'form': form,
        })

    def post(self, request):
        form = PickUpForm(request.POST)
        user = request.user.id
        donation = Donation.objects.filter(user_id=user).order_by('is_taken').order_by('pick_up_date')
        donation_ids = Donation.objects.filter(user_id=user).values('id')
        categories = Category.objects.all().filter(donation__id=donation_ids)
        value = request.POST.get('update')
        if form.is_valid():
            if form.cleaned_data['is_taken'] == True:
                donation.filter(id=value).update(is_taken=True)
                return render(request, 'profile.html', {
                    'donation': donation,
                    'categories': categories,
                    'donation_ids': donation_ids,
                    'form': form,
                })
            else:
                redirect('/')

        return render(request, 'profile.html', {
            'donation': donation,
            'categories': categories,
            'donation_ids': donation_ids,
            'form': form,
        })


class FormSaveView(LoginRequiredMixin, View):
    def post(self, request):
        categories = request.POST.get('categories')
        quantity = request.POST.get('bags')
        institution = request.POST.get('organization')
        try:
            organization = Institution.objects.get(id=institution)
            category = Category.objects.get(id=categories)
        except ObjectDoesNotExist:
            organization = None
            category = None
        else:
            street = request.POST.get('address')
            city = request.POST.get('city')
            post = request.POST.get('postcode')
            phone = request.POST.get('phone')
            data = request.POST.get('data')
            time = request.POST.get('time')
            comments = request.POST.get('more_info')
            user = request.user.id
            email = request.user.email
            donation = Donation.objects.create(
                quantity=quantity,
                institution_id=institution,
                address=street,
                city=city,
                zip_code=post,
                phone_number=phone,
                pick_up_date=data,
                pick_up_time=time,
                pick_up_comment=comments,
                user_id=user,
            )
            donation.categories.set(categories)
            donation.save()

            send_mail(subject="Donation confirmation",
                      message=f"""Twoja donacja:
                              Ilość worków: {quantity} z {category}
                              Organizacja wspierana {organization}
                              Adres odbioru:
                              {street}
                              {city} {post}
                              Data odbioru:
                              {data} o godzinie {time}
                              Dziękujemy, i pamiętaj dobre uczynki zawsze wracają !""",
                      from_email='donation-confirmation@example.com',
                      recipient_list=[email]
                      )

            return render(request, 'form-save.html', {
                'quantity': quantity,
                'institution': institution,
                'street': street,
                'city': city,
                'post': post,
                'phone': phone,
                'data': data,
                'time': time,
                'comments': comments,
                'organization': organization,
                'category': category,
            })

        return redirect('/confirmation/#confirmation')


class ConfirmationView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'form-confirmation.html')


class ContactFormView(View):
    def get(self, request):
        form = ContactForm()
        name = request.user.first_name
        surname = request.user.last_name
        email = request.user.email
        return render(request, 'base.html', {
            'form': form,
            'name': name,
            'surname': surname,
            'email': email,
        })


class ProfileSettingsView(LoginRequiredMixin, View):
    def get(self, request):
        form = UserSettingsForm()
        return render(request, 'profil_settings.html',{'form': form})
