SERVER_NAME = "coilcast"
SERVER_VERSION = "0.0.1"
REST_API_VERSION = "1.16.1"
MEDIA_FILE_EXTENSIONS = [".flac", ".mp3", ".ogg", ".wav"]
ERROR_MESSAGES = {
    0: "A generic error",
    10: "Required parameter is missing",
    20: "Incompatible Subsonic REST protocol version. Client must upgrade",
    30: "Incompatible Subsonic REST protocol version. Server must upgrade",
    40: "Wrong username or password",
    41: "Token authentication not supported for LDAP users",
    42: "Provided authentication mechanism not supported",
    43: "Multiple conflicting authentication mechanisms provided",
    44: "Invalid API key",
    50: "User is not authorized for the given operation",
    70: "The requested data was not found"
}
