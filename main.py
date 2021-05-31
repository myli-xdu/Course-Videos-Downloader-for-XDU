import requests
from urllib import parse
from subprocess import call
import os
import re
import configparser
import progressbar



def get_ID_exist(file_dir):
    for root, dirs, files in os.walk(file_dir):
        continue
    ID_exist = []
    for i in files:
        searchObj = re.search("A[0-9]*A", i)
        tmp = searchObj.group()
        IDtmp = tmp[1:-1]
        ID_exist.append(IDtmp)
    return (ID_exist)

def IDMdown(DownUrl, DownPath, FileName):
    os.chdir(IDM_Path)
    IDM = "IDMan.exe"
    call([IDM, '/d', DownUrl, '/p', DownPath, '/f', FileName, '/a'])
    call([IDM, '/s'])

def DownVideo(ID,Name,DownPath,Mode):#模式0：只下ppt；模式1：只下教师；模式2：两者都下
    html = requests.get('http://newesxidian.chaoxing.com/live/getViewUrl?liveId='+str(ID)+'&status=&jie=&isStudent=')
    url_initial = html.text
    url_decode=parse.unquote(url_initial)
    if Mode==0 or Mode==2:
        index1=url_decode.find("pptVideo")
        url_tmp=url_decode[index1+11:]
        index2=url_tmp.find("\"")
        url_ppt=url_tmp[0:index2]
        if not url_ppt[0:4]=="rtmp":
            print("下载失败，未找到有效的下载地址。")
        else:
            IDMdown(url_ppt, DownPath, Name+"_ppt.flv")
    if Mode==1 or Mode==2:
        index1=url_decode.find("teacherTrack")
        url_tmp=url_decode[index1+15:]
        index2=url_tmp.find("\"")
        url_teacher=url_tmp[0:index2]
        if not url_teacher[0:4]=="rtmp":
            print("下载失败，未找到有效的下载地址。")
        else:
            IDMdown(url_teacher, DownPath, Name+"_teacher.flv")

def DownAll(ID,Mode):
    datas = {"liveId": ID, "fid": "0", "uId": "0"}
    r = requests.post("http://newesxidian.chaoxing.com/live/listSignleCourse", data=datas)
    searchObj = re.search("seName\":\"[\S]*?,\"days", r.text)
    tmp=searchObj.group()
    coursename=tmp[9:-7]
    global Down_Path
    tmp1=os.path.join(Down_Path, coursename)
    Down_Path=tmp1
    if not os.path.exists(Down_Path):
        os.mkdir(Down_Path)

    searchObj = re.finditer('\"status\":[0-9]*', r.text)
    count: int = 0
    for i in searchObj:
        strtmp = i.group()
        if int(strtmp[9]) == 2:
            count += 1

    list_days = []
    searchObj = re.finditer('\"days\":[0-9]*', r.text)
    for i in searchObj:
        strtmp = i.group()
        list_days.append(strtmp[7:])

    list_weekDay = []
    searchObj = re.finditer('\"weekDay\":[0-9]*', r.text)
    for i in searchObj:
        strtmp = i.group()
        list_weekDay.append(strtmp[10:])

    list_jie = []
    searchObj = re.finditer('\"jie\":\"[0-9]*', r.text)
    for i in searchObj:
        strtmp = i.group()
        list_jie.append(strtmp[7:])

    list_id = []
    searchObj = re.finditer('\"id\":[0-9]*', r.text)
    for i in searchObj:
        strtmp = i.group()
        list_id.append(strtmp[5:])

    list_all = []
    for i in range(count):
        tmp={'id': list_id[i], 'days': list_days[i], 'weekDay': list_weekDay[i], 'jie': list_jie[i]}
        list_all.append(tmp)
    n=len(list_all)
    print('即将下载'+str(n)+'个视频。')
    bar = progressbar.ProgressBar()

    for i in bar(range(n)):
        p=list_all[i]
        DownVideo(p['id'],'第'+p['days']+'周_周'+p['weekDay']+'_第'+p['jie']+'节'+'A'+p['id']+'A',Down_Path,Mode)
        print("正在下载："+coursename+'_第'+p['days']+'周_周'+p['weekDay']+'_第'+p['jie']+'节                                                                                       ')

