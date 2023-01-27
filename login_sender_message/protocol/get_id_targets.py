from requests import Session
from json import loads
from sys import argv


class GetRandomIdTarget(object):
    def __init__(self):
        self.req = Session()
        self.DEVICE_SETTINTS = {
        'manufacturer'      : 'Xiaomi',
        'model'             : 'HM 1SW',
        'android_version'   : 18,
        'android_release'   : '4.3'
        }
        self.USER_AGENT = 'Instagram 9.2.0 Android ({android_version}/{android_release}; 320dpi; 720x1280; {manufacturer}; {model}; armani; qcom; en_US)'.format(**self.DEVICE_SETTINTS)



    def get_id_user_insta(self,query):
        result = []
        url = "https://www.instagram.com/web/search/topsearch/?context=blended&query="+query+"&rank_token=0.3953592318270893&count=1"
        self.req.headers.update ({'Connection' : 'close',
                                'Accept' : '*/*',
                                'Content-type' : 'application/x-www-form-urlencoded; charset=UTF-8',
                                'Cookie2' : '$Version=1',
                                'Accept-Language' : 'en-US',
                                'User-Agent' : self.USER_AGENT})


        response = self.req.get(url)
        respJSON = response.json()
        #print(respJSON)

        i = 0
        try:
            while i < 100:
                if respJSON['users'][i]['user']['username']:
                    if respJSON['users'][i]['user']['is_verified'] == False:
                        if respJSON['users'][i]['user']['is_private'] == False:
                            pk = respJSON['users'][i]['user']['pk']
                            result.append(pk)

                i+=1
        except Exception:
            pass

        return result


def read(filex):
    result = []
    i = open(filex,'r')
    lines = i.readlines()
    for ln in lines:
        ii = ln.rstrip('\n\r')
        result.append(ii)

    i.close()

    return result

def write(filex,listx=list()):
    ii = open(filex,'a')
    for i in listx:
        ii.write(i)
        ii.write('\n')


    ii.close()



def main(keyworlds=str()):

    c = 0
    keys = read(keyworlds)


    for i in keys:
        result = GetRandomIdTarget().get_id_user_insta(i)
        write('output_id_target.txt',result)
        print(len(result))
        c+=1




if __name__ == '__main__':
    main(argv[1])







