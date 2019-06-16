import uuid
from datetime import date

import src.models.exercises.constants as constants
from src.common.database import Database
import src.models.exercises.errors as ExerciseErrors


class Exercise(object):
    def __init__(self, name, user_id, record=None, _id=None, split=None):
        self.name = name
        self.user_id = user_id
        self.record = record
        self._id = uuid.uuid4().hex if _id is None else _id
        self.split = split

    def __repr__(self):
        return '<{}\'s exercise record>'.format(self.name)



    def new_exercise(self, name, user_id):
        data = self.get_by_name(name)
        if data is None:
            Exercise(name, user_id).save_to_mongo()
            return True
        else:
            return



    def save_to_mongo(self):
        Database.insert(constants.COLLECTION, self.json())


    def json(self):
        return {
            'name':self.name,
            'user_id':self.user_id,
            '_id':self._id,
            'record':self.record,
            'split':self.split
        }


    def update_record(self, record):
        print('Record Updated!')
        print(record)
        # if self.record[-1]['date'] == record['date']:
        #     del self.record[-1]
        self.record.append(record)
        Database.update(constants.COLLECTION, {'_id':self._id}, self.json())
        print(self.record)





    @classmethod
    def get_by_id(cls, _id):
        return cls(**Database.find_one(constants.COLLECTION, {'_id': _id}))


    @classmethod
    def get_exercise_list(cls, user_id, split):
        exercises = Database.find_all(constants.COLLECTION, {'user_id':user_id, 'split':split})
        return [cls(**exercise) for exercise in exercises]


    @classmethod
    def get_by_name(cls, exercise_name):
        data = Database.find_one(constants.COLLECTION, {'name': exercise_name} )
        if data is not None:
            return cls(**data)

    @classmethod
    def get_by_user_id_and_name(cls,user_id,exercise_name):
        data = Database.find_one(constants.COLLECTION, {'name': exercise_name, 'user_id':user_id})
        if data is not None:
            return cls(**data)




    # @classmethod
    # def get_by_url_prefix(cls, url_prefix):
    #     return cls(**Database.find_one(constants.COLLECTION, {"url_prefix":{"$regex":"^{}".format(url_prefix)}}))
    #
    #
    # @classmethod
    # def get_by_url(cls, url):
    #     for i in range(0, len(url)+1):
    #         try:
    #             store = cls.get_by_url_prefix(url[:i])
    #             return store
    #         except:
    #             raise ExerciseErrors.ExerciseNotExistsError('The url d.')