def UpgradeAll(ID,Mode):
    datas = {"liveId": ID, "fid": "0", "uId": "0"}
    r = requests.post("http://newesxidian.chaoxing.com/live/listSignleCourse", data=datas)

    searchObj = re.search("seName\":\"[\S]*?,\"days", r.text)
    tmp=searchObj.group()
    coursename=tmp[9:-7]
    global Down_Path
    tmp1=os.path.join(Down_Path, coursename)
    Down_Path=tmp1
    if not os.path.exists(Down_Path):
        os.mkdir(Down_Path)

    searchObj = re.finditer('\"status\":[0-9]*', r.text)
    count: int = 0
    for i in searchObj:
        strtmp = i.group()
        if int(strtmp[9]) == 2:
            count += 1

    list_days = []
    searchObj = re.finditer('\"days\":[0-9]*', r.text)
    for i in searchObj:
        strtmp = i.group()
        list_days.append(strtmp[7:])

    list_weekDay = []
    searchObj = re.finditer('\"weekDay\":[0-9]*', r.text)
    for i in searchObj:
        strtmp = i.group()
        list_weekDay.append(strtmp[10:])

    list_jie = []
    searchObj = re.finditer('\"jie\":\"[0-9]*', r.text)
    for i in searchObj:
        strtmp = i.group()
        list_jie.append(strtmp[7:])

    list_id = []
    searchObj = re.finditer('\"id\":[0-9]*', r.text)
    for i in searchObj:
        strtmp = i.group()
        list_id.append(strtmp[5:])

    ID_exist=get_ID_exist(Down_Path)
    list_all = []
    for i in range(count):
        if list_id[i] in ID_exist:
            continue
        tmp={'id': list_id[i], 'days': list_days[i], 'weekDay': list_weekDay[i], 'jie': list_jie[i]}
        list_all.append(tmp)
    n=len(list_all)
    if n==0:
        print("没有需要更新的视频。")
        return
    else:
        print("发现"+str(n)+"个新视频，即将开始下载。")
    bar = progressbar.ProgressBar()
    for i in bar(range(n)):
        p=list_all[i]
        DownVideo(p['id'],'第'+p['days']+'周_周'+p['weekDay']+'_第'+p['jie']+'节'+'A'+p['id']+'A',Down_Path,Mode)
        print("正在下载："+coursename+'_第'+p['days']+'周_周'+p['weekDay']+'_第'+p['jie']+'节                                                                                       ')



curpath = os.getcwd()
cfgpath = os.path.join(curpath, "config.ini")
if  not os.path.exists(cfgpath):
    print("错误：配置文件丢失，请解压缩运行或者重新下载该软件！")
    os.system('pause')
    os._exit()
conf = configparser.ConfigParser()
conf.read(cfgpath, encoding="utf-8")
global IDM_Path
IDM_Path = conf.get("Basic", "IDM_Path")
if  not os.path.exists(os.path.join(IDM_Path,'IDMan.exe')):
    print("错误：IDM下载器的路径不对或还没有安装。请在官网下载IDM并在配置文件中更改IDM路径！(IDM_Path)")
    os.system('pause')
    os._exit()
global Down_Path
Down_Path = conf.get("Basic", "Down_Path")
if Down_Path[0]=='\\':
    Down_Path=os.path.join(curpath, Down_Path[1:])
if not os.path.exists(Down_Path):
    os.mkdir(Down_Path)
#DownAll("10613917",0)
print("西电录播视频下载软件||作者邮箱512008707@qq.com")
print("■■■■■■■■■■■■■■■■■注意事项■■■■■■■■■■■■■■■■■")
print("1.PPT下载到150M、板书下载到700M时请手动停止下载并保存，否则将无限下载。")
print("2.有一切问题请联系作者。")
print("■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■")
print("请粘贴视频链接（复制后在窗口鼠标右键）:",end='')
searchObj = re.search("Id=[0-9]*", input())
tmp = searchObj.group()
ID=tmp[3:]

print("请选择下载模式(模式0：只下ppt；模式1：只下板书；模式2：两者都下):",end='')
Mode=input()
print("请选择(0代表只下载单个视频；1代表下载该课程截止到目前的所有录播;2代表更新所有录播):",end='')
tmp=input()
tmp=int(tmp)
print("提示：进度条100%之前请不要关闭程序！！！")
if tmp==1:
    DownAll(str(ID),int(Mode))
elif tmp==0:
    DownVideo(str(ID), str(ID), Down_Path, int(Mode))
else:
    UpgradeAll(str(ID),int(Mode))


print("下载链接获取完成！请关闭本软件，并保持IDM打开！")
os.system('pause')
os._exit()
