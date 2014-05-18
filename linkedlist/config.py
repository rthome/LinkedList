# Config file for public configuration
# Secret information, such as flask's SECRET_KEY,
# must be put in ../instance/config.py and kept out of version control

DEBUG = False

SECURITY_PASSWORD_HASH = 'pbkdf2_sha512'
SECURITY_PASSWORD_SALT = '8azsfoaflk'

# allow registering users
SECURITY_REGISTERABLE = True

# very basic tracking of login stats
SECURITY_TRACKABLE = True

# disable flask-security email features for now
SECURITY_SEND_REGISTER_EMAIL = False
SECURITY_SEND_PASSWORD_CHANGE_EMAIL = False
SECURITY_SEND_PASSWORD_RESET_NOTICE_EMAIL = False
