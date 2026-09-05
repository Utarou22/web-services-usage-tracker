from django.contrib import admin

from .models import (
    Provider,
    Service,
    Plan,
    UsageMetric,
    UsageRecord,
    PlanLimit,
)


@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ("name", "website")
    search_fields = ("name",)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "provider")
    search_fields = ("name", "provider__name")
    list_filter = ("provider",)

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = (
        "service",
        "name",
        "price",
        "currency",
        "billing_cycle",
        "renewal_date",
        "auto_renew",
    )

    list_filter = (
        "billing_cycle",
        "auto_renew",
        "currency",
    )

    search_fields = (
        "name",
        "service__name",
        "service__provider__name",
    )

@admin.register(UsageMetric)
class UsageMetricAdmin(admin.ModelAdmin):
    list_display = (
        "service",
        "name",
        "unit",
    )

    list_filter = ("service",)

    search_fields = ("name", "service__name",)

@admin.register(UsageRecord)
class UsageRecordAdmin(admin.ModelAdmin):
    list_display = (
        "metric",
        "amount",
        "period_start",
        "period_end",
        "recorded_at",
    )

    list_filter = ("metric",)

@admin.register(PlanLimit)
class PlanLimitAdmin(admin.ModelAdmin):
    list_display = (
        "plan",
        "metric",
        "limit",
    )

    list_filter = (
        "plan",
        "metric",
    )
