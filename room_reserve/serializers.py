from rest_framework import serializers
from rest_framework import status
from django.utils.translation import gettext as _
from room_reserve.helpers import get_user, get_verfication_code 

from room_reserve.models import *
from room_reserve.exceptions import ProjectException





#----------User Change Password:----------
class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(max_length=128)
    new_password     = serializers.CharField(max_length=128)

    def validate(self, attrs):
        self.user = self.context['request'].user
        _current_password = attrs.get('current_password', None)
        _new_password = attrs.get('new_password', None)
        if _new_password:
            if len(_new_password) < 8:
                raise ProjectException(812, _('validation error'),
                                       _("password cannot less than 8 digit"),
                                       status.HTTP_400_BAD_REQUEST)
            if _current_password == _new_password:
                raise ProjectException(805, _('validation error'),
                                       _("The new password cannot be the same as the current one."),
                                       status.HTTP_400_BAD_REQUEST)
        return attrs


# Login
class LoginSerializer(serializers.Serializer):
    access_token    = serializers.CharField(read_only=True)
    id              = serializers.IntegerField(read_only=True)
    username        = serializers.CharField(max_length=150)
    password        = serializers.CharField(max_length=128, write_only=True)
    email           = serializers.CharField(read_only=True)
    name            = serializers.SerializerMethodField(read_only=True,
                                             method_name="get_name")
    gender          = serializers.CharField(read_only=True)
    status          = serializers.IntegerField(read_only=True)
    is_active       = serializers.BooleanField(read_only=True)
    
    def get_name(self, obj):
        _name = "".join([obj.first_name, ' ', obj.last_name])
        return _name
    def validate(self, attrs):
        _username = attrs.pop("username", None)
        _password = attrs.get("password", None)

        if _username:
            _username = _username.lower()
            _object = None
            try:
                _object = UserModel.objects.get(username=_username)
                attrs["username"] = _username
            except:
                try:
                    _object = UserModel.objects.get(cellphone=_username)
                    attrs["username"] = _object.username
                except:
                    try:
                        _object = UserModel.objects.get(email=_username)
                        attrs["username"] = _object.username
                    except:
                        pass

        return attrs


#----------None:----------
class NoneSerializer(serializers.Serializer):
    pass


#----------Room:----------
class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomModel
        fields = ('id','name','capacity')
    name     = serializers.CharField(max_length=80)
    capacity = serializers.IntegerField(required=False)

    def validate(self, attrs):
        self.user = get_user(context=self.context)
        return attrs
    def create(self, validated_data):
        if self.user and self.user.pk:
            validated_data['created_by'] = self.user
            validated_data['modified_by'] = self.user
        new_instance = self.Meta.model(**validated_data)
        new_instance.save()
        return new_instance
    def update(self, instance, validated_data):
        if self.user and self.user.pk:
            validated_data['modified_by'] = self.user
        for attr,value in validated_data.items():
            setattr(instance,attr,value)
        instance.save()
        return instance

class RoomInfoSerializer(serializers.Serializer):
    id       = serializers.IntegerField(read_only=True)
    name     = serializers.CharField(read_only=True)
    capacity = serializers.IntegerField(read_only=True)

class RoomFilterQuerySerializer(serializers.Serializer):
    
    search      = serializers.CharField(max_length=None, required=False,help_text="Search by room name")
    start_date  = serializers.DateTimeField(required=False)
    end_date    = serializers.DateTimeField(required=False)
    
    
    page_size = serializers.IntegerField(required=False)
    page_num = serializers.IntegerField(required=False)


