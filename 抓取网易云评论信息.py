# 1.找到未加密的参数                        #window.arsea(参数,xxxx,xxx,xxx)
# 2.想办法把参数进行加密（必须参考网易的逻辑），params =》 encText,encSecKey => encSecKey
# 3.请求到网易，拿到评论信息

# 需要安装pycrypto
from Crypto.Cipher import AES
from base64 import b64encode
import requests
import json

url = 'https://music.163.com/weapi/comment/resource/comments/get?csrf_token=8f179a723105841a8770aafb2adca618'

# 请求方式是POST
data = {
    "csrf_token": "",
    "cursor": "-1",
    "offset": "0",
    "orderType": "1",
    "pageNo": "1",
    "pageSize": "20",
    "rid": "R_SO_4_760533",
    "threadId": "R_SO_4_760533"
}

# 模拟网易云加密过程
# 服务于d的
e = '010001'
f = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
g = '0CoJUm6Qyw8W8jud'
i = 'EY0GuSxElBhO3P9C'  # 手动固定的 -> 人家函数中是随机的


def get_encSecKey():  # 由于i是固定的，那么encSecText就是固定的，c()函数的结果就是固定的
    return "cee4b44eb88cb6ddf4ba756445edbbdcfe4d3a3cb7e7b99334ee067cc9e231491643ec432028198c07e0acc9b6019f41f75dd921d28e97fa2a1c46053ccd6ea7812b01a0025a44cb19eb6fbc8f6f8aeece000887612736911a023d19e25140284a995a347e091bc02e23f95f1cb1f78cf09c559309260d6af64735ad69ac058f"


# 把参数进行加密
def get_params(data):  # 默认这里接收到的是字符串
    first = enc_params(data, g)
    second = enc_params(first, i)
    return second  # 返回的就是params


# 转化成16的倍数，为下方的加密算法服务
def to_16(data):
    pad = 16 - len(data) % 16
    data += chr(pad) * pad
    return data


# 加密过程
def enc_params(data, key):
    iv = "0102030405060708"
    data = to_16(data)
    aes = AES.new(key=key.encode("utf-8"), IV=iv.encode("utf-8"), mode=AES.MODE_CBC)  # 创建加密器
    bs = aes.encrypt(data.encode("utf-8"))  # 加密，加密的内容的长度必须是16的倍数
    return str(b64encode(bs), "utf-8")  # 转化为字符串返回


# 处理加密过程
'''
function a(a) {     #随机的16位字符串
        var d, e, b = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", c = "";
        for (d = 0; a > d; d += 1)  #循环16次
            e = Math.random() * b.length,   #随机数
            e = Math.floor(e),  #取整
            c += b.charAt(e);   #去字符串中的xxx位置 b
        return c
    }
    function b(a, b) { # a是要加密的内容，
        var c = CryptoJS.enc.Utf8.parse(b) # b是密钥
          , d = CryptoJS.enc.Utf8.parse("0102030405060708")
          , e = CryptoJS.enc.Utf8.parse(a) # e是数据
          , f = CryptoJS.AES.encrypt(e, c, { # c 加密的密钥
            iv: d, # 偏移量
            mode: CryptoJS.mode.CBC # 模式：cbc
        });
        return f.toString()
    }
    function c(a, b, c) { # c里面不产生随机数
        var d, e;
        return setMaxDigits(131),
        d = new RSAKeyPair(b,"",c),
        e = encryptedString(d, a)
    }
    function d(d, e, f, g) {    d:数据,e:010001，f:很长,g:0CoJUm6Qyw8W8jud
        var h = {}      #空对象
          , i = a(16);  #i就是一个16位的随机值，把i设成定值
        return h.encText = b(d, g), # g密钥
        h.encText = b(h.encText, i),    #返回的就是params i也是密钥
        h.encSecKey = c(i, e, f),       #得到的就是encSecKey,e和f是定死的 ,如果此时我把i固定，得到的key一定是固定的
        h
    }
    
    两次加密:
    数据+g => b => 第一次加密+i => b = params
'''

# 发送请求，得到评论结果
resp = requests.post(url, data={
    "params": get_params(json.dumps(data)),
    "encSecKey": get_encSecKey()
})

print(resp.text)
