# -*- coding: utf-8 -*-

"""Blofeld API module."""

import os
import struct
import base64
import logging

import mutagen

from .base import Resource, ResourceGetMixin


def unpack_image(data):
    """
    Helper function to unpack image data from a WM/Picture tag.

    The data has the following format:
    1 byte: Picture type (0-20), see ID3 APIC frame specification at http://www.id3.org/id3v2.4.0-frames
    4 bytes: Picture data length in LE format
    MIME type, null terminated UTF-16-LE string
    Description, null terminated UTF-16-LE string
    The image data in the given length
    """
    (type, size) = struct.unpack_from("<bi", data)
    pos = 5
    mime = ""
    while data[pos:pos+2] != "\x00\x00":
        mime += data[pos:pos+2]
        pos += 2
    pos += 2
    description = ""
    while data[pos:pos+2] != "\x00\x00":
        description += data[pos:pos+2]
        pos += 2
    pos += 2
    image_data = data[pos:pos+size]
    return (mime.decode("utf-16-le"), image_data, type, description.decode("utf-16-le"))


def pack_image(mime, data, type=3, description=""):
    """
    Helper function to pack image data for a WM/Picture tag.
    See unpack_image for a description of the data format.
    """
    tag_data = struct.pack("<bi", type, len(data))
    tag_data += mime.encode("utf-16-le") + "\x00\x00"
    tag_data += description.encode("utf-16-le") + "\x00\x00"
    tag_data += data
    return tag_data


def find_cover(song_location):
    """Attempts to locate a cover image that would be associated with a given
    file.
    """
    # Try to get embedded cover art
    metadata = mutagen.File(song_location)
    pic = None
    if 'APIC:' in metadata.keys():
        pic = metadata.get('APIC:').data
    elif 'covr' in metadata.keys():
        pic = metadata.get('covr')[0]
    elif 'coverart' in metadata.keys():
        data = metadata.get('coverart')[0]
        pic = base64.b64decode(data)
    elif 'metadata_block_picture' in metadata.keys():
        data = metadata.get('metadata_block_picture')[0]
        pic = mutagen.flac.Picture(base64.b64decode(data)).data
    elif 'pictures' in metadata.keys():
        pic = metadata.get('pictures')[0].data
    elif 'WM/Picture' in metadata.keys():
        data = metadata.get('WM/Picture')[0].value
        pic = unpack_image(data)[1]
    else:
        try:
            for picture in metadata.pictures:
                if picture.type == 3:
                    pic = picture.data
                    break
        except:
            pass
    if pic:
        return pic

    # Search the song's directory for images that might be cover art
    try:
        # Get the path to the folder containing the song for which we need a
        # cover image
        path = os.path.dirname(song_location)
        # Look for any files in the path that are images and give them a score
        # based on their filename and append them to our results list.
        images = []
        for item in os.listdir(path):
            name, extension = os.path.splitext(item)
            if extension.lower()[1:] in ('jpg', 'png'):
                score = 0
                if name.lower() in ('cover', ):
                    score += 1
                images.append([score, os.path.join(path, item)])
        # Sort our images by score and return the highest one. Seems like a pretty
        # ham fisted approach, will need to refine this later.
        images.sort(reverse=True)
        with open(images[0][1], 'rb') as image_file:
            pic = image_file.read()
        return pic
    except:
        return None

#def resize_cover(song, cover, size):
    #"""Resizes the cover image for a specific song to a given size and caches
    #the resized image for any subsequent requests."""
    #logger.debug("resize_cover(song=%s, cover=%s, size=%s)" % (song, cover, size))
    ## This is the path to the resized image in the cache
    #img_path = os.path.join(cfg['CACHE_DIR'], str(size), hashlib.sha1(song['artist_hash'] + song['album_hash']).hexdigest() + '.jpg')
    ## Make sure our cache directory exists
    #if not os.path.exists(os.path.split(img_path)[0]):
        #os.makedirs(os.path.split(img_path)[0])
    #try:
        ## Try to create a file object pointing to the image in the cache
        #artwork = open(img_path, "rb")
        #artwork.close()
        #artwork = img_path
    #except:
        ## Load the source image file with PIL
        #image = Image.open(cover)
        ## Check if the image is larger than what the client asked for. If it
        ## is, we'll resize it. Otherwise we'll just send the original.
        #if image.size[0] > size or image.size[1] > size:
            ## Figure out the aspect ratio so we can maintain it
            #wpercent = (size/float(image.size[0]))
            #hsize = int((float(image.size[1])*float(wpercent)))
            ## Resize the image
            #image = image.resize((size,hsize), Image.ANTIALIAS)
            ## Save it to the cache so we won't have to do this again.
            #image.save(img_path)
            ## Create a file object pointing to the image in the cache
            #artwork = img_path
        #else:
            #artwork = cover
    #return artwork

class Cover(Resource, ResourceGetMixin):

    """Library resource class."""

    library = None

    def __init__(self):
        from blofeld.library.backends.mongo import Database
        self.library = Database()

    def _on_get(self, request, response, album):
        cursor = self.library.find({'album': album})
        if not cursor.count():
            response.status = '404 Not Found'
            return
        cover = find_cover(cursor[0]['location'])
        if not cover:
            response.status = '404 Not Found'
            return
        response.body = cover
        response.content_type = 'image/jpeg'
