import requests

def req(type,url,dataType,data,headers):
    if dataType == 'json':
        if type == 'get':
            rep = requests.get(url=url,json=data,headers=headers)
            return rep.json()
        else:
            rep = requests.post(url=url, json=data, headers=headers)
            return rep.json()
    else:
        if type == 'get':
            rep = requests.get(url=url,data=data,headers=headers)
            return rep.json()
        else:
            rep = requests.post(url=url, data=data, headers=headers)
            return rep.json()

def microsoft(mr):
#######################################################两个headers
    h1 = {'Content-Type': 'application/x-www-form-urlencoded'}
    h2 = {'Content-Type': 'application/json'}
#######################################################

######################################获取授权令牌
    json_code1 = {
    "client_id": "00000000402b5328",
    "code": mr,
    "grant_type": "authorization_code",
    "redirect_uri": "https://login.live.com/oauth20_desktop.srf",
    "scope": "service::user.auth.xboxlive.com::MBI_SSL"}
    try:
        access_token = req('post','https://login.live.com/oauth20_token.srf','data',json_code1,h1)['access_token']
    except:
        print('无效的code')
        return None,None,None
    #print(access_token)
######################################XBL验证
    json_RpsTicket = {
    "Properties": {
        "AuthMethod": "RPS",
        "SiteName": "user.auth.xboxlive.com",
        "RpsTicket": access_token
        },
    "RelyingParty": "http://auth.xboxlive.com",
    "TokenType": "JWT"
    }
    allToken = req('post','https://user.auth.xboxlive.com/user/authenticate','json',json_RpsTicket,h2)
    token = allToken['Token']
    uhs = allToken['DisplayClaims']['xui'][0]['uhs']
    #print(token,uhs)
######################################XSTS
    json_UserTokens = {
            "Properties": {
                "SandboxId": "RETAIL",
                "UserTokens": [
                    token
                ]
            },
        "RelyingParty": "rp://api.minecraftservices.com/",
        "TokenType": "JWT"
        }

    userTokenAll = req('post','https://xsts.auth.xboxlive.com/xsts/authorize','json',json_UserTokens,h2)
    userToken = userTokenAll['Token']
    uhs2 =  userTokenAll['DisplayClaims']['xui'][0]['uhs'] #好像uhs和uhs2是一模一样的
    #print(userToken,uhs2)
###########################################验证Minecraft
    json_identityToken = {
    "identityToken": "XBL3.0 x=%s;%s" % (uhs2,userToken)
    }
    AllMC = req('post','https://api.minecraftservices.com/authentication/login_with_xbox','json',json_identityToken,h2)
    MCaccessToken = AllMC['access_token']
    tokenType = AllMC['token_type']
    #print(MCaccessToken,tokenType)
##########################################获取档案
    headers = {'Authorization':'%s %s' % (tokenType,MCaccessToken)}
    file = req('get','https://api.minecraftservices.com/minecraft/profile','data',None,headers)
    try:
        uuid = file['id']
        name = file['name']
        return uuid,name,MCaccessToken
    except:
        print('您似乎未拥有正版Minecraft')
        return None,None,None


def mojang(username,password):
    url = "https://authserver.mojang.com/authenticate"
    h = {'Content-Type': 'application/json'}
    data= {
   "agent": {
       "name": "Minecraft",
       "version": 1
   },
   "username": username,
   "password": password,
   "clientToken": "客户端标识符"
    }

    file = req('post',url,'json',data,h)
    try:
        MCaccessToken = file['accessToken']
        uuid = file['availableProfiles'][0]['id']
        name = file['availableProfiles'][0]['name']
        return uuid,name,MCaccessToken
    except:
        print('您似乎未拥有正版Minecraft')
        return None,None,None


if __name__ == '__main__':
    print('by TigGrak')
    print('1.microsoft\n2.mojang AB(and bug)\n3.offline')
    an = input('>>>')
    if an == '1':
        an = input('>>>')
        if an=='test':
            uuid, name, token = 'a_test_uuid','a_test_name','a_test_accessToken'
        else:
            uuid,name,token = microsoft(an)

    elif an=='2':
        username = input('>>>')
        password = input('>>>')
        if username == 'test' and password =='test':
            uuid, name, token = 'a_test_uuid','a_test_name','a_test_accessToken'
        else:
            uuid, name, token = mojang(username, password)
    else:
        print('输入错误？？？')

    if name:
        print('name:%s\n\nuuid:%s\n\naccessToken:%s' % (name,uuid,token))
        with open('file.txt','w') as w:
            w.write('name:%s\n\nuuid:%s\n\naccessToken:%s' % (name,uuid,token))


    input()
    exit()
    #https://login.live.com/oauth20_authorize.srf?client_id=00000000402b5328&response_type=code&scope=service%3A%3Auser.auth.xboxlive.com%3A%3AMBI_SSL&redirect_uri=https%3A%2F%2Flogin.live.com%2Foauth20_desktop.srf