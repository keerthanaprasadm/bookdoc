from django.shortcuts import render, get_object_or_404, redirect
from .models import DoctorProfile
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def doctor_list(request):
    # Get search query from URL (GET)
    specialization = request.GET.get("specialization")

    # Base queryset
    doctors = DoctorProfile.objects.select_related('user')

    # Apply filter only if user typed something
    if specialization:
        doctors = doctors.filter(specialization__icontains=specialization)

    return render(request, 'doctors/doctor_list.html', {
        'doctors': doctors
    })


def doctor_detail(request, doctor_id):
    doctor = get_object_or_404(DoctorProfile, id=doctor_id)
    availability = doctor.availabilities.all()

    return render(request, 'doctors/doctor_detail.html', {
        'doctor': doctor,
        'availability': availability
    })

@login_required
def doctor_profile_details(request):
   
    doctor_profile, created = DoctorProfile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":
        doctor_profile.specialization = request.POST.get("specialization")
        doctor_profile.experience_years = request.POST.get("experience_years")
        doctor_profile.consultation_fee = request.POST.get("consultation_fee")
        doctor_profile.bio = request.POST.get("bio")

        doctor_profile.save()
        messages.success(request, "Doctor profile details saved successfully.")
        return redirect("doctor_dashboard")

    return render(
        request,
        "doctors/doctor_profile_details.html",
        {"doctor": doctor_profile}
    )