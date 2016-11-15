#coding:utf-8

import urllib
import urllib2
import re
import cookielib


class Login:

    __cookiejar = cookielib.CookieJar()
    __url_1 = 'http://4m3.tongji.edu.cn/eams/login.action'
    __url_2 = 'http://4m3.tongji.edu.cn/eams/samlCheck'
    __url_3 = 'https://ids.tongji.edu.cn:8443'
    __url_4 = 'http://4m3.tongji.edu.cn/eams/saml/SAMLAssertionConsumer'
    __menu_url = 'http://4m3.tongji.edu.cn/eams/home!submenus.action?menu.id='
    __welcome_url = 'http://4m3.tongji.edu.cn/eams/home!welcome.action'


    def Login(self):

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

        #get username&password post url
        final_credential_page = urllib2.urlopen(urllib2.Request(final_credential_url)).read()
        post_url = re.findall('''<form name="IDPLogin" enctype="application/x-www-form-urlencoded" method="POST" action="(.*?)" AUTOCOMPLETE="off">''', final_credential_page)[0]

        #post username and pw
        data = {'Ecom_User_ID': '1452716', 'Ecom_Password':'852147'}

        ret_page_1 = urllib2.urlopen( urllib2.Request(post_url, urllib.urlencode(data))).read()

        #get SamlAssertionCustomer url from the <javascript></javascript> label

        ret_url_1 = re.findall('''top.location.href='(.*?)';''', ret_page_1)[0]

        #get the infomation from the form and simulate the post request

        ret_page_2 = urllib2.urlopen(urllib2.Request(ret_url_1)).read()

        samlResponseValue = re.findall('''<input type="hidden" name="SAMLResponse" value="(.*?)"/>''',ret_page_2)[0]

        relayStateValue = re.findall('''<input type="hidden" name="RelayState" value="(.*?)"/>''', ret_page_2)[0]

        data_2 = {'SAMLResponse':samlResponseValue, 'RelayState': relayStateValue}

        samlAssertionPage = urllib2.urlopen(urllib2.Request(self.__url_4, urllib.urlencode(data_2))).read()

        #now you can get whatever you want

        menu_page = urllib2.urlopen( urllib2.Request(self.__menu_url)).read() #menu

        welcome_page = urllib2.urlopen(urllib2.Request(self.__welcome_url)).read() #menu

        return [samlAssertionPage, menu_page, welcome_page]




if __name__ == '__main__':
    testobj=Login()
    print testobj.Login()




