import configparser

config = configparser.ConfigParser()
config.read("settings.conf")

class Authentication(object):

    def isUserLoggedIn():
        return boolean

    def validLogin(username, password):
        if password == config.get('LOGINDETAILS','password'):
            logTheUserIn()
        else:
            return false


    def logTheUserIn():
        pass
