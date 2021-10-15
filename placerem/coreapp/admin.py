from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from coreapp.forms import CustomUserCreationForm, CustomUserChangeForm
from coreapp.models import CustomUser, Recollection


# Here we can configure how the model will look like in admin dashboard
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    # Controls which fields are displayed on the change list(!) page of the admin.
    list_display = ('email', 'username', 'is_staff', 'is_active', 'date_joined',)
    # Controls what filters are available
    list_filter = ('date_joined', 'is_staff', 'is_active',)
    # When editing user
    fieldsets = (
        ('Information', {'fields': ('email', 'username', 'photo', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    # When creating new user via admin dashboard
    add_fieldsets = (
        (
            None,
            {
                # CSS style classes
                'classes': ('wide',),
                'fields': ('email', 'photo', 'password1', 'password2', 'is_staff', 'is_active')
            }
        ),
    )
    # Search
    search_fields = ('email',)
    # Ordering
    ordering = ('email',)


class RecollectionAdmin(admin.ModelAdmin):
    model = Recollection
    list_display = ('name', 'description', 'user', 'published')
    list_filter = ('published',)
    fieldsets = (
        ('Information', {'fields': ('name', 'description', 'user', 'geom',)}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('name', 'description', 'user', 'geom',)
            }
        ),
    )
    search_fields = ('name',)
    ordering = ('published',)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Recollection, RecollectionAdmin)
