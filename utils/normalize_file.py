import re

async def normalize_file(filename):
    filename = re.sub(r'[<>:"|?*\s]', '_', filename)
    #also shorten the filename if it's too long
    if len(filename) > 30:
        filename = filename[:27] + "___"
    return filename