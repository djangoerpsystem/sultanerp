# from .validator_functions.date_validator import val_date_not_past
from django.core.cache import cache  # Importing cache
from django.contrib.auth.decorators import login_required
# https://docs.djangoproject.com/en/4.2/ref/contrib/admin/#the-staff-member-required-decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, FileResponse
from .models import *  # import all models
import datetime
import os, json, csv, io
import requests  # for the Bayern Public Holidays JSON API import requests:
from django.conf import settings
from .forms import UploadCSVForm, VacationApplicationForm, InventoryForm, DepositForm, MessageForm
from django.urls import get_resolver
from django.utils import timezone # for correct timezones
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator

# if i would develop my own calendar app or connect another one
from .my_calendar import generate_monthly_calendar, calendar_view

# only for testing purposes for the CRM module ( Webhook API ) !!!
from django.views.decorators.csrf import csrf_exempt

# custom made user_level checker utility function
from .utilities.check_view_permission import check_view_permission


########################################################################
#admin tools

@login_required
@staff_member_required
def admin_tools(request):
    tools = AdminTools.objects.all()
    context = {
        'admin_tools': tools
    }
    return render(request, 'admin_tools.html', context)

    
########################################################################
##Caching 
#Dynamic Text

def dynamic_text_context(request):
    dynamic_text = cache.get('dynamic_texts')

    if dynamic_text is None:
        # Fetch DynamicText objects & create dict
        dynamic_text = {
            text.title: text.text for text in DynamicText.objects.all()}

        # Cache dictionary for 1 hour
        cache.set('dynamic_text', dynamic_text, 3600)

    return {'dynamic_text': dynamic_text}


########################################################################
# Helper functions


def check_order_date(delivery_date):
    parsed_date = datetime.datetime.strptime(delivery_date, "%Y-%m-%d").date()
    return parsed_date < datetime.now().date()


def check_order_date_time(delivery_datetime):
    parsed_datetime = datetime.datetime.strptime(
        delivery_datetime, "%Y-%m-%dT%H:%M")
    return parsed_datetime < datetime.datetime.now()



def handle_order_date_warning(delivery_date):
    if check_order_date(delivery_date):
        order_date_alert = DynamicText.objects.filter(
            title="orderdatewarning").first()
        return True, order_date_alert.text if order_date_alert else "You cannot select a date which is earlier than today for any order!"
    return False, ""

def handle_order_sent():
    order_sent = DynamicText.objects.filter(title="order_sent").first()
    show_alert = bool(order_sent)
    message = order_sent.text if order_sent else "Order has been sent successfully!"
    return {"show_alert": show_alert, "message": message}

########################################################################


class CustomLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return '/erp'

# "https://docs.djangoproject.com/en/4.2/topics/auth/default/#django.contrib.auth.decorators.login_required"

@login_required
def dashboard_view(request):
    number_of_tasks = Task.objects.count()
    supplier_orders_count = SupplierOrders.objects.count()
    internal_orders_count = InternalOrders.objects.count()
    customer_orders_count = CustomerOrders.objects.count()
    retoure_orders_count = Retoure.objects.count()

   # crm_messages_count = CRMMessage.objects.count() # crm module not in development mode (after server deployment)
    new_messages_count = Message.objects.filter(
        recipient=request.user, is_read=False).count()
    message = Message.objects.filter(
        recipient=request.user, is_read=False
    ).order_by('-timestamp').first()

    today = date.today()
    all_tasks_for_today = RoutineTasks.objects.filter(due_date__date=today)
    tasks_for_today = Task.objects.filter(dueDate=today)

    user_level = request.user.user_level
    
    if user_level:
        if user_level.role == 'admin':
            calendar_entries = CalendarEntriesStore.objects.all()
        elif user_level.role == 'office':
            calendar_entries = CalendarEntriesOffice.objects.all()
        else:
            calendar_entries = []
    else:
        calendar_entries = []

    return render(request, 'dashboard.html', {
        'number_of_tasks': number_of_tasks,
        'supplier_orders_count': supplier_orders_count,
        'internal_orders_count': internal_orders_count,
        'customer_orders_count': customer_orders_count,
        'retoure_orders_count': retoure_orders_count,
        'message': message,
        # 'crm_messages_count': crm_messages_count, # crm module not in development mode (after server deployment)
        'new_messages_count': new_messages_count,
        'today': today,
        'tasks_for_today': tasks_for_today,
        'all_tasks_for_today': all_tasks_for_today,
        'calendar_entries': calendar_entries,
    })

########################################################################
#Messenger


@login_required
def messenger_view(request):
    current_user = request.user

    all_users_except_current = User.objects.exclude(id=current_user.id)

    sent_to_users = Message.objects.filter(sender=current_user).values_list(
        'recipient_id', flat=True).distinct()  # distinct method for unique list ofer users
    received_from_users = Message.objects.filter(
        recipient=current_user).values_list('sender_id', flat=True).distinct() 

    conversational_ids = set(sent_to_users) | set(received_from_users)
    conversational_users = User.objects.filter(id__in=conversational_ids)

    conversational_partners = []
    for user in conversational_users:
        unread_count = Message.objects.filter(
            sender=user, recipient=current_user, is_read=False).count()

        sent_messages = Message.objects.filter(
            sender=current_user, recipient=user).order_by('-timestamp')
        received_messages = Message.objects.filter(
            sender=user, recipient=current_user).order_by('-timestamp')

        if sent_messages and received_messages:
            latest_message = sent_messages[0] if sent_messages[
                0].timestamp > received_messages[0].timestamp else received_messages[0]
        elif sent_messages:
            latest_message = sent_messages[0]
        elif received_messages:
            latest_message = received_messages[0]
        else:
            latest_message = None

        latest_timestamp = latest_message.timestamp if latest_message else None

        conversational_partners.append({
            'user': user,
            'unread_count': unread_count,
            'latest_message_timestamp': latest_timestamp,
        })

    return render(request, "messenger/messenger.html", {
        'all_users_except_current': all_users_except_current,
        'conversational_partners': conversational_partners,
    })



