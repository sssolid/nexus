from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib.auth.models import Permission

User = get_user_model()


class Command(BaseCommand):
    help = "Create default development users and sample data."

    def handle(self, *args, **options):

        if not settings.DEBUG:
            self.stdout.write(self.style.WARNING("DEBUG=False, skipping bootstrap_dev"))
            return

        self.stdout.write(self.style.NOTICE("Running development bootstrap..."))

        # =========================================================
        # ADMIN USER (EMPLOYEE)
        # =========================================================
        admin_email = "admin@example.com"
        admin_password = "admin123"

        admin, created = User.objects.get_or_create(
            email=admin_email,
            defaults={
                "user_type": User.UserType.EMPLOYEE,
                "employee_role": User.EmployeeRole.ADMIN,
                "is_staff": True,
                "is_superuser": True,
                "is_active": True,
                "email_verified": True,
                "is_approved": True,
                "first_name": "Admin",
                "last_name": "User",
            },
        )

        if created:
            admin.set_password(admin_password)
            admin.user_permissions.set(Permission.objects.all())
            admin.save()
            self.stdout.write(
                self.style.SUCCESS(f"Superuser created: {admin_email}/{admin_password}")
            )
        else:
            self.stdout.write("Superuser already exists — skipping")

        # =========================================================
        # TEST USER (CUSTOMER)
        # =========================================================
        test_email = "test@example.com"
        test_password = "test123"

        test_user, created = User.objects.get_or_create(
            email=test_email,
            defaults={
                "user_type": User.UserType.CUSTOMER,
                "is_staff": False,
                "is_superuser": False,
                "is_active": True,
                "email_verified": True,
                "is_approved": True,
                "first_name": "Test",
                "last_name": "Customer",
            },
        )

        if created:
            test_user.set_password(test_password)
            test_user.save()
            self.stdout.write(
                self.style.SUCCESS(f"Test user created: {test_email}/{test_password}")
            )
        else:
            self.stdout.write("Test user already exists — skipping")

        # =========================================================
        # OPTIONAL: DataMapping
        # =========================================================
        from apps.data_sync.models import DataMapping
        from apps.products.models import ProductCategory, ProductManufacturer

        ProductCategory.objects.get_or_create(
            slug="uncategorized",
            defaults={
                "name": "Uncategorized",
                "description": "Temporary category for imported products",
                "is_active": True,
            },
        )

        ProductManufacturer.objects.get_or_create(
            code="UNKNOWN",
            defaults={
                "name": "Unknown Manufacturer",
                "slug": "unknown-manufacturer",
                "is_active": True,
            },
        )

        DataMapping.objects.get_or_create(
            filemaker_table="Master",
            filemaker_field="AS400_NumberStripped",
            target_model="PRODUCT",
            target_field="part_number",
            defaults={
                "name": "Product Part Number",
                "description": "Maps stripped AS400 part number",
                "is_required": True,
                "is_active": True,
            },
        )
        DataMapping.objects.get_or_create(
            filemaker_table="Master",
            filemaker_field="AS400_JobberPrice",
            target_model="PRODUCT",
            target_field="base_price",
            defaults={
                "name": "Default base price",
                "description": "Temporary default until pricing sync exists",
                "default_value": "0.00",
                "is_required": True,
                "is_active": True,
            },
        )

        # =========================================================
        # OPTIONAL: SyncConfiguration
        # =========================================================
        from apps.data_sync.models import SyncConfiguration

        SyncConfiguration.objects.get_or_create(
            name="Product Basic Sync",
            defaults={
                "description": "Sync only part_number from FileMaker Master",
                "is_enabled": True,
                "sync_interval_minutes": 5,
                "filemaker_layout": "Master",
                "filemaker_query": '"AS400_NumberStripped" IS NOT NULL',
                "batch_size": 500,
                "enable_incremental": False,
            },
        )

        self.stdout.write(self.style.SUCCESS("Development bootstrap complete."))
