
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Count, Sum
import json

from .models import *

# -------------------------------------------------
# LOGIN CHECK
# -------------------------------------------------

def require_login(request, redirect_url="/login"):
    if "lid" not in request.session:
        messages.error(request, "Please login first")
        return redirect(redirect_url)
    return None


# -------------------------------------------------
# INDEX
# -------------------------------------------------

def index(request):
    logout(request)
    return render(request, "index.html")


# -------------------------------------------------
# LOGIN
# -------------------------------------------------

def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            username=username,
            password=password
        )

        if user:

            login(request, user)
            request.session["lid"] = user.id

            if user.userType == "admin":
                return redirect("/admin_home")

            elif user.userType == "staff":

                staff = StaffProfile.objects.get(
                    loginid=user
                )

                if staff.status == "approved":
                    return redirect("/staff_home")

                messages.error(request, f"Account {staff.status}")
                return redirect("/login")

            elif user.userType == "recycling_center":

                center = RecyclingCenterProfile.objects.get(
                    loginid=user
                )

                if center.status == "approved":
                    return redirect("/recycling_home")

                messages.error(request, f"Account {center.status}")
                return redirect("/login")

            elif user.userType == "user":
                return redirect("/user_home")

        messages.error(request, "Invalid username or password")
        return redirect("/login")

    return render(request, "login.html")


def signout(request):
    logout(request)
    request.session.flush()
    return redirect("/")


# -------------------------------------------------
# USER REGISTRATION
# -------------------------------------------------

def register_user(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        if Login.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("/register_user")

        login_obj = Login.objects.create_user(
            username=username,
            password=password,
            userType="user",
            viewPass=password
        )

        UserProfile.objects.create(
            loginid=login_obj,
            name=request.POST.get("name"),
            email=request.POST.get("email"),
            phone=request.POST.get("phone"),
            address=request.POST.get("address")
        )

        messages.success(request, "Registration successful")
        return redirect("/login")

    return render(request, "user_register.html")


# -------------------------------------------------
# STAFF REGISTRATION
# -------------------------------------------------

def register_staff(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        if Login.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("/register_staff")

        login_obj = Login.objects.create_user(
            username=username,
            password=password,
            userType="staff",
            viewPass=password
        )

        StaffProfile.objects.create(
            loginid=login_obj,
            name=request.POST.get("name"),
            email=request.POST.get("email"),
            phone=request.POST.get("phone"),
            address=request.POST.get("address"),
            profile_pic=request.FILES.get("profile_pic")
        )

        messages.success(
            request,
            "Registration submitted for approval"
        )

        return redirect("/login")

    return render(request, "staff_register.html")


# -------------------------------------------------
# RECYCLING CENTER REGISTRATION
# -------------------------------------------------

def register_recycling_center(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        if Login.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("/register_recycling")

        login_obj = Login.objects.create_user(
            username=username,
            password=password,
            userType="recycling_center",
            viewPass=password
        )

        RecyclingCenterProfile.objects.create(
            loginid=login_obj,
            center_name=request.POST.get("center_name"),
            email=request.POST.get("email"),
            phone=request.POST.get("phone"),
            address=request.POST.get("address")
        )

        messages.success(
            request,
            "Registration submitted for approval"
        )

        return redirect("/login")

    return render(request, "recycling_register.html")


# -------------------------------------------------
# ADMIN
# -------------------------------------------------

def admin_home(request):

    context = {
        "users": UserProfile.objects.count(),
        "staff": StaffProfile.objects.count(),
        "bins": WasteBin.objects.count(),
        "requests": PickupRequest.objects.count()
    }

    return render(
        request,
        "ADMIN/admin_home.html",
        context
    )

def admin_view_staff(request):

    staff = StaffProfile.objects.all()

    return render(
        request,
        "ADMIN/view_staff.html",
        {"val": staff}
    )

def admin_staff_action(request):

    sid = request.GET.get("id")
    action = request.GET.get("act")

    staff = get_object_or_404(
        StaffProfile,
        id=sid
    )

    staff.status = action
    staff.save()

    return redirect("/admin_view_staff")

def admin_view_users(request):

    users = UserProfile.objects.all()

    return render(
        request,
        "ADMIN/view_users.html",
        {"val": users}
    )

def admin_view_bins(request):

    bins = WasteBin.objects.all()

    return render(
        request,
        "ADMIN/view_bins.html",
        {"val": bins}
    )

def admin_add_bin(request):

    if request.method == "POST":

        WasteBin.objects.create(
            bin_code=request.POST.get("bin_code"),
            location=request.POST.get("location"),
            waste_type=request.POST.get("waste_type"),
            capacity=request.POST.get("capacity"),
            current_level=0,
            status="empty"
        )

        messages.success(request, "Bin added successfully")

        return redirect("/admin_view_bins")

    return render(request, "ADMIN/add_bin.html")

def admin_view_pickups(request):

    requests = PickupRequest.objects.all().order_by("-created_at")

    return render(
        request,
        "ADMIN/view_pickups.html",
        {"val": requests}
    )

def admin_assign_task(request):

    request_id = request.GET.get("id")

    pickup = get_object_or_404(
        PickupRequest,
        id=request_id
    )

    staff = StaffProfile.objects.filter(
        status="approved"
    )

    if request.method == "POST":

        CollectionTask.objects.create(
            pickup_request=pickup,
            staff_id=request.POST.get("staff"),
            collection_status="assigned"
        )

        pickup.status = "assigned"
        pickup.save()

        messages.success(request, "Task assigned")

        return redirect("/admin_view_pickups")

    return render(
        request,
        "ADMIN/assign_task.html",
        {
            "pickup": pickup,
            "staff": staff
        }
    )


def staff_home(request):
    return render(request, "STAFF/staff_home.html")

def user_home(request):
    return render(request, "USER/user_home.html")

def recycling_home(request):
    return render(request, "RECYCLING_CENTER/recycling_home.html")