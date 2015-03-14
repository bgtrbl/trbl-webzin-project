import re


def get_visible_string(tags, join_char=" "):
    def _visible(tag):
        if tag.parent.name in ['style', 'script', '[document]', 'head', 'title']:
            return False
        elif tag.name in ['img']:
            return False
        elif re.match('<!--.*-->', str(tag)):
            return False
        return True
    return join_char.join(filter(_visible, tags))
