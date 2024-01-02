import os
import time

from flask import Blueprint, request, render_template, jsonify

from common.utility import compress_image

ueditor = Blueprint("ueditor", __name__)


@ueditor.route('/uedit', methods=['GET', 'POST'])
def uedit():
    param = request.args.get('action')
    if request.method == 'GET' and param == 'config':
        return render_template('config.json')
    elif request.method == 'POST' and request.args.get('action') == 'uploadimage':
        f = request.files['upfile']
        filename = f.filename
        # 为传上来的文件生成统一用户名
        suffix = filename.split('.')[-1]
        # 保存原图到upload目录
        f.save('./resource/upload/' + filename)

        newname = time.strftime('%Y%m%d_%H%M%S.' + suffix)
        # # 对图片进行压缩，按照1200像素的宽度为准，并覆盖原始文件
        source = './resource/upload/' + filename
        dest = './resource/upload/' + newname
        compress_image(source, dest, 720)

        result = {}
        result['state'] = 'SUCCESS'
        result['url'] = f"upload/{newname}"
        result['title'] = filename
        result['original'] = filename
        return jsonify(result)  # 以json数据可是返回，供前端引用
    elif request.method == 'GET' and param == 'listimage':
        list = []
        filelist = os.listdir('./resource/upload')
        for filename in filelist:
            if filename.lower().endswith('.png') or filename.lower().endswith('.jpg') or filename.lower().endswith(
                    '.bmp'):
                list.append({'url': 'upload/%s' % filename})
        result = {}
        result['state'] = 'SUCCESS'
        result['list'] = list
        result['start'] = 0
        result['total'] = 50
        return jsonify(result)  # 以json数据可是返回，供前端引用
