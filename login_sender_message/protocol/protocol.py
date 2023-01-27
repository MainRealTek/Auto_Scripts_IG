from requests import Session
from random import randint
from base64 import b64encode,b64decode
from time import time
from json import loads,dumps
from hashlib import md5,sha256
from hmac import new
from urllib import parse
from uuid import uuid4


"""Main object"""
class INSTA_SENDER_DM(object):
    def __init__(self,username=str(),password=str(),target_user=str()) -> None:
        self.API_URL      = 'https://i.instagram.com/api/v1/'
        self.s            = Session()
        self.username     = username
        self.password     = password
        self.target_user  = target_user
        self.uuid         = self.generateUUID(True)
        self.md5          = md5()
   
        self.isLoggedIn = False
        self.LastResponse = None

        self.DEVICE_SETTINTS = {
        'manufacturer'      : 'Xiaomi',
        'model'             : 'HM 1SW',
        'android_version'   : 18,
        'android_release'   : '4.3'
        }

        self.USER_AGENT = 'Instagram 9.2.0 Android ({android_version}/{android_release}; 320dpi; 720x1280; {manufacturer}; {model}; armani; qcom; en_US)'.format(**self.DEVICE_SETTINTS)
        self.IG_SIG_KEY = '012a54f51c49aa8c5c322416ab1410909add32c966bbaa0fe3dc58ac43fd7ede'
        self.SIG_KEY_VERSION = '4'


    def main(self,dm_message):
        self.params = self.md5.update(self.username.encode('utf-8') + self.password.encode('utf-8'))
        self.device_id = self.generateDeviceId(self.md5.hexdigest())

        """out vars into login()"""
        val_login,token,pk_id_mine = self.login()
        """get id of member on telegram"""
        val_pk,pk = self.get_id_user_insta(username=self.target_user)
        """main function that send to dm"""
        ultimate = self.send_dm(id_to_dm=pk,message=dm_message,AUTHORIZATION=self.dm_mess1(userid=pk_id_mine,token=token))


        if val_login == True:
            if val_pk == True:
                if ultimate == True:
                    return True,pk
                if ultimate == False:
                    return False,'ERROR|SEND'
            if val_pk == False:
                return False,'ERROR|PK'
        if val_login == False:
            return False,'ERROR|LOGIN'
        
        self.s.close()
        self.s.close()
        self.s.close()



    def generateUUID(self, type):
        generated_uuid = str(uuid4())
        if (type):
            return generated_uuid
        else:
            return generated_uuid.replace('-', '')
    """Get random device id""""
    def generateDeviceId(self, seed):
        volatile_seed = "12345"
        m = md5()
        m.update(seed.encode('utf-8') + volatile_seed.encode('utf-8'))
        return 'android-' + m.hexdigest()[:16]

    """part of uri"""
    def generateSignature(self, data):
        try:
            parsedData = parse.quote(data)
        except AttributeError:
            parsedData = parse.quote(data)
 
        return 'ig_sig_key_version=' + self.SIG_KEY_VERSION + '&signed_body=' + new(self.IG_SIG_KEY.encode('utf-8'), data.encode('utf-8'), sha256).hexdigest() + '.' + parsedData

    def generate_device_id(self,seed):
        return "android-" + seed[:16]


    """get in base64 the json for send with method post"""
    def dm_mess1(self,userid,token):

        to_encrypt = {"ds_user_id": userid, "sessionid": token, "should_use_header_over_cookies": True}
        to_encrypt = str(to_encrypt).replace("'", '"').replace('True', 'true').replace(' ', '')
        message_bytes = to_encrypt.encode('ascii')
        base64_bytes = b64encode(message_bytes)
        auth = base64_bytes.decode('ascii')
        
        return auth


    """Do login on instagram"""
    def login(self, force = False):
        if (not self.isLoggedIn or force):
            if (self.SendRequest('si/fetch_headers/?challenge_type=signup&guid=' + self.generateUUID(False), None, True)):
 
                data = {'phone_id'   : self.generateUUID(True),
                        '_csrftoken' : self.LastResponse.cookies['csrftoken'],
                        'username'   : self.username,
                        'guid'       : self.uuid,
                        'device_id'  : self.device_id,
                        'password'   : self.password,
                        'login_attempt_count' : '0'}
 
                if (self.SendRequest('accounts/login/', self.generateSignature(dumps(data)), True)):
                    self.isLoggedIn = True
                    self.username_id = self.LastJson["logged_in_user"]["pk"]
                    self.rank_token = "%s_%s" % (self.username_id, self.uuid)
                    self.token = self.LastResponse.cookies["csrftoken"]
                    return True,self.token,self.username_id
                else:
                    print("Login not successful")

    def send_dm(self,id_to_dm, message, AUTHORIZATION):
        json_auth = loads(b64decode(AUTHORIZATION).decode('utf-8'))
        my_user_id = json_auth['ds_user_id']
        #print(my_user_id)

        a_uuid = self.generateUUID(True)
        a_device_id = self.generate_device_id(self.generateUUID(False))

        """Header for send the msg"""#Got from requests I/O on network with firefox browser
        REQUEST_HEADERS = {
            'User-Agent':self.USER_AGENT,
            "X-Pigeon-Rawclienttime": str(round(time() * 1000)),
            "X-IG-Bandwidth-Speed-KBPS": str(randint(7000, 10000)),
            "X-IG-Bandwidth-TotalBytes-B": str(randint(500000, 900000)),
            "X-IG-Bandwidth-TotalTime-MS": str(randint(50, 150)),
            "x-ig-app-startup-country": "AR",
            "x-bloks-version-id": "251c3023d7ef985a0e5d91b885c0c03bbb32b4b721d8de33bf9f667ba39b41ff",
            "x-ig-www-claim": "hmac.AR3ilHwjy8Cu_OTGprygpxuify0pDUKnrJvY1wRvzNSFRwwD",
            "x-bloks-is-layout-rtl": "false",
            "x-bloks-is-panorama-enabled": "true",
            "x-ig-device-id": a_uuid,
            "x-ig-family-device-id": "0ff91d16-df30-4b83-91bb-ef6fe5a751fa",
            "x-ig-android-id": a_device_id,
            "x-ig-timezone-offset": "-7200",
            "x-ig-nav-chain": "1kw:feed_timeline:1,UserDetailFragment:profile:5,ProfileMediaTabFragment:profile:6,3xM:direct_thread:7",
            "x-ig-salt-ids": "1061163349",
            "x-ig-connection-type": "WIFI",
            "x-ig-capabilities": "3brTvx0=",
            "x-ig-app-id": "567067343352427",
            "priority": "u=3",
            "accept-language": "es-ES, en-US",
            "authorization": "Bearer IGT:2:" + AUTHORIZATION,
            "x-mid": "YYMo4AALAAFf64y70slcLACzpklN",
            "ig-u-ig-direct-region-hint": "ATN,48835113737,1667518455:01f7b0ee46fcbbaff69dfacfa670268aabc23145ec3868c74813073fb68730959e36791f",
            "ig-u-shbid": "9315,48835113737,1667316351:01f7d3483a632756a67739318c409667f8bf628ab96357ac142d5f8d8b1aec633e00925d",
            "ig-u-shbt": "1635780351,48835113737,1667316351:01f71ee7fe18abe0f30183c1e9ee8bf2e11701e107f982cf35ad9f2095bf08e0b3d69414",
            "ig-u-ds-user-id": str(my_user_id),
            "ig-u-rur": "VLL,48835113737,1667518478:01f7e869dc139eee715e5c5bfff4db350fe9c7f4c59979f70010e4333adbede244d9d068",
            "ig-intended-user-id": str(my_user_id),
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "accept-encoding": "zstd, gzip, deflate",
            "x-fb-http-engine": "Liger",
            "x-fb-client-ip": "True",
            "x-fb-server-cluster": "True"

        }

        #print('Dm to [{}] current session-id {}'.format(id_to_dm, my_user_id))
        """All parameters in json for send media,such as photo"""
        send_media = {
            "client_context": self.generateUUID(True),
            "action": "send_item",
            "recipient_users": "[[" + id_to_dm + "]]",
            "send_attribution": "photo_view_other",
            "media_id": "2687403059380025174_3949224551",
            "_uuid": a_uuid
        }
        """send type of text msg"""
        send_txt = {
            "client_context": self.generateUUID(True),
            "action": "send_item",
            "recipient_users": "[[" + id_to_dm + "]]",
            "text": message,
            "_uuid": a_uuid
        }

        """send request post for see if the message is sent or not"""
        resp_message = self.s.post(self.API_URL+'direct_v2/threads/broadcast/text/',headers=REQUEST_HEADERS, data=send_txt)
        if resp_message.status_code == 200:
            return True
        else:
            return False
            


    """main function for send requests get or post"""
    def SendRequest(self, endpoint, post = None, login = False):
        if (not self.isLoggedIn and not login):
            raise Exception("Not logged in!\n")
            return;
        self.s.headers.update ({'Connection' : 'close',
                                'Accept' : '*/*',
                                'Content-type' : 'application/x-www-form-urlencoded; charset=UTF-8',
                                'Cookie2' : '$Version=1',
                                'Accept-Language' : 'en-US',
                                'User-Agent' : self.USER_AGENT})
        if (post != None): # POST
            response = self.s.post(self.API_URL + endpoint, data=post) # , verify=False
        else: # GET
            response = self.s.get(self.API_URL + endpoint) # , verify=False
 
        if response.status_code == 200:
            self.LastResponse = response
            self.LastJson = loads(response.text)
            #print(self.LastJson)
            return True
        else:
            try:
                self.LastResponse = response
                self.LastJson = loads(response.text)
                #print(self.LastJson)
            except:
                pass
            return False
 

 

 #https://www.instagram.com/web/search/topsearch/?context=blended&query=username&rank_token=0.3953592318270893&count=1
    def get_id_user_insta(self,username):
        url = "https://www.instagram.com/web/search/topsearch/?context=blended&query="+username+"&rank_token=0.3953592318270893&count=1"
        self.s.headers.update ({'Connection' : 'close',
                                'Accept' : '*/*',
                                'Content-type' : 'application/x-www-form-urlencoded; charset=UTF-8',
                                'Cookie2' : '$Version=1',
                                'Accept-Language' : 'en-US',
                                'User-Agent' : self.USER_AGENT})


        response = self.s.get(url)
        #see in dict
        respJSON = response.json()
        #print(respJSON)

        i = 0
        try:
            while i < 100:
                if respJSON['users'][i]['user']['username'] == username:
                    pk = respJSON['users'][i]['user']['pk']
                    return True,str(pk)


                if respJSON['users'][i]['user']['username'] != username:
                    i+=1
 
            #return str(pk)
        except Exception:
            return False


