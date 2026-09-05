from django.db import models


class Provider(models.Model):
    name = models.CharField(max_length=100)
    website = models.URLField(blank=True)

    def __str__(self):
        return self.name


class Service(models.Model):
    name = models.CharField(max_length=100)
    provider = models.ForeignKey(
        Provider,
        on_delete=models.PROTECT,
        related_name="services",
    )

    def __str__(self):
        return self.name

class Plan(models.Model):
    service = models.ForeignKey(
        Service,
        on_delete=models.PROTECT,
        related_name="plans",
    )

    name = models.CharField(max_length=100)

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    currency = models.CharField(
        max_length=3,
        choices=(("USD", "USD"), ("EUR", "EUR"), ("PHP", "PHP"))
    )

    billing_cycle = models.CharField(
        max_length=20,
        choices=(
            ("none", "Free"),
            ("pay_go", "Pay-as-you-Go"),
            ("monthly", "Monthly"),
            ("annually", "Annually"),
        ),
        default="none",
    )

    renewal_date = models.DateField(
        null=True,
        blank=True,
    )

    auto_renew = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return f"{self.service.name} - {self.name}"

class UsageMetric(models.Model):
    service = models.ForeignKey(
        Service,
        on_delete=models.PROTECT,
        related_name="metrics",
    )

    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=50, help_text="Examples: emails, requests, GB, credits",)

    def __str__(self):
        return f"{self.service.name} - {self.name}"

class UsageRecord(models.Model):
    metric = models.ForeignKey(
        UsageMetric,
        on_delete=models.CASCADE,
        related_name="records",
    )

    amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
    )

    period_start = models.DateField()
    period_end = models.DateField()

    recorded_at = models.DateField(
        auto_now_add=True,
    )

    def __str__(self):
        return f"{self.metric.name} - {self.amount}"

class PlanLimit(models.Model):
    plan = models.ForeignKey(
        Plan,
        on_delete=models.CASCADE,
        related_name="limits",
    )

    metric = models.ForeignKey(
        UsageMetric,
        on_delete=models.PROTECT,
        related_name="plan_limits",
    )

    limit = models.DecimalField(
        max_digits=15,
        decimal_places=2,
    )

    period_start = models.DateField()
    period_end = models.DateField()

    def __str__(self):
        return f"{self.plan.name} - {self.metric.name}: {self.limit}"