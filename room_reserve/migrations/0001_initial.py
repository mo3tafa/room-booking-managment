# Generated by Django 4.0.4 on 2022-05-10 09:51

import datetime
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('gender', models.CharField(choices=[('none', 'none'), ('male', 'male'), ('female', 'female')], default='male', max_length=8)),
                ('cellphone', models.CharField(blank=True, max_length=15, null=True)),
                ('email', models.CharField(blank=True, max_length=130, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('verification_code', models.CharField(blank=True, max_length=15)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_creator', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_modifier', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'db_table': 'tbl_user',
                'managed': True,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='RoleModel',
            fields=[
                ('title', models.CharField(max_length=130, primary_key=True, serialize=False)),
                ('order', models.SmallIntegerField(default=0)),
                ('priority', models.SmallIntegerField(default=0)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='role_creator', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='role_modifier', to=settings.AUTH_USER_MODEL)),
                ('parent', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subordinates', to='room_reserve.rolemodel')),
            ],
            options={
                'verbose_name': 'role',
                'verbose_name_plural': 'roles',
                'db_table': 'tbl_role',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='TokenModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.TextField(unique=True)),
                ('remote_addr', models.TextField()),
                ('user_agent', models.TextField()),
                ('player_id', models.TextField(unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bearer_token', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'token',
                'verbose_name_plural': 'tokens',
                'db_table': 'tbl_token',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='RoomModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, unique=True)),
                ('capacity', models.IntegerField(default=1)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='room_creator', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='room_modifier', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'room',
                'verbose_name_plural': 'rooms',
                'db_table': 'tbl_room',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='ReservationModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reserved_start_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('reserved_end_date', models.DateTimeField(default=datetime.datetime(2022, 5, 11, 9, 51, 55, 879081, tzinfo=utc))),
                ('comment', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reservation_creator', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reservation_modifier', to=settings.AUTH_USER_MODEL)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='room_reserve.roommodel')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservationsInfo', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'reservation',
                'verbose_name_plural': 'reservations',
                'db_table': 'tbl_reservation',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='UserRoleModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='role_user', to='room_reserve.rolemodel')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='roles', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'user_role',
                'verbose_name_plural': 'user_roles',
                'db_table': 'tbl_user_role',
                'managed': True,
                'unique_together': {('user', 'role')},
            },
        ),
    ]
