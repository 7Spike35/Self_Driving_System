from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.preprocessing_view, name='processing'),
    path('enhancement/', views.enhancement_view, name='enhancement_and_transformation'),
    path('fusion/', views.fusion_view, name='concatenation_and_fusion'),
    path('rotate-image/', views.rotate_image, name='rotate_image'),
    path('grayscale-image/', views.grayscale_image, name='grayscale_image'),
    path('sharpening-image/', views.sharpening_image, name='sharpening_image'),
    path('frequency-transform/', views.frequency_transform, name='frequency_transform'),
    path('gaussian_blur/', views.gaussian_blur, name='gaussian_blur'),
    path('binarize-image/', views.binarize_image, name='binarize_image'),
    path('concatenation/', views.concatenation, name='concatenation'),
    path('concatenation1/', views.concatenation1, name='concatenation1'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)