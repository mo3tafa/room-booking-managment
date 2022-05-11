from rest_framework.test import APITestCase
from rest_framework import status
from datetime import datetime

from room_reserve.serializers import *

class DefaultAPITest(APITestCase):
    # python manage.py test room_reserve.tests.DefaultAPITest.main
    _path = '/booking/core/api/'

    def setUp(self):
        self._data_login_admin = {"username": "admin","password": "adminadmin"}
        self._data_user = {
            "first_name": "mostafa","last_name": "hosseini",
            "username": "utest","password": "ptest1234",
            "email": "mostafa@gmail.com","cellphone": "09216733700",
            "gender": "male"
        }
        self._data_login = {
            "username": "utest","password": "ptest1234"
        }
        self.user = UserModel.objects.create_user(**self._data_user)
        self.user.save()
    def tearDown(self):
        self.user.delete()
    
    def test_login(self):
        # ./manage.py test room_reserve.tests.DefaultAPITest.test_login
        _url = self._path + 'login/'
        response = self.client.post(path=_url, data=self._data_login, format='json')
        print("***********Login User:*************************")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response)
        print(response.data)
    def test_logout(self):

        _url = self._path + 'logout/'
        response = self.client.post(path=_url,data={},format="json")
        print("***********Logout User:*************************")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response)
        print(response.data)

    def main(self):
        # python manage.py test room_reserve.tests.DefaultAPITest.main
        self.test_login()
        self.test_logout()


class RoomAPITest(DefaultAPITest):
    # python manage.py test room_reserve.tests.RoomAPITest.room_main
    
    _path_room = '/booking/core/api/room/'
    def setUp(self):
        super().setUp()
        self._room_data_list = [{'name':'10'},{'name':'20'},{'name':'30'},{'name':'40'},{'name':'50'}]
    


    def test_create_room(self,data=None):
        print(self._path_room)
        response = self.client.post(path=self._path_room,data=data,format='json')
        print("***********Create Room:*************************")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        print(response)
        print(response.data)
    def test_list_room(self):
        
        response = self.client.get(path=self._path_room)
        print("***********List Room:*************************")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response)
        print(response.data)


    def room_main(self):
        # python manage.py test room_reserve.tests.RoomAPITest.room_main
        self.test_login()
        for item in self._room_data_list:
            self.test_create_room(data=item)
        # self.test_list_room()

class ReservationAPITest(RoomAPITest):
    # python manage.py test room_reserve.tests.ReservationAPITest.reservation_main
    
    _path_reserve = '/booking/core/api/reservation/'
    def setUp(self):
        super().setUp()
        self._reserve_data = {"room": 1,
                            "first_name": "mostafa","last_name": "hosseini","cellphone": "09168249265",
                            "reserved_start_date": "2022-05-11T08:17:54.029Z",
                            "reserved_end_date": "2022-05-15T08:17:54.029Z"
                        }
    
    def test_create_reservation(self,data):
        response = self.client.post(path=self._path_reserve,data=data,format='json')
        print("***********Create Reservation:*************************")
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        print(response)
        print(response.data)
    
    def test_get_unreserved_rooms(self,start,end):
        _filter_path = self._path_room + f'?start_date={start}&end_date={end}'
        response = self.client.get(path=_filter_path)
        print("***********List Unreserved Room:*************************")
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        print(response)
        print(response.data)
    

    def reservation_main(self):
        # python manage.py test room_reserve.tests.ReservationAPITest.reservation_main
        self.room_main()
        self.test_create_reservation(data=self._reserve_data)
        _start = datetime(year=2022, month=5, day=11, hour=10, minute=0, second=0)
        _end   = datetime(year=2022, month=5, day=16, hour=12, minute=0, second=0)
        self.test_get_unreserved_rooms(start=_start,end=_end)