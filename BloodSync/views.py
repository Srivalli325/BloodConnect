from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

from .models import Donor, BloodRequest, UserSecurity


# =====================================
# FORGOT PASSWORD
# =====================================
def forgot_password(request):

    if request.method == "POST":

        username = request.POST.get("username")
        question = request.POST.get("security_question")
        answer = request.POST.get("security_answer").lower()

        try:
            user = User.objects.get(username=username)
            profile = UserSecurity.objects.get(user=user)

            if profile.security_question == question and profile.security_answer == answer:
                request.session["reset_user"] = user.id
                return redirect("reset_password")

            return render(request, "forgot_password.html", {
                "error": "Incorrect security details"
            })

        except User.DoesNotExist:
            return render(request, "forgot_password.html", {
                "error": "User not found"
            })

        except UserSecurity.DoesNotExist:
            return render(request, "forgot_password.html", {
                "error": "Security question not set for this user"
            })

    return render(request, "forgot_password.html")


# =====================================
# RESET PASSWORD
# =====================================
def reset_password(request):

    user_id = request.session.get("reset_user")

    if not user_id:
        return redirect("login")

    user = User.objects.get(id=user_id)

    if request.method == "POST":

        password = request.POST.get("new_password")
        confirm = request.POST.get("confirm_password")

        if password != confirm:
            return render(request, "reset_password.html", {
                "error": "Passwords do not match"
            })

        user.set_password(password)
        user.save()

        del request.session["reset_user"]

        return redirect("login")

    return render(request, "reset_password.html")


# =====================================
# REGISTER
# =====================================
def register_view(request):

    if request.method == "POST":

        full_name = request.POST.get("full_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            return render(request, "register.html", {
                "error": "Passwords do not match."
            })

        if User.objects.filter(username=username).exists():
            return render(request, "register.html", {
                "error": "Username already exists."
            })

        if User.objects.filter(email=email).exists():
            return render(request, "register.html", {
                "error": "Email already exists."
            })

        first_name = full_name.split()[0]

        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            email=email,
            password=password
        )

        # SAVE SECURITY DATA
        UserSecurity.objects.create(
            user=user,
            security_question=request.POST.get("security_question"),
            security_answer=request.POST.get("security_answer").lower()
        )

        messages.success(request, "Registration Successful. Please Login.")

        return redirect("login")

    return render(request, "register.html")


# =====================================
# LOGIN
# =====================================
def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        user_type = request.POST.get("user_type")

        user = authenticate(request, username=username, password=password)

        if user is None:
            return render(request, "login.html", {
                "error": "Invalid Username or Password."
            })

        if user.email != email:
            return render(request, "login.html", {
                "error": "Email does not match."
            })

        if user_type == "admin":

            if user.is_superuser:
                login(request, user)
                return redirect("home")

            return render(request, "login.html", {
                "error": "You are not an Admin."
            })

        elif user_type == "user":

            if not user.is_superuser:
                login(request, user)
                return redirect("home")

            return render(request, "login.html", {
                "error": "Please login as Admin."
            })

    return render(request, "login.html")


# =====================================
# LOGOUT
# =====================================
def logout_view(request):

    logout(request)
    return redirect("login")


# =====================================
# HOME
# =====================================
def home(request):

    context = {
        "total_donors": Donor.objects.count(),
        "total_requests": BloodRequest.objects.count()
    }

    return render(request, "home.html", context)


# =====================================
# DONOR
# =====================================
@login_required(login_url='login')
def add_donor(request):

    if request.method == "POST":
        Donor.objects.create(
            name=request.POST.get("name"),
            gender=request.POST.get("gender"),
            age=request.POST.get("age"),
            blood_group=request.POST.get("blood_group"),
            weight=request.POST.get("weight"),
            phone=request.POST.get("phone"),
            hemoglobin=request.POST.get("hemoglobin"),
            city=request.POST.get("city"),
            state=request.POST.get("state"),
            last_donation_date=request.POST.get("last_donation_date"),
            health_issues=request.POST.get("health_issues")
        )

        return redirect("donor_list")

    return render(request, "add_donor.html")


@login_required(login_url='login')
def donor_list(request):

    donors = Donor.objects.all().order_by("-id")

    return render(request, "donor_list.html", {
        "donors": donors
    })


@login_required(login_url='login')
def update_donor(request, id):

    if not request.user.is_superuser:
        return redirect("home")

    donor = get_object_or_404(Donor, id=id)

    if request.method == "POST":

        donor.name = request.POST.get("name")
        donor.gender = request.POST.get("gender")
        donor.age = request.POST.get("age")
        donor.blood_group = request.POST.get("blood_group")
        donor.weight = request.POST.get("weight")
        donor.phone = request.POST.get("phone")
        donor.hemoglobin = request.POST.get("hemoglobin")
        donor.city = request.POST.get("city")
        donor.state = request.POST.get("state")
        donor.last_donation_date = request.POST.get("last_donation_date")
        donor.health_issues = request.POST.get("health_issues")

        donor.save()
        return redirect("donor_list")

    return render(request, "update_donor.html", {"donor": donor})


@login_required(login_url='login')
def delete_donor(request, id):

    if not request.user.is_superuser:
        return redirect("home")

    donor = get_object_or_404(Donor, id=id)
    donor.delete()

    return redirect("donor_list")


# =====================================
# BLOOD REQUEST
# =====================================
@login_required(login_url='login')
def blood_request_view(request):

    if request.method == "POST":

        BloodRequest.objects.create(
            patient_name=request.POST.get("patient_name"),
            blood_group=request.POST.get("blood_group"),
            units_required=request.POST.get("units_required"),
            hospital_name=request.POST.get("hospital_name"),
            city=request.POST.get("city"),
            contact_number=request.POST.get("contact_number")
        )

        return redirect("request_list")

    return render(request, "blood_request.html")


@login_required(login_url='login')
def request_list(request):

    requests = BloodRequest.objects.all().order_by("-id")

    return render(request, "request_list.html", {
        "requests": requests
    })


@login_required(login_url='login')
def update_request(request, id):

    if not request.user.is_superuser:
        return redirect("home")

    blood_req = get_object_or_404(BloodRequest, id=id)

    if request.method == "POST":

        blood_req.patient_name = request.POST.get("patient_name")
        blood_req.blood_group = request.POST.get("blood_group")
        blood_req.units_required = request.POST.get("units_required")
        blood_req.hospital_name = request.POST.get("hospital_name")
        blood_req.city = request.POST.get("city")
        blood_req.contact_number = request.POST.get("contact_number")

        blood_req.save()
        return redirect("request_list")

    return render(request, "update_request.html", {
        "blood_req": blood_req
    })


@login_required(login_url='login')
def delete_request(request, id):

    if not request.user.is_superuser:
        return redirect("home")

    blood_req = get_object_or_404(BloodRequest, id=id)
    blood_req.delete()

    return redirect("request_list")