@login_required
def messages_list(request):
    current_user = request.user
    sent_messages = Message.objects.filter(
        sender=current_user).order_by('-timestamp')
    received_messages = Message.objects.filter(
        recipient=current_user).order_by('-timestamp')

    user_ids = set()

    latest_timestamps = {}

    for message in sent_messages:
        if message.recipient_id not in user_ids:
            user_ids.add(message.recipient_id)
            latest_timestamps[message.recipient_id] = message.timestamp

    for message in received_messages:
        if message.sender_id not in user_ids or latest_timestamps[message.sender_id] < message.timestamp:
            user_ids.add(message.sender_id)
            latest_timestamps[message.sender_id] = message.timestamp

    other_users = User.objects.filter(pk__in=user_ids)

    conversations = [
        {
            'recipient': user,
            'latest_message_timestamp': latest_timestamps[user.pk]
        }
        for user in other_users
    ]

    return render(request, 'messenger/messages_list.html', {'conversations': conversations})


@login_required
def conversation(request, recipient_id):
    current_user = request.user
    recipient = User.objects.get(pk=recipient_id)

    messages_sent_by_current_user = Message.objects.filter(
        sender=current_user, recipient=recipient)
    messages_received_by_current_user = Message.objects.filter(
        sender=recipient, recipient=current_user)

    all_messages = messages_sent_by_current_user | messages_received_by_current_user
    all_messages = all_messages.order_by('timestamp')
    all_messages.filter(is_read=False).update(is_read=True)

    return render(request, 'messenger/conversation.html', {'recipient': recipient, 'messages': all_messages})


@login_required
def send_message(request, recipient_id=None):
    recipient = User.objects.get(pk=recipient_id) if recipient_id else None

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            recipient_id = request.POST.get('recipient')
            recipient = User.objects.get(
                pk=recipient_id)  
            Message.objects.create(sender=request.user,
                                   recipient=recipient, content=content)
            return redirect('conversation', recipient_id=recipient_id)
    else:
        form = MessageForm()

    # exclude the current user
    users = User.objects.exclude(pk=request.user.id)
    return render(request, 'messenger/send_message.html', {'form': form, 'recipient': recipient, 'users': users})


@login_required
def send_message_no_id(request):
    recipient_id = request.GET.get(
        'recipient_id', request.POST.get('recipient_id'))
    # "https://docs.djangoproject.com/en/4.2/topics/http/shortcuts/#get-object-or-404"
    recipient = get_object_or_404(User, pk=recipient_id)

    messages_sent_by_current_user = Message.objects.filter(
        sender=request.user, recipient=recipient)
    messages_received_by_current_user = Message.objects.filter(
        sender=recipient, recipient=request.user)
    all_messages = messages_sent_by_current_user | messages_received_by_current_user
    all_messages = all_messages.order_by('timestamp')

    all_messages.filter(is_read=False).update(is_read=True)

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            Message.objects.create(sender=request.user,
                                   recipient=recipient, content=content)

            all_messages = messages_sent_by_current_user | messages_received_by_current_user
            all_messages = all_messages.order_by('timestamp')
    else:
        form = MessageForm()

    return render(request, 'messenger/send_message.html', {
        'form': form,
        'recipient': recipient,
        'previous_messages': all_messages
    })



########################################################################
#CRM

@csrf_exempt #only in development, in production i have to solve the csrf somhow while using json payload
@login_required
def handle_webhook(request):
    if request.method == 'POST':
        # json.loads() https://www.w3schools.com/python/python_json.asp - converts from JSON to Python dictionary
        payload = json.loads(request.body)
        email = payload.get('contact.Email[0]')
        phone = payload.get('contact.Phone[1]')
        field1 = payload.get('field:comp-l9bskj5j')
        field2 = payload.get('field:comp-l9bsqtp6')
        field3 = payload.get('field:comp-kf5bsqi0')
        form_name = payload.get('form-name')

        webhook_data = WebhookData(
            email=email,
            phone=phone,
            field1=field1,
            field2=field2,
            field3=field3,
            form_name=form_name
        )
        webhook_data.save()

        return HttpResponse(status=200)

    return HttpResponse(status=405)


@csrf_exempt
@login_required
def crm_view(request):

    inbox_items = WebhookData.objects.filter(status="Inbox")
    in_progress_items = WebhookData.objects.filter(status="In Progress")
    done_items = WebhookData.objects.filter(status="Done")
    archive_items = WebhookData.objects.filter(status="Archive")

    context = {
        "inbox_items": inbox_items,
        "in_progress_items": in_progress_items,
        "done_items": done_items,
        "archive_items": archive_items,
    }

    return render(request, "crm/crm.html", context)


@login_required
def update_crm_status(request):
    if request.method == 'POST':
        item_id = request.POST.get('id')
        new_status = request.POST.get('status')

        item = WebhookData.objects.get(id=item_id)
        item.status = new_status
        item.save()

        return HttpResponse("Status updated successfully!")


