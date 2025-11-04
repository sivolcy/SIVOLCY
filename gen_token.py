#1、服务器利用下列代码加密生成token（JWT）---->2、（JWT）客户端----->3、服务器收到jwt解密后--->4、解密后jwt_secret与config.toml中的jwt_secret对比--->相同/不相同
#cgpt_OznsUz9UrgbTwnsnMNsOjCVCKSfvo9OU
#-----------------------------------------------------------------开发环境------------------------------------------------------------------------------
import jwt
payload={'user_id': 1, 'user_name': 'platformaigpt@gmail.com', 'role': 'subscription', 'api_key': 'cgpt_oOtQljEyoYBHvW3F2MmZX218yROo3lrn', 'exp': 1771320280}
print( jwt.encode(payload, "vgb0tnl9d58+6n-6h-ea&u^1#s0ccp!794=kbvqacjq75vzps$", algorithm="HS256") )
#-----------------------------------------------------------------生产环境------------------------------------------------------------------------------
# import jwt
# payload={'user_id': 86, 'user_name': 'sivolcy', 'role': 'subscription', 'api_key': 'cgpt_ZeL49OeTcd5hJNqT0YkqdvuL5POPsv4f', 'exp': 1771320280}
# print( jwt.encode(payload, "vgb0tnl9d58+6n-6h-ea&u^1#s0ccp!794=kbvqacjq75vzps$", algorithm="HS256") )