#----------Reservation:----------
class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model  = ReservationModel
        fields = ('id','room','first_name','last_name','cellphone','reserved_start_date','reserved_end_date','comment')
    
    room                = serializers.PrimaryKeyRelatedField(many=False,required = True,
                                queryset=RoomModel.objects.all(),
                                error_messages={
                                    "does_not_exist": _("room does not exist"),
                                    "invalid": _("invalid value"),
                                },
                            )
    first_name          = serializers.CharField(max_length=150)
    last_name           = serializers.CharField(max_length=150)
    cellphone           = serializers.CharField(max_length=15,required=True)
    reserved_start_date = serializers.DateTimeField()
    reserved_end_date   = serializers.DateTimeField()
    comment             = serializers.CharField(max_length=None,allow_blank=True,required=False)
    
    def validate(self, attrs):
        from django.db.models import Q
        self.user = get_user(context=self.context)
        _room       = attrs.get('room',None)
        _start_date = attrs.get('reserved_start_date',None)
        _end_date   = attrs.get('reserved_end_date',None)
        _reserves   = ReservationModel.objects.filter(Q(room=_room),
                                Q(reserved_start_date__lte=_start_date,reserved_end_date__gt=_start_date)|
                                Q(reserved_start_date__gte=_start_date,reserved_start_date__lt=_end_date)
                                )
        if _reserves:
            raise ProjectException(813, _('validation error'), _('The room is reserved at the appropriate time.'),status.HTTP_400_BAD_REQUEST)
        
        return attrs
    def create(self, validated_data):
        _first_name = validated_data.pop('first_name',None)
        _last_name  = validated_data.pop('last_name',None)
        _cellphone  = validated_data.pop('cellphone',None)
        _user = None
        try:
            _user = UserModel.objects.get(cellphone=_cellphone)
            _user.first_name = _first_name
            _user.last_name  = _last_name
            _user.save()
        except:
            _pass = str(get_verfication_code(6))
            _user_data = {
                'first_name':_first_name, 'last_name':_last_name,'cellphone':_cellphone,
                'username':_cellphone, 'verification_code':_pass
            }
            _user = UserModel(**_user_data)
            _user.set_password(_pass)
            _user.save()
        validated_data['user'] = _user

        if self.user and self.user.pk:
            validated_data['created_by']  = self.user
            validated_data['modified_by'] = self.user
        
        new_instance = self.Meta.model(**validated_data)
        new_instance.save()
        return new_instance

class ReservationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model  = ReservationModel
        fields = ('id','room','reserved_start_date','reserved_end_date')
    
    room                = serializers.PrimaryKeyRelatedField(many=False,required = False,
                                queryset=RoomModel.objects.all(),
                                error_messages={
                                    "does_not_exist": _("room does not exist"),
                                    "invalid": _("invalid value"),
                                },
                            )
    reserved_start_date = serializers.DateTimeField(required = False)
    reserved_end_date   = serializers.DateTimeField(required = False)
    

    def validate(self, attrs):
        from django.db.models import Q
        self.user = get_user(context=self.context)
        _room       = attrs.get('room',None)
        _start_date = attrs.get('reserved_start_date',None)
        _end_date   = attrs.get('reserved_end_date',None)
        if _room is None:
            _room = self.instance.room
        if _start_date is None:
            _start_date = self.instance.reserved_start_date
        if _end_date is None:
            _end_date = self.instance.reserved_end_date
        _reserves   = ReservationModel.objects.filter(Q(room=_room),
                                Q(reserved_start_date__lte=_start_date,reserved_end_date__gt=_start_date)|
                                Q(reserved_start_date__gte=_start_date,reserved_start_date__lt=_end_date)
                                ).exclude(pk=self.instance.pk)
        if _reserves:
            raise ProjectException(813, _('validation error'), _('The room is reserved at the appropriate time.'),status.HTTP_400_BAD_REQUEST)
        
        return attrs
    def update(self, instance, validated_data):
        
        if self.user and self.user.pk:
            validated_data['modified_by'] = self.user
        for attr,value in validated_data.items():
            setattr(instance,attr,value)
        instance.save()
        return instance
    
class ReservationInfoSerializer(serializers.Serializer):
    
    id                  = serializers.IntegerField(read_only=True)
    room                = serializers.SerializerMethodField(read_only=True)
    first_name          = serializers.SerializerMethodField(read_only=True)
    last_name           = serializers.SerializerMethodField(read_only=True)
    cellphone           = serializers.SerializerMethodField(read_only=True)
    reserved_start_date = serializers.DateTimeField(read_only=True)
    reserved_end_date   = serializers.DateTimeField(read_only=True)
    comment             = serializers.CharField(read_only=True)
    
    def get_room(self,obj):
        return obj.room.name
    def get_first_name(self,obj):
        return obj.user.first_name
    def get_last_name(self,obj):
        return obj.user.last_name
    def get_cellphone(self,obj):
        return obj.user.cellphone

class ReservationFilterQuerySerializer(serializers.Serializer):
    
    search      = serializers.CharField(max_length=None, required=False,help_text="Search by user fullname")
    room        = serializers.CharField(required=False)
    start_date  = serializers.DateTimeField(required=False)
    end_date    = serializers.DateTimeField(required=False)
    
    page_size = serializers.IntegerField(required=False)
    page_num = serializers.IntegerField(required=False)


