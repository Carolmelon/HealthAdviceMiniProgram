
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'secret key should be filled in here'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app1.apps.App1Config',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    #  csrf攻击防御暂时关闭
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'TimeProject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'TimeProject.wsgi.application'



DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    # }
    # 'default': {
    #     'ENGINE': 'django.db.backends.mysql',
    #     'NAME': 'wx_mini',
    #     'USER': 'root',
    #     'PASSWORD': 'lrs.12345',
    #     'HOST': 'localhost',
    #     'PORT': '3306',
    #     'OPTIONS': {
    #         'autocommit': True,
    #     },
    # }
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'wx_mini',
        'USER': 'lrs',
        'PASSWORD': 'mysql password should be filled in here',
        'HOST': 'mysql host should be filled in here',
        'PORT': '3306',
        'OPTIONS': {
            'autocommit': True,
        },
    }
}



AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]



LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False



STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'collected_static')

MEDIA_ROOT = os.path.join(BASE_DIR, "static", "img")

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

# domain_url = 'http://127.0.0.1:8011'
domain_url = "https://www.example.com"
app_id = 'wx app id should be filled in here'
app_secret = 'wx app secret should be filled in here'
Mch_key = "mch key should be filled in here"
Mch_id = "mch id should be filled in here"
order_url = 'https://api.mch.weixin.qq.com/pay/unifiedorder'
notify_url = "https://www.example.com/wx_mini/wx_pay_notify_url"

# 第三方 SMTP 服务
mail_host = "smtp.163.com"  # SMTP服务器
mail_user = " "  # 用户名
mail_pass = " "  # 授权密码，非登录密码
sender = ' '  # 发件人邮箱(最好写全, 不然会失败)
receivers = [' ']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
receiver = ' '