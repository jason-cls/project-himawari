import os
import logging
import logging.config
import pandas as pd
from essential_generators import DocumentGenerator
from random import randint
from kaguya import db, create_app
from kaguya.models import Anime, User, UserAnime, Review

# Reference for data generators: 
# https://pypi.org/project/essential-generators/0.9.2/

class PopulateDB():
    '''
    Populate DB with scraped or generated data
    :param new_db: if true, will delete curret db and create a new one
    :param path: path to anime.csv file
    '''
    def __init__(self, path, anime_limit, user_limit, new_db=False):
        self.logger = logging.getLogger(__name__)
        self.new_db = new_db
        self.path = path
        self.anime_limit = anime_limit
        self.user_limit = user_limit
        self.gen = DocumentGenerator()

        # Create new db delete old one
        if new_db:
            self.__create_db()
            self.app = create_app(create_db=True)
            if os.path.exists(self.db_file):
                self.logger.info("Created new db file at %s", self.db_file)
        else:
            self.app = create_app(create_db=False)
            self.logger.info("No new db file created")
        

    def popAll(self):
        # Populate both anime and user tables
        self.popAnime()
        self.popFakeUsers()


    def popAnime(self):
        # Populate anime table
        self.logger.info("Populating Anime DB...")

        with self.app.app_context():
            # Load data from csv
            self.logger.info("Getting data from %s", self.path)
            df_anime = pd.read_csv(self.path)
            for index, row in df_anime.iterrows():
                anime = Anime(
                    title=row['title'],
                    type=row['type'],
                    episodes=float(row['episodes']),
                    rating=row['rating'],
                    score=float(row['score']),
                    status=row['status'],
                    premiered=row['premiered'],
                    genres=row['genres'],
                    synopsis=row['synopsis'],
                    image_file=row['image_url']
                    )
                db.session.add(anime)
                # Log
                if (index)%100==0:
                    self.logger.info("Number of anime-rows added to session: %s", index)
                if index==self.anime_limit:
                    break

            db.session.commit()
            self.logger.info("Anime DB updated!")


    def popFakeUsers(self):
        # Get generator for users
        self.logger.info("Populating User DB with fake users...")

        self.__get_user_gen()
        self.__get_useranime_gen()
        accounts = self.user_gen.documents(self.user_limit)


        with self.app.app_context():
            for index, account in enumerate(accounts):
                user = User(
                    username=account['username'].replace(' ', '_').lower(),
                    email=account['email'])
                user.set_password('password')
                if (index)%10==0:
                    self.logger.info("Number of user-rows added to session: %s", index)
                db.session.add(user)
                db.session.commit()

                # Populate random reviews
                anime_ids = [randint(1,self. anime_limit) for iter in range(randint(5,50))]
                anime_ids = list(set(anime_ids))
                userAnimes = self.useranime_gen.documents(len(anime_ids))

                for (userAnimeInfo, anime_id) in zip(userAnimes, anime_ids):
                    review = Review(
                        content=self.gen.paragraph(),
                        rating=randint(0, 5),
                        user_id=index+1,
                        anime_id=anime_id
                        )

                    userAnime = UserAnime(
                        status=userAnimeInfo['status'],
                        episodes_watched=userAnimeInfo['episodes_watched'],
                        user_id=index+1 ,
                        anime_id=anime_id,
                        )

                    db.session.add(userAnime)
                    db.session.add(review)
                    db.session.commit()

    #--------------------------Private Functions-------------------------------#

    def __create_db(self):
        # Delete and make new db
        self.logger.info("WARNING: Deleting current db...")
        parent_folder = os.path.abspath('..')
        self.db_file = os.path.join(parent_folder, 'kaguya', 'site.db')
        try:
            os.remove(self.db_file)
            self.logger.info('Deleted db at %s', self.db_file)
        except:
            self.logger.error('Failed to delete the DB! at %s', self.db_file)

    def __get_user_gen(self):
        # Create generator for users
        self.logger.info('Creating user generator...')
        self.user_gen = DocumentGenerator()

        template = {
            'username': {'typemap': 'name', 'unique': True, 'tries': 10},
            'email': {'typemap': 'email', 'unique': True, 'tries': 10},
            'password': 'small_int'
        }

        self.user_gen.set_template(template)

    def __get_useranime_gen(self):
        # Create generator for user_anime
        self.logger.info('Creating user-anime generator...')
        self.useranime_gen = DocumentGenerator()

        template = {
            'status': ['Watch List', 'Watching', 'Finished'],
            'episodes_watched': 'small_int'
        }
        self.useranime_gen.set_template(template)

    def __check_db(self):
        # count and check if db is okay
        print('To do later')


if __name__ == "__main__":
    # Logs
    logging.config.fileConfig('log/logging.conf')
    logger = logging.getLogger(__name__)
    logger.info("Running populate-db.py...")
    
    path = os.path.join('data', 'anime.csv')
    
    popDB=PopulateDB(
        path=path,
        new_db=True,
        anime_limit=1000, 
        user_limit=200)

    popDB.popAll()
    


