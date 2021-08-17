import json,os,requests,threading

class B():
    data = {}
    all = []
    allth = []

def alist(listTemp, n):
    for i in range(0, len(listTemp), n):
        yield listTemp[i:i + n]

def openjson(path):
    with open(path,'r') as r:
        text = r.read()
    B.data = json.loads(text)
    B.data = B.data['objects']

def arrangement(list):
    after = []
    for key in list:
        after.append(list[key]['hash'])
    return after

def th(list):

    for i in range(0,len(list)):
        B.allth.append(threading.Thread(target=download, args=[list[i]]))
    for b in B.allth:
        b.start()




def download(list):
    headers = {
        'User-Agent': 'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
    for i in list:
        try: #多线程创建文件夹冲突，试试这样行不行qwq
            if not(os.path.isdir(i[0:2])):
                os.makedirs(i[0:2])
        except:
            if not(os.path.isdir(i[0:2])):
                os.makedirs(i[0:2])
        #print(i[0:2])
        print('下载%s中...' % (i))

        while True:  #套个死循环，还下不出来就卡死算了......
            try:
                file = requests.get(url='http://resources.download.minecraft.net/'+i[0:2]+'/'+i,headers=headers)
                with open(i[0:2]+'/'+i, "wb") as code:
                    code.write(file.content)
                break
            except:
                pass
        print('下载完成')





if __name__ == '__main__':
    #path = r'E:\mctest\.minecraft\assets\indexes\1.16.json'
    print('MC assets json')
    path = input('>>>')
    openjson(path)
    hashlist = arrangement(B.data)
    print(len(hashlist))
    work = alist(hashlist,200)
    for i in work:
        B.all.append(i)
    th(B.all)

    #download(hashlist)
    #d6c41fbec35949f5ab7423d0a3cd174bacfd406d



