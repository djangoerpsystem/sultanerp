from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone 
from django.contrib.auth import get_user_model
from datetime import timedelta, date, datetime
from django_resized import ResizedImageField


class Store(models.Model):
    branchTitle = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.branchTitle


class Roles(models.Model):
    role = models.CharField(max_length=20, null=True, blank=True)
    hierarchy = models.PositiveIntegerField(default=9)

    def __str__(self):
        return f"{self.hierarchy} - {self.role}"
    
    #https: // www.geeksforgeeks.org/meta-class - in -models-django/
    # for easier ordering in the models
    class Meta:
     ordering = ['hierarchy']


class User(AbstractUser):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    personal_nr = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    branch = models.ForeignKey(
        Store, on_delete=models.CASCADE, related_name="users", null=True, blank=True)

    user_level = models.ForeignKey(
        Roles, on_delete=models.CASCADE, related_name="users", null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    

class AdminTools(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    reference = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f" {self.title} | %URL {self.reference}"
    

class MeasureUnits(models.Model):

    UNIT_CATEGORY = [
        ("weight", "weight"),
        ("distance", "distance"),
        ("packaging", "packaging"),
        ("currency", "currency"),
    ]

    units = models.CharField(max_length=20, null=True, blank=True, unique=True)
    unit_category = models.CharField(max_length=20, choices=UNIT_CATEGORY)

    def __str__(self):
        return f"{self.units} - {self.unit_category}"
    

class Category(models.Model):
    name = models.CharField(max_length=25, unique=True)

    def __str__(self):
        return self.name
    

class DocumentData(models.Model):
    CATEGORY = [
        ("Forms", "Forms"),
        ("HACCP", "HACCP"),
        ("Wiki", "Wiki"),
        ("PersonalDocuments", "PersonalDocuments"),
        ("Branch", "Branch")
    ]

    category = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    filename = models.CharField(max_length=255)
    directory = models.CharField(max_length=255)
    filesize_mb = models.FloatField(max_length=255)
    creation_date = models.DateField()

    file_url = models.URLField(max_length=255)

    def __str__(self):
        return f"{self.title} - {self.filename}"


class WebhookData(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    field1 = models.CharField(max_length=255)
    field2 = models.CharField(max_length=255)
    field3 = models.CharField(max_length=255)
    field4 = models.CharField(max_length=255, default='')
    form_name = models.CharField(max_length=25)
    status = models.CharField(max_length=100, default="Inbox")

    def __str__(self):
        return (self.form_name + " " + str(self.id))


class CRMItem(models.Model):
    STATUS_CHOICES = [
        ("inbox", "Inbox"),
        ("in_progress", "In Progress"),
        ("done", "Done"),
        ("archive", "Archive")
    ]

    # You can use this to name or describe the CRM item
    title = models.CharField(max_length=255)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="inbox")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    # if you want to associate the CRM item with a user or other entities, add ForeignKey here

    def __str__(self):
        return self.title


class TortenBestellungsID(models.Model):
    timeStamp = models.DateTimeField(auto_now_add=True)
    cakePrice = models.FloatField(default=0.00)
    quittung = models.IntegerField(null=True)
    orderDate = models.DateField(default=None, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    ordertype = models.CharField(max_length=30)

    def __str__(self):
        # return f"{self} - {self.id} - {self.cakePrice}"
        return f"TortenBestellung - {self.id} - {self.cakePrice}"
    

########################################################################


class Supplier(models.Model):

    categories = models.ManyToManyField(Category)
    title = models.CharField(max_length=255)

    def __str__(self):
        categories = ", ".join(
            [category.name for category in self.categories.all()])
        return f"{self.id} | {self.title} | {categories}"
    

class SuppliersProduct(models.Model):

    artNr = models.CharField(max_length=255, default='', null=True, blank=True)
    title = models.CharField(max_length=255)
    suppliers = models.ManyToManyField(Supplier, related_name='products')
    unit = models.ForeignKey(
        MeasureUnits, on_delete=models.SET_NULL, null=True, blank=True)
    # Assuming this is an integer field
    inhalt = models.CharField(max_length=4,null=True, blank=True)


    def __str__(self):
        suppliers_str = ", ".join([str(supplier)
                                for supplier in self.suppliers.all()])
        return f"{self.id} - {self.title} ({self.inhalt} {self.unit})|| Lieferant: {suppliers_str}"

    
class SupplierOrders(models.Model):
    products = models.ManyToManyField(
        SuppliersProduct, through='SupplierOrderProduct')
    productAmounts = models.CharField(max_length=255, null=True, blank=True)
    order_time = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateField(default=None, null=True)
    ordering_person = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True)
    branch = models.ForeignKey(
        Store, on_delete=models.CASCADE, null=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        product_details = []
        for product in self.products.all():
            product_amount = self.get_product_amount(product.id)
            product_details.append(
                f"{product.title} (Amount: {product_amount})")
        products_str = ", ".join(product_details)
        return f"{self.id} - {products_str}"


    def get_product_amount(self, product_id):
        if not self.productAmounts:
            return 0

        amounts = self.productAmounts.split(',')
        products_ids = [p.id for p in self.products.all()]

        if product_id in products_ids:
            index = products_ids.index(product_id)
            if index < len(amounts):
                try:
                    return int(amounts[index])
                except ValueError:
                    return 0
        return 0


class SupplierOrderProduct(models.Model):
    order = models.ForeignKey(SupplierOrders, on_delete=models.CASCADE)
    product = models.ForeignKey(SuppliersProduct, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=0)



class InternalProducts(models.Model):
    CATEGORY = [
        ("Teigwaren", "Teigwaren"),
        ("Baklava", "Baklava"),
        ("Konditorei", "Konditorei"),
        ("Backstube", "Backstube"),
        ("Snacks", "Snacks"),
        ("Restaurant", "Restaurant"),
        ("Nachspeisen", "Nachspeisen")
    ]

    # all data comes from the POS Database, but filtered from category
    posNr = models.CharField(max_length=20, blank=True)
    title = models.CharField(max_length=50)
    category = models.CharField(max_length=255, blank=True, choices=CATEGORY)

    def __str__(self):
        return f"{self.posNr} - {self.title} - {self.category}"


class InternalOrders(models.Model):

    products = models.ManyToManyField(
        InternalProducts)
    orderAmount = models.CharField(max_length=255, null=True, blank=True)
    timeStamp = models.DateTimeField(auto_now_add=True)
    orderDate = models.DateField(default=date.today)

    branch = models.ForeignKey(Store, on_delete=models.CASCADE, null=True)

    def __str__(self):
        product_details = []
        for product in self.products.all():
            product_amount = self.get_product_amount(product.id)
            product_details.append(
                f"{product.title} (Amount: {product_amount})")
        products_str = ", ".join(product_details)
        return f"{self.id} - {products_str} - {self.orderAmount} - {self.timeStamp} - {self.orderDate}"

    def get_product_amount(self, product_id):
        if not self.orderAmount:
            return 0

        amounts = self.orderAmount.split(',')
        product_index = product_id - 1

        if product_index < len(amounts):
            try:
                return int(amounts[product_index])
            except ValueError:
                return 0
        else:
            return 0
        

class CustomerOrders(models.Model):
    products = models.ManyToManyField(InternalProducts)
    customerName = models.CharField(max_length=255)
    customerTel = models.CharField(max_length=50)
    totalAmounts = models.CharField(max_length=255, blank=True, null=True)
    timeStamp = models.DateTimeField(auto_now_add=True)
    orderDate = models.DateTimeField(blank=True, null=True)
    branch = models.ForeignKey(Store, on_delete=models.CASCADE, null=True, blank=True)
    delivery_address = models.CharField(max_length=255, blank=True, null=True)
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    paid = models.BooleanField(default=False)
    quittung = models.IntegerField(null=True, blank=True)
    

    def __str__(self):
        product_names = ', '.join(
            [product.title for product in self.products.all()])

        return f"ID: {self.id} - {self.orderDate} - {self.customerName} - Products: {product_names} - {self.totalAmounts}"

########################################################################
#Retour Management


class Retoure(models.Model):

    products = models.ManyToManyField(InternalProducts)
    orderAmount = models.CharField(max_length=255, null=True, blank=True)
    timeStamp = models.DateTimeField(auto_now_add=True)

    branch = models.ForeignKey(Store, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"Retoure from {self.branch} on {self.timeStamp}"

        
########################################################################
#Tasks


class Task(models.Model):
    STATUS = [
        ("open", "open"),
        ("done", "done")
    ]
    title = models.CharField(max_length=255)
    dueDate = models.DateField(null=True, blank=True)
    responsiblePerson = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    status = models.CharField(max_length=10, default='open', choices=STATUS)
    description = models.TextField(null=True, blank=True)
    priority = models.IntegerField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    category = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.title

################################################################
# inventory

class Storage(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    storagePlace = models.CharField(max_length=30)

    # Python property decorator
    @property
    def storedIn(self):
        return F"{self.store.branchTitle} - {self.storagePlace}"

    def __str__(self):
        return self.storedIn

class InventorySection(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Inventory(models.Model):
    section = models.ForeignKey(InventorySection, on_delete=models.CASCADE)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    boughtOn = models.DateField(null=True, blank=True)
    storedIn = models.ForeignKey(Storage, on_delete=models.CASCADE)
    value = models.IntegerField(null=True, blank=True)
    amount = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.id} - {self.section} - {self.category} - {self.name} - {self.boughtOn} - {self.storedIn} - {self.amount}"
    
 ################################################################
 #Deposit   

class DepositObject(models.Model):
    deposit = models.CharField(max_length=50, blank=True, null=True)
    value = models.DecimalField(
        decimal_places=2, blank=True, null=True, max_digits=4)

    def __str__(self):
        return f"{self.deposit}: {self.value}"


class Deposit(models.Model):
    deposit_object = models.ForeignKey(
        DepositObject, related_name="deposits", on_delete=models.PROTECT) # PROTECT dont want to loose data here because its customers money
    value = models.DecimalField(
        decimal_places=2, blank=True, null=True, max_digits=5)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    branch = models.ForeignKey(Store, on_delete=models.CASCADE, blank=True, null=True)
    customer_name = models.CharField(max_length=50, blank=True, null=True)
    customer_tel = models.CharField(max_length=50, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    paid_back = models.BooleanField(default=False, blank=True, null=True)
    paid_back_date = models.DateField(blank=True, null=True)

    def __str__(self):
        customer_name_available = self.customer_name if self.customer_name else ""
        format_timestamp = (
            self.timestamp + timedelta(hours=2)).strftime('%d.%m.%y, %H:%M')


        return f" (Pfand Nr: {self.id}) {format_timestamp} - {self.deposit_object.deposit} {self.value} € {customer_name_available}"

    # "https://learndjango.com/tutorials/django-slug-tutorial"
    def save(self, *args, **kwargs):
        # this allows the employee to fill in custom deposit amount (less or more then coming frmo the table 
        # (if euqal, then leave the form field emtpy, it fetchs from the table)
        if self.value is None:
            self.value = self.deposit_object.value
        super().save(*args, **kwargs)


################################################################    
#Message


class Message(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"From {self.sender.username} to {self.recipient.username} - {self.timestamp}"

################################################################


class VacationRecord(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="vacation_records")
    date_changed = models.DateTimeField(auto_now_add=True)
    days_changed = models.IntegerField()  # Can be positive or negative
    current_balance = models.PositiveIntegerField()
    reason = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.days_changed} days on {self.date_changed}"


class VacationApplication(models.Model):
    APPROVAL = [
        ("no", "no"),
        ("yes", "yes")
    ]

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    days_requested = models.PositiveIntegerField()
    free_days = models.PositiveIntegerField(null=True, blank=True)
    days_on_sunday = models.PositiveIntegerField(default=0)
    days_on_holiday = models.PositiveIntegerField(default=0)
    vacation_days = models.PositiveIntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    approval = models.CharField(
        max_length=20, choices=APPROVAL, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.days_requested = (self.end_date - self.start_date).days + 1

        public_holidays_in_range = PublicHoliday.objects.filter(
            date__range=[self.start_date, self.end_date])
        self.days_on_holiday = public_holidays_in_range.count()

        current_date = self.start_date
        sundays = 0
        while current_date <= self.end_date:
            if current_date.weekday() == 6:  # = Sundays
                sundays += 1
            current_date += timedelta(days=1)
        self.days_on_sunday = sundays

        self.free_days = self.days_on_sunday + self.days_on_holiday
        self.vacation_days = self.days_requested - self.free_days

        super().save(*args, **kwargs)


class VacationDays(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="manual_vacation_days")
    days_added = models.PositiveIntegerField(
        default=24)
    days_used = models.PositiveIntegerField(default=0)

    works_day = models.PositiveIntegerField(default=0, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.days_added - self.days_used} days left"


class PublicHoliday(models.Model):
    date = models.CharField(max_length=50)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.name} - {self.date}'
    

################################################################
#Routines


class Frequency(models.Model):
    frequency = models.TextField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.frequency
    
class RoutinesCategory(models.Model):
    category = models.TextField(max_length=25, blank=True, null=True)

    def __str__(self):
        return self.category

class Routines(models.Model):
    routines = models.TextField(max_length=100, blank=True, null=True)
    category = models.ForeignKey(RoutinesCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.routines + " (" + self.category.category + ") "

class Places(models.Model):
    places = models.TextField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.places
    

class RoutineTasks(models.Model):
    title = models.CharField(max_length=30)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    due_date = models.DateTimeField(blank=True, null=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    frequency = models.ForeignKey(
        Frequency, on_delete=models.SET_NULL, null=True, blank=True)
    routines = models.ManyToManyField(Routines)
    place = models.ForeignKey(
        Places, on_delete=models.SET_NULL, null=True, blank=True)
    
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Routine: {self.title} für {self.user.username} bei {self.place}"
    

class TaskFrequency(models.Model):
    routineTasks = models.ForeignKey(RoutineTasks, on_delete=models.CASCADE)
    frequency = models.ForeignKey(Frequency, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.routineTasks) + " " + "(" + str(self.frequency) + ")"
    
    
########################################################################
#Calendar

class CalendarEntriesStore(models.Model):
    termin = models.CharField(max_length=50, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    label = models.CharField(max_length=20, blank=True, null=True)
    user_level = models.ForeignKey(
        Roles, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return f"{self.termin} - date: {self.date} - time: {self.time}"
    

class CalendarEntriesOffice(models.Model):
    termin = models.CharField(max_length=50, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    label = models.CharField(max_length=20, blank=True, null=True)
    user_level = models.ForeignKey(
        Roles, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.termin} - date: {self.date} - time: {self.time}"

########################################################################
#Dynamic content {dynamic_texts.content.text} --> replace content with the one set in table DynamicText
# used together with preprocessor in utilities folder context_processors.py :)

class DynamicText(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()

    def __str__(self):
        return self.title

################################################################
#Wiki

class WikiCategory(models.Model):
    category = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.category}"

class WikiContent(models.Model):
    title = models.CharField(max_length=30, blank=True, null=True)
    content = models.TextField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return f"{self.title}"


class WikiImages(models.Model):
    image_title = models.CharField(max_length=50, blank=True, null=True)
    image_alt_title = models.CharField(max_length=100, blank=True, null=True)
    # use the ImageField instead of URLField because it handles the url and file location but needs another
    # pip package named pillow
    #image_url = models.URLField(blank=True, null=True)
    # also installed pip install django-resized and use it with ResizedImageField()
    image = models.ImageField(upload_to='wiki/images/', null=True, blank=True)
    # python3.9 -m pip install django-resized # "https://pypi.org/project/django-resized/"
    image_resized = ResizedImageField(
        scale=0.5, quality=75, upload_to='wiki/images/', null=True, blank=True)
    
    def __str__(self):
        image_display = f"image: {self.image.url}" if self.image else ""
        image_resized_display = f"resized Image: {self.image_resized.url}" if self.image_resized else ""
        return f"{self.image_title} [{image_display} {image_resized_display}]".strip() 
                                                                #strip off all empty space in a string

class Wiki(models.Model):
    header = models.CharField(max_length=30, blank=True, null=True)

    categories = models.ManyToManyField(WikiCategory, blank=True)
    contents = models.ManyToManyField(WikiContent, blank=True)
    images = models.ManyToManyField(WikiImages, blank=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        formatted_time = timezone.localtime(
            self.timestamp).strftime('%d.%m.%y - %H:%M')  # "https://www.geeksforgeeks.org/python-strftime-function/"
        return f"{self.header} | created on: {formatted_time}"


################################################################
#Logs

class Logs(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timeStamp = models.DateTimeField(auto_now_add=True)
    log = models.TextField(max_length=20)
    done = models.BooleanField(default=False, null=True)

    def __str__(self):
        return f"{self.user}, {self.timeStamp}, {self.log}, {self.done}"


class LoginLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timeStamp = models.DateTimeField(auto_now_add=True)
    loggedIn = models.BooleanField(default=False)

    def __str__(self):
        local_timestamp = timezone.localtime(self.timeStamp)
        action = "logged in" if self.loggedIn else "logged out"
        return f"{self.user.username} {action} on {local_timestamp.strftime('%d.%m.%y %H:%M')}"


################################################################
#External Links

class ExternalLinks(models.Model):
    title = models.CharField(max_length=50, null=True, blank=True)
    description = models.CharField(max_length=100, null=True, blank=True)
    link = models.URLField(null=True, blank=True)
    user_level = models.ForeignKey(
        Roles, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.title}"


################################################################
