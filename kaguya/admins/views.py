from flask_admin.contrib.sqla import ModelView

class UserView(ModelView):
    column_filters = ('id', 'username', 'email')
    column_searchable_list = ['id', 'username', 'email', 'image_file', 
        'datetime_created'] 
    column_list = ('id', 'username', 'email', 'image_file', 'datetime_created')
    page_size = 10

class AnimeView(ModelView):
    column_searchable_list = ['title'] 
    column_filters = ('id', 'title', 'status')
    column_list = ('id', 'title', 'episodes', 'rating', 
        'status','premiered','image_file', 'datetime_created')
    page_size = 10

class ReviewView(ModelView):
    column_list = ('user_id', 'anime_id', 'content', 'rating', 
        'datetime_created')
    column_filters = ('user_id', 'anime_id')
    page_size = 10

class UserAnimeView(ModelView):
    column_list = ('id', 'user_id','anime_id', 'status', 'episodes_watched',
        'datetime_created')
    column_filters = ('user_id', 'anime_id')
    page_size = 10