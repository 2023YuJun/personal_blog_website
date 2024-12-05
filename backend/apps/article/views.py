from rest_framework.views import APIView

from apps.article.article_service import *
from utils.minioUpload import delete_minio_imgs
from utils.result import result, ERRORCODE, throw_error
from .articleTag_service import delete_article_tag
from .common import create_category_or_return, create_article_tag_by_article_id

error_code = ERRORCODE['ARTICLE']


class ArticleView(APIView):

    def post(self, request, *args, **kwargs):
        if 'add' in request.path:
            return self.create_article(request)
        elif 'titleExist' in request.path:
            return self.get_article_info_by_title(request)
        elif 'getArticleListByTagId' in request.path:
            return self.get_article_list_by_tag_id(request)
        elif 'getArticleListByCategoryId' in request.path:
            return self.get_article_list_by_category_id(request)
        elif 'getArticleList' in request.path:
            return self.get_article_list(request)
        elif 'updateUrl' in request.path:
            return update_url()

    def put(self, request, *args, **kwargs):
        id = kwargs.get('id')
        is_top = kwargs.get('is_top')
        status = kwargs.get('status')
        duration = kwargs.get('duration')
        if 'updateTop' in request.path:
            return self.update_top(request, id, is_top)
        elif 'update' in request.path:
            return self.update_article(request)
        elif 'revert' in request.path:
            return self.revert_article(request, id)
        elif 'isPublic' in request.path:
            return self.toggle_article_public(request, id, status)
        elif 'like' in request.path:
            return self.article_like(request, id)
        elif 'cancelLike' in request.path:
            return self.cancel_article_like(request, id)
        elif 'addReadingDuration' in request.path:
            return self.add_reading_duration(request, id, duration)

    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')
        current = kwargs.get('current')
        size = kwargs.get('size')
        if 'add' in request.path:
            return self.create_article(request)
        elif 'blogHomeGetArticleList' in request.path:
            return self.blog_home_get_article_list(request, current, size)
        elif 'blogTimelineGetArticleList' in request.path:
            return self.blog_timeline_get_article_list(request, current, size)
        elif 'getRecommendArticleById' in request.path:
            return self.get_recommend_article_by_id(request, id)
        elif 'getArticleListByContent' in request.path:
            content = kwargs.get('content')
            return self.get_article_list_by_content(request, content)
        elif 'getHotArticle' in request.path:
            return self.get_hot_article(request)
        elif 'getArticleById' in request.path:
            return self.get_article_by_id(request, id)

    def delete(self, request, *args, **kwargs):
        id = kwargs.get('id')
        status = kwargs.get('status')
        if 'delete' in request.path:
            return self.delete_article(request, id, status)

    def create_article(self, request):
        try:
            response = verify_article_param(request)
            if response is None:
                response = create_judge_title_exist(request)
                if response is None:
                    data = request.data
                    tag_list = data.get("tagList")
                    category = data.get("category")
                    data["category_id"] = create_category_or_return(category)
                    new_article = create_article(data)
                    if new_article:
                        new_article_tag_list = create_article_tag_by_article_id(new_article.id, tag_list)
                        serialized_article = ArticleSerializer(new_article).data
                        return Response(result("新增文章成功", {
                            "article": serialized_article,
                            "articleTagList": new_article_tag_list,
                        }), status=201)
                    else:
                        return Response(throw_error(error_code, "新增文章失败"), status=400)
                else:
                    return response
            else:
                return response
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "新增文章失败"), status=400)

    def update_article(self, request):
        try:
            verify_article_param(request)
            update_judge_title_exist(request)
            data = request.data
            tag_list = data.get("tagList")
            category = data.get("category")
            old_cover = get_article_cover_by_id(data["id"])

            # 删除旧封面图片的逻辑
            if old_cover and old_cover != data["article_cover"]:
                delete_minio_imgs([old_cover.split("/")[-1]])

            delete_article_tag(data["id"])
            data["category_id"] = create_category_or_return(category)
            new_article_tag_list = create_article_tag_by_article_id(data["id"], tag_list)
            res = update_article(data)
            if res:
                return Response(result("修改文章成功", {
                    "res": res,
                    "newArticleTagList": new_article_tag_list,
                }), status=200)
            else:
                return Response(throw_error(error_code, "修改文章失败"), status=400)
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "修改文章失败"), status=400)

    def update_top(self, request, id, is_top):
        try:
            response = verify_top_param(id, is_top)
            if response is None:
                res = update_top(id, is_top)
                return Response(result("修改文章置顶状态成功", res), status=200)
            else:
                return response
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "修改文章置顶状态失败"), status=400)

    def delete_article(self, request, id, status):
        try:
            response = verify_del_param(id, status)
            if response is None:
                if int(status) == 3:
                    old_cover = get_article_cover_by_id(id)
                    delete_minio_imgs([old_cover.split("/")[-1]]) if old_cover else None

                res = delete_article(id, status)
                return Response(result("删除文章成功", res), status=200)
            else:
                return response
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "删除文章失败"), status=400)

    def revert_article(self, request, id):
        try:
            res = revert_article(id)
            return Response(result("恢复文章成功", res), status=200)
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "恢复文章失败"), status=400)

    def toggle_article_public(self, request, id, status):
        try:
            verify_del_param(id, status)
            res = toggle_article_public(id, status)
            message = "公开文章" if int(status) == 1 else "隐藏文章"
            return Response(result(f"{message}成功", res), status=200)
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, message + "失败"), status=400)

    def get_article_list(self, request):
        try:
            res = get_article_list(request.data)
            return Response(result("查询文章成功", res), status=200)
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "查询文章失败"), status=400)

    def get_article_info_by_title(self, request):
        try:
            data = request.data
            res = get_article_info_by_title(data)
            return Response(result("文章查询结果", res), status=200)
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "根据标题查询文章失败"), status=400)

    def get_article_by_id(self, request, id):
        try:
            res = get_article_by_id(id)
            return Response(result("查询文章详情成功", res), status=200)
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "查询文章详情失败"), status=400)

    def blog_home_get_article_list(self, request, current, size):
        try:
            res = blog_home_get_article_list(current, size)
            return Response(result("获取文章列表成功", res), status=200)
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "获取文章列表失败"), status=400)

    def blog_timeline_get_article_list(self, request, current, size):
        try:
            res = blog_timeline_get_article_list(current, size)
            return Response(result("获取文章时间轴列表成功", res), status=200)
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "获取文章列表失败"), status=400)

    def get_article_list_by_tag_id(self, request):
        try:
            data = request.data
            id = data.get("id")
            current = data.get("current")
            size = data.get("size")
            if not id:
                return Response(throw_error(error_code, "标签id不能为空"), status=400)

            res = get_article_list_by_tag_id(current, size, id)
            return Response(result("根据标签获取文章列表成功", res), status=200)
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "根据标签获取文章列表失败"), status=400)

    def get_article_list_by_category_id(self, request):
        try:
            data = request.data
            id = data.get("id")
            current = data.get("current")
            size = data.get("size")
            if not id:
                return Response(throw_error(error_code, "分类id不能为空"), status=400)

            res = get_article_list_by_category_id(current, size, id)
            return Response(result("根据分类获取文章列表成功", res), status=200)
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "根据分类获取文章列表失败"), status=400)

    def get_recommend_article_by_id(self, request, id):
        try:
            res = get_recommend_article_by_id(id)
            return Response(result("获取推荐文章成功", res), status=200)
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "获取推荐文章失败"), status=400)

    def get_article_list_by_content(self, request, content):
        try:
            articles = get_article_list_by_content(content)
            return Response(result("按照内容搜索文章成功", articles), status=200)
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "按照内容搜索文章失败"), status=400)

    def get_hot_article(self, request):
        try:
            articles = get_hot_article()
            return Response(result("获取热门文章成功", articles), status=200)
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "获取热门文章失败"), status=400)

    def article_like(self, request, id):
        try:
            res = article_like(id)
            return Response(result("点赞成功", res), status=200)
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "点赞失败"), status=400)

    def cancel_article_like(self, request, id):
        try:
            res = cancel_article_like(id)
            return Response(result("取消点赞成功", res), status=200)
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "取消点赞失败"), status=400)

    def add_reading_duration(self, request, id, duration):
        try:
            res = add_reading_duration(id, duration)
            return Response(result("增加阅读时长成功", res), status=200)
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "增加阅读时长失败"), status=400)
