from django.db import models


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
                'created_at': self.created_at.isoformat(),
                'updated_at': self.updated_at.isoformat()
                }
    

class Blog(models.Model):
    class Meta:
        get_latest_by = 'created_at'
        ordering = ['-created_at']

    class Category(models.TextChoices):
        SIENCE_FICTION = 'Sience fiction'
        DRAMA = 'Drama'
        COMEDIA = 'Comedia'
        SIENCE = 'Sience'
        DETECTIVE = 'Detective'
        MEDICINE = 'Medicine'

    class PublishStatus(models.TextChoices):
        PUBLISHED = 'published'
        NOT_PUBLISHED = 'not published'
        BANNED = 'banned'

    title = models.CharField(max_length=256)
    text = models.TextField(max_length=10000)
    category = models.CharField(max_length=50, choices=Category.choices, null=True)
    author = models.CharField(max_length=256)
    status = models.CharField(max_length=25, choices=PublishStatus.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(null=True)

    def __str__(self):
        return f'id: {self.pk }, author: {self.author}, {self.title}, {self.status}, created_at: {self.created_at}'
    
    def to_json(self):
        return {'title': self.title,
                'text': self.text,
                'category': self.category,
                'author': self.author,
                'status': self.status,
                'created_at': self.created_at.isoformat(),
                'published_at': self.published_at.isoformat() if self.published_at else None
                }
                
