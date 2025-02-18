from django.db import models

class Domain(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Module(models.Model):
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.domain.name} - {self.name}"

class TestCase(models.Model):
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    content = models.TextField()  # This will store test case details

    def __str__(self):
        return f"{self.domain.name} - {self.module.name}"
