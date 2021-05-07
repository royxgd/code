import numpy as np
import pandas as pd
import pymysql
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

#连接数据
sql_cmd='select * from history;'
con=pymysql.connect(host='localhost',user='',password='',database='',charset='utf8', use_unicode=True)
df=pd.read_sql(sql_cmd,con)
X=df.iloc[:,:-1]
Y=df.iloc[:,-1]
X_train,X_test,Y_train,Y_test=train_test_split(X,Y,test_size=0.25,random_state=42)
#建模，后期进行优化
RFRegressor=RandomForestRegressor(n_estimators = 30)
#训练
RFRegressor.fit(X_train, Y_train)
#预测结果
predictions = RFRegressor.predict(X_test)
#计算误差
errors = predictions-Y_test
accuracy=round(1-abs(np.sum(errors))/np.sum(Y_test),2)*100
print('测试集数量和：{}，预测数量和：{}，accuracy:{}%'.format(np.sum(Y_test),round(np.sum(predictions),2),accuracy))
