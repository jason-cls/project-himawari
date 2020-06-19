from flask_admin.contrib.sqla import ModelView

class UserView(ModelView):
    column_searchable_list = ['id', 'username', 'email', 'image_file', 
        'datetime_created'] 
    column_list = ('id', 'username', 'email', 'image_file', 'datetime_created')
    page_size = 10

class AnimeView(ModelView):
    column_searchable_list = ['id', 'title'] 
    column_list = ('id', 'title', 'episodes', 'rating', 
        'status','premiered','image_file', 'datetime_created')
    page_size = 10
