from django.urls import path

import main_app.views as views

urlpatterns = [
    # path('projects', views.ProjectsView.as_view()),

    # Pages
    path('pages', views.PagesView.as_view()),
    path('pages/update', views.UpdatePageView.as_view()),

    # Preview
    path('preview', views.PreviewView.as_view()),
]
