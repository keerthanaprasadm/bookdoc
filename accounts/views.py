from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import SignupForm
from django.contrib import messages


def home(request):
    return render(request, 'accounts/home.html')


def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = form.cleaned_data["first_name"]
            user.last_name = form.cleaned_data["last_name"]
            user.email = form.cleaned_data["email"]
            user.role = form.cleaned_data["role"]
            user.save()

            login(request, user)
            return redirect("dashboard")
    else:
        form = SignupForm()

    return render(request, "accounts/signup.html", {"form": form})

@login_required
def dashboard_redirect(request):
    if request.user.role == 'doctor':
        return redirect('doctor_dashboard')
    elif request.user.role == 'patient':
        return redirect('patient_dashboard')

    return redirect('login')


# ------------------------
# ADMIN DASHBOARD
# ------------------------
# @login_required
# def admin_dashboard(request):
#     if request.user.role != 'admin':
#         return redirect('login')
#     return render(request, 'accounts/admin_dashboard.html')

# ------------------------
# DOCTOR DASHBOARD
# ------------------------
@login_required
def doctor_dashboard(request):
    if request.user.role != 'doctor':
        return redirect('login')

    return render(request, 'accounts/doctor_dashboard.html')


# ------------------------
# PATIENT DASHBOARD
# ------------------------
@login_required
def patient_dashboard(request):
    if request.user.role != 'patient':
        return redirect('login')

    return render(request, 'accounts/patient_dashboard.html')

@login_required
def logout_view(request):
    """
    Proper logout that clears old messages
    """
    logout(request)

   
    storage = messages.get_messages(request)
    for _ in storage:
        pass

    return redirect('login')


@login_required
def edit_doctor_profile(request):
    user = request.user

    if request.method == "POST":
        username = request.POST.get("username")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        # Update username
        if username and username != user.username:
            user.username = username
            user.save()
            messages.success(request, "Username updated successfully.")

        # Password logic
        if new_password or confirm_password:

            #  mismatch
            if new_password != confirm_password:
                messages.error(request, "Passwords do not match.")
                return redirect("edit_doctor_profile")

            #  same as current
            if user.check_password(new_password):
                messages.error(
                    request,
                    "New password cannot be the same as the current password."
                )
                return redirect("edit_doctor_profile")

        
            user.set_password(new_password)
            user.save()

            logout(request)
            messages.success(
                request,
                "Password updated successfully. Please login again."
            )
            return redirect("login")

        return redirect("doctor_dashboard")

    return render(request, "accounts/edit_doctor_profile.html")

@login_required
def edit_patient_profile(request):
    user = request.user

    if request.method == "POST":
        username = request.POST.get("username")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        user.username = username

        if new_password:
            if new_password != confirm_password:
                messages.error(request, "Passwords do not match")
                return redirect("edit_patient_profile")

            if user.check_password(new_password):
                messages.error(request, "New password cannot be same as old password")
                return redirect("edit_patient_profile")

            user.set_password(new_password)
            update_session_auth_hash(request, user)

        user.save()
        messages.success(request, "Profile updated successfully")
        return redirect("patient_dashboard")

    return render(request, "accounts/edit_patient_profile.html")
