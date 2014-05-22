#!/home/sites/nackshop.com/pyenv/bin/activate
#encoding=utf8

import web

web.config.smtp_server='smtp.qq.com'
web.config.smtp_port=25
web.config.smtp_username='www@garning.com'
web.config.smtp_password='Ning8887'

web.sendmail('www@garning.com', 'insion@garning.com','欢迎你，Insion', '我看到你分享在我们嘉宁网上的图了，很漂亮呢～')