from passlib.hash import pbkdf2_sha512
import re
import pygal
import doctest


class Utils(object):

    @staticmethod
    def hash_password(password):
        """
        hashes password using pbkdf2_sha512
        :param password: sha512 password from login/register form
        :return: A sha512 -> pbkdf2_sha512 encrypted password
        """
        return pbkdf2_sha512.encrypt(password)


    @staticmethod
    def check_hashed_password(password, hashed_password):
        """
        Checks that password user sent matches that of database
        Password in the database is encrypted more that users password at this stage
        :param password: sha512-hashed password
        :param hashed_password: pbkdf2-sha512 encrypted password
        :return: True if pw matches / False otherwise
        """
        return pbkdf2_sha512.verify(password, hashed_password)


    @staticmethod
    def email_is_valid(email):
        email_adress_matcher = re.compile('^[\w-]+@([\w-]+\.)+[\w-]$')
        return email_adress_matcher.match(email)

def calculate_1rm(weight, reps):
    """
    calculate 1RM from the record
    :param record: weight, reps
    :return: 1RM in float
    '100.0'
    """
    switcher = {
        1:100, 2:97, 3:94, 4:92, 5:89, 6:86, 7:83, 8:81, 9:78, 10: 75, 11:73, 12:71, 13:70, 14:68, 15:67, 16:65, 17:64, 18:63, 19:61, 20:60, 21:59, 22:58, 23:57, 24:56, 25:55, 26:54, 27:53, 28:52, 29:51, 30:50
    }
    reps = int(reps)
    weight = int(weight)
    result = 100*weight / switcher[reps]
    return '{0:.1f}'.format(result)


def from_1rm(one_rm, reps):
    switcher = {
        1: 100, 2: 97, 3: 94, 4: 92, 5: 89, 6: 86, 7: 83, 8: 81, 9: 78, 10: 75, 11: 73, 12: 71, 13: 70, 14: 68, 15: 67,
        16: 65, 17: 64, 18: 63, 19: 61, 20: 60, 21: 59, 22: 58, 23: 57, 24: 56, 25: 55, 26: 54, 27: 53, 28: 52, 29: 51,
        30: 50
    }
    reps = int(reps)
    weight = int(one_rm)
    result = weight * switcher[reps] / 100
    return float('{0:.1f}'.format(result))


def create_graph(records, exercise):
    line_chart = pygal.Line(y_title='1RM', x_title='Date')
    line_chart.title = f'1RM Growth of {exercise}'
    if records[exercise]:
        weight = []
        for record in records[exercise]:
            weight.append(float(record[0]))
        line_chart.x_labels = [record[1] for record in records[exercise]]
        line_chart.add(exercise, weight)
        graph_data = line_chart.render_data_uri()
        return graph_data
    return None
