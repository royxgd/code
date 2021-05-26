import hashlib
import json
import datetime
import requests
#获取当前系统时间
now_time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#请求url地址
url='https://openapi.winit.com.cn/openapi/service'
#创建查询类
class Winit_query(object):
    def __init__(self):
        self.action="queryProductInventoryList4Page"
        self.app_key=""
        self.inventoryType="Country"
        self.isActive="Y"
        self.pageNum="1"
        self.pageSize="100"
        self.client_id=""
        self.token= ''
        self.client_secret='='
        self.format="json"
        self.language="zh_CN"
        self.platform="thxsilk"
        self.sign_method="md5"
        self.version="1.0"
        self.data = {
            "DOITier": "",  # N DOI层级
            "categoryID": "",  # N产品类型ID
            "inventoryType": self.inventoryType,  # Y库存类型，常量
            "isActive": self.isActive,  # N商品是否有效，常量
            "name": "",  # N产品名称
            "pageNum": self.pageNum,  # Y页码，常量
            "pageSize": self.pageSize,  # Y每页显示数量，常量
            "productCode": "",  # N产品SKU编码
            "specification": "",  # N规格
            "warehouseCode": "DE0001",  # N仓库code
            "warehouseId": ""  # Y仓库ID
        }
        self.data_concat = json.dumps(self.data, separators=(',', ':'), sort_keys=False)
    #获取用户签名sign
    def get_sign(self,timestamp=now_time):
        sign_concat = self.token + 'action' + self.action + 'app_key' + self.app_key + 'data' + self.data_concat + 'format' + self.format + \
                 'platform' + self.platform + 'sign_method' + self.sign_method + 'timestamp' + timestamp + 'version' + self.version + self.token
        hash_sign = hashlib.md5()
        hash_sign.update(bytes(sign_concat, encoding='utf-8'))
        return hash_sign.hexdigest().upper()
    #获取应用签名client_sign
    def get_client_sign(self,timestamp=now_time):
        client_sign_concat = self.client_secret + 'action' + self.action + 'app_key' + self.app_key + 'data' + self.data_concat + 'format' + self.format + \
                 'platform' + self.platform + 'sign_method' + self.sign_method + 'timestamp' + timestamp + 'version' + self.version + self.client_secret
        hash_client_sign = hashlib.md5()
        hash_client_sign.update(bytes(client_sign_concat, encoding='utf-8'))
        return hash_client_sign.hexdigest().upper()
    def parse(self,sign,client_sign,timestamp=now_time):
        self.sign = sign
        self.client_sign = client_sign
        self.timestamp = timestamp
        self.productCode = ""
        self.warehouseId = ""
        self.warehouseCode = "DE0001" #变量
        pyload = {
            "action": self.action,  # 常量
            "app_key": self.app_key,  # 常量
            "client_id": self.client_id,  # 常量
            "client_sign": self.client_sign,  # 变动
            "data": {
                "categoryID": "",  # N产品类型ID
                "DOITier": "",  # N DOI层级
                "inventoryType": self.inventoryType,  # Y库存类型，常量
                "isActive": self.isActive,  # N商品是否有效，常量
                "pageNum": self.pageNum,  # Y页码，常量
                "pageSize": self.pageSize,  # Y每页显示数量，常量
                "productCode": self.productCode,  # N产品SKU编码
                "name": "",  # N产品名称
                "specification": "",  # N规格
                "warehouseId": self.warehouseId,  # Y仓库ID
                "warehouseCode": self.warehouseCode  # N仓库code
            },
            "format": self.format,
            "language": self.language,
            "platform": self.platform,  # 常量
            "sign": self.sign,  # 变动
            "sign_method": self.sign_method,
            "timestamp": self.timestamp,
            "version": self.version
        }
        response = requests.post(url, data=json.dumps(pyload))
        return response.text
#实例化对象
item=Winit_query()
sign=item.get_sign()
client_sign=item.get_client_sign()
#返回查询结果
content=item.parse(sign,client_sign)
print(sign)
print(client_sign)
print(content)
