import os,json
class Bat():
    things = ''


def mian(minecraft,java,xmn,xmx,dosname,dosversion,mcjar,natives,lJarList):
        temp = '@echo off\n'
        temp += 'title 启动游戏 - BY TigGrak\n'
        temp += 'set APPDATA="%s"\n' % minecraft
        temp += 'cd /D %s\n' % minecraft
        temp += '"%s" -XX:+UseG1GC -XX:-UseAdaptiveSizePolicy -XX:-OmitStackTraceInFastThrow -Dfml.ignoreInvalidMinecraftCertificates=True -Dfml.ignorePatchDiscrepancies=True -XX:HeapDumpPath=MojangTricksIntelDriversForPerformance_javaw.exe_minecraft.exe.heapdump -Dos.name="%s" -Dos.version=%s -Djava.library.path="%s" -Dminecraft.launcher.brand=TigGrak -Dminecraft.launcher.version=1.0 ' % (java,dosname,dosversion,natives)
        temp += '-cp "'
        for i in lJarList:
            if not('3.2.1' in i):
                temp += '%s;' % i
        temp += '%s" ' % mcjar
        temp += '-Xmn%s -Xmx%s ' % (xmn,xmx)
        with open('stmc.bat','w') as w:
            w.write(temp)





def getLibrariesJar(path):
    all_files = [f for f in os.walk(path)]  # 输出根path下的所有文件名到一个列表中
    # 对各个文件进行处理
    print(all_files)

class B():
    data = {}


def openjson(path):
    with open(path,'r') as r:
        text = r.read()
    B.data = json.loads(text)
    B.data = B.data['libraries']

def arrangement(list):
    after = []
    for i in list:
        after.append(i['downloads']['artifact']['path'])
        if 'classifiers' in i['downloads']:
            if 'javadoc' in i['downloads']['classifiers']:
                after.append(i['downloads']['classifiers']['javadoc']['path'])
            if 'natives-windows' in i['downloads']['classifiers']:
                after.append(i['downloads']['classifiers']['natives-windows']['path'])
    return after




def getLibrariesJar(list,path):
    #os.makedirs('libraries')
    after = []
    for i in list:
        after.append(path+'libraries/'+i)
    return after



if __name__ == '__main__':

    minecraft = input('.minecraft路径\n>>>')
    java = input('java路径\n>>>')
    xmx = input('最大内存\n>>>')
    xmn = input('最小内存\n>>>')
    dosname = input('当前系统名称\n>>>')
    dosversion = input('当前系统版本\n>>>')
    mcjar = input('MC本体文件\n>>>')
    path = input('MC本体json\n>>>')
    '''
    minecraft = 'E:/mctest/.minecraft/'
    java = r'E:\java\bin\java.exe'
    xmx = '7680m'
    xmn = '256m'
    dosname = 'Windows 10'
    dosversion = '10.0'
    path = r'E:\mctest\.minecraft\versions\1.16.5\1.16.5.json'
    mcjar = r'E:\mctest\.minecraft\versions\1.16.5\1.16.5.jar'
    '''
    natives = os.path.split(mcjar)[0] + '/natives/'
    openjson(path)
    pAu = arrangement(B.data)
    ljar = getLibrariesJar(pAu,minecraft)
    #os.makedirs('libraries')
    mian(minecraft,java,xmn,xmx,dosname,dosversion,mcjar,natives,ljar)