@csrf_exempt  # only in development, in production i have to solve the csrf somhow while using json payload
@login_required
def webhook_view(request):

    if request.method != "POST":
        HttpResponse("Error, invalid method", status = 405)

    try:
        json_data = json.loads(request.body)

        id = json_data["data"].get("id", None)
        email = json_data["data"].get("contact.Email[0]", '')
        phone = json_data["data"].get("contact.Phone[1]", '')
        field1 = json_data["data"].get("field:comp-l9bskj5j", '')
        field2 = json_data["data"].get("field:comp-l9bsqtp6", '')
        field3 = json_data["data"].get("field:comp-kf5bsqi3", '')
        field4 = json_data["data"].get("field:comp-kf5bsqi0", '')
        form_name = json_data["data"].get("form-name", '')

        webhook_data = WebhookData(
            id=id,
            email=email,
            phone=phone,
            field1=field1,
            field2=field2,
            field3=field3,
            field4=field4,
            form_name=form_name,
            status="Inbox"  # default status when a new entry is created
        )
        webhook_data.save()

        return HttpResponse(status=200)

    except Exception:  # "https://docs.python.org/3/tutorial/errors.html#handling-exceptions"
        return HttpResponse(content=f"Error: {str(Exception)}", status=400)
    

########################################################################
#csv


@login_required
def upload_csv_internal_products(request):
    uploader = "Internal"
    success_msg = None

    if request.method == 'POST':
        form = UploadCSVForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            csv_file.readline()
            reader = csv.reader(line.decode() for line in csv_file) 
            for row in reader:
                InternalProducts.objects.create(
                    posNr=row[0],
                    title=row[1],
                    category=row[2],
                )
            success_msg = 'Upload successful'

    else:
        form = UploadCSVForm()
    return render(request, 'upload.html', {'form': form, 'uploader': uploader, 'success_msg': success_msg})


@login_required
def upload_csv_supplier_products(request):
    uploader = "Supplier"
    success_msg = None

    if request.method == 'POST':
        form = UploadCSVForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            csv_file.readline()  # Skip header
            reader = csv.reader(line.decode() for line in csv_file)
            for row in reader:
                unit_instance, created = MeasureUnits.objects.get_or_create(
                    units=row[2])  # to check for duplicate before creating new object "https://docs.djangoproject.com/en/4.2/ref/models/querysets/#get-or-create"

                product = SuppliersProduct.objects.create(
                    artNr=row[0],
                    title=row[1],
                    unit=unit_instance,
                    inhalt=row[3],
                )

                supplier_names = row[4].split(';')
                for name in supplier_names:
                    supplier_instance, created = Supplier.objects.get_or_create(
                        title=name.strip())
                    product.suppliers.add(supplier_instance)

            success_msg = 'Supplier Product Upload successful'

    else:
        form = UploadCSVForm()

    return render(request, 'upload.html', {'form': form, 'uploader': uploader, 'success_msg': success_msg})


########################################################################
#CakeID


@login_required
def get_cake_id(request):
    user = request.user

    if request.method == "POST":
        cake_price = request.POST.get('cakePrice', '0.00')
        quittung = request.POST.get('quittung')
        order_date = request.POST.get('orderdate')
        ordertype = request.POST.get('ordertype')

        if cake_price == '':
            cake_price = '0.00'

        if quittung == '':
            messages.error(request, 'quittung cannot be blank')
            return render(request, 'orders/get_cake_id.html')

        cake_price = float(cake_price)

        # Save the order date along with other data
        new_id = TortenBestellungsID(
            cakePrice=cake_price, quittung=quittung, orderDate=order_date,
            ordertype=ordertype, user=user)

        new_id.save()

        if ordertype == "delivery":
            CalendarEntriesStore.objects.create(
                termin=f"Cake Order - date: {order_date}",
                date=order_date,
                label="Delivery",
                user_level_id=3  
            )

        return redirect('cake_order')

    return render(request, 'orders/get_cake_id.html')


@login_required
def cake_order(request):
    # use the user_level checker utility function check_view_permisison
    if check_view_permission(request.user, 0,3):
        orders = TortenBestellungsID.objects.all().order_by('-id')
        return render(request, 'orders/orders.html', {'orders': orders})
    else:
        return render(request, 'orders/orders.html')


########################################################################
#Orders (Internal order, Customer order, Supplier order)

@login_required
def orders_view(request):
    context = {}

### before using user_level checker utility function check_view_permisison ###
    # user_role_hierarchy = request.user.user_level.hierarchy
    # context['user_level'] = user_role_hierarchy
    # if 0 <= user_role_hierarchy <= 3:
### before using user_level checker utility function check_view_permisison ###

    if check_view_permission(request.user,0,3):
        supplier_orders = SupplierOrders.objects.all().order_by('-id')
        internal_orders = InternalOrders.objects.all().order_by('-id')
        customer_orders = CustomerOrders.objects.all().order_by('-id')
        show_orders_list = request.resolver_match.url_name == 'orders_view' #and 0 <= user_role_hierarchy <= 3 # before check_view_permission utiltiy function
        context.update({
            'show_orders_list': show_orders_list,
            'supplier_orders': supplier_orders,
            'internal_orders': internal_orders,
            'customer_orders': customer_orders
        })

    return render(request, 'orders/orders.html', context)


#internal_orders

