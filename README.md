# Course-Videos-Downloader-for-XDU
本项目主要用于解救被超星Flash播放器毒害的XDU学子
# 开始
请下载最新版IDM,并修改config.ini中的`IDM_Path`为IDM的安装路径，`Down_Path`为视频的下载路径。
然后运行main.py即可

如果您只是想使用本项目，请前往[Releases](https://github.com/notrainbow/Course-Videos-Downloader-for-XDU/releases/)下载。
# 注意

**避免循环下载**：PPT下载到150M、板书下载到700M时请手动停止下载并保存，否则将无限下载。

**怎么查看下载进度**：桌面右下角小图标-![image](https://user-images.githubusercontent.com/65484889/120215456-5564f880-c268-11eb-832f-8de494bcd02e.png)-右键-还原所有下载窗口(如果一次还原太多窗口电脑会炸，建议一个一个看)

**如何手动保存视频** ：

![image](https://user-images.githubusercontent.com/65484889/120215671-93621c80-c268-11eb-863b-5d1ff1c9ede8.png)

![image](https://user-images.githubusercontent.com/65484889/120215718-a2e16580-c268-11eb-8b9b-1950df336ac1.png)

**关于下载速度**：ppt下载几十kb/s、板书下载几百kb/s都是正常的。请并行下载！

**并行下载多个文件的方法**：IDM-下载-计划任务-队列中的文件-同时下载XX个文件


# 声明
代码写得很烂，请多包容！希望有时间可以重构一下。本项目可以给出录播网址转m3u8流的api,有兴趣的可以尝试写个h5播放器前端。

![image](https://user-images.githubusercontent.com/65484889/120161075-81ad5480-c229-11eb-99a8-8373ad3401b5.png)
