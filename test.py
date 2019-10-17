import configparser
config = configparser.ConfigParser()
config.read("settings.py")
# config['DEFAULT'] = {'loginPassword': 'password'}
# print(config['DEFAULT']['loginPassword'])
print(config.get('LOGINDETAILS','loginPassword'))
print(config.get('PUSHERDETAILS','app_id'))
print(config.get('PUSHERDETAILS','key'))
print(config.get('PUSHERDETAILS','secret'))
print(config.get('PUSHERDETAILS','ssl'))
print(type(bool(config.get('PUSHERDETAILS','ssl'))))
