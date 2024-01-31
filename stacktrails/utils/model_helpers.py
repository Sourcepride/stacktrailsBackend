from utils.helpers import encoded_uuid4_to_str


def create_uid():
    return encoded_uuid4_to_str()[:12]
