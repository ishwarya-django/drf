
from django.urls import path,include
from . import views

from rest_framework import routers
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
# router.register("Transformer",views.Trans_former)
router.register("Singer",views.Singer_view)
router.register("Song",views.Song_view)  
router.register("product",views.product,basename="product")  

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    # path('product/',views.product,name='product'),
    path('transformers/<int:pk>/',views.transformer_detail,name = 'transformer_detail'),
    path('transformers/',views.transformer_list,name = 'transformer_list'),
]+ router.urls
# ]+ router.urls