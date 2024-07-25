from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin


class LoginCheckMiddleWare(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        modulename = view_func.__module__
        user = request.user

        # Allow registration-related views to pass through
        registration_views = ["views"]  # Add your registration view names here
        if any(view_name in modulename for view_name in registration_views):
            return None

        # if request.path.startswith('/accounts/'):
        #     return None

        if user.is_authenticated:
            if user.user_type == "1":
                if modulename == "schoolcorp_app.AdminViews" or modulename.startswith("django.contrib.staticfiles"):
                    pass
                elif modulename == "schoolcorp_app.views":
                    pass
                else:
                    return HttpResponseRedirect(reverse("admin_home"))
            elif user.user_type == "2":
                if modulename == "schoolcorp_app.EmployeeViews" or modulename.startswith("django.contrib.staticfiles"):
                    pass
                elif modulename == "schoolcorp_app.views":
                    pass
                else:
                    return HttpResponseRedirect(reverse("employee_home"))
            elif user.user_type == "3":
                if modulename == "schoolcorp_app.SchoolViews" or modulename.startswith("django.contrib.staticfiles"):
                    pass
                elif modulename == "schoolcorp_app.views":
                    pass
                else:
                    return HttpResponseRedirect(reverse("school_home"))
            elif user.user_type == "4":
                if modulename == "schoolcorp_app.TeacherViews" or modulename.startswith("django.contrib.staticfiles"):
                    pass
                elif modulename == "schoolcorp_app.views":
                    pass
                else:
                    return HttpResponseRedirect(reverse("teacher_home"))
            else:
                return HttpResponseRedirect(reverse("login"))
        else:
            if (
                    request.path == reverse("login")
                    or request.path == reverse("doLogin")
                    or request.path == reverse("index")
                    or modulename == "django.contrib.auth.views"
                    or modulename.startswith("django.contrib.staticfiles")
                    or modulename == "django.contrib.auth.views"
            ):
                pass
            else:
                return HttpResponseRedirect(reverse("login"))

        return None
