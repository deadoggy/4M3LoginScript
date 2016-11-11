#coding:utf-8

import urllib
import  urllib2
import re
import cookielib
import httplib2


class Login:

    __cookiejar = cookielib.CookieJar()
    __url_1 = 'http://4m3.tongji.edu.cn/eams/login.action'
    __url_2 = 'http://4m3.tongji.edu.cn/eams/samlCheck'
    __url_3 = 'https://ids.tongji.edu.cn:8443'


    def getIdsUrl(self):

        opener = urllib2.build_opener( urllib2.HTTPCookieProcessor(self.__cookiejar))
        urllib2.install_opener(opener)

        #get cookie
        urllib2.urlopen(urllib2.Request(self.__url_1))

        #get middle credential url
        middle_credential_text = urllib2.urlopen(urllib2.Request(self.__url_2)).read()
        middle_credential_url = re.findall('''url=(.*?)">''', middle_credential_text)[0]

        #get credential page
        credential_page = urllib2.urlopen(urllib2.Request(middle_credential_url)).read()
        final_credential_url = self.__url_3 + re.findall(''' <form method="POST" enctype="application/x-www-form-urlencoded" action="(.*?)">''', credential_page)[0]

        #get final post url
        final_credential_page = urllib2.urlopen(urllib2.Request(final_credential_url)).read()
        post_url = re.findall('''<form name="IDPLogin" enctype="application/x-www-form-urlencoded" method="POST" action="(.*?)" AUTOCOMPLETE="off">''', final_credential_page)[0]

        #post username and pw
        data = {'Ecom_User_ID': '1452716', 'Ecom_Password':'852147'}

        ret_page = urllib2.urlopen( urllib2.Request(post_url, urllib.urlencode(data))).read()


        pass



if __name__ == '__main__':
    testobj=Login()
    testobj.getIdsUrl()




