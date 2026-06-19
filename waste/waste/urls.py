"""
URL configuration for waste project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.index),
    path("login", views.login_view),
    path("signout", views.signout),
    path("register_user", views.register_user),
    path("register_staff", views.register_staff),
    path("register_recycling", views.register_recycling_center),

    # Admin
    path("admin_home", views.admin_home),
    path("admin_view_staff", views.admin_view_staff),
    path("admin_staff_action", views.admin_staff_action),
    path("admin_view_users", views.admin_view_users),
    path("admin_view_bins", views.admin_view_bins),
    path("admin_add_bin", views.admin_add_bin),
    path("admin_view_pickups", views.admin_view_pickups),
    path("admin_assign_task", views.admin_assign_task),
    path("admin_send_notification", views.admin_send_notification),

    # Staff
    path("staff_home", views.staff_home),
    path("staff_view_tasks", views.staff_view_tasks),
    path("staff_update_task", views.staff_update_task),
    path("staff_report_bin", views.staff_report_bin),
    path("staff_notifications", views.staff_notifications),

    # User
    path("user_home", views.user_home),
    path("user_view_bins", views.user_view_bins),
    path("user_request_pickup", views.user_request_pickup),
    path("user_report_bin", views.user_report_bin),
    path("user_request_history", views.user_request_history),
    path("user_notifications", views.user_notifications),

    # Recycling Center
    path("recycling_home", views.recycling_home),
    # path("recycling_view_records", views.recycling_view_records),
    # path("recycling_update_status", views.recycling_update_status),
    # path("recycling_notifications", views.recycling_notifications),
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
