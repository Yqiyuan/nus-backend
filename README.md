## 查询图片

POST包 在body段使用form-data形式建立键值对

file: <图片文件>

user_id: <10位的user_id>

发送至http://<目标ip>:5000/upload

返回图片查询的详细信息

同时在数据库历史表内生成新记录

(记录编号(自动累加的INT)，user_id, date(标准日期格式, 相当于YYYY-MM-DD的字符串), 以base64保存的查询记录)

## 查询记录

POST包 在body段内使用form-data形式建立键值对

user_id: <10位的user_id>

date: <YYYY-MM-DD的字符串>

发送至http://<目标ip>:5000/history

返回用户在该日期查询的历史记录项的编号表

json格式

## 查询记录项

POST包 在body段内使用form-data形式建立键值对

h_id: <表项编号>

发送至http://<目标ip>:5000/search

返回经过base64编码的对应的查询记录
