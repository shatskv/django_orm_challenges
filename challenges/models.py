from django.db import models
from django.forms.models import model_to_dict
ALL_STATUSES = ['published', 'not published', 'banned']
ALL_CATEGORIES = ['Sience fiction', 'Drama', 'Comedia', 'Sience', 'Detective', 'Medicine']

def get_tuples_from_list(data):
    return [(item, item) for item in data]

class Book(models.Model):
    title = models.CharField(max_length=256)
    author_full_name = models.CharField(max_length=256)
    isbn = models.CharField(max_length=10)

    def __str__(self):
        return self.title
    

class Laptop(models.Model):
    

    brand = models.CharField(max_length=256)
    model = models.CharField(max_length=256)
    quantity = models.IntegerField()
    price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.brand}: {self.quantity}, price {self.price}'
    
    def to_json(self):
        return {'id': self.pk,
                'brand': self.brand,
                'model': self.model,
                'quantity': self.quantity,
                'price': self.price,
                'created_at': str(self.created_at),
                'updated_at': str(self.updated_at)
                }
    

class Blog(models.Model):
    class Meta:
        get_latest_by = 'created_at'
        ordering = ['-created_at']

    title = models.CharField(max_length=256)
    text = models.TextField()
    author = models.CharField(max_length=256)
    status = models.CharField(max_length=25, choices=get_tuples_from_list(ALL_STATUSES))
    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(null=True)
    category = models.CharField(max_length=50, choices=get_tuples_from_list(ALL_CATEGORIES), null=True)

    def __str__(self):
        return f'id: {self.pk }, author: {self.author}, {self.title}, {self.status}, created_at: {self.created_at}'
    
    def to_json(self):
        return {'title': self.title,
                'text': self.text,
                'author': self.author,
                'status': self.status,
                'created_at': self.created_at.isoformat(),
                'published_at': self.published_at.isoformat() if self.published_at else None,
                'category': self.category}
