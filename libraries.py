import json,os,requests,threading

class B():
    data = {}
    all = []

def alist(listTemp, n):
    for i in range(0, len(listTemp), n):
        yield listTemp[i:i + n]

def th(list):
    for i in range(0,len(list)):
        threading.Thread(target=download, args=[list[i]]).start()


def openjson(path):
    with open(path,'r') as r:
        text = r.read()
    B.data = json.loads(text)
    B.data = B.data['libraries']

def arrangement(list):
    after = []
    for i in list:
        after.append([i['downloads']['artifact']['path'],i['downloads']['artifact']['url']])
        if 'classifiers' in i['downloads']:
            if 'javadoc' in i['downloads']['classifiers']:
                after.append([i['downloads']['classifiers']['javadoc']['path'], i['downloads']['classifiers']['javadoc']['url']])
            if 'natives-windows' in i['downloads']['classifiers']:
                after.append([i['downloads']['classifiers']['natives-windows']['path'], i['downloads']['classifiers']['natives-windows']['url']])

    return after




def download(list):
    #os.makedirs('libraries')

    for i in list:
        try:
            if not(os.path.isdir(os.path.split(i[0])[0])):
                os.makedirs(os.path.split(i[0])[0])
        except:
            if not(os.path.isdir(os.path.split(i[0])[0])):
                os.makedirs(os.path.split(i[0])[0])
        print('下载%s中...' % (os.path.split(i[0])[1]))
        while True:  #套个死循环，还下不出来就卡死算了......
            try:
                file = requests.get(url=i[1])
                with open(i[0], "wb") as code:
                    code.write(file.content)
                break
            except:
                pass
        print('下载完成！')




if __name__ == '__main__':
    print('MC本体json')
    path = input('>>>')
    #path = r'E:\mctest\.minecraft\versions\1.16.5\1.16.5.json'
    openjson(path)
    pAu = arrangement(B.data)
    work = alist(pAu,16)
    for i in work:
        B.all.append(i)
    th(B.all)
    #download(pAu)
    #os.makedirs('libraries')
