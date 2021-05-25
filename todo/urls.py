from django.conf import settings
from django.urls import path

from todo import views

app_name = "todo"

urlpatterns = [
    path("", views.list_lists, name="lists"),
    path("illustration_petitions/", views.task_lists, name="task_lists"),
    # View reorder_tasks is only called by JQuery for drag/drop task ordering.
    path("accepted_petitions/", views.accepted_petitions, name="accepted_petitions"),
    path("reorder_tasks/", views.reorder_tasks, name="reorder_tasks"),
    path("set_firstime_password/<str:uuid>/", views.set_ft_pass, name="set_ft_pass"),
    # Allow users to post tasks from outside django-todo (e.g. for filing tickets - see docs)
    path("ticket/add/", views.external_add, name="external_add"),
    # Three paths into `list_detail` view
    path("mine/", views.list_detail, {"list_slug": "mine"}, name="mine"),
    path("mine/completed", views.list_detail, {"list_slug": "mine", "view_completed": True}, name="mine_completed"),
    path(
        "<int:list_id>/<str:list_slug>/completed/",
        views.list_detail,
        {"view_completed": True},
        name="list_detail_completed",
    ),
    path("<int:list_id>/<str:list_slug>/", views.list_detail, name="list_detail"),
    path("book/<int:book_id>/assign", views.book_assign, name="book_assign"),
    path("task/<int:task_id>/assign", views.designer_assign, name="designer_assign"),
    path("book/<int:book_id>/publish", views.book_publish, name="book_publish"),
    path("book/<int:book_id>/detail", views.book_detail, name="book_detail"),
    path("task/<int:task_id>/", views.task_detail, name="task_detail"),
    path(
        "attachment/remove/<int:attachment_id>/", views.remove_attachment, name="remove_attachment"
    ),
    path("toggle_done/<int:task_id>/", views.toggle_done, name="task_toggle_done"),
    path("delete/<int:task_id>/", views.delete_task, name="delete_task"),
    path("search/", views.search, name="search"),
    path("categories/<str:category_id>/", views.book_category, name="book_category"),
    path("createsubscription", views.create_subscription, name="create_subscription"),
]

