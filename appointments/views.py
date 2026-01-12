from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime

from doctors.models import DoctorProfile, Availability
from .models import Appointment,DoctorRating
from datetime import datetime, timedelta
from django.http import JsonResponse
from .forms import AppointmentForm,DoctorRatingForm



@login_required
def book_appointment(request, doctor_id):
    doctor = get_object_or_404(DoctorProfile, id=doctor_id)

    if request.method == "POST":
        date_str = request.POST.get('date')
        time_str = request.POST.get('time')

        if not date_str or not time_str:
            messages.error(request, "Date and time are required.")
            return redirect('book_appointment', doctor_id=doctor.id)

        # Convert date string → date object
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()

        # Convert date → weekday number (0 = Monday)
        day_of_week = date_obj.weekday()

        # Convert time string → time object
        time_obj = datetime.strptime(time_str, "%H:%M").time()

        # ✅ Check doctor availability
        availability_exists = Availability.objects.filter(
            doctor=doctor,
            day_of_week=day_of_week,
            start_time__lte=time_obj,
            end_time__gte=time_obj
        ).exists()

        if not availability_exists:
            messages.error(
                request,
                "Doctor is not available at the selected date and time."
            )
            return redirect('book_appointment', doctor_id=doctor.id)

        # ✅ Prevent double booking
        already_booked = Appointment.objects.filter(
            doctor=doctor,
            date=date_obj,
            time=time_obj,
            status__in=['PENDING', 'CONFIRMED']
        ).exists()

        if already_booked:
            messages.error(request, "This slot is already booked.")
            return redirect('book_appointment', doctor_id=doctor.id)

        # ✅ Create appointment (STORE IT)
        appointment = Appointment.objects.create(
            patient=request.user,
            doctor=doctor,
            date=date_obj,
            time=time_obj
        )

        # ✅ Redirect to success page instead of my_appointments
        return redirect('appointment_success', appointment_id=appointment.id)

    return render(request, 'appointments/book_appointment.html', {
        'doctor': doctor
    })


@login_required
def my_appointments(request):
    appointments = Appointment.objects.filter(patient=request.user)

    selected_date = request.GET.get('date')

    if selected_date:
        appointments = appointments.filter(date=selected_date)

    return render(request, 'appointments/my_appointments.html', {
        'appointments': appointments,
        'selected_date': selected_date
    })


@login_required
def doctor_appointments(request):
    try:
        doctor_profile = DoctorProfile.objects.get(user=request.user)
    except DoctorProfile.DoesNotExist:
        return redirect('dashboard')

    selected_date = request.GET.get('date')

    appointments = Appointment.objects.filter(doctor=doctor_profile)

    if selected_date:
        appointments = appointments.filter(date=selected_date)

    return render(request, 'appointments/doctor_appointments.html', {
        'appointments': appointments,
        'selected_date': selected_date
    })



@login_required
def confirm_appointment(request, appt_id):
    appointment = get_object_or_404(Appointment, id=appt_id)

    if appointment.doctor.user != request.user:
        return HttpResponseForbidden("You are not allowed")

    appointment.status = 'CONFIRMED'
    appointment.save()

    messages.success(request, "Appointment confirmed.")
    return redirect('doctor_appointments')


@login_required
def cancel_appointment(request, appt_id):
    appointment = get_object_or_404(Appointment, id=appt_id)

    if appointment.doctor.user != request.user:
        return HttpResponseForbidden("You are not allowed")

    appointment.status = 'CANCELLED'
    appointment.save()

    messages.error(request, "Appointment cancelled.")
    return redirect('doctor_appointments')



@login_required
def get_available_slots(request, doctor_id):
    date_str = request.GET.get('date')
    doctor = get_object_or_404(DoctorProfile, id=doctor_id)

    if not date_str:
        return JsonResponse({'slots': []})

    selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()

    # ✅ IMPORTANT FIX: use weekday NUMBER (0–6)
    day_number = selected_date.weekday()

    availabilities = Availability.objects.filter(
        doctor=doctor,
        day_of_week=day_number
    )

    slots = []

    for availability in availabilities:
        start = datetime.combine(selected_date, availability.start_time)
        end = datetime.combine(selected_date, availability.end_time)

        while start < end:
            slots.append(start.strftime("%H:%M"))
            start += timedelta(minutes=30)

    return JsonResponse({'slots': slots})


@login_required
def appointment_success(request, appointment_id):
    appointment = get_object_or_404(
        Appointment,
        id=appointment_id,
        patient=request.user
    )

    return render(request, 'appointments/appointment_success.html', {
        'appointment': appointment
    })


@login_required
def rate_doctor(request, appointment_id):
    appointment = get_object_or_404(
        Appointment,
        id=appointment_id,
        patient=request.user,
        status='CONFIRMED'
    )

 
    existing_rating = DoctorRating.objects.filter(
        doctor=appointment.doctor,
        patient=request.user
    ).first()

    if existing_rating:
        messages.info(request, "You have already rated this doctor.")
        return redirect('my_appointments')

    if request.method == 'POST':
        form = DoctorRatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.doctor = appointment.doctor
            rating.patient = request.user
            rating.save()

            messages.success(request, "Thank you for rating the doctor!")
            return redirect('my_appointments')
    else:
        form = DoctorRatingForm()

    return render(request, 'appointments/rate_doctor.html', {
        'form': form,
        'appointment': appointment
    })