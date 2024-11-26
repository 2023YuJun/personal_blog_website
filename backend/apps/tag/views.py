from rest_framework.views import APIView
from rest_framework import status
from apps.tag.service import *
from utils.result import result, throw_error, ERRORCODE

error_code = ERRORCODE['TAG']


class TagView(APIView):
    def post(self, request, *args, **kwargs):
        if 'add' in request.path:
            return self.add_tag(request)
        elif 'delete' in request.path:
            return self.delete_tags(request)
        elif 'getTagList' in request.path:
            return self.get_tag_list(request)

    def put(self, request, *args, **kwargs):
        if 'update' in request.path:
            return self.update_tag(request)

    def get(self, request, *args, **kwargs):
        if 'getTagDictionary' in request.path:
            return self.get_tag_dictionary(request)

    def add_tag(self, request):
        """
        新增标签
        """
        try:
            tag = request.data
            response = verify_tag(tag)
            if response is None:
                res = create_tag(tag)
                return Response(result("新增标签成功", {
                    'id': res.id,
                    'tag_name': res.tag_name,
                }), status=status.HTTP_201_CREATED)
            else:
                return response
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "新增标签失败"), status=status.HTTP_400_BAD_REQUEST)

    def update_tag(self, request):
        """
        修改标签
        """
        try:
            tag = request.data
            response = verify_tag(tag)
            if response is None:
                res = update_tag(tag)
                return Response(result("修改标签成功", res), status=status.HTTP_200_OK)
            else:
                return response
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "修改标签失败"), status=status.HTTP_400_BAD_REQUEST)

    def delete_tags(self, request):
        """
        删除标签
        """
        try:
            tag = request.data
            response = verify_delete_tags(tag)
            if response is None:
                res = delete_tags(tag)
                return Response(result("删除标签成功", {'updateNum': res}), status=status.HTTP_200_OK)
            else:
                return response
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "删除标签失败"), status=status.HTTP_400_BAD_REQUEST)

    def get_tag_list(self, request):
        """
        分页查找标签
        """
        try:
            tag = request.data
            res = get_tag_list(tag)
            return Response(result("分页查找标签成功", res), status=status.HTTP_200_OK)
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "分页查找标签失败"), status=status.HTTP_400_BAD_REQUEST)

    def get_tag_dictionary(self, request):
        """
        获取标签字典
        """
        try:
            res = get_tag_dictionary()
            return Response(result("获取标签字典成功", res), status=status.HTTP_200_OK)
        except Exception as err:
            print(err)
            return Response(throw_error(error_code, "获取标签字典失败"), status=status.HTTP_400_BAD_REQUEST)
