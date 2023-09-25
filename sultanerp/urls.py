"""
URL configuration for sultanerp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from sultanerp import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    
    
    path("", views.dashboard_view, name="dashboard"),
    
    path('accounts/', include('django.contrib.auth.urls')),
    path("admin/", admin.site.urls),

    path('admin-tools/', views.admin_tools, name='admin_tools'),

    path('webhook/', views.webhook_view, name='webhook_view'),
    path('crm/', views.crm_view, name='crm_view'),
    path('update_crm_status/', views.update_crm_status, name='update_crm_status'),
    
    path('get_cake_id/', views.get_cake_id, name='get_cake_id'),
    path('tasks/', views.task_list, name='task_list'),
    path('tasks/add/', views.add_task, name='add_task'),
    # "https://docs.djangoproject.com/en/4.2/topics/http/urls/#example" - "to capture an integer parameter from the URL..."
    path('tasks/edit/<int:task_id>/', views.edit_task, name='edit_task'),
    path('tasks/<int:task_id>/', views.task_detail, name='task_detail'),
    path('tasks/delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path('mark_task_open/<int:task_id>/',
         views.mark_task_open, name='mark_task_open'),
    path('mark_task_done/<int:task_id>/',
         views.mark_task_done, name='mark_task_done'),

    path('routine/add_routine/', views.add_routine, name='add_routine'),
    path('routine/daily_routines/<int:task_id>/',
         views.daily_routines_detail, name='routine_detail'),
    path('routine/routines/', views.routines_and_daily_list, name='routine_list'),

    path('documents/', views.document_management_view, name='documents'),
    path('folder_content/<str:folder_name>/<str:document_filename>/',
         views.folder_content_view, name='folder_content_view'),

    # upload products using csv
    path('upload_csv_internal/',
         views.upload_csv_internal_products, name='upload_csv'),
    path('upload_csv_supplier/',
         views.upload_csv_supplier_products, name='upload_supplierproduct'),
    
    #orders
     path('orders/', views.orders_view, name='orders_view'),

    path('orders/cake_order/', views.cake_order, name='cake_order'),
        
    path('orders/internal_orders/', views.internal_orders, name='internal_orders'),
    path('orders/internal_orders/<int:order_id>/',
         views.internal_order_detail, name='internal_order_detail'),
    path('orders/internal_orders_list/', views.internal_orders_list_view,
         name='internal_orders_list_view'),

    path('orders/customer_orders/', views.customer_orders, name='customer_orders'),
    path('orders/customer_order_detail/<int:order_id>/',
         views.customer_order_detail, name='customer_order_detail'),
    path('orders/customer_orders_list/', views.customer_orders_list_view,
         name='customer_orders_list_view'),

    path('orders/supplier_orders/', views.supplier_orders, name='supplier_orders'),
    path('orders/supplier_orders/<int:order_id>/',
         views.supplier_order_detail, name='supplier_order_detail'),
    path('orders/supplier_orders_list/', views.supplier_orders_list_view,
         name='supplier_orders_list_view'),

    path('retoure/', views.retoure_view, name='retoure'),
    path('orders/retoure/<int:order_id>/',
         views.retoure_detail, name='retoure_detail'),
    path('retoure_list', views.retoure_list_view,
         name='retoure_list'),

    path('inventory/', views.inventory_view, name='inventory'),
    path('deposit/', views.deposit_view, name='deposit'),
    path('deposit-list/', views.deposit_list_view, name='deposit_list'),

    path("calendar/", views.calendar_view, name="calendar"),
    
    path('stats/logs/', views.show_logs, name='logs'),
    path('stats/logs/routine_task_logs/',
         views.show_logs, name='routine_task_logs'),
    path('stats/logs/login_logs/', views.show_logs, name='login_logs'),

    path("messenger/", views.messenger_view, name="messenger"),
    path('messenger/messages/send/<int:recipient_id>/',
         views.send_message, name='send_message'),
    path('messenger/messages/send/',
         views.send_message_no_id, name='send_message_no_id'),
    path('messenger/messages/', views.messages_list, name='messages_list'),
    path('messenger/messages/conversation/<int:recipient_id>/',
         views.conversation, name='conversation'),

    path('stats/statistics/', views.statistics, name='statistics'),
    path('stats/statistics/cake_order_statistics/',
         views.statistics, name='cake_order_statistics'),
    path('stats/statistics/retoure/', views.statistics, name='retoure_statistics'),

    path('urlaubsantrag/', views.apply_for_vacation,
         name='urlaubsantrag'),

    path('view_applications/', views.view_vacation_applications,
         name='view_applications'),

    path('wiki/', views.wiki_view, name='wiki_index'),
    path('wiki/<str:category>/', views.wiki_category, name='category_detail'),
    path('wiki/<str:category>/<str:header>/',
          views.wiki_detail, name='wiki_detail'),

    path('external_links/', views.external_links, name='external_links'),

]

# https: // docs.djangoproject.com/en/4.2/howto/static-files/
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
