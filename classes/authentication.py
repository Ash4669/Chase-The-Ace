import configparser

config = configparser.ConfigParser()
config.read("settings.conf")

class Authentication(object):

    def isUserLoggedIn():
        return boolean

        # Look into remote_user in flask to get username of person who authenticted.

    def validLogin(username, password):
        if password == config.get('LOGINDETAILS','password'):
            logTheUserIn()
        else:
            return false


    def logTheUserIn():
        pass
