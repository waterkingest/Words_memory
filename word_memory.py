import random
import matplotlib.pyplot as pl
import json
import pygame
import requests
import os
import time
# import pyttsx3
from hashlib import md5
os.system('')
pl.rcParams['font.family'] = ['sans-serif']
pl.rcParams['font.sans-serif'] = ['SimHei']

# from aip import AipSpeech

# def generateMusic(word):
#     """ 你的 APPID AK SK """
#     APP_ID = 'a24711947'
#     API_KEY = 'HeGSarBun8THlEQge5Ih84Bh'
#     SECRET_KEY = 'LIBY5NNGFVivB0z284S0OSrgGzjZY3wd'

#     client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

#     # 详细参数可看python sdk 文档
#     result = client.synthesis(word, 'zh', 1, {
#         'vol': 5,
#         'per': 3,
#         'spd': 7,
#     })
#     # 识别正确返回语音二进制 错误则返回dict 参照下面错误码
#     if not isinstance(result, dict):
#         with open('audio.mp3', 'wb') as f:
#             f.write(result)
def get_translate_jinshan(word):
    url = "https://dict-mobile.iciba.com/interface/index.php?c=word&m=getsuggest&nums=10&is_need_mean=1&word="
    try:
        response = requests.get(url+word)
        content = json.loads(response.text)
        result = (content["message"][0]["paraphrase"]).replace('，','、').replace('/','、').replace('[','(').replace(']',')').replace(';','、')
        print('金山词霸查询结果：'+result)
        return result
    except:
        return False
def get_translate_Baidu(word):
    appid = '20201121000622493'
    appkey = 'H0YKKsTNsNHOSZpsosvm'

    # For list of language codes, please refer to `https://api.fanyi.baidu.com/doc/21`
    from_lang = 'en'
    to_lang =  'zh'

    endpoint = 'http://api.fanyi.baidu.com'
    path = '/api/trans/vip/translate'
    url = endpoint + path
    def make_md5(s, encoding='utf-8'):
        return md5(s.encode(encoding)).hexdigest()
    salt = random.randint(32768, 65536)
    sign = make_md5(appid + word + str(salt) + appkey)

    # Build request
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {'appid': appid, 'q': word, 'from': from_lang, 'to': to_lang, 'salt': salt, 'sign': sign}
    for j in range(2):
        r = requests.post(url, params=payload, headers=headers)
        try:     
            result = r.json()
            result = (result['trans_result'][0]['dst']).replace('，','、').replace('/','、').replace('[','(').replace(']',')').replace(';','、')
            print('百度查询结果：'+result)
            return result
        except:
            time.sleep(1)
            pass
    return False
def playMusic(filename,loops=0, start=0.0, value=0.5):
    """
    :param word: 朗读的单词
    :param loops: 循环次数
    :param start: 从多少秒开始播放
    :param value: 设置播放的音量，音量value的范围为0.0到1.0
    :return:
    """

    flag = False  # 是否播放过
    pygame.mixer.init(frequency=111000)  # 音乐模块初始化
    while 1:
        if flag == 0:
            pygame.mixer.music.load(filename)
            # pygame.mixer.music.play(loops=0, start=0.0) loops和start分别代表重复的次数和开始播放的位置。
            pygame.mixer.music.play(loops=loops, start=start)
            pygame.mixer.music.set_volume(value)  # 来设置播放的音量，音量value的范围为0.0到1.0。
        if pygame.mixer.music.get_busy() == True:
            flag = True
        else:
            if flag:
                pygame.mixer.music.stop()  # 停止播放
                break
    pygame.mixer.quit()
    pygame.quit()
    # os.remove('audio.mp3')
print(r'''

  ___  ___                          _     _                                     _       _____  _____ 
  |  \/  |                         (_)   (_)                                   | |     / __  \|  _  |
  | .  . | ___ _ __ ___   ___  _ __ _ _____ _ __   __ _  __      _____  _ __ __| |___  `' / /'| |/' |
  | |\/| |/ _ \ '_ ` _ \ / _ \| '__| |_  / | '_ \ / _` | \ \ /\ / / _ \| '__/ _` / __|   / /  |  /| |
  | |  | |  __/ | | | | | (_) | |  | |/ /| | | | | (_| |  \ V  V / (_) | | | (_| \__ \ ./ /___\ |_/ /
  \_|  |_/\___|_| |_| |_|\___/|_|  |_/___|_|_| |_|\__, |   \_/\_/ \___/|_|  \__,_|___/ \_____(_)___/ 
                                                   __/ |                                             
                                                  |___/                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
                                                ©Waterking
''')
def read_word(word,times):
    try:
        filename="audio/{}.mp3".format(word)
        if not os.path.exists(filename):
            data=requests.get('http://dict.youdao.com/dictvoice?audio='+word,timeout=5).content
            with open(filename, 'wb') as f:
                f.write(data)
        playMusic(filename,loops=times)
    except:
        try:
            data=requests.get('https://fanyi.baidu.com/gettts?lan=uk&text={}&spd=3&source=web'.format(word),timeout=5).content
            with open(filename, 'wb') as f:
                f.write(data)
            playMusic(filename,loops=times)
        except:
            print('没有相关语音')
    # t1 = threading.Thread(target=playMusic(loops=times))
    # t1.start()
    # px = pyttsx3.init()
    # # 设置新的语音速率
    # px.setProperty('rate', 120)
    # for i in range(times):
    #     px.say(word)
    # px.runAndWait()
