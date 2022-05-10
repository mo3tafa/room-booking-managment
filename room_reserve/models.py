from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime, timedelta
from django.utils import timezone




class ReservationModel(models.Model):
    user                = models.ForeignKey('UserModel',on_delete=models.CASCADE,related_name='reservationsInfo')
    room                = models.ForeignKey('RoomModel',on_delete=models.CASCADE,related_name='reservations')
    reserved_start_date = models.DateTimeField(default=timezone.now)
    reserved_end_date   = models.DateTimeField(default=timezone.now()+timedelta(days=1))
    comment             = models.TextField(blank=True,null=True)

    created_by  = models.ForeignKey( "UserModel",on_delete=models.SET_NULL,related_name='reservation_creator',editable=False,null=True)
    modified_by = models.ForeignKey( "UserModel",on_delete=models.SET_NULL,related_name='reservation_modifier',null=True)
    created     = models.DateTimeField(auto_now_add=True, editable=False)
    modified    = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tbl_reservation'
        managed = True
        verbose_name = 'reservation'
        verbose_name_plural = 'reservations'



class RoomModel(models.Model):
    name     = models.CharField(max_length=80, unique=True)
    capacity = models.IntegerField(default=1)

    created_by  = models.ForeignKey( "UserModel",on_delete=models.SET_NULL,related_name='room_creator',editable=False,null=True)
    modified_by = models.ForeignKey( "UserModel",on_delete=models.SET_NULL,related_name='room_modifier',null=True)
    created     = models.DateTimeField(auto_now_add=True, editable=False)
    modified    = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tbl_room'
        managed = True
        verbose_name = 'room'
        verbose_name_plural = 'rooms'



class TokenModel(models.Model):
    user = models.ForeignKey('UserModel',on_delete=models.CASCADE,related_name='bearer_token',)
    key = models.TextField(unique=True)
    # access_token  = models.TextField(unique=True)
    # refresh_token = models.TextField(unique=True)
    remote_addr = models.TextField()
    user_agent = models.TextField()
    player_id = models.TextField(unique=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'tbl_token'
        managed = True
        verbose_name = "token"
        verbose_name_plural = "tokens"



class RoleModel(models.Model):
    title    = models.CharField(max_length=130, primary_key=True)
    parent   = models.ForeignKey('RoleModel',on_delete=models.SET_NULL,related_name='subordinates',editable=False,null=True)
    order    = models.SmallIntegerField(default=0)
    priority = models.SmallIntegerField(default=0)
    
    created_by = models.ForeignKey('UserModel',
                                   on_delete=models.SET_NULL,
                                   related_name='role_creator',
                                   editable=False,
                                   null=True)
    modified_by = models.ForeignKey('UserModel',
                                    on_delete=models.SET_NULL,
                                    related_name='role_modifier',
                                    null=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tbl_role'
        managed = True
        verbose_name = 'role'
        verbose_name_plural = 'roles'



class UserModel(AbstractUser):
    groups = None
    user_permissions = None
    GENDER_CHOICE   = (('none', 'none'),('male', 'male'), ('female', 'female'))
    
    gender      = models.CharField(choices=GENDER_CHOICE,max_length=8,default='male')
    cellphone   = models.CharField(max_length=15, blank=True,null=True)
    email       = models.CharField(max_length=130, blank=True,null=True)
    is_active   = models.BooleanField(default=True)
    is_staff    = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=15, blank=True)


    created_by = models.ForeignKey('UserModel',
                                   on_delete=models.SET_NULL,
                                   related_name='user_creator',
                                   null=True,
                                   editable=False)
    modified_by = models.ForeignKey('UserModel',
                                    on_delete=models.SET_NULL,
                                    related_name='user_modifier',
                                    null=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tbl_user'
        managed = True
        verbose_name = 'user'
        verbose_name_plural = 'users'



class UserRoleModel(models.Model):
    user = models.ForeignKey("UserModel", on_delete=models.CASCADE, related_name="roles")
    role = models.ForeignKey("RoleModel", on_delete=models.CASCADE, related_name="role_user")

    class Meta:
        db_table = "tbl_user_role"
        managed = True
        unique_together = ["user", "role"]
        verbose_name = "user_role"
        verbose_name_plural = "user_roles"


