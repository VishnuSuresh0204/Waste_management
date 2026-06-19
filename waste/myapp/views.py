
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

    requests = PickupRequest.objects.all().order_by("-request_date")

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

def admin_send_notification(request):

    if request.method == "POST":

        Notification.objects.create(
            title=request.POST.get("title"),
            message=request.POST.get("message"),
            target_role=request.POST.get("target_role")
        )

        messages.success(request, "Notification sent")

        return redirect("/admin_send_notification")

    return render(
        request,
        "ADMIN/send_notification.html"
    )

# -------------------------------------------------
# STAFF
# -------------------------------------------------

def staff_home(request):
    return render(request, "STAFF/staff_home.html")

def staff_view_tasks(request):

    staff = StaffProfile.objects.get(
        loginid_id=request.session["lid"]
    )

    tasks = CollectionTask.objects.filter(
        staff=staff
    ).order_by("-id")

    return render(
        request,
        "STAFF/view_tasks.html",
        {"val": tasks}
    )

def staff_update_task(request):

    task_id = request.GET.get("id")

    task = get_object_or_404(
        CollectionTask,
        id=task_id
    )

    if request.method == "POST":

        task.collection_status = request.POST.get("status")
        task.collected_quantity = request.POST.get("quantity")
        task.notes = request.POST.get("notes")

        task.save()

        messages.success(request, "Task updated")

        return redirect("/staff_view_tasks")

    return render(
        request,
        "STAFF/update_task.html",
        {"task": task}
    )

def staff_report_bin(request):

    staff = StaffProfile.objects.get(
        loginid_id=request.session["lid"]
    )

    if request.method == "POST":

        BinReport.objects.create(
            staff=staff,
            bin_id=request.POST.get("bin"),
            issue_type=request.POST.get("issue_type"),
            description=request.POST.get("description")
        )

        messages.success(request, "Report submitted")

        return redirect("/staff_view_tasks")

    bins = WasteBin.objects.all()

    return render(
        request,
        "STAFF/report_bin.html",
        {"bins": bins}
    )

# -------------------------------------------------
# USER
# -------------------------------------------------

def user_home(request):
    return render(request, "USER/user_home.html")

def user_view_bins(request):

    bins = WasteBin.objects.all()

    return render(
        request,
        "USER/view_bins.html",
        {"val": bins}
    )

def user_request_pickup(request):

    user = UserProfile.objects.get(
        loginid_id=request.session["lid"]
    )

    if request.method == "POST":

        PickupRequest.objects.create(
            user=user,
            waste_type=request.POST.get("waste_type"),
            quantity=request.POST.get("quantity"),
            pickup_address=request.POST.get("pickup_address")
        )

        messages.success(request, "Pickup request submitted")

        return redirect("/user_request_history")

    return render(
        request,
        "USER/request_pickup.html"
    )

def user_report_bin(request):

    user = UserProfile.objects.get(
        loginid_id=request.session["lid"]
    )

    if request.method == "POST":

        BinReport.objects.create(
            user=user,
            bin_id=request.POST.get("bin"),
            issue_type=request.POST.get("issue_type"),
            description=request.POST.get("description")
        )

        messages.success(request, "Issue reported")

        return redirect("/user_home")

    bins = WasteBin.objects.all()

    return render(
        request,
        "USER/report_bin.html",
        {"bins": bins}
    )

def user_request_history(request):

    user = UserProfile.objects.get(
        loginid_id=request.session["lid"]
    )

    requests = PickupRequest.objects.filter(
        user=user
    ).order_by("-id")

    return render(
        request,
        "USER/request_history.html",
        {"val": requests}
    )

# -------------------------------------------------
# RECYCLING CENTER
# -------------------------------------------------

def recycling_home(request):
    return render(
        request,
        "RECYCLING/recycling_home.html"
    )

def recycling_view_records(request):

    center = RecyclingCenterProfile.objects.get(
        loginid_id=request.session["lid"]
    )

    records = RecyclingRecord.objects.filter(
        center=center
    )

    return render(
        request,
        "RECYCLING/view_records.html",
        {"val": records}
    )

def recycling_update_status(request):

    record_id = request.GET.get("id")

    record = get_object_or_404(
        RecyclingRecord,
        id=record_id
    )

    if request.method == "POST":

        record.processing_status = request.POST.get("status")
        record.processed_quantity = request.POST.get("quantity")

        record.save()

        messages.success(request, "Record updated")

        return redirect("/recycling_view_records")

    return render(
        request,
        "RECYCLING/update_record.html",
        {"record": record}
    )

# -------------------------------------------------
# NOTIFICATIONS
# -------------------------------------------------

def user_notifications(request):

    notifications = Notification.objects.filter(
        target_role__in=["user", "all"]
    ).order_by("-created_at")

    return render(
        request,
        "USER/notifications.html",
        {"val": notifications}
    )

def staff_notifications(request):

    notifications = Notification.objects.filter(
        target_role__in=["staff", "all"]
    ).order_by("-created_at")

    return render(
        request,
        "STAFF/notifications.html",
        {"val": notifications}
    )

def recycling_notifications(request):

    notifications = Notification.objects.filter(
        target_role__in=["recycling_center", "all"]
    ).order_by("-created_at")

    return render(
        request,
        "RECYCLING/notifications.html",
        {"val": notifications}
    )


