from django.urls import path
from .views import *

urlpatterns = [
    path('', MailingListView.as_view(), name='mailing_list'),
    path('<int:pk>/', MailingDetailView.as_view(), name='mailing_detail'),
    path('create/', MailingCreateView.as_view(), name='mailing_create'),
    path('<int:pk>/update/', MailingUpdateView.as_view(), name='mailing_update'),
    path('<int:pk>/delete/', MailingDeleteView.as_view(), name='mailing_delete'),

    path('messages/', MessageListView.as_view(), name='message_list'),
    path('messages/create/', MessageCreateView.as_view(), name='message_create'),
    path('messages/<int:pk>/', MessageDetailView.as_view(), name='message_detail'),
    path('messages/<int:pk>/update/', MessageUpdateView.as_view(), name='message_update'),
    path('messages/<int:pk>/delete/', MessageDeleteView.as_view(), name='message_delete'),

    path('clients/', ClientListView.as_view(), name='client_list'),
    path('clients/create/', ClientCreateView.as_view(), name='client_create'),
    path('clients/<int:pk>/', ClientDetailView.as_view(), name='client_detail'),
    path('clients/<int:pk>/update/', ClientUpdateView.as_view(), name='client_update'),
    path('clients/<int:pk>/delete/', ClientDeleteView.as_view(), name='client_delete'),
]
