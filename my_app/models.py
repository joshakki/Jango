from django.db import models

class Domain(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Module(models.Model):
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ('domain', 'name')  # Prevent duplicate modules under the same domain

    def __str__(self):
        return f"{self.domain.name} - {self.name}"

class TestCase(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name="test_cases")
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    expected_result = models.TextField()
    actual_result = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=[('Pass', 'Pass'), ('Fail', 'Fail'), ('Pending', 'Pending')],
        default='Pending'
    )

    def __str__(self):
        return self.title