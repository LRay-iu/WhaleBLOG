import random, string
from email.header import Header
from email.mime.text import MIMEText
from io import BytesIO
from smtplib import SMTP_SSL,SMTP

from PIL import Image, ImageFont, ImageDraw


def send_email(receiver, ecode):
    sender = 'WhaleBLOG<WhaleBLOG@163.com>'
    content = f"<br/>欢迎注册鲸鱼blog系统账号，您的邮箱验证码为:"\
              f"<span style='color:red;font-size:20px;'>{ecode}</span>," \
              f"请复制到注册窗口中完成注册，感谢您的支持<br/>"
    message = MIMEText(content, 'html', 'utf-8')
    message['Subject'] = Header('鲸鱼blog的注册验证码','utf-8')
    message['From'] = sender
    message['To'] = receiver
    smtpObj = SMTP_SSL('smtp.163.com', 994)
    smtpObj.login('WhaleBLOG@163.com', 'GOPDFVJPLCJRHSBR')  # 请替换成授权密码
    smtpObj.sendmail(sender, [receiver], message.as_string())  # 使用 message.as_string() 将 message 对象转换为字符串
    smtpObj.close()
    # print("finish")

def gen_email_code():
    str=random.sample(string.ascii_letters+string.digits,6)
    return ''.join(str)

class imageCode:
    # 生成随机颜色
    def rand_color(self):
        red = random.randint(32, 200)
        green = random.randint(32, 255)
        blue = random.randint(20, 127)
        return red, green, blue

    # 生成随机字符
    def gen_text(self):
        # sample用于从一个大的列表当中，随机取N个字符，来构建出一个子列表
        list = random.sample(string.ascii_letters + string.digits, 4)
        # print(list)
        return ''.join(list)

    # 绘制干扰线
    def draw_lines(self, draw, num, width, height):
        for num in range(num):
            x1 = random.randint(0, width / 2)
            y1 = random.randint(0, height / 2)
            x2 = random.randint(0, width)
            y2 = random.randint(height / 2, height)
            draw.line(((x1, y1), (x2, y2)), fill='purple', width=2)

    # 绘制验证码图片
    def draw_verify_code(self):
        code = self.gen_text()
        width, height = 120, 50  # 设定图片大小
        # 创建图片对象，并将背景设置成白色
        im = Image.new('RGB', (width, height), 'white')
        font = ImageFont.truetype(font='arial.ttf', size=40)
        draw = ImageDraw.Draw(im)  # 新建ImageDraw对象
        # 绘制字符串
        for i in range(4):
            draw.text((5 + random.randint(-3, 3) + 23 * i, 5 + random.randint(-3, 3)),
                      text=code[i],
                      fill=self.rand_color(), font=font)
        # 绘制干扰线
        self.draw_lines(draw, 5, width, height)
        # im.show()  # 如需临时调试，可以直接将生成的图片显示出来
        return im, code

    # 生成图片验证码并返回给控制器
    def get_code(self):
        image, code = self.draw_verify_code()
        buf = BytesIO()
        # 将生成的验证码图片存入内存之中
        image.save(buf, 'jpeg')
        # 从内存中读取上一步存储的验证码图片
        bstring = buf.getvalue()
        return code, bstring

# code=gen_email_code()
# print(code)
# send_email('1159074129@qq.com',code)
# imageCode().gen_text()
# imageCode().draw_verify_code()
