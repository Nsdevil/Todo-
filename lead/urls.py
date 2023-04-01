from django.urls import path
from . import views

app_name = 'leads'

urlpatterns = [
    # path('', views.leads_list, name='list'),
    path('', views.LeadListView.as_view(), name='list'),
    # path('<int:pk>/', views.leads_details, name='details'),
    path('<int:pk>/', views.LeadDetailView.as_view(), name='details'),
    # path('<int:pk>/delete/', views.leads_delete, name='delete'),
    path('<int:pk>/delete/', views.LeadDeleteView.as_view(), name='delete'),
    # path('<int:pk>/edit/', views.leads_edit, name='edit'),
    path('<int:pk>/edit/', views.LeadUpdateView.as_view(), name='edit'),
    # path('<int:pk>/covert/', views.convert_to_client, name='convert'),
    path('<int:pk>/covert/', views.ConvertToClient.as_view(), name='convert'),
    path('<int:pk>/add-comment/', views.AddCommentView.as_view(), name='add_comment'),
    path('<int:pk>/add-file/', views.AddFileView.as_view(), name='add_file'),
    # path('add-lead/', views.add_lead, name='add_lead'),
    path('add/', views.LeadCreateView.as_view(), name='add_lead')
]
