from nacl.public import PublicKey, SealedBox
from string import ascii_lowercase
from Crypto.Cipher import AES
from binascii import unhexlify
from datetime import datetime
from base64 import b64encode
from requests import Session
from random import randrange,randint
from Crypto import Random
from random import choice
from struct import pack
from json import loads
from sys import exit


class RegisterIG(object):
    def __init__(self,email=str(),first_name=str(),pasw=str()) -> None:
        self.API_URL       = 'https://i.instagram.com/api/v1'
        self.email         = email
        self.first_name    = first_name
        self.pasw          = pasw

        self.key_id = 235
        self.pub_key = '3d274f9ca06a1d895ed48f7ca14465848aeb82f6ecc0be10333137f525b0135d'
        self.pasw_key = 10

        self.DEVICE_SETTINTS = {
        'manufacturer'      : 'Xiaomi',
        'model'             : 'HM 1SW',
        'android_version'   : 18,
        'android_release'   : '4.3'
        }

        self.USER_AGENT = 'Instagram 9.2.0 Android ({android_version}/{android_release}; 320dpi; 720x1280; {manufacturer}; {model}; armani; qcom; en_US)'.format(**self.DEVICE_SETTINTS)


        self.isLoggedIn = False
        self.LastResponse = None


        pass


    def get_random_string(self):
        # choose from all lowercase letter
        letters = ascii_lowercase
        result_str = ''.join(choice(letters) for i in range(28)).upper()
        return result_str



    def main(self):
        check_users = self.check_user()

        if check_users == False:
            print('|ERROR|check user')
        if check_users[0] == True:
            print('CHECK USERNAME')
            self.users_avaiable = check_users[1]
            user_set = self.set_user(list_users=self.users_avaiable)
            self.username = user_set[1]
            print(self.username)
            if user_set[0] == True:
                print('SET USERNAME')
                age_check = self.check_age()[0]
                self.day,self.month,self.year = self.check_age()[1],self.check_age()[2],self.check_age()[3]
                if age_check == True:
                    print('SET AGE')
                    try:
                    	self.id_clientx = self.check_OTP()[1]
                    except Exception:
                    	print('ERROR OTP ')
                    	exit()
                    print('PUT HERE YOUR SMS CODE')
                    self.ii = input('')
                    if self.send_OPT(id_client=self.id_clientx,code=self.ii) == True:
                        finished = self.ultimate_POST()
                        if finished == True:

                            print('Account Created')
                            print(f'{self.email}|{self.first_name}|{self.username}|{self.pasw}')
                        #return self.email,self.first_name,self.username,self.pasw








    def check_user(self):
        self.recv = self.ReqSend(endpoint='/web/accounts/web_create_ajax/attempt/',post_get=True,
                                                                                              datax={
                                                                                                "email": self.email,#phone_number
                                                                                                "username": "",
                                                                                                "first_name": self.first_name,
                                                                                                "opt_into_one_tap": "false"
                                                                                                      })


        if self.recv == False:
            return False
        if self.recv[0] == True:
            self.users = self.recv[1]['username_suggestions']

            return True,self.users



    def set_user(self,list_users=list()):
        lenght = len(list_users)
        user_found = list_users[randrange(0,lenght)]
        self.recv = self.ReqSend(endpoint='/web/accounts/web_create_ajax/attempt/',post_get=True,
                                                                                              datax={
                                                                                               "enc_password": self.encrypt_password(key_id=self.key_id,pub_key=self.pub_key,password=self.pasw,version=self.pasw_key),
                                                                                                "email": self.email,#phone_number
                                                                                                "username": user_found,
                                                                                                "first_name": self.first_name,
                                                                                                "opt_into_one_tap": "false"
                                                                                                     })
        if self.recv == False:
            return False
        if self.recv[0] == True:
            self.response = self.recv[1]
            if self.response['status'] == 'ok':
                return True,user_found


    def check_age(self):
        day = randint(1,28);month = randint(1,12);year = randint(1980,2000)
        self.resp = self.ReqSend(endpoint='/web/consent/check_age_eligibility/',post_get=True,datax={
                                                                                                "day": randint(1,28),
                                                                                                "month": randint(1,12),
                                                                                                "year": randint(1980,2000)
                                                                                                 })
        return True,str(day),str(month),str(year)

