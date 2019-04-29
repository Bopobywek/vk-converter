import os
import uuid
from pathlib import Path

import ffmpeg
from PIL import Image
from pydub import AudioSegment

PICTURE_SUPPORTED_FORMATS = ['WEBP', 'BMP', 'PPM',
                             'JPEG', 'TIFF', 'GIF', 'PNG', 'SGI', 'JPG']
AUDIO_SUPPORTED_FORMATS = ['MP3', 'WAV', 'OGG', 'FLAC', 'OPUS']
VIDEO_SUPPORTED_FORMATS = ['AVI', 'GIF', 'OGG', 'FLV', 'MKV', 'MP4']


class PictureConverter(object):

    def __init__(self, path, filename):
        self.convertations = {'BMP': self.to_bmp, 'GIF': self.to_gif, 'JPEG': self.to_jpeg, 'PNG': self.to_png,
                              'MSP': self.to_msp, 'PCX': self.to_pcx, 'PPM': self.to_ppm, 'SGI': self.to_sgi,
                              'TIFF': self.to_tiff, 'WEBP': self.to_webp, 'XBM': self.to_xbm,
                              'JPG': self.to_jpeg}
        self.path = path
        self.file_suffix = Path(filename).suffix
        self.filename = filename[:filename.rfind(Path(filename).suffix)]
        self.original_file = os.path.join(path, filename)

    def get_image_object(self):
        im = Image.open(self.original_file)
        rgb_im = im.convert('RGB')
        return rgb_im

    def convert(self, new_format):
        try:
            if self.original_file == os.path.join(self.path, '{}.{}'.format(self.filename, new_format.lower())):
                self.filename = '{}{}'.format(uuid.uuid4().hex, self.filename)
            func = self.convertations.get(new_format)
            func()
            os.remove(self.original_file)
            return {'old_file_path': self.original_file,
                    'new_file_path': os.path.join(self.path, '{}.{}'.format(self.filename, new_format.lower()))}
        except Exception as e:
            return e

    def to_bmp(self):
        self.get_image_object().save(os.path.join(self.path, '{}.bmp'.format(self.filename)))

    def to_gif(self):
        self.get_image_object().save(os.path.join(self.path, '{}.gif'.format(self.filename)))

    def to_jpeg(self):
        self.get_image_object().save(os.path.join(self.path, '{}.jpeg'.format(self.filename)))

    def to_png(self):
        self.get_image_object().save(os.path.join(self.path, '{}.png'.format(self.filename)))

    def to_msp(self):
        self.get_image_object().save(os.path.join(self.path, '{}.msp'.format(self.filename)))

    def to_pcx(self):
        self.get_image_object().save(os.path.join(self.path, '{}.pcx'.format(self.filename)))

    def to_ppm(self):
        self.get_image_object().save(os.path.join(self.path, '{}.ppm'.format(self.filename)))

    def to_sgi(self):
        self.get_image_object().save(os.path.join(self.path, '{}.sgi'.format(self.filename)))

    def to_tiff(self):
        self.get_image_object().save(os.path.join(self.path, '{}.tiff'.format(self.filename)))

    def to_webp(self):
        self.get_image_object().save(os.path.join(self.path, '{}.webp'.format(self.filename)))

    def to_xbm(self):
        self.get_image_object().save(os.path.join(self.path, '{}.xbm'.format(self.filename)))

    def to_ico(self):
        self.get_image_object().save(os.path.join(self.path, '{}.ico'.format(self.filename)))


