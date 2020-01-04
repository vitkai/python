from django.db import models

class Category(models.Model):
    """Model representing a transaction category."""
    name = models.CharField(max_length=200, help_text='Enter a transaction category (e.g. Food)')
    
    def __str__(self):
        """String for representing the Model object."""
        return self.name

class CCY(models.Model):
    """Model representing a currency."""
    name = models.CharField(max_length=10, help_text='Enter a short name for a currency (e.g. RUB)')
    full_name = models.CharField(max_length=200, help_text='Enter a full name for a currency (e.g. Russian ruble)')
    
    def __str__(self):
        """String for representing the Model object."""
        return '{0} ({1})'.format(self.name, self.full_name)
