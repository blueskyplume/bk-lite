from rest_framework.viewsets import ModelViewSet
from apps.core.utils.web_utils import WebUtils
from apps.log.models.log_group import LogGroup, LogGroupOrganization
from apps.log.services.access_scope import LogAccessScopeService
from apps.log.serializers.log_group import LogGroupSerializer
from apps.log.filters.log_group import LogGroupFilter
from apps.log.constants.permission import PermissionConstants


class LogGroupViewSet(ModelViewSet):
    queryset = LogGroup.objects.all()
    serializer_class = LogGroupSerializer
    filterset_class = LogGroupFilter

    def get_queryset(self):
        try:
            queryset, _ = LogAccessScopeService.get_accessible_group_queryset(self.request)
            return queryset
        except ValueError:
            return LogGroup.objects.none()

    def _attach_item_permissions(self, items, permission):
        """为日志分组列表补充实例权限字段。"""
        instance_permissions = permission.get("instance", []) if isinstance(permission, dict) else []
        instance_permission_map = {}
        if isinstance(instance_permissions, list):
            for item in instance_permissions:
                if not isinstance(item, dict) or "id" not in item:
                    continue
                instance_permission_map[str(item["id"])] = item.get("permission") or PermissionConstants.DEFAULT_PERMISSION

        for item in items:
            item["permission"] = instance_permission_map.get(str(item.get("id")), PermissionConstants.DEFAULT_PERMISSION)

        return items

    def create(self, request, *args, **kwargs):
        try:
            _, permission = LogAccessScopeService.get_accessible_group_queryset(request)
        except ValueError as exc:
            return WebUtils.response_error(error_message=str(exc), status_code=400)

        if not permission.get("team"):
            return WebUtils.response_error(error_message="当前用户无权限创建日志分组", status_code=403)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 设置创建者
        serializer.validated_data["created_by"] = request.user.username

        log_group = serializer.save()

        return WebUtils.response_success({"id": log_group.id, "name": log_group.name})

    def list(self, request, *args, **kwargs):
        try:
            queryset, permission = LogAccessScopeService.get_accessible_group_queryset(request)
        except ValueError as exc:
            return WebUtils.response_error(error_message=str(exc), status_code=400)

        # 应用过滤器
        queryset = self.filter_queryset(queryset)

        # 检查是否为全量查询（page_size为-1时不分页）
        page_size = request.query_params.get("page_size")
        if page_size == "-1":
            # 全量查询，直接返回所有数据
            serializer = self.get_serializer(queryset, many=True)
            results = self._attach_item_permissions(serializer.data, permission)
            return WebUtils.response_success(results)

        # 分页
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            results = self._attach_item_permissions(serializer.data, permission)
            return self.get_paginated_response(results)

        serializer = self.get_serializer(queryset, many=True)
        results = self._attach_item_permissions(serializer.data, permission)
        return WebUtils.response_success(results)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        # 设置更新者
        serializer.validated_data["updated_by"] = request.user.username

        log_group = serializer.save()

        return WebUtils.response_success({"id": log_group.id, "name": log_group.name})

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        log_group_name = instance.name

        # 删除相关的组织关联
        LogGroupOrganization.objects.filter(log_group=instance).delete()

        # 删除日志分组
        instance.delete()

        return WebUtils.response_success({"name": log_group_name})
