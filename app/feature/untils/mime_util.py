import mimetypes


def is_video_link(link):
    mime_str = mimetypes.guess_type(link)[0]
    return mime_str and 'video' in mime_str


def is_video_mime(mime_str):
    return 'video' in mime_str


def is_image_link(link):
    mime_str = mimetypes.guess_type(link)[0]
    return mime_str and 'image' in mime_str


def is_image_mime(mime_str):
    return 'image' in mime_str


def is_mp4_link(link):
    return 'mp4' in mimetypes.guess_type(link)[0]