@login_required
def internal_orders(request):
    categories = InternalProducts.objects.values_list(
        'category', flat=True).distinct()
    branches = Store.objects.all()

    selected_category = request.POST.get('category')
    selected_branch = request.POST.get('branch')
    selected_date = request.POST.get('delivery_date', '')

    if selected_branch:
        selected_branch = int(selected_branch)

    if request.method == 'POST':
        action_type = request.POST.get('action_type')

        # Category Filter
        if action_type == "filter":
            internal_products = InternalProducts.objects.filter(
                category=selected_category) if selected_category else InternalProducts.objects.all()

        # Order Creation
        elif action_type == "order":
            product_ids = request.POST.getlist('product_ids')
            branch_id = selected_branch
            delivery_date = selected_date


            amounts = [int(request.POST.get(
                f'amounts_{product_id}') or 0) for product_id in product_ids]


            if any(amounts):  
                try:
                    order_amount = ",".join(map(str, amounts))
                    internal_order = InternalOrders.objects.create(
                        orderAmount=order_amount,
                        branch_id=branch_id,
                        orderDate=delivery_date,
                    )
                    for product_id in product_ids:
                        product = InternalProducts.objects.get(id=product_id)
                        internal_order.products.add(product)

                    return redirect('internal_order_detail', order_id=internal_order.id)
                except Exception:
                    messages.error(request, f"Error: {str(Exception)}")


        if 'internal_products' not in locals():
            internal_products = InternalProducts.objects.all()
    else:  # If GET request
        print("All Categories")
        internal_products = InternalProducts.objects.all()

    return render(request, 'orders/internal_orders.html', {
        'branches': branches,
        'categories': categories,
        'selected_category': selected_category,
        'selected_branch': selected_branch,
        'selected_date': selected_date,
        'internal_products': internal_products,
    })


@login_required
@staff_member_required
def internal_order_detail(request, order_id):

    try:
        order = InternalOrders.objects.get(pk=order_id)
    except InternalOrders.DoesNotExist:
        print(request, "Order not found!")
        return redirect('internal_orders')

    order = InternalOrders.objects.get(pk=order_id)
    products = order.products.all()
    order_amounts = order.orderAmount.split(',') #split for saving the order amounts in one row of the column, instead of every product and its order in new rows 

    order_amounts = [int(amount) for amount in order_amounts]

    total_order_amount = sum(order_amounts)

    # only  products > 0
    # zip "https://www.w3schools.com/python/ref_func_zip.asp" join iterable object (products and their amounts in one order) 
    product_order_amounts = [(product, amount) for product, amount in zip(
        products, order_amounts) if amount > 0]

    return render(request, 'orders/internal_order_detail.html', {
        'order': order,
        'products': product_order_amounts,
        'orderDate': order.orderDate,
        'total_order_amount': total_order_amount,
    })



@login_required
@staff_member_required
def internal_orders_list_view(request):
    if check_view_permission(request.user, 0, 3):
        all_internal_orders = InternalOrders.objects.all().order_by('-id') # desc order
        return render(request, 'orders/internal_orders_list.html', {'all_internal_orders': all_internal_orders,})
    else:
        return render(request, 'orders/internal_orders_list.html')

#customer_orders

@login_required
def customer_orders(request):
    categories = InternalProducts.objects.values_list(
        'category', flat=True).distinct()
    branches = Store.objects.all()

    selected_category = request.POST.get('category')
    selected_branch = request.POST.get('branch') if request.POST.get(
        'order_type', 'pickup') != "delivery" else None
    selected_date = request.POST.get('delivery_date', '')

    products = InternalProducts.objects.all()  

    if request.method == 'POST':
        action_type = request.POST.get('action_type')

        if action_type == "filter":
            products = InternalProducts.objects.filter(
                category=selected_category) if selected_category else InternalProducts.objects.all()

        elif action_type == "order":
            if check_order_date_time(selected_date):
                messages.error(
                    request, "The selected order date and time is in the past!")
                return render(request, 'orders/customer_orders.html', {
                    'branches': branches,
                    'categories': categories,
                    'selected_category': selected_category,
                    'selected_branch': selected_branch,
                    'selected_date': selected_date,
                    'internal_products': products,
                    'order_type': request.POST.get('order_type', 'pickup')
                })

            customer_name = request.POST.get('customer_name', '')
            customer_tel = request.POST.get('customer_tel', '')
            quittung_value = request.POST.get('quittung', None)
            paid_status = True if request.POST.get(
                'paid') == 'on' and quittung_value else False

            product_ids = request.POST.getlist('product_ids')
            amounts = [request.POST.get(
                f'amounts_{product_id}') for product_id in product_ids]

            products_with_amounts = {product_id: amt for product_id, amt in zip(
                product_ids, amounts) if amt and float(amt) > 0}

            total_amounts = ','.join(products_with_amounts.values())
            total_price_from_form = float(request.POST.get(
                'total_price')) if request.POST.get('total_price') else None

            delivery_address = request.POST.get(
                'delivery_address', '') if selected_branch is None else None

            try:
                customer_order = CustomerOrders.objects.create(
                    customerName=customer_name,
                    customerTel=customer_tel,
                    delivery_address=delivery_address,
                    totalAmounts=total_amounts,
                    quittung=quittung_value if quittung_value else None,
                    paid=paid_status,
                    total_price=total_price_from_form,
                    orderDate=selected_date,
                    branch_id=selected_branch
                )

                for product_id in products_with_amounts.keys():
                    product = InternalProducts.objects.get(id=product_id)
                    customer_order.products.add(product)

                return redirect('customer_order_detail', order_id=customer_order.id)

            except Exception:
                messages.error(request, f"Error: {str(Exception)}")

    return render(request, 'orders/customer_orders.html', {
        'branches': branches,
        'categories': categories,
        'selected_category': selected_category,
        'selected_branch': selected_branch,
        'selected_date': selected_date,
        'internal_products': products,
        'order_type': request.POST.get('order_type', 'pickup')
    })




