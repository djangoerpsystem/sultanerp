from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin

from .models import (User, AdminTools, DocumentData, InternalProducts, TortenBestellungsID,
                     WebhookData, MeasureUnits, Category, Store, Storage,
                     Supplier, SuppliersProduct, SupplierOrders, CustomerOrders,
                     InternalOrders, Task, Inventory, InventorySection, Deposit, DepositObject,
                     VacationApplication, VacationDays, VacationRecord, PublicHoliday,
                     Frequency, Routines, Places, RoutineTasks, RoutinesCategory, TaskFrequency, Retoure,
                     CalendarEntriesStore, CalendarEntriesOffice, Logs, LoginLog, Roles, DynamicText, Message,
                     WikiCategory, Wiki, WikiContent, WikiImages, ExternalLinks, 
                     )


class UserAdmin(DefaultUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (('Personal info'), {'fields': ('first_name',
         'last_name', 'email', 'branch', 'personal_nr')}),
        (('Permissions'), {'fields': ('is_active', 'is_staff',
         'is_superuser', 'groups', 'user_permissions')}),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (('Roles & Branch'), {'fields': ('user_level',)})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'branch', 'personal_nr', 'user_level'),
        }),
    )
    list_display = ('username', 'first_name', 'last_name',
                    'branch', 'personal_nr', 'user_level', 'is_staff')
    search_fields = ('username', 'first_name', 'last_name', 'branch')
    ordering = ('username',)


if admin.site.is_registered(User):
    admin.site.unregister(User)

admin.site.register(User, UserAdmin)
admin.site.register(AdminTools)
admin.site.register(MeasureUnits)
admin.site.register(Category)
admin.site.register(Store)
admin.site.register(Storage)
admin.site.register(DocumentData)
admin.site.register(TortenBestellungsID)
admin.site.register(WebhookData)
admin.site.register(Supplier)
admin.site.register(SuppliersProduct)
admin.site.register(SupplierOrders)
admin.site.register(InternalOrders)
admin.site.register(CustomerOrders)
admin.site.register(Retoure)
admin.site.register(Task)
admin.site.register(Frequency)
admin.site.register(TaskFrequency)
admin.site.register(Routines)
admin.site.register(RoutineTasks)
admin.site.register(RoutinesCategory)
admin.site.register(Places)
admin.site.register(Inventory)
admin.site.register(InventorySection)
admin.site.register(Deposit)
admin.site.register(DepositObject)
admin.site.register(InternalProducts)
admin.site.register(VacationRecord)
admin.site.register(VacationApplication)
admin.site.register(VacationDays)
admin.site.register(PublicHoliday)
admin.site.register(CalendarEntriesStore)
admin.site.register(CalendarEntriesOffice)
admin.site.register(Message)
admin.site.register(Logs)
admin.site.register(LoginLog)
admin.site.register(DynamicText)
admin.site.register(Roles)
admin.site.register(WikiCategory)
admin.site.register(WikiContent)
admin.site.register(WikiImages)
admin.site.register(Wiki)
admin.site.register(ExternalLinks)