class Config(object):
    DEBUG = False
    SECRET_KEY = 'this is secret string'

    ERROR_LOG = "../logs/error.log"
    INFO_LOG = "../logs/info.log"

    AVATAR_PATH = "resource/image/avatar"
    TMP_PATH = "resource/tmp"
    IMAGE_PATH = "resource/image/image"

    DBHost=""
    DBUser=""
    DBPassword=""
    DBName="pnet"