# Token:
class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = TokenModel
        fields = ('key','user', 'remote_addr', 'user_agent', 'player_id')

    key  = serializers.CharField(max_length=None)
    remote_addr = serializers.CharField(max_length=None)
    player_id = serializers.CharField(max_length=None)
    user_agent = serializers.CharField(max_length=None)
    user = serializers.PrimaryKeyRelatedField(many=False,
                                              queryset=UserModel.objects.all(),
                                              error_messages={
                                                  'does_not_exist':
                                                  "user does not exist",
                                                  'invalid': "invalid value"
                                              })

    def validate(self, attrs):
        return attrs
    def create(self, validated_data):
        _player_id = validated_data['player_id']
        _remote_addr = validated_data['remote_addr']
        _user_agent = validated_data['user_agent']
        _user = validated_data['user']
        _user_id = _user.id
        if _player_id:
            try:
                _object = TokenModel.objects.get(player_id=_player_id)
                _object.delete()
            except TokenModel.DoesNotExist:
                pass
        _new_instance = self.Meta.model(**validated_data)
        _new_instance.save()
        return _new_instance


# User:
class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('id', 'first_name', 'last_name','username','password','cellphone', 'email','gender',)
        extra_kwargs = {'password': {'write_only': True},}

    first_name  = serializers.CharField(max_length=150)
    last_name   = serializers.CharField(max_length=150)
    username    = serializers.CharField(max_length=150,required=True)
    password    = serializers.CharField(max_length=128,required = True)
    cellphone   = serializers.CharField(max_length=15,required=False)
    email       = serializers.EmailField(required=False)
    gender      = serializers.ChoiceField(choices=UserModel.GENDER_CHOICE,required=False)

    def validate(self, attrs):
        self.user  = get_user(context=self.context)
        _password  = attrs.get('password', None)
        _username  = attrs.pop('username', None)
        _cellphone = attrs.get('cellphone', None)
        _email     = attrs.get('email', None)

        # Check unique Field:
        if _email:
            try:
                UserModel.objects.get(email=_email)
                raise ProjectException(809,'validation error','There is a user with this email in this system.',status_code=status.HTTP_400_BAD_REQUEST)
            except UserModel.DoesNotExist:
                pass
        if _cellphone:
            from room_reserve.helpers import validate_phone_number
            if not validate_phone_number(_cellphone,"IR"):
                raise ProjectException(807,
                                _("validation error"),_("'Cellphone': this field is invalid"),
                                status.HTTP_400_BAD_REQUEST)
            try:
                UserModel.objects.get(cellphone=_cellphone)
                raise ProjectException(808,
                                'validation error','There is a user with this cellphone in this system.',
                                status_code=status.HTTP_400_BAD_REQUEST)
            except UserModel.DoesNotExist:
                pass
        if _username:
            _username = _username.lower()
            try:
                UserModel.objects.get(username=_username)
                raise ProjectException(810,'validation error','There is a user with this username in this system.',status_code=status.HTTP_400_BAD_REQUEST)
            except UserModel.DoesNotExist:
                if len(_username) < 4:
                    raise ProjectException(811, _('validation error'),_("username cannot les than 4 digit"),status.HTTP_400_BAD_REQUEST)
                attrs['username']=_username
        if _password:
            if len(_password) < 8:
                raise ProjectException(812, 
                        _('validation error'), _("password cannot les than 8 digit"),
                        status.HTTP_400_BAD_REQUEST)
        
        return attrs
    def create(self, validated_data):
        _password = validated_data.pop('password', None)
        new_instance = self.Meta.model(**validated_data)
        if _password:
            new_instance.set_password(_password)
            new_instance.verification_code = _password
        new_instance.is_active = True
        new_instance.save()
        return new_instance


class UserInfoSerializer(serializers.Serializer):

    id          = serializers.IntegerField(read_only=True)
    first_name  = serializers.CharField(read_only=True)
    last_name   = serializers.CharField(read_only=True)
    name        = serializers.SerializerMethodField(read_only=True)
    username    = serializers.CharField(read_only=True)
    email       = serializers.EmailField(read_only=True)
    cellphone   = serializers.CharField(read_only=True)
    gender      = serializers.CharField(read_only=True)
    status      = serializers.IntegerField(read_only=True)
    is_active   = serializers.BooleanField(read_only=True)
    created     = serializers.DateTimeField(read_only=True)
    

    def get_name(self, obj):
        _name = "".join([obj.first_name, ' ', obj.last_name])
        return _name
