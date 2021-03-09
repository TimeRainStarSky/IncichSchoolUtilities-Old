from incich_api import IncichStudent
from api.netease_music_api import query_song, get_163_music
from api.wiki_api import wiki_search
import time
import os
# import ffmpy
import random
import json


# 命令格式：方法, 对应指令, 说明
commands = []

def runtype(msg):
    global stu

    if run_type == '2':
        print(msg)
    if command_log == "是":
        stu.send_msg(msg)


def handle(msg):
    global stu

    if msg == 'help':
        res = ''
        for i in commands:
            res += i[1] + " - " + i[2] + "\n"
        runtype(res)
        return

    for i in commands:
        if msg[:len(i[1])] == i[1]:
            i[0](msg)
            break
    else:
        runtype("未知的命令：" + msg + " 请输入Help获取更多信息")


def send(msg):
    global stu

    if msg[:10] == 'send view ':
        if os.path.exists(msg[10:]):
            if os.path.isfile(msg[10:]):
                runtype("错误：路径 " + os.path.abspath(msg[10:]) + " 指向一个文件")
            else:
                res = "正在查看服务器目录：" + os.path.abspath(msg[10:])
                for listdir in os.listdir(msg[10:]):
                    res += "\n" + listdir
                runtype(res)
        else:
            runtype("错误：目录 " + os.path.abspath(msg[10:]) + " 不存在")
        return

    if msg[:13] == 'send message ':
        runtype("正在发送消息至班牌……")
        stu.send_msg(msg[13:])
        return

    if msg[:10] == 'send text ':
        if os.path.isfile(msg[10:]):
            runtype("正在发送文本至班牌……")
            f = open(msg[10:])
            stu.send_msg(f.read())
            f.close()
        else:
            runtype("错误：文本文件" + msg[10:] + "不存在")
        return

    if msg[:11] == 'send sound ':
        if os.path.isfile(msg[11:]):
            runtype("正在发送音频至班牌……")
            f = open(msg[11:], "rb")
            stu.send_sound_msg(f)
            f.close()
        else:
            runtype("错误：音频文件" + msg[10:] + "不存在")
        return

    if msg[:11] == 'send image ':
        if os.path.isfile(msg[11:]):
            runtype("正在发送图片至班牌……")
            f = open(msg[11:], "rb")
            stu.send_image_msg(f)
            f.close()
        else:
            runtype("错误：图片文件" + msg[10:] + "不存在")
        return

    if msg[:11] == 'send video ':
        if os.path.isfile(msg[11:]):
            runtype("正在发送视频至班牌……")
            f = open(msg[11:], "rb")
            stu.send_video_msg(f)
            f.close()
        else:
            runtype("错误：视频文件" + msg[10:] + "不存在")
        return

    raise Exception("未知的子命令")


music_vol = 100


def music(msg):
    global stu
    global music_vol
    if msg[:13] == 'music search ':
        res = query_song(msg[13:])
        runtype(res)
        return

    if msg[:10] == 'music get ':
        try:
            runtype("正在下载音乐至服务器……")
            get_163_music(msg[10:], msg[10:] + ".mp3")

            # 测试转码是否可以省略
            # runtype("正在转码……")
            # global music_vol
            # ff = ffmpy.FFmpeg(
            #     inputs={msg[10:] + ".mp3"：None},
            #     outputs={msg[10:] + ".amr"："-ab 23.85k -acodec amr_wb -ac 1 -ar 16000 -vol " + str(music_vol)}
            # )
            # ff.run()

            runtype("正在发送音乐至班牌……")
            # f = open(msg[10:] + ".amr", "rb")
            f = open(msg[10:] + ".mp3", "rb")
            stu.send_sound_msg(f)
            f.close()
            # os.remove(msg[10:] + ".amr")
            os.remove(msg[10:] + ".mp3")
            return
        except Exception as e:
            try:
                os.remove(msg[10:] + ".mp3")
                # os.remove(msg[10:] + ".amr")
            except Exception as e1:
                pass
            raise e

    if msg[:10] == 'music vol ':
        music_vol = int(msg[10:])
        # runtype("音量更改成功")
        runtype("本命令已经弃用, 可通过班牌设置更改音量")
        return
    raise Exception("未知的子命令")


def status(msg):
    global stu
    f=os.popen("neofetch")
    res = "服务器信息：" + f.read()
    res += "服务器正在正常运行.\n"
    res += "Token:" + stu.token + "\n"
    res += "邀请码信息：" + str(stu.code_info) + "\n"
    res += "绑定学生信息：" + str(stu.stu_info) + "\n"
    res += "已经处理的消息：" + str(stu.msg_processed) + "\n"
    runtype(res)


def search(msg):
    runtype("正在搜索……")
    res = wiki_search(msg[msg.find(" ") + 1:])
    runtype("搜索完成! 以下是搜索结果：")
    time.sleep(1)
    runtype(res)


commands.append([status, "status", "查询服务器状态"])
commands.append([search, "search", "百度百科搜索"])
commands.append([music, "music", "网易云音乐 子命令：search & get & vol"])
commands.append([send, "send", "发送文件至班牌 子命令：view & message & text & sound & image & video"])

config = json.loads("{}")

try:
    config = json.load(open("config.json", "r"))
except Exception as e:
    print("读取配置文件时出错：" + str(e))
    print("尝试注册新账号……")
    code = input("请输入你的邀请码(班主任提供, 也可由 get_code.py 获取)：")
    name = input("请输入你的真实姓名：")
    config['name'] = name
    config['code'] = code
    config['unionid'] = str(hex(random.randint(int("11111111111111111111111111111111", 16), int("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF", 16))))[2:].upper()
    config['run_type'] = '1'
    config['command_log'] = "是"
    json.dump(config, open("config.json", "w"))


stu = IncichStudent(config['unionid'], config['name'], config['code'])
print("1.对话模式 2.命令模式")
run_type = input("请选择运行模式：")
if run_type == '1':
    print("当前模式：对话模式")
    config['run_type'] = run_type
    json.dump(config, open("config.json", "w"))
    command_log = "是"
elif run_type == '2':
    print("当前模式：2.命令模式")
    command_log = input("是否发送执行命令日志？")
    if not command_log == "是":
        if not command_log == "否":
            print("错误：输入无法识别，使用默认模式")
            command_log = config['command_log']
    config['command_log'] = command_log
    config['run_type'] = run_type
    json.dump(config, open("config.json", "w"))
else:
    run_type = config['run_type']
    if run_type == '1':
        print("错误：输入无法识别，进入对话模式")
        command_log = "是"
    elif run_type == '2':
        print("错误：输入无法识别，进入命令模式")
        command_log = config['command_log']

msg = "Incich School Utilities v3-Beta 启动成功！"
if run_type == '2':
    msg += " 当前为命令模式"
if command_log == "是":
    print("尝试发送文本消息……")
    msg_res = stu.send_msg(msg)
    if not msg_res['success']:
        print("发送消息失败：" + str(msg_res))
print(msg)

if run_type == '1':
    while True:
        print("获取消息……")
        try:
            handle(stu.wait_new_msg().lower())
        except Exception as e:
            print(e)
            runtype("服务器内部错误：" + str(e))
            time.sleep(5)
if run_type == '2':
    while True:
        try:
            command = input("输入命令：")
            runtype("正在执行命令：" + command)
            handle(command.lower())
        except Exception as e:
            runtype("服务器内部错误：" + str(e))
            time.sleep(5)