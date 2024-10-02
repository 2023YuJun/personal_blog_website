# src/views/article_views.py

from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import ArticleSerializer
from service.article import article_service
from utils.minioUpload import delete_minio_imgs
from utils.result import result, ERRORCODE, throw_error

error_code = ERRORCODE['ARTICLE']


@api_view(['POST'])
def create_article_view(request):
    try:
        article_data = request.data
        new_article = article_service.create_article(article_data)
        return JsonResponse(result("新增文章成功", new_article), status=status.HTTP_201_CREATED)
    except Exception as err:
        print(err)
        return JsonResponse(throw_error(error_code, "新增文章失败"), status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def update_article_view(request, article_id):
    try:
        article_data = request.data
        old_cover = article_service.get_article_cover_by_id(article_id)

        # 删除旧封面图片的逻辑
        if old_cover and old_cover != article_data.get('article_cover'):
            delete_minio_imgs([old_cover.split("/")[-1]])

        updated_article = article_service.update_article(article_id, article_data)
        return JsonResponse(result("修改文章成功", updated_article), status=status.HTTP_200_OK)
    except Exception as err:
        print(err)
        return JsonResponse(throw_error(error_code, "修改文章失败"), status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
def update_top_view(request, article_id):
    try:
        is_top = request.data.get('is_top')
        updated_article = article_service.update_top(article_id, is_top)
        return JsonResponse(result("修改文章置顶状态成功", updated_article), status=status.HTTP_200_OK)
    except Exception as err:
        print(err)
        return JsonResponse(throw_error(error_code, "修改文章置顶状态失败"), status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_article_view(request, article_id):
    try:
        status = request.data.get('status', 0)
        if status == 3:
            old_cover = article_service.get_article_cover_by_id(article_id)
            delete_minio_imgs([old_cover.split("/")[-1]]) if old_cover else None

        res = article_service.delete_article(article_id, status)
        return JsonResponse(result("删除文章成功", res), status=status.HTTP_200_OK)
    except Exception as err:
        print(err)
        return JsonResponse(throw_error(error_code, "删除文章失败"), status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def revert_article_view(request, article_id):
    try:
        res = article_service.revert_article(article_id)
        return JsonResponse(result("恢复文章成功", res), status=status.HTTP_200_OK)
    except Exception as err:
        print(err)
        return JsonResponse(throw_error(error_code, "恢复文章失败"), status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
def toggle_article_public_view(request, article_id):
    try:
        status = request.data.get('status')
        res = article_service.toggle_article_public(article_id, status)
        message = "公开文章" if status == 1 else "隐藏文章"
        return JsonResponse(result(f"{message}成功", res), status=status.HTTP_200_OK)
    except Exception as err:
        print(err)
        return JsonResponse(throw_error(error_code, f"{message}失败"), status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def get_article_list_view(request):
    try:
        articles = article_service.get_article_list(request.data)
        return JsonResponse(result("查询文章成功", articles), status=status.HTTP_200_OK)
    except Exception as err:
        print(err)
        return JsonResponse(throw_error(error_code, "查询文章失败"), status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def get_article_info_by_title_view(request):
    try:
        title_info = request.data
        res = article_service.get_article_info_by_title(title_info)
        return JsonResponse(result("文章查询结果", res), status=status.HTTP_200_OK)
    except Exception as err:
        print(err)
        return JsonResponse(throw_error(error_code, "根据标题查询文章失败"), status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_article_by_id_view(request, article_id):
    try:
        article = article_service.get_article_by_id(article_id)
        return JsonResponse(result("查询文章详情成功", article), status=status.HTTP_200_OK)
    except Exception as err:
        print(err)
        return JsonResponse(throw_error(error_code, "查询文章详情失败"), status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def blog_home_get_article_list_view(request, current, size):
    try:
        articles = article_service.blog_home_get_article_list(current, size)
        return JsonResponse(result("获取文章列表成功", articles), status=status.HTTP_200_OK)
    except Exception as err:
        print(err)
        return JsonResponse(throw_error(error_code, "获取文章列表失败"), status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def blog_timeline_get_article_list_view(request, current, size):
    try:
        articles = article_service.blog_timeline_get_article_list(current, size)
        return JsonResponse(result("获取文章时间轴列表成功", articles), status=status.HTTP_200_OK)
    except Exception as err:
        print(err)
        return JsonResponse(throw_error(error_code, "获取文章列表失败"), status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def get_article_list_by_tag_id_view(request):
    try:
        tag_id = request.data.get('id')
        current = request.data.get('current')
        size = request.data.get('size')
        if not tag_id:
            return JsonResponse(throw_error(error_code, "标签id不能为空"), status=status.HTTP_400_BAD_REQUEST)

        articles = article_service.get_article_list_by_tag_id(current, size, tag_id)
        return JsonResponse(result("根据标签获取文章列表成功", articles), status=status.HTTP_200_OK)
    except Exception as err:
        print(err)
        return JsonResponse(throw_error(error_code, "根据标签获取文章列表失败"), status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def get_article_list_by_category_id_view(request):
    try:
        category_id = request.data.get('id')
        current = request.data.get('current')
        size = request.data.get('size')
        if not category_id:
            return JsonResponse(throw_error(error_code, "分类id不能为空"), status=status.HTTP_400_BAD_REQUEST)

        articles = article_service.get_article_list_by_category_id(current, size, category_id)
        return JsonResponse(result("根据分类获取文章列表成功", articles), status=status.HTTP_200_OK)
    except Exception as err:
        print(err)
        return JsonResponse(throw_error(error_code, "根据分类获取文章列表失败"), status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_recommend_article_by_id_view(request, article_id):
    try:
        res = article_service.get_recommend_article_by_id(article_id)
        return JsonResponse(result("获取推荐文章成功", res), status=status.HTTP_200_OK)
    except Exception as err:
        print(err)
        return JsonResponse(throw_error(error_code, "获取推荐文章失败"), status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_article_list_by_content_view(request, content):
    try:
        articles = article_service.get_article_list_by_content(content)
        return JsonResponse(result("按照内容搜索文章成功", articles), status=status.HTTP_200_OK)
    except Exception as err:
        print(err)
        return JsonResponse(throw_error(error_code, "按照内容搜索文章失败"), status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_hot_article_view(request):
    try:
        articles = article_service.get_hot_article()
        return JsonResponse(result("获取热门文章成功", articles), status=status.HTTP_200_OK)
    except Exception as err:
        print(err)
        return JsonResponse(throw_error(error_code, "获取热门文章失败"), status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def article_like_view(request, article_id):
    try:
        res = article_service.article_like(article_id)
        return JsonResponse(result("点赞成功", res), status=status.HTTP_200_OK)
    except Exception as err:
        print(err)
        return JsonResponse(throw_error(error_code, "点赞失败"), status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def cancel_article_like_view(request, article_id):
    try:
        res = article_service.cancel_article_like(article_id)
        return JsonResponse(result("取消点赞成功", res), status=status.HTTP_200_OK)
    except Exception as err:
        print(err)
        return JsonResponse(throw_error(error_code, "取消点赞失败"), status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def add_reading_duration_view(request, article_id):
    try:
        duration = request.data.get('duration')
        res = article_service.add_reading_duration(article_id, duration)
        return JsonResponse(result("增加阅读时长成功", res), status=status.HTTP_200_OK)
    except Exception as err:
        print(err)
        return JsonResponse(throw_error(error_code, "增加阅读时长失败"), status=status.HTTP_400_BAD_REQUEST)