@login_required
@staff_member_required
def customer_order_detail(request, order_id):
    order = get_object_or_404(CustomerOrders, id=order_id)
    product_names = [product.title for product in order.products.all()]
    amounts = order.totalAmounts.split(",") if order.totalAmounts else []
    product_amounts = zip(product_names, amounts)

    return render(request, 'orders/customer_order_detail.html', {
        'order': order,
        'product_amounts': product_amounts,
    })


@login_required
@staff_member_required
def customer_orders_list_view(request):

    if check_view_permission(request.user, 0,3):
        all_customer_orders = CustomerOrders.objects.all().order_by('-id')
        return render(request, 'orders/customer_orders_list.html', {
        'all_customer_orders': all_customer_orders})
    else:
        return render(request, 'orders/customer_orders_list.html')

#supplier_orders

@login_required
def supplier_orders(request):
    categories = Category.objects.all()
    suppliers = Supplier.objects.all()
    branches = Store.objects.all()
    products = []

    selected_category = None
    selected_supplier = None
    delivery_date = None

    all_supplier_orders = SupplierOrders.objects.all()  

    if request.method == "POST":
        action_type = request.POST.get('action_type', None)

        if action_type == "filter":
            selected_category = request.POST.get('category', None)
            selected_supplier = request.POST.get('supplier', None)

            if selected_category:
                selected_category_instance = Category.objects.get(
                    name=selected_category)
                suppliers = suppliers.filter(categories=selected_category_instance)

            if selected_supplier:
                selected_supplier_instance = Supplier.objects.get(
                    id=selected_supplier)
                products = selected_supplier_instance.products.all()

        elif action_type == "order":
            selected_branch = request.POST.get('branch', None)

            selected_product_ids = request.POST.getlist('product_ids')
            product_amounts = {}
            for product_id in selected_product_ids:
                amount = request.POST.get(f'amounts_{product_id}') or '0'
                if int(amount) > 0:
                    product_amounts[product_id] = amount

            if not product_amounts:
                messages.error(
                    request, "Please input at least one product amount!")
                return redirect('supplier_orders')

            amounts_string = ','.join(product_amounts.values())
            supplier_id = request.POST.get('selected_supplier', None)
            supplier_instance = None
            if supplier_id:
                try:
                    supplier_instance = Supplier.objects.get(id=supplier_id)
                except Supplier.DoesNotExist:
                    messages.error(request, "Invalid supplier selected!")
                    return redirect('supplier_orders')

            new_order = SupplierOrders.objects.create(
                productAmounts=amounts_string,
                delivery_date=request.POST.get('delivery_date', None),
                ordering_person=request.user,
                supplier=supplier_instance,
                branch_id=selected_branch
            )

            new_order.products.set(product_amounts.keys())
            return redirect('supplier_order_detail', order_id=new_order.id)


    context = {
        'categories': categories,
        'suppliers': suppliers,
        'products': products,
        'selected_category': selected_category,
        'selected_supplier': selected_supplier,
        'branches': branches,
        'all_supplier_orders': all_supplier_orders
    }

    return render(request, 'orders/supplier_orders.html', context)


@login_required
@staff_member_required
def supplier_orders_list_view(request):

    context = {}
    if check_view_permission(request.user, 0,3):
        all_supplier_orders = SupplierOrders.objects.all().order_by('-id')
        context = {'all_supplier_orders': all_supplier_orders,}

    return render(request, 'orders/supplier_orders_list.html', context)


@login_required
@staff_member_required
def supplier_order_detail(request, order_id):
    try:
        order = SupplierOrders.objects.get(pk=order_id)
    except SupplierOrders.DoesNotExist:
        messages.error(request, "Order not found!")
        return redirect('supplier_orders')

    products = [(product, order.get_product_amount(product.id))
                for product in order.products.all() if order.get_product_amount(product.id) > 0]
    total_order_amount = sum([amount for _, amount in products])

    supplier = order.supplier

    return render(request, 'orders/supplier_orders_detail.html', {
        'order': order,
        'products': products,
        'orderDate': order.delivery_date,
        'total_order_amount': total_order_amount,
        'supplier': supplier,
    })


########################################################################
# Retoure


@login_required
def retoure_view(request):
    categories = InternalProducts.objects.values_list(
        'category', flat=True).distinct()
    branches = Store.objects.all()

    selected_category = request.POST.get('category')

    products = InternalProducts.objects.all()

    if request.method == 'POST':
        action_type = request.POST.get('action_type')

        if action_type == "filter":
            products = InternalProducts.objects.filter(
                category=selected_category) if selected_category else InternalProducts.objects.all()

        elif action_type == "retoure":
            branch_id = request.POST.get('branch')
            branch = Store.objects.get(pk=branch_id)

            product_ids = request.POST.getlist('product_ids')
            amounts = [request.POST.get(
                f'amounts_{product_id}') for product_id in product_ids]

            new_retoure = Retoure(branch=branch, timeStamp=datetime.datetime.now())
            new_retoure.orderAmount = ','.join(amounts)
            new_retoure.save()

            # "https://www.w3schools.com/django/ref_lookups_in.php" -> __in lookup in itarable
            selected_products = InternalProducts.objects.filter(id__in=product_ids)
            new_retoure.products.add(*selected_products) # add() method "https://docs.djangoproject.com/en/4.2/ref/models/relations"

            return redirect('retoure_list')

    return render(request, 'orders/retoure.html', {
        'branches': branches,
        'categories': categories,
        'selected_category': selected_category,
        'internal_products': products,
    })


