from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User


class RegistrationForm(FlaskForm):
    usertype = SelectField(
    "usertype",
    choices=[
        ("job_seeker", "Job Seeker")
    ],
    default="job_seeker"
    )



    # usertype = SelectField(
    #     'Select Usertype',
    #     choices=[('Job Seeker', 'Job Seeker'),
    #              ('Company', 'Company')],
    #     validators=[DataRequired()]
    # )

    username = StringField(
        'Username',
        validators=[DataRequired(), Length(min=2, max=20)]
    )

    email = StringField(
        'Email',
        validators=[DataRequired(), Email()]
    )

    password = PasswordField(
        'Password',
        validators=[DataRequired()]
    )

    confirm_password = PasswordField(
        'Confirm Password',
        validators=[DataRequired(), EqualTo('password')]
    )

    submit = SubmitField('Sign Up')
    # company_name = StringField("Company Name")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                'That username is already taken. Please choose a different one.'
            )

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                'That email is already taken. Please choose a different one.'
            )

class LoginForm(FlaskForm):
    usertype = SelectField(
        'Select User Type',
        choices=[
            ('Job Seeker', 'Job Seeker')
        ],
        default='Job Seeker',
        validators=[DataRequired()]
    )

    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


# class LoginForm(FlaskForm):
#     usertype = SelectField('Select Usertype',
#                            choices=[('Job Seeker', 'Job Seeker'),
#                                     ('Company', 'Company')],
#                            validators=[DataRequired()])
#     email = StringField('Email',
#                         validators=[DataRequired(), Email()])
#     password = PasswordField('Password', validators=[DataRequired()])
#     remember = BooleanField('Remember Me')
#     submit = SubmitField('Login')


class ReviewForm(FlaskForm):
    username = StringField('Name',
                           validators=[DataRequired()])
    review = TextAreaField('Review',
                           validators=[DataRequired()])
    submit = SubmitField('Submit Review')


class JobForm(FlaskForm):
    title = StringField('Job Title',
                        validators=[DataRequired(), Length(min=2, max=100)])
    company_name = StringField(
    'Company Name',
    validators=[DataRequired(), Length(min=2, max=100)]
    )
    industry = SelectField(
    'Industry',
    default='Information Technology',
    choices=[
        ('Information Technology', 'Information Technology'),
        ('Software Development', 'Software Development'),
        ('Cloud Computing', 'Cloud Computing'),
        ('Artificial Intelligence', 'Artificial Intelligence'),
        ('Cybersecurity', 'Cybersecurity'),
        ('Data Science & Analytics', 'Data Science & Analytics'),
        ('Telecommunications', 'Telecommunications'),
        ('Electronics & Semiconductor', 'Electronics & Semiconductor'),
        ('Manufacturing', 'Manufacturing'),
        ('Automobile', 'Automobile'),
        ('Aerospace & Defense', 'Aerospace & Defense'),
        ('Construction', 'Construction'),
        ('Real Estate', 'Real Estate'),
        ('Healthcare', 'Healthcare'),
        ('Pharmaceutical', 'Pharmaceutical'),
        ('Biotechnology', 'Biotechnology'),
        ('Education', 'Education'),
        ('Agriculture', 'Agriculture'),
        ('Food & Beverage', 'Food & Beverage'),
        ('Retail & E-Commerce', 'Retail & E-Commerce'),
        ('Banking & Financial Services', 'Banking & Financial Services'),
        ('Insurance', 'Insurance'),
        ('Media & Entertainment', 'Media & Entertainment'),
        ('Advertising & Marketing', 'Advertising & Marketing'),
        ('Hospitality & Tourism', 'Hospitality & Tourism'),
        ('Transportation & Logistics', 'Transportation & Logistics'),
        ('Energy & Utilities', 'Energy & Utilities'),
        ('Oil & Gas', 'Oil & Gas'),
        ('Mining & Metals', 'Mining & Metals'),
        ('Chemicals', 'Chemicals'),
        ('Textiles & Apparel', 'Textiles & Apparel'),
        ('Government & Public Sector', 'Government & Public Sector'),
        ('Legal Services', 'Legal Services'),
        ('Consulting', 'Consulting'),
        ('Non-Profit', 'Non-Profit'),
        ('Others', 'Others')
    ],
    validators=[DataRequired()]
    )
    
    description = TextAreaField(
    'Job Description',
    validators=[DataRequired()]
    )

    company_name = StringField(
        'Company Name',
        validators=[DataRequired()]
    )
    experience = SelectField(
    'Experience',
    choices=[
        ('Fresher', 'Fresher'),
        ('0-2 Years', '0-2 Years'),
        ('1-3 Years', '1-3 Years'),
        ('3-5 Years', '3-5 Years'),
        ('5+ Years', '5+ Years')
    ],
    validators=[DataRequired()]
    )

    location = StringField(
    'Location',
    validators=[DataRequired()]
    )
    job_type = SelectField(
    'Job Type',
    choices=[
        ('Full Time', 'Full Time'),
        ('Internship', 'Internship'),
        ('Remote', 'Remote'),
        ('Hybrid', 'Hybrid'),
        ('Contract', 'Contract')
    ],
    validators=[DataRequired()]
    )

    apply_link = StringField(
    "Official Apply Link",
    validators=[DataRequired()]
    )

    submit = SubmitField('Submit')


