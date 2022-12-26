from repo import Implement


class ServiceBus:

    @classmethod
    def upload_file_and_store(cls,file):
        return Implement().upload_file_and_store(file)

    @classmethod
    def train_data(cls, start_date, end_date):
        return Implement().train_data(start_date,end_date)

    @classmethod
    def predict_data(cls, start_date, days):
        return Implement().predict_data(start_date,days)