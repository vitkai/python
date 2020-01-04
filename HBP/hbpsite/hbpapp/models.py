from django.db import models

class Category(models.Model):
    """Model representing a transaction category."""
    name = models.CharField(max_length=200, help_text='Enter a transaction category (e.g. Food)')
    
    def __str__(self):
        """String for representing the Model object."""
        return self.name