def read_history_file(filename):
    with open("以往数据\{}错误单词.txt".format(filename), encoding='UTF-8')as f:
        time_f=[]
        fi=f.read()
        fil=fi.split('\n')  
        time_f+=map(eval,(fil[-2].split(';')[:-1]))
    return time_f
def remember(answer,result,aquestion,aw,wrong_answer,number,rol):
    early_end='0'
    print('共{}个'.format(len(result)))
    models=input('选择背诵模式：\n 1--------30个一组\n 2--------50个一组\n 3--------复习所有单词\n')
    if models=='1':
        num=30
        print('每组30个')
    elif models=='2':
        num=50
        print('每组50个')
    else:
        num=999999
        print('复习所有单词')
    ttt=input('输入期望音频播放的次数:')
    caculate=0
    rate=int(input('输入期望音频听写单词的概率是1/X'))
    while answer!='-1':   
        x=random.randint(0,len(result)-1)
        ChineseOrEnglish=random.randint(1,100)
        repeatif=random.randint(1,100)
        if x not in aquestion:
            caculate+=1
            times=0
            if ChineseOrEnglish%rate==0:
                read_word(result[x][0],int(ttt))
                answer=input('英文(输入‘-1’结束,‘0’查看答案)：')
                while aw==0 and answer!='-1':
                    times+=1
                    if answer=='1':
                        read_word(result[x][0],1)
                        answer=input('英文(‘0’查看答案)：')
                    elif answer == result[x][0]:
                        print('-----------------正确-----------------')
                        print('\n')
                        print('英文：'+result[x][0])
                        print('中文：'+result[x][1])
                        print('\n')
                        aw=1
                    elif answer != result[x][0] and answer!='0':
                        print('\033[41m-----------------错误-----------------\033[0m')
                        if [result[x][0],result[x][1]] not in wrong_answer:
                            wrong_answer.append([result[x][0],result[x][1]])
                        read_word(result[x][0],1)
                        print('中文：'+result[x][1])
                        answer=input('重新输入（‘0’查看答案）：')
                        if answer=='0':
                            print('-----------------答案-----------------')
                            print('英文：'+result[x][0])
                            print('中文：'+result[x][1])
                            print('\n')
                            aw=1
                    elif aw!=1 and answer=='0':
                        if [result[x][0],result[x][1]] not in wrong_answer:
                            wrong_answer.append([result[x][0],result[x][1]])
                        print('-----------------答案-----------------')
                        print('英文：'+result[x][0])
                        print('中文：'+result[x][1])
                        print('\n')
                        aw=1
            else:
                print('中文：'+result[x][1])
                answer=input('英文(输入‘-1’结束,‘0’查看答案)：')
                while aw==0 and answer!='-1':
                    times+=1
                    if answer==result[x][0]:
                        print('-----------------正确-----------------')
                        read_word(result[x][0],1)
                        print('\n')
                        aw=1
                    if answer!=result[x][0] and answer!='0':
                        print('\033[41m-----------------错误-----------------\033[0m')
                        read_word(result[x][0],1)
                        if [result[x][0],result[x][1]] not in wrong_answer:
                            wrong_answer.append([result[x][0],result[x][1]])
                        answer=input('重新输入（‘0’查看答案）：')
                        if answer=='0':
                            print('-----------------答案-----------------')
                            print(result[x][0])
                            print('\n')
                            aw=1
                    if aw!=1 and answer=='0':
                        if [result[x][0],result[x][1]] not in wrong_answer:
                            wrong_answer.append([result[x][0],result[x][1]])
                        print('-----------------答案-----------------')
                        print(result[x][0])
                        print('\n')
                        aw=1
            if times==1:
                aquestion.append(x)
            elif repeatif%3==0:
                aquestion.append(x)
            print('已背 '+str(caculate)+' 个')
            if num!=999999:
                    if caculate%num==0:
                        continue_if=input('再来一组输入 1 ;结束则输入任意：')
                        if continue_if=='1':
                            continue_if='0'
                            pass
                        else:early_end='-1'
            aw=0      
        if (len(aquestion)==len(result) and answer!='-1')or early_end=='-1':
            if len(wrong_answer)!=0:
                result=wrong_answer
                wrong_answer=[]
                aquestion=[]
                print('错误单词如下：')
                print(result)
                if rol==1:
                    with open("以往数据/"+str(number)+"错误单词.txt",'a',encoding='UTF-8')as f:
                        for i in result:
                            f.write(str(i)+';')
                        f.write('\n')
                    rol+=1 
                print('开始复习错误单词！！！')
                print('\n')
                remember(answer,result,aquestion,aw,wrong_answer,number,rol)
            if len(wrong_answer)==0:
                if rol==1:
                    with open("以往数据/"+str(number)+"错误单词.txt",'a', encoding='UTF-8')as f:
                        f.write('')
                        f.write('\n')
            answer='-1'
