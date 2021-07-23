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

## 用户注册

POST

```
email: <string>
passwd: <string>
nickname: <string>(default:'')
age: <int>(default:0)
calories_limit: <double>(default:8400)
fat_limit: <double>(default:60)
protein_limit: <double>(default:60)
carbs_limit: <double>(default:300)
```

发送至http://8.130.49.155:5000/sign_up

```
{
    "result": "Email exists"
}
{
    "result": "Success"
}
```



## 用户登录

POST

```
email: <string>
passwd: <string>
```

发送至http://8.130.49.155:5000/login

```
{
    "info": {
        "age": 0,
        "calories_limit": 8400.0,
        "carbs_limit": 300.0,
        "email": "test@qq.com",
        "fat_limit": 60.0,
        "id": 1,
        "nickname": "haha",
        "passwd": "123456",
        "protein_limit": 60.0
    },
    "result": "Success"
}

{
    "info": "",
    "result": "Wrong password"
}

{
    "info": "",
    "result": "No such user"
}
```

## 获取用户信息

POST

```
email: <string>
```

发送至http://8.130.49.155:5000/get_user_info

```
{
    "info": {
        "age": 0,
        "calories_limit": 8400.0,
        "carbs_limit": 300.0,
        "email": "test@qq.com",
        "fat_limit": 60.0,
        "id": 1,
        "nickname": "haha",
        "passwd": "123456",
        "protein_limit": 60.0
    },
    "result": "Success"
}

{
    "info": "",
    "result": "No such user"
}
```

## 修改用户信息

POST

```
email: <string>
passwd: <string>
nickname: <string>(optional)
age: <int>(optional)
calories_limit: <double>(optional)
fat_limit: <double>(optional)
protein_limit: <double>(optional)
carbs_limit: <double>(optional)
```

发送至http://8.130.49.155:5000/get_user_info

```
{
    "result": "No such user"
}

{
    "result": "Success"
}
```



