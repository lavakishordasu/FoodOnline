from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager

# Create your models here.

# Note:---
# AbstractBaseUser: This is a abstract base class that you can subclass to create your own user model in Django. It provides the core implementation of a user model, including fields like username, password, and methods like is_authenticated, is_active, etc. By subclassing AbstractBaseUser, you have the flexibility to define your own fields for the user model.
# BaseUserManager: This is a base class for managing user creation and handling password hashing. It provides methods like create_user and create_superuser which you can override to define custom user creation logic. By default, BaseUserManager is used to manage user creation for the default Django user model, but you can also subclass it to customize user creation behavior for your custom user model.

class UserManager(BaseUserManager):
    # usermanager will not contain any fields only methods
    # This class for createing a regular user
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError("User must have an email address")

        if not username:
            raise ValueError("User must have an username")
        
        user =  self.model(
            email = self.normalize_email(email),     # normalize_email:-- for example if you give a uppercasae email id then it will convert into lower case witjh normalization method.
            username = username,
            first_name = first_name,
            last_name = last_name,
        )
        user.set_password (password)   #set_password is a method that will encode your password and save it in DB.
        user.save(using=self._db)   #using=self.db when we have multiple databases we are telling to use particular db.
        return user
    
    def create_superuser(self,first_name, last_name, username, email, password=None):
        user = self.create_user(
            email = email,     # normalize_email:-- for example if you give a uppercasae email id then it will convert into lower case witjh normalization method.
            username = username,
            first_name = first_name,
            last_name = last_name,
            password=password
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user
 

class User(AbstractBaseUser):
    # this will take full control of models.we can do what ever we want.
    RESTAURANT = 1
    CUSTOMER = 2

    ROLE_CHOICE = (
        (RESTAURANT,"Restaurant"),
        (CUSTOMER,"Customer"),
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=12, blank=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICE, blank=True, null=True)

    # required fields
    data_joined = models.DateTimeField(auto_now_add = True)
    last_login = models.DateTimeField(auto_now_add = True)
    created_date = models.DateTimeField(auto_now_add= True)
    modified_data = models.DateTimeField(auto_now_add= True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

   
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']
    objects = UserManager()

   

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True

    

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='users/profile_pictures',blank=True, null=True)
    cover_photo = models.ImageField(upload_to='users/cover_photos',blank=True, null=True)
    address_line1 = models.CharField(max_length=50, blank=True, null=True)
    address_line2 = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    pin_code = models.CharField(max_length=6, blank=True, null=True)
    latitude = models.CharField(max_length=20, blank=True, null= True)
    logitude = models.CharField(max_length=20, blank=True, null= True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.user.email