class ApplicationForm(FlaskForm):
    gender = SelectField('Gender', choices=[('Male', 'Male'),
                                            ('Female', 'Female'),
                                            ('Others', 'Other')],
                         default='male',
                         validators=[DataRequired()])
    degree = SelectField('Degree',
                         default='eSchool',
                         choices=[('eSchool', 'School'),
                                  ('dHighSchool', 'HighSchool'),
                                  ('cBachelor', 'Bachelor'),
                                  ('bMaster', 'Master'),
                                  ('aPHD', 'PHD')],
                         validators=[DataRequired()])
    industry = SelectField(
    'Industry',
    default='Information Technology',
    choices=[
        ('Information Technology', 'Information Technology'),
        ('Software Development', 'Software Development'),
        ('Cloud Computing', 'Cloud Computing'),
        ('Artificial Intelligence', 'Artificial Intelligence'),
        ('Cybersecurity', 'Cybersecurity'),
        ('Data Science & Analytics', 'Data Science & Analytics'),
        ('Telecommunications', 'Telecommunications'),
        ('Electronics & Semiconductor', 'Electronics & Semiconductor'),
        ('Manufacturing', 'Manufacturing'),
        ('Automobile', 'Automobile'),
        ('Aerospace & Defense', 'Aerospace & Defense'),
        ('Construction', 'Construction'),
        ('Real Estate', 'Real Estate'),
        ('Healthcare', 'Healthcare'),
        ('Pharmaceutical', 'Pharmaceutical'),
        ('Biotechnology', 'Biotechnology'),
        ('Education', 'Education'),
        ('Agriculture', 'Agriculture'),
        ('Food & Beverage', 'Food & Beverage'),
        ('Retail & E-Commerce', 'Retail & E-Commerce'),
        ('Banking & Financial Services', 'Banking & Financial Services'),
        ('Insurance', 'Insurance'),
        ('Media & Entertainment', 'Media & Entertainment'),
        ('Advertising & Marketing', 'Advertising & Marketing'),
        ('Hospitality & Tourism', 'Hospitality & Tourism'),
        ('Transportation & Logistics', 'Transportation & Logistics'),
        ('Energy & Utilities', 'Energy & Utilities'),
        ('Oil & Gas', 'Oil & Gas'),
        ('Mining & Metals', 'Mining & Metals'),
        ('Chemicals', 'Chemicals'),
        ('Textiles & Apparel', 'Textiles & Apparel'),
        ('Government & Public Sector', 'Government & Public Sector'),
        ('Legal Services', 'Legal Services'),
        ('Consulting', 'Consulting'),
        ('Non-Profit', 'Non-Profit'),
        ('Others', 'Others')
    ],
    validators=[DataRequired()]
    )
    experience = IntegerField(
    'Professional Experience in years',
    validators=[DataRequired()]
    )
    
    cv = FileField(
        'Update Resume',
        validators=[FileAllowed(
            ['pdf', 'doc', 'docx'],
            'Only PDF, DOC, or DOCX resumes are allowed!'
        )]
    )
    
    cover_letter = TextAreaField(
        'Cover Letter',
        validators=[DataRequired()]
    )
    
    submit = SubmitField('Submit')