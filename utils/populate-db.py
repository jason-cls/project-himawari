import os
import pandas as pd
from kaguya import db, create_app
from kaguya.models import Anime

def populateAnime():
    app = create_app(create_db=True)
    
    with app.app_context():
        # Load data from csv
        df_anime = pd.read_csv(os.path.join('crawler',
            'animeData.csv'))
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
        
            if index == 500:
                break 
    
        db.session.commit()

if __name__ == "__main__":
    populateAnime()