@login_required
@staff_member_required
def retoure_detail(request, order_id):

    try:
        retoure = Retoure.objects.get(pk=order_id)
    except Retoure.DoesNotExist:
        print(request, "Retoure not found!")
        return redirect('retoure')

    retoure = Retoure.objects.get(pk=order_id)
    products = retoure.products.all()
    retoure_amounts = retoure.orderAmount.split(',')

    retoure_amounts = [int(amount) for amount in retoure_amounts if amount]

    total_retoure_amount = sum(retoure_amounts)

    # zip products + retoure amounts, but only include products withthout zero amounts
    product_retoure_amounts = [(product, amount) for product, amount in zip(
        products, retoure_amounts) if amount > 0]

    return render(request, 'orders/retoure_detail.html', {
        'retoure': retoure,
        'products': product_retoure_amounts,
        'timeStamp': retoure.timeStamp,
        'total_retoure_amount': total_retoure_amount,
    })


@login_required
@staff_member_required
def retoure_list_view(request):
    if check_view_permission(request.user, 0,3):
        all_retoures = Retoure.objects.all().order_by('-timeStamp')

        return render(request, 'orders/retoure_list.html', {
        'all_retoures': all_retoures})
    else:
        return render(request, 'orders/retoure_list.html')


########################################################################
#Inventory


@login_required
def inventory_view(request):

    allow_add_item = check_view_permission(request.user, 0, 3)

    if request.method == 'POST' and allow_add_item: 
        form = InventoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventory')
    else:
        form = InventoryForm()

    order_by = request.GET.get('order_by', 'section')
    direction = request.GET.get('direction', 'asc')
    if direction == 'desc':
        order_by = '-' + order_by

    inventory = Inventory.objects.all().order_by(order_by)

    context = {
        'inventory': inventory,
        'form': form,
        'allow_add_item': allow_add_item
    }

    return render(request, 'inventory.html', context)



########################################################################
#Deposit


@login_required
def deposit_view(request):
    if request.method == 'POST':
        deposit_form = DepositForm(request.POST)
        if deposit_form.is_valid():
            deposit = deposit_form.save(commit=False)
            deposit.user = request.user
            deposit.save()

            if request.user.user_level.hierarchy <= 2:
                return redirect('deposit_list')
            elif request.user.user_level.hierarchy >= 3:
                return redirect('deposit')

    else:
        deposit_form = DepositForm()

    context = {
        'deposit_form': deposit_form
    }

    return render(request, 'deposit/deposit.html', context)


@login_required
@staff_member_required
def deposit_list_view(request):
    deposits = Deposit.objects.all().order_by(
        '-timestamp')
    context = {
        'deposits': deposits,
    }
    return render(request, 'deposit/deposit_list.html', context)


################################################################################
#Document Management


@login_required
def document_management_view(request):
    media_root = settings.MEDIA_ROOT
    folders = {}
    exclude_folders = ["images", "wiki"]

    for root, dirs, files in os.walk(media_root):
        for dir in dirs:
            if dir not in exclude_folders:
                folder_content = os.listdir(os.path.join(root, dir))
                # Filter out .DS_Store files
                folder_content = [
                    f for f in folder_content if not f.endswith('.DS_Store')]
                folders[dir] = folder_content

    selected_folder_name = request.GET.get('folder_name', None)
    selected_folder_content = folders.get(
        selected_folder_name, []) if selected_folder_name else []

    return render(request, 'document_management.html', {
        'folders': folders,
        'selected_folder_content': selected_folder_content,
        'selected_folder_name': selected_folder_name
    })



@login_required
def folder_content_view(request, folder_name, document_filename):
    document_path = os.path.join(
        settings.MEDIA_ROOT, folder_name, document_filename)

    if os.path.exists(document_path):
        # "https://docs.djangoproject.com/en/4.2/ref/request-response/#fileresponse-objects"
        response = FileResponse(open(document_path, 'rb'),
                                content_type='application/pdf')
        response['Content-Disposition']
        return response
    else:
        return render(request, 'document_management.html')


################################################################
#External Links

@login_required
def external_links(request):
    user_hierarchy = request.user.user_level.hierarchy if request.user.user_level else None

    if user_hierarchy is None:
        print("You don't have permission to view this page.")
        return redirect('dashboard')

    # Fetch all links where link's user_level hierarchy is greater or equal to user's hierarchy.
    links = ExternalLinks.objects.filter(
        user_level__hierarchy__gte=user_hierarchy)

    context = {
        'links': links,
    }
    return render(request, "external_links.html", context)




################################################################################
#Task Management


def task_list(request):
    # If user is staff/admin, show all open tasks, otherwise show only tasks where they're responsible
    if request.user.is_staff:
        tasks = Task.objects.filter(status='open')
    else:
        tasks = Task.objects.filter(
            status='open', responsiblePerson=request.user)

    show_done_tasks = request.GET.get('show_done_tasks', 'false') == 'true'

    if show_done_tasks:
        # If user is staff/admin, show all done tasks, otherwise show only tasks where they're responsible
        if request.user.is_staff:
            done_tasks = Task.objects.filter(status='done')
        else:
            done_tasks = Task.objects.filter(
                status='done', responsiblePerson=request.user)
    else:
        done_tasks = []

    return render(request, 'tasks/task_list.html', {'tasks': tasks, 'done_tasks': done_tasks, 'show_done_tasks': show_done_tasks})

