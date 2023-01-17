from repository_example import Repo_example


class ServiceBus:

    @classmethod
    def upload_file_and_store(cls,file):
        return Repo_example().upload_file_and_store(file)

    @classmethod
    def train_data(cls, start_date, end_date):
        return Repo_example().train_data(start_date,end_date)

    @classmethod
    def predict_data(cls, start_date, days):
        return Repo_example().predict_data(start_date,days)