from flask import Blueprint, request, render_template

ueditor = Blueprint("ueditor", __name__)


@ueditor.route('/uedit', methods=['GET', 'POST'])
def uedit():
    param = request.args.get('action')
    if request.method == 'GET' and param == 'config':
        return render_template('config.json')
    else:
        print(param)
        return 'qwe'

# @ueditor.route('/uedit', methods=['POST'])
# def upload():
#     # 获取上传的文件对象
#     upload_file = request.files['file']
#
#     # 在这里处理上传文件，可以保存到指定目录等操作
#     # 示例：保存文件到指定目录
#     upload_file.save('/resource/img/save/' + upload_file.filename)
#
#     # 返回上传成功的响应，这里可以返回给前端 UEditor 所需的数据格式
#     # 示例：返回 JSON 格式的数据
#     return {
#         'state': 'SUCCESS',
#         'url': '/path/to/save/' + upload_file.filename,  # 可以返回文件的 URL
#         'title': upload_file.filename,
#         'original': upload_file.filename
#     }