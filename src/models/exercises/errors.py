

class ExerciseError(Exception):
    def __init__(self, message):
        self.message=message



class ExerciseNotExistsError(ExerciseError):
    pass

class ExerciseAlreadyExistsError(ExerciseError):
    pass

class IncorrectPasswordError(ExerciseError):
    pass

class UserAlreadyRegisteredError(ExerciseError):
    pass

class InvalidEmailError(ExerciseError):
    pass

