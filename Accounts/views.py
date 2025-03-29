import os
import csv
from django.core.files import File
from django.conf import settings
from Accounts.models import Student
from django.contrib import auth,messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login

def slogin(request):
    if request.method == "POST":
        form_type = request.POST.get("form_type")  # Check which form was submitted

        if form_type == "login":
            # Handle login form submission
            username = request.POST.get("username")
            password = request.POST.get("password")
            if username and password:
                user = authenticate(username=username, password=password)
                if user is not None:
                    if user.is_superuser:
                        messages.warning(request, "Please Login Using Teacher Login!!")
                        return redirect("/auth/tlogin")
                    else:
                        auth_login(request, user)
                        messages.success(request, "Login successful")
                        return redirect('student')
                else:
                    messages.error(request, "User Doesn't Exist")
                    
            return render(request, "student.html", {"username": username})

        elif form_type == "signup":
            username = request.POST.get("username")
            password = request.POST.get("password")
            email = request.POST.get("email")
            try:
                user = User.objects.create_user(username = username , password = password)
                user.save()
                auth.login(request ,user)

            except:
                messages.error(request,"Username Already exists")
                return render(request,"student.html",{"username":username,"email":email}) 
                
            messages.success(request,"Success")
    return render(request, "student.html")

def tlogin(request):
    if request.method == "POST":
        form_type = request.POST.get("form_type")  # Check which form was submitted

        if form_type == "login":
            username = request.POST.get("username")
            password = request.POST.get("password")
            if username and password:
                user = authenticate(username=username, password=password)
                if user is not None:
                    if user.is_superuser:
                        # Handle superuser login
                        auth_login(request, user)
                        messages.success(request, "Superuser login successful")
                        return redirect('/dashboard/teacher')  # Redirect to superuser dashboard or another page
                    else:
                        messages.warning(request, "Please Login Using Student Login!!")
                        return redirect('/auth/slogin')
                else:
                    messages.error(request, "Invalid credentials")
                    return render(request, "teacher.html", {"username": username})

        elif form_type == "signup":
            # Handle signup form submission
            username = request.POST.get("username")
            password = request.POST.get("password")
            email = request.POST.get("email")
            try:
                user = User.objects.create_superuser(username = username , password = password,email = email)
                user.save()
                auth.login(request ,user)

            except:
                messages.error(request,"Username Already exists")
                return render(request,"teacher.html",{"username":username,"email":email}) 
        messages.success(request,"Success")
    return render(request, "teacher.html")

def preview_users(request):
    csv_file_path = os.path.join(settings.STATICFILES_DIRS[0], 'upload_user', 'upload.csv')

    if not os.path.exists(csv_file_path):
        return render(request, 'error.html', {'message': 'File not found'})

    users_data = []
    with open(csv_file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)  # Skip the header row

        for row in reader:
            (username, email, name, password, picture, fathername, gender, dob, religion,admitioncategory, address, phone, category, mole, dept, section) = row

            user_exists = User.objects.filter(username=username).exists()

            users_data.append({
                'username': username,
                'email': email,
                'name': name,
                'password': password,
                'picture': picture,
                'fathername': fathername,
                'gender': gender,
                'dob': dob,
                'religion': religion,
                'admitioncategory': admitioncategory,
                'address': address,
                'phone': phone,
                'category': category,
                'mole': mole,
                'dept': dept,
                'section': section,
                'exists': user_exists,
            })

    return render(request, 'bulk_upload.html', {'users_data': users_data})

def import_users(request):
    if request.method == "POST":
        selected_usernames = request.POST.getlist("selected_users")
        usernames = request.POST.getlist("usernames")
        emails = request.POST.getlist("emails")
        names = request.POST.getlist("names")
        passwords = request.POST.getlist("passwords")
        pictures = request.POST.getlist("pictures")
        fathernames = request.POST.getlist("fathernames")
        genders = request.POST.getlist("genders")
        dobs = request.POST.getlist("dobs")
        religions = request.POST.getlist("religions")
        admitioncategories = request.POST.getlist("admitioncategories")
        addresses = request.POST.getlist("addresses")
        phones = request.POST.getlist("phones")
        categories = request.POST.getlist("categories")
        moles = request.POST.getlist("moles")
        depts = request.POST.getlist("depts")
        sections = request.POST.getlist("sections")

        users_data = zip(usernames, emails, names, passwords, pictures, fathernames, genders, dobs, religions, admitioncategories, addresses, phones, categories, moles, depts, sections)
        for username, email, name, password, picture, fathername, gender, dob, religion, admitioncategory, address, phone, category, mole, dept, section in users_data:
            user = User.objects.create_user(username=username, email=email, password=password)
            if gender=="MALE":
                gender="M"
            else:
                gender="F"

            if picture=="":
                if gender=="M":
                    picture = r"D:\PYTHON\Smart Classroom Management Software (SCMS)\Django_Final\static\avatar.jpg"
                else:
                    picture = r"D:\PYTHON\Smart Classroom Management Software (SCMS)\Django_Final\static\avatar1.webp"
            
            student = Student.objects.create(
                user=user,
                roll_number=username,
                # username=username,
                email=email,
                name=name,
                password=password,
                fathername=fathername,
                gender=gender,
                date_of_birth=dob,
                religion=religion,
                admission_category=admitioncategory,
                address=address,
                phone_number=phone,
                category=category,
                mole=mole,
                department=dept,
                section=section
            ) 

            if os.path.exists(picture):  
                new_filename = f"{username}.jpg"  # Rename file using username
                with open(picture, "rb") as f:
                    student.profile_picture.save(new_filename, File(f))
            student.save()
            print(f"User {username} created successfully!")

        messages.success(request, f"{len(selected_usernames)} user(s) have been imported successfully.")
        return redirect('preview_users')

    return render(request, 'bulk_upload.html')

def logout(request):
    auth.logout(request)
    messages.success(request, "Logout successful")
    return redirect("slogin")

def profile(request):   
    return render(request, "profile.html") 