class AudioConverter(object):

    def __init__(self, path, filename):
        self.convertations = {'MP3': self.to_mp3, 'WAV': self.to_wav, 'OGG': self.to_ogg, 'OPUS': self.to_opus,
                              'FLAC': self.to_flac}
        self.path = path
        self.file_suffix = Path(filename).suffix
        self.filename = filename[:filename.rfind(Path(filename).suffix)]
        self.original_file = os.path.join(path, filename)

    def get_audio_object(self):
        audio = AudioSegment.from_file(self.original_file)
        return audio

    def convert(self, new_format):
        try:
            if self.original_file == os.path.join(self.path, '{}.{}'.format(self.filename, new_format.lower())):
                self.filename = '{}{}'.format(uuid.uuid4().hex, self.filename)
            func = self.convertations.get(new_format)
            func()
            os.remove(self.original_file)
            return {'old_file_path': self.original_file,
                    'new_file_path': os.path.join(self.path, '{}.{}'.format(self.filename, new_format.lower()))}
        except Exception as e:
            return e

    def to_mp3(self):
        self.get_audio_object().export(os.path.join(self.path, '{}.mp3'.format(self.filename)), format='mp3')

    def to_wav(self):
        self.get_audio_object().export(os.path.join(self.path, '{}.wav'.format(self.filename)), format='wav')

    def to_ogg(self):
        self.get_audio_object().export(os.path.join(self.path, '{}.ogg'.format(self.filename)), format='ogg')

    def to_opus(self):
        self.get_audio_object().export(os.path.join(self.path, '{}.opus'.format(self.filename)), format='opus')

    def to_flac(self):
        self.get_audio_object().export(os.path.join(self.path, '{}.flac'.format(self.filename)), format='flac')


class VideoConverter(object):

    def __init__(self, path, filename):
        self.convertations = {'AVI': self.to_avi, 'GIF': self.to_gif, 'OGG': self.to_ogg,
                              'MP4': self.to_mp4, 'MKV': self.to_mkv, 'FLV': self.to_flv}
        self.path = path
        self.file_suffix = Path(filename).suffix
        self.filename = filename[:filename.rfind(Path(filename).suffix)]
        self.original_file = os.path.join(path, filename)

    def get_stream_object(self):
        stream = ffmpeg.input(self.original_file)
        return stream

    def convert(self, new_format):
        try:
            if self.original_file == os.path.join(self.path, '{}.{}'.format(self.filename, new_format.lower())):
                self.filename = '{}{}'.format(uuid.uuid4().hex, self.filename)
            func = self.convertations.get(new_format)
            ffmpeg.run(func())
            os.remove(self.original_file)
            return {'old_file_path': self.original_file,
                    'new_file_path': os.path.join(self.path, '{}.{}'.format(self.filename, new_format.lower()))}
        except Exception as e:
            return e

    def to_avi(self):
        return ffmpeg.output(self.get_stream_object(), os.path.join(self.path, '{}.avi'.format(self.filename)))

    def to_gif(self):
        return ffmpeg.output(self.get_stream_object(), os.path.join(self.path, '{}.gif'.format(self.filename)))

    def to_mkv(self):
        return ffmpeg.output(self.get_stream_object(), os.path.join(self.path, '{}.mkv'.format(self.filename)))

    def to_mp4(self):
        return ffmpeg.output(self.get_stream_object(), os.path.join(self.path, '{}.mp4'.format(self.filename)))

    def to_ogg(self):
        return ffmpeg.output(self.get_stream_object(), os.path.join(self.path, '{}.ogg'.format(self.filename)))

    def to_flv(self):
        return ffmpeg.output(self.get_stream_object(), os.path.join(self.path, '{}.flv'.format(self.filename)),
                             **{'c:v': 'libx264', 'crf': '28', 'ar': '22050'})


class Converter(object):

    def __init__(self, path, filename, new_format):
        self.path = path
        self.filename = filename
        self.new_format = new_format

    def convert(self):
        converter = None
        errors = list()
        if self.new_format.upper() in AUDIO_SUPPORTED_FORMATS:
            converter = AudioConverter(self.path, self.filename)
        elif self.new_format.upper() in VIDEO_SUPPORTED_FORMATS:
            converter = VideoConverter(self.path, self.filename)
        elif self.new_format.upper() in PICTURE_SUPPORTED_FORMATS:
            converter = PictureConverter(self.path, self.filename)
        if converter is not None:
            result = converter.convert(self.new_format)
            if not isinstance(result, dict):
                errors.append(result)
        return errors


if __name__ == '__main__':
    pass
