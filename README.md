## 运行

### 安装依赖

```shell
pip install -r requirements.txt
```

### 迁移数据库

```shell
python manage.py makemigrations TestModel
python manage.py migrate
```

### 运行

```shell
python manage.py runserver
```

## 部署

> 使用 git 来部署 Azure APP Service的方式 [点击这里](https://docs.azure.cn/zh-cn/app-service/app-service-web-get-started-php)

 ### 添加 azure git 仓库源

```shell
git remote add azure https://xinleima@python-app.scm.chinacloudsites.cn/python-app.git
```

### 推送到azure app service，自动部署

```shell
git push azure master
```