number=input("开始复习英语单词('-1'进入生成图,输入背诵文件名开始复习)：")
print('\n')
while number!='-1':
    rol=1
    file=str(number)+'.txt'
    try:
        filelist=[]
        with open(file, encoding='UTF-8') as f:
            result=[]
            aquestion=[]
            f=f.read()
            a=f.split('\n')
            a = [i for i in a if i != '']
            answer='0'
            aw=0
            wrong_answer=[]
            rewrite=0
            for i in a:
                if '/'not in i:
                    rewrite=1
                    translate=get_translate_jinshan(i) 
                    translate=translate if translate else get_translate_Baidu(i)
                    if not translate:
                        print('输入中文翻译')
                        translate=input(i+'/')
                    i=i+'/'+translate
                filelist.append(i)
                b=str(i).split('，')
                for j in b:
                    c=str(j).split('/')
                    result.append(c)
            if rewrite==1:
                zz=open(file,"w",encoding='UTF-8')
                for lili in filelist:
                    zz.writelines(lili+'\n')
                zz.close()
            filename="以往数据\{}错误单词.txt".format(str(number))
            if os.path.exists(filename):
                review=input('是否复习错误单词？(1:是，其余：否)')
                if review=='1':
                    result=read_history_file(str(number))
            remember(answer,result,aquestion,aw,wrong_answer,number,rol)
            print('\n')
            if len(aquestion)!=len(result):
                number=input("单词终止复习，输入('-1'结束)：")
                print('\n')
            else:
                number=input("单词复习完毕，输入('-1'结束)：")
                print('\n')     
    except:
        number=input("无此单元请重新输入('-1'结束)：")
        print('\n')
print("学习结束！！！！！！！！！！！！")
print("\n")
order=input("是否需要生成单词背诵情况图？？（y/n）")

while order=='y':
    order=input('需要生成的文件名是：')
    result=[]
    try:
        with open(order+'.txt', encoding='UTF-8') as file:
            file=file.read()
            file_s=file.split('\n')
            for i in file_s:
                file_sb=str(i).split('，')
                for j in file_sb:
                    file_sbc=str(j).split('/')
                    result.append(file_sbc)
        with open("以往数据/"+str(order)+"错误单词.txt", encoding='UTF-8')as f:
            tu_y=[]
            tu_x=[]
            time_f=[]
            fi=f.read()
            fil=fi.split('\n')
            for i in fil[:-1]:
                time_f.append(i.split(';')[:-1])
            for i in time_f:
                tu_y.append(round(((len(result)-len(i))/len(result)),2))
            for j in range(len(tu_y)):
                tu_x.append(int(j)+1)
            pl.title('unit '+order)
            pl.xlabel("time")
            pl.ylabel("accuracy")
            pl.plot(tu_x,tu_y)
            for i,j in zip(tu_x,tu_y):
                pl.text(i,j,j,ha='center',va='bottom',fontsize=11)
            pl.show()
            all_f=[]
            all_onen=[]
            for i in time_f:
                if i!=[]:
                    for j in i:
                        all_f.append(j)
            all_one=set(all_f)
            for i in range(len(all_one)):
                all_onen.append(0)
            dic=dict(zip(all_one,all_onen))
            for i in all_f:
                dic[i]+=1
            print('\n')
            print("错误词汇排序如下:\n")
            e=sorted(dic.items(),key=lambda x:x[1],reverse=True)
            for i in e:
                print('错误词汇：'+i[0]+' 错误次数: '+str(i[1]))
            print('\n')
            order=input("是否需要生成其他的单词背诵情况图？？（y/n）")
    except:
        order=input("没有这个单元啊！！是不是要生成啊！（y/n）")
        
else:
    print("复习愉快！！！")