#https://www.instagram.com/api/v1/web/accounts/send_signup_sms_code_ajax/
    def check_OTP(self):
        self.id_client = self.get_random_string()
        self.resp = self.ReqSend(endpoint='/web/accounts/send_signup_sms_code_ajax/',post_get=True,datax={
                                                                                            "client_id": self.id_client,#device_id
                                                                                            "phone_number": self.email#email
                                                                                            })
        if self.resp == False:
            print('ERROR')
        if self.resp[0] == True:
            return True,self.id_client


    #https://www.instagram.com/api/v1/accounts/check_confirmation_code/   email
    #https://www.instagram.com/api/v1/web/accounts/validate_signup_sms_code_ajax/ sms
    def send_OPT(self,id_client=str(),code=str()):
        self.resp = self.ReqSend(endpoint='/web/accounts/validate_signup_sms_code_ajax/',post_get=True,datax={
                                                                "client_id": id_client,    #device_id
                                                                "phone_number": self.email,#phone_number
                                                                "sms_code": code           #code

                                                                   })
        if self.resp == False:
            print('ERROR')
        if self.resp[0] == True:
            return True
    def ReqSend(self,endpoint,post_get=True,datax=dict()):
        self.s = Session()
        self.s.headers.update ({'Connection' : 'close',
                                'Accept' : '*/*',
                                'Content-type' : 'application/x-www-form-urlencoded; charset=UTF-8',
                                'Cookie2' : '$Version=1',
                                'Accept-Language' : 'en-US',
                                'User-Agent' : self.USER_AGENT})

        

        if post_get == True: # POST
            response = self.s.post(self.API_URL + endpoint, data=datax,) # , verify=False
        if post_get == False: # GET
            response = self.s.get(self.API_URL + endpoint) # , verify=False
        if post_get == None:
            response = self.s.get(endpoint)

        #print(response.status_code)
        #print(response.text)
        if response.status_code == 200:
            self.LastResponse = response
            #print(self.LastResponse.text)
            try:
                self.LastJson = loads(self.LastResponse.text)
                #print(self.LastJson)
                return True, self.LastJson
            except Exception as i:
                #print(i)
                return False


    
    def ultimate_POST(self):
        self.recv = self.ReqSend(endpoint='/web/accounts/web_create_ajax/attempt/',post_get=True,datax={
                                                                                                        'enc_password':self.encrypt_password(key_id=self.key_id,pub_key=self.pub_key,password=self.pasw,version=self.pasw_key),
                                                                                                        'phone_number':self.email,
                                                                                                        "username":self.username,
                                                                                                        "first_name": self.first_name,
                                                                                                        "sms_code": self.ii,
                                                                                                        "client_id": self.id_clientx,
                                                                                                        "seamless_login_enabled": "1"
                                                                                                        })

        if self.recv[0] == True:
            self.recv = self.ReqSend(endpoint='/web/accounts/web_create_ajax/', post_get=True, datax={
                                                                                                        'enc_password': self.encrypt_password(key_id=self.key_id, pub_key=self.pub_key, password=self.pasw,version=self.pasw_key),
                                                                                                        'phone_number': self.email,
                                                                                                        "username": self.username,
                                                                                                        "first_name": self.first_name,
                                                                                                        "month": self.month,
                                                                                                        "day": self.day,
                                                                                                        "year": self.year,
                                                                                                        "sms_code": self.ii,
                                                                                                        "client_id": self.id_clientx,
                                                                                                        "seamless_login_enabled": "1",
                                                                                                        "tos_version" : "eu"
                                                                                                        })






    def encrypt_password(self,key_id, pub_key, password, version=10):
        key = Random.get_random_bytes(32)
        iv = bytes([0] * 12)

        time = int(datetime.now().timestamp())

        aes = AES.new(key, AES.MODE_GCM, nonce=iv, mac_len=16)
        aes.update(str(time).encode('utf-8'))
        encrypted_password, cipher_tag = aes.encrypt_and_digest(password.encode('utf-8'))

        pub_key_bytes = unhexlify(pub_key)
        seal_box = SealedBox(PublicKey(pub_key_bytes))
        encrypted_key = seal_box.encrypt(key)

        encrypted = bytes([1,
                           key_id,
                           *list(pack('<h', len(encrypted_key))),
                           *list(encrypted_key),
                           *list(cipher_tag),
                           *list(encrypted_password)])
        encrypted = b64encode(encrypted).decode('utf-8')

        return f'#PWD_INSTAGRAM_BROWSER:{version}:{time}:{encrypted}'

########################################################################################################################






