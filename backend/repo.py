import os
from app import app


class Implement:

    @classmethod
    def upload_file_and_store(cls,file):
        file.save(os.path.join(app.config['UPLOAD_FOLDER'],file.filename))
        pass

    @classmethod
    def train_data(cls,start_date,end_date):
        print(start_date)
        print(end_date)
        pass

    @classmethod
    def predict_data(cls,start_date,days):
        print(start_date)
        print(days)
        pass