@login_required
def mark_task_done(request, task_id):
    task = Task.objects.get(pk=task_id)
    task.status = 'done'
    task.save()
    return redirect('task_list')


@login_required
def mark_task_open(request, task_id):
    task = Task.objects.get(pk=task_id)
    task.status = 'open'
    task.save()
    return redirect('task_list')


@login_required
def add_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        due_date = request.POST.get('due_date')
        responsible_person_id = request.POST.get('responsible_person')
        status = request.POST.get('status')
        description = request.POST.get('description')
        priority = request.POST.get('priority')
        category = request.POST.get('category')

        responsible_person = User.objects.get(
            id=responsible_person_id) if responsible_person_id else None

        task = Task(
            title=title,
            dueDate=due_date,
            responsiblePerson=responsible_person,
            status=status,
            description=description,
            priority=priority,
            category=category
        )
        task.save()
        return redirect('task_list')

    users = User.objects.all()
    return render(request, 'tasks/add_task.html', {'users': users})


@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.method == 'POST':
        title = request.POST.get('title')
        due_date = request.POST.get('due_date')
        responsible_person_id = request.POST.get('responsible_person')
        status = request.POST.get('status')
        description = request.POST.get('description')
        priority = request.POST.get('priority')
        category = request.POST.get('category')

        responsible_person = User.objects.get(
            id=responsible_person_id) if responsible_person_id else None

        task.title = title
        task.dueDate = due_date
        task.responsiblePerson = responsible_person
        task.status = status
        task.description = description
        task.priority = priority
        task.category = category

        task.save()
        return redirect('task_list')

    users = User.objects.all()
    context = {
        'task': task,
        'users': users,
        'edit_mode': True
    }
    return render(request, 'tasks/add_task.html', context)



@login_required
def task_detail(request, task_id):
    task = Task.objects.filter(id=task_id).first()
    context = {
        'task': task,
    }
    return render(request, 'tasks/task_detail.html', context)


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect('task_list')


########################################################################
#Logs

def show_logs(request):
    context = {}

    # "https://docs.djangoproject.com/en/4.2/ref/urlresolvers/#django.urls.ResolverMatch.url_name"
    if request.resolver_match.url_name == 'routine_task_logs':
        context['logs'] = Logs.objects.all()

    elif request.resolver_match.url_name == 'login_logs':
        context['logs'] = LoginLog.objects.all()

    return render(request, 'stats/logs.html', context)


@login_required
@staff_member_required
def statistics(request):
    context = {}

    now = datetime.datetime.now()
    current_year = now.year
    current_month = now.month

    if request.resolver_match.url_name == 'cake_order_statistics':
        orders = TortenBestellungsID.objects.filter(
            orderDate__year=current_year, orderDate__month=current_month)
        total_orders = orders.count()
        total_income = sum([order.cakePrice for order in orders])

        context['total_orders'] = total_orders
        context['total_income'] = total_income

    elif request.resolver_match.url_name == 'retoure_statistics':
        context['message'] = "Placeholder data for retoure statistics."

    return render(request, 'stats/statistics.html', context)


################################################################
#Routine Tasks

def add_routine(request):
    if request.method == 'POST':
        title = request.POST['title']
        user_id = request.POST['user']
        due_date = request.POST['due_date']
        store_id = request.POST['store']
        frequency_id = request.POST['frequency'] or None
        routines_ids = request.POST.getlist('routine')
        place_id = request.POST['place'] or None

        routine_task = RoutineTasks(
            title=title,
            user=User.objects.get(id=user_id),
            due_date=due_date,
            store=Store.objects.get(id=store_id),
            frequency=Frequency.objects.get(
                id=frequency_id) if frequency_id else None,
            place=Places.objects.get(id=place_id) if place_id else None,
        )
        routine_task.save()
        routine_task.routines.set(
            [Routines.objects.get(id=r_id) for r_id in routines_ids])

        return redirect('/')

    context = {
        'users': User.objects.all(),
        'stores': Store.objects.all(),
        'frequencies': Frequency.objects.all(),
        'routines': Routines.objects.all(),
        'places': Places.objects.all(),
    }
    return render(request, 'routines/addroutine.html', context)


@login_required
def routines_and_daily_list(request):
    today = date.today()
    all_tasks_for_today = RoutineTasks.objects.filter(due_date__date=today)
    routines = RoutineTasks.objects.all()

    context = {
        'all_tasks_for_today': all_tasks_for_today,
        'routines': routines,
    }
    return render(request, 'routines/routine_list.html', context)


@login_required
def daily_routines_detail(request, task_id):
    task = get_object_or_404(RoutineTasks, id=task_id)
    all_routines_done = True

    if request.method == "POST":
        for routine in task.routines.all():
            checkbox_name = f"routine_{routine.id}"
            if checkbox_name in request.POST:
                log_entry = Logs(
                    user=request.user,
                    log=routine.routines,
                    done=True
                )
                log_entry.save()
            else:
                all_routines_done = False

        if all_routines_done:
            task.completed = True
            task.save()

        return redirect('routine_list')

    context = {
        'task': task
    }
    return render(request, 'routines/routine_detail.html', context)


# before there was 1 view function for daily routines but i decided to spereate the concerns and therefore created 2 views for each operation

################################################################
#Calendar






