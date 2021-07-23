## 分析图片

POST包 在body段使用form-data形式建立键值对

```
file: <图片文件的base64字符串>

user_id: <int类型的user_id>
```

发送至http://8.130.49.155:5000/upload

```
response = {
        'id': '1',
        'name': 'burger',
        'nutrition': {
            'calories': '100',
            'fat': '100',
            'protein': '100',
            'carbs': '100'
        }
    }
```

同时在数据库历史表内生成新记录


## 查询某一天的食物图片

POST包 在body段内使用form-data形式建立键值对

```
user_id: <int类型的user_id>

date: <YYYY-MM-DD的字符串>

max_num: <大于1>返回的最大数量(optional)
```

发送至http://8.130.49.155:5000/get_daily_images

```
user_id: 1
date: 2021-07-22

{
    "image_amount": 1,
    "images": [base64]
}
```

## 查询某一天的总营养

POST包 在body段内使用form-data形式建立键值对

```
user_id: <int类型的user_id>

date: <YYYY-MM-DD的字符串>
```

发送至http://8.130.49.155:5000/get_daily_nutrition

```
user_id: 1
date: 2021-07-22

{
    "calories": 449.0,
    "carbs": 17.0,
    "fat": 18.0,
    "protein": 41.0
}
```

