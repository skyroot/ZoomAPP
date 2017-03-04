#  ZoomEye API Python Controller
使用之前需要先配置好 config.json 中的用户名和密码
也可以直接调用命令接口
```
root@Qingxuan:~/PycharmProjects/ZoomEye# python35 Zoom.py -h
[*]Load Parser Success ...
Usage: Zoom.py [options]

Options:
  -h, --help            show this help message and exit
  -s USERINFO, --status=USERINFO
                        查看用户信息
  -w WEB, --web=WEB     搜索WEB应用
  -o HOST, --host=HOST  搜索主机应用
  -i INIT, --init=INIT  初始化配置文件
  -r RESOURCE, --resource=RESOURCE
                        查看当前用户权限
  --app=APP             组件名
  --os=OS               操作系统
  --country=COUNTRY     国家或者地区代码
  --city=CITY           城市
  --page=PAGE           翻页参数(默认为1)
  --facets=FACETS       统计项目，如果为多个，使用, 号分隔各个统计项
  --site=SITE           网站域名
  --device=DEVICE       设备类型
  --title=TITLE         网站标题
  --service=SERVICE     服务名
  --hostname=HOSTNAME   主机名
  --version=VERSION     组件版本
  --ver=VER             组件版本
  --headers=HEADERS     HTTP 头
  --port=PORT           端口
  --ip=IP               IP地址
  --username=USERNAME   用户名
  --password=PASSWORD   密码
  --cidr=CIDR           CIDR IP段， 例如 8.8.8.8/24
  --desc=DESC           <meta name="description">定义的页面说明
  --keywords=KEYWORDS   <meta name="Keywords">定义的页面关键词
```
### 配置用户名和密码：

```
root@Qingxuan:~/PycharmProjects/ZoomEye# python35 Zoom.py --username=payloads@aliyun.com --password=XXXX
[*]Load Parser Success ...
[*]Load Zye API Boot Success ...
[*]Load user and password success ...
[*]NOT FOUND ACCESS TOKEN ..
[*]Create a json config file ...config.json
root@Qingxuan:~/PycharmProjects/ZoomEye#
```

可以看到config.json文件中会有配置好的配置文件，由于保证安全性，并没有写入TOKEN，每一次搜索都将会获取新的TOKEN。

```
{
  "web_search": "https://api.zoomeye.org/web/search",
  "username": "payloads@aliyun.com",
  "host_search": "https://api.zoomeye.org/host/search",
  "password": "XXXX",
  "access_token": "",
  "loginURL": "https://api.zoomeye.org/user/login",
  "resourceURL": "https://api.zoomeye.org/resources-info"
}
```
### 查看用户剩余查询次数：
在这里必须保证用户名与密码配置正常。我们可以使用 -r 参数或者 --resource:

```
root@Qingxuan:~/PycharmProjects/ZoomEye# python35 Zoom.py -r 1
[*]Load Parser Success ...
[*]Load Zye API Boot Success ...
[*]Load user and password success ...
[+]Get access token success ...
[/]Plan: [developer] WebSearch: [4970] HostSearch: [4995]
[\]Please check whether the parameters match properly ...
[\]Please check whether the parameters match properly ...
root@Qingxuan:~/PycharmProjects/ZoomEye#
```
## 遗留的问题：
这个项目做的比较粗糙，只是完成了用户与API的简单交互，但是后期数据可视化做的不是很好，代码量比较多。

```
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
```

这一段中的WebTable和HostTable都采用了表格，但是数据复杂，看起来也不是特别好，还是要花功夫做到一个网页文件中，并且同时在终端输出。

感谢支持 ！ Cora Labtoratory QX - Rvn0xsy