################################################################
#Vacation

def get_net_vacation_days(start_date, end_date, public_holidays):
    total_days = (end_date - start_date).days + 1
    net_days = 0

    for single_date in (start_date + datetime.timedelta(n) for n in range(total_days)):
        # Check if the day is not a weekend and not a public holiday
        if single_date.weekday() != 6 and single_date not in public_holidays:
            net_days += 1

    return net_days

@login_required
def apply_for_vacation(request):
    user = request.user
    latest_record = VacationRecord.objects.filter(user=user).last()
    vacation_days = VacationDays.objects.filter(user=user).first()

    if not vacation_days:
        aktuelle_urlaubstage = 0
    elif latest_record:
        aktuelle_urlaubstage = latest_record.current_balance - vacation_days.days_used
    else:
        aktuelle_urlaubstage = vacation_days.days_added - vacation_days.days_used

    if request.method == "POST":
        form = VacationApplicationForm(request.POST)
        if form.is_valid():
            vacation_application = form.save(commit=False)
            vacation_application.user = user
            vacation_application.save()

            if vacation_application.free_days > aktuelle_urlaubstage:
                print(
                    request, 'Du hast nicht genug Urlaubstage verfügbar.')
                vacation_application.delete()
            else:
                messages.success(request, 'Vacation applied successfully!')
                return redirect('/view_applications')
        else:
                print(request, 'Please fill in the form correctly.')
    else:
        form = VacationApplicationForm()

    context = {
        'form': form,
        'company_name': 'Münchner Systemgastronomie GmbH',
        'current_date': date.today(),
        'aktuelle_urlaubstage': aktuelle_urlaubstage,
        'public_holidays': get_public_holidays(date.today().year),
        'current_year': date.today().year
    }
    return render(request, 'forms/urlaubsantrag.html', context)


@login_required
def view_vacation_applications(request):
    applications_list = VacationApplication.objects.all().order_by('-id')
    paginator = Paginator(applications_list, 20)
    page_number = request.GET.get('page')
    applications = paginator.get_page(page_number)
    #this broked somehow during later development
    #is_admin = request.user.user_level == 'admin'
    is_admin = request.user.user_level.role == 'admin'


    public_holidays = get_public_holidays(datetime.date.today().year)

    if request.method == "POST" and is_admin:
        for app in applications_list:
            net_days = app.vacation_days
            checkbox_name = f"approve_{app.id}"
            was_approved = app.approval == "yes"


            if checkbox_name in request.POST and not was_approved:
                app.approval = "yes"
                app.save()

                latest_record = VacationRecord.objects.filter(user=app.user).last()


                vacation_days = VacationDays.objects.filter(user=app.user).first()
                if not vacation_days or vacation_days.days_added is None:
                    raise Exception("{{dynamic_texts.vacationdays_error.text}}")
                days_added = vacation_days.days_added

                current_balance = latest_record.current_balance if latest_record else days_added
                new_balance = current_balance - net_days

                record = VacationRecord(
                    user=app.user,
                    days_changed=-net_days,
                    current_balance=new_balance,
                    reason=f"Vacation from {app.start_date} to {app.end_date}",
                )
                record.save()


            elif not checkbox_name in request.POST and was_approved:
                app.approval = "no"
                app.save()

                latest_record = VacationRecord.objects.filter(
                    user=app.user).last()
                current_balance = latest_record.current_balance if latest_record else (
                    VacationDays.objects.get(user=app.user).days_added if VacationDays.objects.get(
                        user=app.user) else 24
                )
                new_balance = current_balance + net_days

                record = VacationRecord(
                    user=app.user,
                    days_changed=net_days,
                    current_balance=new_balance,
                    reason=f"Revoked vacation from {app.start_date} to {app.end_date}",
                )
                record.save()

        return redirect('/view_applications')

    context = {
        'applications': applications,
        'is_admin': is_admin,
    }

    return render(request, 'forms/view_applications.html', context)


def get_public_holidays(year):
    url = f"https://get.api-feiertage.de/?states=by&years={year}"
    response = requests.get(url)

    if response.status_code != 200:
        return []

    holidays_data = response.json()

    holidays_in_bavaria = []

    for holiday_data in holidays_data['feiertage']:
        # Exclude Augsburger Friedensfest
        if holiday_data['fname'] == "Augsburger Friedensfest":
            continue
        if 'by' in holiday_data and holiday_data['by'] == '1':
            date_obj = datetime.datetime.strptime(
                holiday_data['date'], "%Y-%m-%d")

            holidays_in_bavaria.append({
                'date': date_obj,
                'title': holiday_data['fname']
            })


    return holidays_in_bavaria


################################################################
#Wiki


def wiki_view(request):
    categories = WikiCategory.objects.all()
    context = {
        'categories': categories
    }

    return render(request, 'wiki/index.html', context)


def wiki_category(request, category):
    category_obj = get_object_or_404(WikiCategory, category=category)
    
    wikis = Wiki.objects.filter(categories=category_obj)
    print(wikis)
    return render(request, 'wiki/wiki_category.html', {
        'category': category_obj,
        'wikis': wikis
    })


def wiki_detail(request, category, header):
    wiki = get_object_or_404(
        Wiki, categories__category=category, header=header)
    wiki_contents = wiki.contents.all()
    wiki_images = wiki.images.all()

    return render(request, 'wiki/wiki_content.html', {
        'wiki': wiki,
        'wiki_contents': wiki_contents,
        'wiki_images': wiki_images,
        'category': category
    })