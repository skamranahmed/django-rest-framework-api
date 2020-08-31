from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('article', views.ArticleViewSet, basename = 'article')

urlpatterns = [
    path('viewset/', include(router.urls)),
    path('viewset/<int:pk>/', include(router.urls)),
    # path('article/', views.article_list),
    path('article/', views.ArticleAPIView.as_view()),
    path('generic/article/<int:id>/', views.GenericAPIView.as_view()),
    # path('detail/<int:primary_key>/', views.article_detail),
    path('detail/<int:primary_key>/', views.ArticleDetailAPIView.as_view()),
]