import os
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.article.article_service import get_article_count
from apps.category.service import get_category_count
from apps.tag.service import get_tag_count
from apps.user.service import get_user_count
from apps.config.service import *
from utils.minioUpload import minio_upload, delete_minio_imgs
from utils.result import result, throw_error, ERRORCODE

error_code_upload = ERRORCODE['UPLOAD']
error_code_config = ERRORCODE['CONFIG']
error_code = ERRORCODE['STATISTIC']


class ConfigView(APIView):
    def post(self, request, *args, **kwargs):
        if 'update' in request.path:
            return self.update_config(request)
        elif 'img' in request.path:
            return self.upload(request)

    def put(self, request, *args, **kwargs):
        if 'addView' in request.path:
            return self.add_view_count(request)

    def get(self, request, *args, **kwargs):
        if 'config' in request.path:
            return self.get_config(request)
        elif 'statistic' in request.path:
            return self.home_get_statistic(request)

    def upload(self, request):
        file = request.FILES.get('file')

        if file:
            res = minio_upload(file)
            if res:
                return Response(result("图片上传成功", {'url': res}), status=200)
            else:
                return Response(throw_error(error_code_upload, "图片上传失败"), status=400)
        return Response(throw_error(error_code_upload, "文件上传失败"), status=400)

    def delete_online_imgs(self, request):
        img_list = request.data.get('imgList', [])
        for img in img_list:
            file_path = os.path.join(settings.BASE_DIR, "upload/online", img)
            if os.path.exists(file_path):
                os.remove(file_path)
        return Response(result("删除图片成功"), status=200)

    def update_config(self, request):
        try:
            config = get_config()
            request_data = request.data

            for key in ['avatar_bg', 'blog_avatar', 'qq_link', 'we_chat_link',
                        'we_chat_group', 'qq_group', 'we_chat_pay', 'ali_pay']:
                if key in request_data and config and config.get(key) != request_data[key]:
                    delete_minio_imgs([config[key].split("/")[-1]])

            res = update_config(request_data)
            return Response(result("修改网站设置成功", res), status=200)
        except Exception as err:
            print(err)
            return Response(throw_error(error_code_config, "修改网站设置失败"), status=400)

    def get_config(self, request):
        try:
            res = get_config()
            if res:
                return Response(result("获取网站设置成功", res), status=200)
            else:
                return Response(result("请去博客后台完善博客信息", res))
        except Exception as err:
            print(err)
            return Response(throw_error(error_code_config, "获取网站设置失败"), status=400)

    def add_view_count(self, request):
        try:
            res = add_view()
            if res == "添加成功":
                return Response(result("增加访问量成功", res), status=200)
            elif res == "需要初始化":
                return Response(result("请先初始化网站信息", res), status=200)
        except Exception as err:
            print(err)
            return Response(throw_error(error_code_config, "增加网站访问量失败"), status=400)

    def home_get_statistic(self, request):
        try:
            article_count = get_article_count()
            tag_count = get_tag_count()
            category_count = get_category_count()
            user_count = get_user_count()

            return Response(result("获取数据统计成功", {
                "articleCount": article_count,
                "tagCount": tag_count,
                "categoryCount": category_count,
                "userCount": user_count,
            }), status=200)
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "获取数据统计失败"), status=400)
