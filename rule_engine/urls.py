from django.urls import path
from . import views
from .views import combine_rules_view
from .views import test_rule_view

urlpatterns = [
    path('create_rule/', views.create_rule_view, name='create_rule'),
    path('edit_rule/<int:node_id>/', views.edit_rule_view, name='edit_rule'),  # New URL for editing rules
    path('combine_rules/', combine_rules_view, name='combine_rules'),
    path('test_rule/', test_rule_view, name='test_rule'),

]

