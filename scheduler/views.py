from rest_framework.generics import ListAPIView
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from .utils import send_notification_to_user
from .models import Prisoner, ActivityType, RequestTemplate, ApprovalProcess, DepartmentRole
from .serializers import (
    PrisonerSerializer, ActivityTypeSerializer, RequestTemplateSerializer, 
    ApprovalProcessSerializer, DepartmentRoleSerializer
)
from rest_framework.views import APIView


class PrisonerViewSet(viewsets.ModelViewSet):
    queryset = Prisoner.objects.all()
    serializer_class = PrisonerSerializer
    permission_classes = [IsAuthenticated]


class ActivityTypeViewSet(viewsets.ModelViewSet):
    queryset = ActivityType.objects.all()
    serializer_class = ActivityTypeSerializer
    permission_classes = [IsAuthenticated]


class RequestTemplateViewSet(viewsets.ModelViewSet):
    queryset = RequestTemplate.objects.all()
    serializer_class = RequestTemplateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'], url_path='approve')
    def approve_request(self, request, pk=None):
        # Custom endpoint to handle the approval of a request
        request_instance = self.get_object()
        current_user = request.user

        # Check if the current user belongs to the department that should handle this request
        user_departments = DepartmentRole.objects.filter(users__in=[current_user])
        current_department_order = user_departments.values_list('order', flat=True)

        # Find the current stage of the request's approval process
        last_approval = request_instance.approval_processes.order_by('approved_at').last()
        next_department_order = (last_approval.department.order + 1) if last_approval else 1

        if next_department_order in current_department_order:

            ApprovalProcess.objects.create(
                request_template=request_instance,
                approved_by=current_user,
                status=True, 
            )
            request_instance.status = 'In Process' if next_department_order < DepartmentRole.objects.count() else 'Approved'
            request_instance.save()

            send_notification_to_user(request_instance.created_by.id, "Your request has been approved.")
            return Response({'message': 'Request approved successfully!'}, status=status.HTTP_200_OK)

            return Response({'message': 'Request approved successfully!'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'You are not authorized to approve this request at this stage.'}, status=status.HTTP_403_FORBIDDEN)

    @action(detail=True, methods=['post'], url_path='deny')
    def deny_request(self, request, pk=None):
        request_instance = self.get_object()
        current_user = request.user

        ApprovalProcess.objects.create(
            request_template=request_instance,
            approved_by=current_user,
            status=False, 
        )

        request_instance.status = 'Denied'
        request_instance.save()
        send_notification_to_user(request_instance.created_by.id, "Your request has been denied.")
        return Response({'message': 'Request denied successfully!'}, status=status.HTTP_200_OK)
    

class ApprovalProcessViewSet(viewsets.ModelViewSet):
    queryset = ApprovalProcess.objects.all()
    serializer_class = ApprovalProcessSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()


class DepartmentRoleViewSet(viewsets.ModelViewSet):
    queryset = DepartmentRole.objects.all()
    serializer_class = DepartmentRoleSerializer
    permission_classes = [IsAuthenticated]


class PrisonerSearchAPIView(ListAPIView):
    serializer_class = PrisonerSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned prisoners by `prisoner_id` and approval status.
        """
        queryset = Prisoner.objects.all()
        prisoner_id = self.request.query_params.get('prisoner_id')
        approved = self.request.query_params.get('approved')

        if prisoner_id is not None:
            queryset = queryset.filter(prisoner_id=prisoner_id)
        if approved is not None:
            approved = approved.lower() in ['true', '1', 't']  # Accepts 'true', '1', or 't' as true values
            queryset = queryset.filter(approved=approved)

        return queryset



class UserDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user  
        department_roles = DepartmentRole.objects.filter(users__in=[user]) 

        # Prepare the response data
        data = {
            "username": user.username,
            "full_name": f"{user.first_name} {user.last_name}",
            "departments": [role.name for role in department_roles]  # List of department names
        }

        return Response(data)