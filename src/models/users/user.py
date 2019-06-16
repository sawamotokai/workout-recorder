import uuid
import src.models.users.errors as UserErrors
from src.common.database import Database
from src.common.utils import Utils
from src.models.exercises.exercise import Exercise


class User(object):
    def __init__(self, email, password, _id=None, exercise_list=None, split_list=None, big3_counter=None, big3_max=None):
        #self.name = name
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id
        self.exercise_list = []
        self.split_list = [] if split_list is None else split_list
        self.big3_counter = {'BENCH PRESS': 0, 'DEAD LIFT': 0, 'SQUAT': 0} if big3_counter is None else big3_counter
        self.big3_max = {'BENCH PRESS': None, 'DEAD LIFT': None, 'SQUAT': None} if big3_max is None else big3_max

        # not sure if i can call self in __init__

    def __repr__(self):
        return "<User {}>".format(self.email)


    @staticmethod
    def is_login_valid(email, password):
        """
        This method verifies email/pw combo(as sent by site form) is valid or not.
        Checks that email exists , and that pw associated with to the email is correct
        "param email: User's email
        :param password: A sha512 hashed pw
        :return: True / False
        """
        user_data = Database.find_one(collection='users', query={"email":email})
        if user_data is None:
            #tell user their email does not exist
            raise UserErrors.UserNotExistsError("User Does Not Exist")

        if not Utils.check_hashed_password(password, user_data['password']):
            #tell user password is wrong
            raise UserErrors.IncorrectPasswordError("Password Does not match")

        return True


    def load_exercise_list(self, split):
        self.exercise_list = Exercise.get_exercise_list(self._id, split)


    @staticmethod
    def register_user(email, password):
        """
        This method registers users using email and pw. Pw already comes hashed as sha512

        :param name: User's name
        :param email: Users email (might be invalid)
        :param password: sha512 hashed password
        :return: True if registered successfully false otherwise
        """
        user_data = Database.find_one(collection='users', query={"email":email})
        if user_data is not None:
            #tell user they ara already registered
            raise UserErrors.UserAlreadyRegisteredError('The email you used already exists')

        if not Utils.email_is_valid:
            # tell email is not constructed properly
            raise UserErrors.InvalidEmailError('The email does not have the right format')

        User(email, Utils.hash_password(password)).save_to_db()

        return True




    def json(self):
        return {
            '_id':self._id,
            'email':self.email,
            'password':self.password,
            'exercise_list':self.exercise_list,
            'split_list':self.split_list,
            'big3_counter':self.big3_counter,
            'big3_max':self.big3_max
        }


    def save_to_db(self):
        Database.insert(collection='users', data=self.json())


    @classmethod
    def get_by_email(cls, email):
        data = Database.find_one(collection='users', query={'email':email})
        if data is not None:
            return cls(**data)


    @classmethod
    def get_by_id(cls, _id):
        data = Database.find_one(collection='users', query={'_id': _id})
        if data is not None:
            return cls(**data)