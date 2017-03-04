import json
import requests
import prettytable
import os
from optparse import OptionParser
WebTable = prettytable.PrettyTable(['IP','Server','Site','Title','Domains'])
HostTable = prettytable.PrettyTable(['IP','Banner','Timestamp','Port'])
class Zye:
    def __init__(self):
        self.config = 'config.json'
        self.uData = {
            'username':'',
            'password':'',
            'loginURL':'https://api.zoomeye.org/user/login',
            'resourceURL':'https://api.zoomeye.org/resources-info',
            'access_token':'',
            'host_search':'https://api.zoomeye.org/host/search',
            'web_search':'https://api.zoomeye.org/web/search'
        }
        self.headers = {'Authorization':'JWT '}
        if os.path.isfile(self.config):
            jsonFile = open(self.config,'r')
            data = ''
            for j in jsonFile.readlines():
                data=data+j
            uObj = json.loads(data)
            self.uData['username'] = uObj['username']
            self.uData['password'] = uObj['password']
            print('[*]Load user and password success ...')
        else:
            fp = open(self.config,'w')
            fp.writelines(json.dumps(self.uData))
            fp.close()
            print('[*]Create a json config file ...' + self.config)
        self.login()
    def login(self):
        try:
            udata = {'username':self.uData['username'],'password':self.uData['password']}
            req = requests.post(self.uData['loginURL'],data=json.dumps(udata))
        except:
            print('[*]Login Error')
            exit()
        if 'access_token' not in req.json():
            print('[*]NOT FOUND ACCESS TOKEN ..')
            return False
        self.uData['access_token'] = req.json()['access_token']
        print('[+]Get access token success ...')
        self.headers['Authorization']=self.headers['Authorization']+self.uData['access_token']
        return True
    def resource(self):
        try:
            req = requests.get(self.uData['resourceURL'],headers=self.headers)
        except:
            print('[*]Confirm resources Error')
            exit()
        print('[/]Plan: ['+ req.json()['plan'] + '] WebSearch: ['+ req.json()['resources']['web-search'] + '] HostSearch: ['+ req.json()['resources']['host-search']+']')
    def hostSearch(self,data):
        try:
            req = requests.get(self.uData['host_search'],params=data,headers=self.headers)
        except:
            print('[*]Confirm resources Error')
            exit()
        return req.json()
    def webSearch(self,data):
        try:
            req = requests.get(self.uData['web_search'],params=data,headers=self.headers)
        except:
            print('[*]Confirm resources Error')
            exit()
        return req.json()
    def loadUserInfo(self):
        print('[*]Username :' + self.uData['username'])
        if(self.login()):
            print('[*]Access token status is normal ...')
        else:
            print('[-]Please check config file ...')
            exit()
    def queryComb(self,optList,options):
        query = ''
        for opt in optList:
            value = getattr(options,opt,'')
            if value == '':
                continue
            else:
                query += opt+':'+value+'%20'
        print('[*]The search parameter combination is complete ...')
        return query[:-3]
    def optUserInfo(self,username,password):
        self.uData['username'] = username
        self.uData['password'] = password
        fp = open(self.config,'w')
        fp.writelines(json.dumps(self.uData))
        fp.close()
        print('[*]Create a json config file ...' + self.config)
        exit(0)
if __name__ == '__main__':
    opt = OptionParser()
    opt.add_option('-s','--status',dest='userInfo',help='查看用户信息',default=0,type='int')
    opt.add_option('-w','--web',dest='web',help='搜索WEB应用',default =None,type='string')
    opt.add_option('-o','--host',dest='host',help='搜索主机应用',default=None,type='string')
    opt.add_option('-i','--init',dest='init',help='初始化配置文件',default = 0,type='int')
    opt.add_option('-r','--resource',dest='resource',help='查看当前用户权限',default =0,type='int')
    opt.add_option('--app',dest='app',help='组件名',default ='',type='string')
    opt.add_option('--os',dest='os',help='操作系统',default ='',type='string')
    opt.add_option('--country',dest='country',help='国家或者地区代码',default = '',type='string')
    opt.add_option('--city',dest='city',help='城市',default = '',type='string')
    opt.add_option('--page',dest='page',help='翻页参数(默认为1)',default = 1,type='int')
    opt.add_option('--facets',dest='facets',help='统计项目，如果为多个，使用, 号分隔各个统计项',default ='',type='string')
    opt.add_option('--site',dest='site',help='网站域名',default = '',type='string')
    opt.add_option('--device',dest='device',help='设备类型',default = '',type='string')
    opt.add_option('--title',dest='title',help='网站标题',default = '',type='string')
    opt.add_option('--service',dest='service',help='服务名',default = '',type='string')
    opt.add_option('--hostname',dest='hostname',help='主机名',default = '',type='string')
    opt.add_option('--version',dest='version',help='组件版本',default = '',type='string')
    opt.add_option('--ver',dest='ver',help='组件版本',default = '',type='string')
    opt.add_option('--headers',dest='headers',help='HTTP 头',default = '',type='string')
    opt.add_option('--port',dest='port',help='端口',default = '',type='string')
    opt.add_option('--ip',dest='ip',help='IP地址',default = '',type='string')
    opt.add_option('--username',dest='username',help='用户名',default = '',type='string')
    opt.add_option('--password',dest='password',help='密码',default = '',type='string')
    opt.add_option('--cidr',dest='cidr',help='CIDR IP段， 例如 8.8.8.8/24',default = '',type='string')
    opt.add_option('--desc',dest='desc',help='<meta name="description">定义的页面说明',default = '',type='string')
    opt.add_option('--keywords',dest='keywords',help='<meta name="Keywords">定义的页面关键词',default = '',type='string')
    print('[*]Load Parser Success ...')
    (options, args) = opt.parse_args()
    print('[*]Load Zye API Boot Success ...')
    Zye = Zye()
    if options.username !='' and options.password !='':
        Zye.optUserInfo(options.username,options.password)
    if options.userInfo > 0:
        print('[*]Loading User info ...')
        Zye.loadUserInfo()
    if options.init > 0:
        Zye = Zye()
        pass
    if options.resource > 0:
        Zye.resource()
        pass
    if options.web == None and options.host == None:
        print('[\]Please check whether the parameters match properly ...')
    if options.web != None:
        optList = ['app','ver','country','city','site','os','title','headers','ip','cidr','desc','keywords']
        query = Zye.queryComb(optList,options)
        data = {'query':query,'page':options.page,'facets':options.facets}
        data = Zye.webSearch(data)
        print('[*]We found pieces of data :' + '<'+ str(data['total']) +'>')
        for target in data['matches']:
            WebTable.add_row([target['ip'][0],target['server'][0]['name'],target['site'],target['title'],target['domains']])
        print(WebTable)
    elif options.host !=None:
        optList = ['app','version','country','city','port','device','os','service','hostname','ip','cidr']
        query = Zye.queryComb(optList,options)
        data = {'query':query,'page':options.page,'facets':options.facets}
        data = Zye.hostSearch(data)
        print('[*]We found pieces of data :' + '<'+ str(data['total']) +'>')
        for target in data['matches']:
            HostTable.add_row([target['ip'],target['portinfo']['banner'],target['timestamp'],target['portinfo']['port']])
        print(HostTable)
    else:
        print('[\]Please check whether the parameters match properly ...')
        exit()