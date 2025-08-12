from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from .models import Notification


@login_required
def notification_list(request):
    """Display all notifications for the current user"""
    # Get all notifications for the current user
    notifications = Notification.objects.filter(
        recipient=request.user
    ).select_related('sender').prefetch_related('content_type')
    
    # Filter by status if requested
    status_filter = request.GET.get('status')
    if status_filter == 'unread':
        notifications = notifications.filter(is_read=False)
    elif status_filter == 'read':
        notifications = notifications.filter(is_read=True)
    
    # Filter by type if requested
    type_filter = request.GET.get('type')
    if type_filter:
        notifications = notifications.filter(notification_type=type_filter)
    
    # Paginate notifications
    paginator = Paginator(notifications, 20)  # Show 20 notifications per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get counts for the filter tabs
    total_count = Notification.objects.filter(recipient=request.user).count()
    unread_count = Notification.objects.filter(recipient=request.user, is_read=False).count()
    read_count = total_count - unread_count
    
    context = {
        'page_obj': page_obj,
        'notifications': page_obj.object_list,
        'total_count': total_count,
        'unread_count': unread_count,
        'read_count': read_count,
        'current_filter': status_filter or 'all',
        'current_type': type_filter or 'all',
        'notification_types': Notification.NOTIFICATION_TYPES,
    }
    
    return render(request, 'notifications/notification_list.html', context)


@login_required
def mark_as_read(request, notification_id):
    """Mark a specific notification as read"""
    if request.method == 'POST':
        notification = get_object_or_404(
            Notification, 
            id=notification_id, 
            recipient=request.user
        )
        
        if not notification.is_read:
            notification.mark_as_read()
            
        # Return JSON response for AJAX requests
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': 'Notification marked as read'
            })
        
        messages.success(request, 'Notification marked as read.')
        return redirect('notifications:list')
    
    return redirect('notifications:list')


@login_required
def mark_all_as_read(request):
    """Mark all notifications as read for the current user"""
    if request.method == 'POST':
        unread_notifications = Notification.objects.filter(
            recipient=request.user,
            is_read=False
        )
        
        count = unread_notifications.count()
        unread_notifications.update(is_read=True, read_at=timezone.now())
        
        # Return JSON response for AJAX requests
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': f'{count} notifications marked as read',
                'count': count
            })
        
        messages.success(request, f'{count} notifications marked as read.')
        return redirect('notifications:list')
    
    return redirect('notifications:list')


@login_required
def delete_notification(request, notification_id):
    """Delete a specific notification"""
    if request.method == 'POST':
        notification = get_object_or_404(
            Notification, 
            id=notification_id, 
            recipient=request.user
        )
        
        notification.delete()
        
        # Return JSON response for AJAX requests
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': 'Notification deleted'
            })
        
        messages.success(request, 'Notification deleted.')
        return redirect('notifications:list')
    
    return redirect('notifications:list')


@login_required
def delete_all_read(request):
    """Delete all read notifications for the current user"""
    if request.method == 'POST':
        read_notifications = Notification.objects.filter(
            recipient=request.user,
            is_read=True
        )
        
        count = read_notifications.count()
        read_notifications.delete()
        
        # Return JSON response for AJAX requests
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': f'{count} read notifications deleted',
                'count': count
            })
        
        messages.success(request, f'{count} read notifications deleted.')
        return redirect('notifications:list')
    
    return redirect('notifications:list')


@login_required
def get_unread_count(request):
    """Get the count of unread notifications (for AJAX updates)"""
    count = Notification.objects.filter(
        recipient=request.user,
        is_read=False
    ).count()
    
    return JsonResponse({'unread_count': count})
