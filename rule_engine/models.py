# Create your models here.

from django.db import models

class Node(models.Model):
    NODE_TYPE_CHOICES = [
        ('operator', 'Operator'),
        ('operand', 'Operand'),
    ]
    
    node_type = models.CharField(max_length=10, choices=NODE_TYPE_CHOICES)
    left = models.ForeignKey('self', related_name='left_node', on_delete=models.SET_NULL, null=True, blank=True)
    right = models.ForeignKey('self', related_name='right_node', on_delete=models.SET_NULL, null=True, blank=True)
    value = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"Node(type={self.node_type}, value={self.value})"

