from flask import render_template, url_for, flash, redirect, request, send_file, session
from app import app, db, bcrypt
from PIL import Image
import os
import secrets
from app.forms import RegistrationForm, LoginForm, ReviewForm, JobForm, ApplicationForm
from app.models import User, Jobs, Review, Application
from flask_login import login_user, current_user, logout_user, login_required
import random

rev = [
    {
        'username': 'Micheal Scott',
        'review': 'I hired multiple people using this website. Thank you'
    },
    {
        'username': 'Dwight Schrute',
        'review': 'It could be better'
    },
    {
        'username': 'Andy Bernard',
        'review': 'Best website ever'
    }
]

def get_random_reviews():
    review_obj = Review.query.all()

    if len(review_obj) < 3:
        return rev

    return random.sample(review_obj, 3)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        if current_user.usertype == 'Job Seeker':
            return redirect(url_for('show_jobs'))
        elif current_user.usertype == 'Company':
            return redirect(url_for('posted_jobs'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            username=form.username.data,
            # company_name=form.company_name.data,
            usertype=form.usertype.data,
            email=form.email.data,
            password=hashed_password
            )       
        db.session.add(user)
        db.session.commit()
        flash('You account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form, Random_Review=get_random_reviews())

@app.route("/admin", methods=["GET", "POST"])
def admin():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        if username == "admin" and password == "admin123":
            session["admin"] = True
            return redirect(url_for("admin_dashboard"))

        flash("Invalid Admin Credentials", "danger")

    return render_template(
        "admin_login.html",
        Random_Review=get_random_reviews()
    )

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.usertype == 'Job Seeker':
            return redirect(url_for('show_jobs'))
        elif current_user.usertype == 'Company':
            return redirect(url_for('posted_jobs'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            print('password clear')
            if form.usertype.data == user.usertype and form.usertype.data == 'Company':
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('posted_jobs'))
            elif form.usertype.data == user.usertype and form.usertype.data == 'Job Seeker':
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('show_jobs'))
            else:
                flash('Login Unsuccessful. Please check email, password and usertype', 'danger')
        else:
            flash('Login Unsuccessful. Please check email, password and usertype', 'danger')
            return render_template('login.html', form=form, Random_Review=get_random_reviews())
    return render_template('login.html', form=form, Random_Review=get_random_reviews())

@app.route("/admin/jobs")
def admin_jobs():
    jobs = Jobs.query.all()
    return render_template(
        "admin_jobs.html",
        jobs=jobs,
        Random_Review=get_random_reviews()
    )
@app.route("/admin_logout")
def admin_logout():
    session.pop("admin", None)
    flash("Admin logged out successfully.", "success")
    return redirect(url_for("admin"))
@app.route("/admin/delete_job/<int:job_id>", methods=["POST"])
def delete_job(job_id):
    if "admin" not in session:
        return redirect(url_for("admin"))

    job = Jobs.query.get_or_404(job_id)

    # Delete all applications for this job
    Application.query.filter_by(job_id=job.id).delete()

    # Delete the job
    db.session.delete(job)
    db.session.commit()

    flash("Job deleted successfully!", "success")

    return redirect(url_for("admin_jobs"))
@app.route("/admin/dashboard")
def admin_dashboard():
    if "admin" not in session:
        return redirect(url_for("admin"))
    jobs = Jobs.query.all()
    return render_template("admin_dashboard.html", Random_Review=get_random_reviews())


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('show_jobs'))
def save_picture(form_picture):
    f_name, f_ext = os.path.splitext(form_picture.filename)

    picture_fn = f_name + f_ext

    picture_path = os.path.join(
        app.root_path,
        'static',
        'resumes',
        picture_fn
    )

    form_picture.save(picture_path)

    return "resumes/" + picture_fn

@app.route("/post_cvs/<jobid>", methods=['GET', 'POST'])
@login_required
def post_cvs(jobid):
    form = ApplicationForm()
    job = Jobs.query.filter_by(id=jobid).first()
    if form.validate_on_submit():
        picture_file = save_picture(form.cv.data)

        application = Application(
            gender=form.gender.data,
            degree=form.degree.data,
            industry=form.industry.data,
            experience=form.experience.data,
            cover_letter=form.cover_letter.data,
            application_submiter=current_user,
            application_jober=job,
            cv=picture_file
        )
        db.session.add(application)
        db.session.commit()
        flash("🎉 Your application has been submitted successfully!", "success")

        return redirect(url_for('show_jobs'))
    return render_template('post_cvs.html', form=form, Random_Review=get_random_reviews())
@app.route("/post_jobs", methods=["GET", "POST"])
def post_jobs():

    if "admin" not in session:
        return redirect(url_for("admin"))

    form = JobForm()

    if form.validate_on_submit():
        # print("Company Name:", form.company_name.data)
        job = Jobs(
            title=form.title.data,
            company_name=form.company_name.data,
            industry=form.industry.data,
            description=form.description.data,
            user_id=1
        )
        db.session.add(job)
        db.session.commit()

        flash("Job added successfully!", "success")
        return redirect(url_for("admin_dashboard"))

    return render_template(
        "post_jobs.html",
        form=form,
        Random_Review=get_random_reviews()
    )

@app.route("/review", methods=['GET', 'POST'])
@login_required
def review():
    form = ReviewForm()
    print(User.query.all())
    if form.validate_on_submit():
        review = Review(username=form.username.data,
                            review=form.review.data)
        db.session.add(review)
        db.session.commit()
        flash('Thank you for providing the review!', 'success')
        return redirect(url_for('show_jobs'))
    return  render_template('review.html', form=form, Random_Review=get_random_reviews())

@app.route("/posted_jobs")

def posted_jobs():
    jobs = Jobs.query.all()
    return render_template(
        'show_jobs.html',
        jobs=jobs,
        Random_Review=get_random_reviews()
    )

@app.route("/show_applications/<jobid>", methods=['GET'])
@login_required
def show_applications(jobid):
    applications = Application.query.filter_by(job_id=jobid).order_by(Application.degree, Application.experience.desc()).all()
    return render_template('show_applications.html', applications=applications, Random_Review=get_random_reviews())

@app.route("/meeting/<application_id>")
@login_required
def meeting(application_id):
    applicant_id = Application.query.get(int(application_id)).user_id
    applicant = User.query.get(applicant_id)
    return render_template('meeting.html', applicant=applicant, Random_Review=get_random_reviews())

@app.route("/")
def home():
    if current_user.is_authenticated:
        if current_user.usertype == "Job Seeker":
            return redirect(url_for("show_jobs"))
        elif current_user.usertype == "Company":
            return redirect(url_for("posted_jobs"))

    return render_template(
        "landing.html",
        Random_Review=get_random_reviews()
    )
@app.route('/admin/applications')
def admin_applications():

    if not session.get("admin"):
        flash("Please login as Admin.", "danger")
        return redirect(url_for("admin"))

    applications = Application.query.order_by(
        Application.date_posted.desc()
    ).all()

    return render_template(
        "admin_applications.html",
        applications=applications,
        Random_Review=get_random_reviews()
    )
@app.route("/profile")
@login_required
def profile():

    applications = Application.query.filter_by(
        user_id=current_user.id
    ).count()

    return render_template(
        "profile.html",
        applications=applications,
        Random_Review=get_random_reviews()
    )
@app.route("/show_jobs")
@login_required
def show_jobs():

    search = request.args.get("search", "")
    industry = request.args.get("industry", "")

    jobs = Jobs.query

    if search:
        jobs = jobs.filter(Jobs.title.ilike(f"%{search}%"))

    if industry:
        jobs = jobs.filter(Jobs.industry == industry)

    jobs = jobs.all()

    industries = db.session.query(Jobs.industry).distinct().all()
    industries = [i[0] for i in industries]

    return render_template(
        "show_jobs.html",
        jobs=jobs,
        industries=industries,
        search=search,
        industry=industry,
        Random_Review=get_random_reviews()
    )

@app.route("/resume/<id>", methods=['GET'])
def resume(id):
    cv = Application.query.get(int(id)).cv
    return render_template(
        'resume.html',
        cv=cv,
        Random_Review=get_random_reviews(),
        id=id
    )

@app.route("/job/<int:id>")
@login_required
def job_details(id):

    job = Jobs.query.get_or_404(id)

    return render_template(
        "job_details.html",
        job=job,
        Random_Review=get_random_reviews()
    )


