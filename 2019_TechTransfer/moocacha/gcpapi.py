from google.cloud import speech, storage
from google.cloud.speech import enums
from google.cloud.speech import types

import os
import json
import collections
from pydub import AudioSegment
from django.conf import settings

def get_blobs(bucket_name, blob_name):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    
    blob = bucket.get_blob(blob_name)
    return blob

def list_blobs(bucket_name):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    
    blobs = bucket.list_blobs()
    return blobs
        

def list_blobs_with_prefix(bucket_name, prefix, delimiter=None):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    
    blobs = bucket.list_blobs(prefix=prefix, delimiter=delimiter)
    return blobs

def download_blob(bucket_name, source_blob_name, destination_file_name):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)

    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)

def make_blob_public(bucket_name, blob_name):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.get_blob(blob_name)
    if blob is None:
        return blob
    else:
        blob.make_public()
        return blob.public_url

def blob_metadata(bucket_name, blob_name):
    """Prints out a blob's metadata."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.get_blob(blob_name)

    print('Blob: {}'.format(blob.name))
    print('Bucket: {}'.format(blob.bucket.name))
    print('Storage class: {}'.format(blob.storage_class))
    print('ID: {}'.format(blob.id))
    print('Size: {} bytes'.format(blob.size))
    print('Updated: {}'.format(blob.updated))
    print('Generation: {}'.format(blob.generation))
    print('Metageneration: {}'.format(blob.metageneration))
    print('Etag: {}'.format(blob.etag))
    print('Owner: {}'.format(blob.owner))
    print('Component count: {}'.format(blob.component_count))
    print('Crc32c: {}'.format(blob.crc32c))
    print('md5_hash: {}'.format(blob.md5_hash))
    print('Cache-control: {}'.format(blob.cache_control))
    print('Content-type: {}'.format(blob.content_type))
    print('Content-disposition: {}'.format(blob.content_disposition))
    print('Content-encoding: {}'.format(blob.content_encoding))
    print('Content-language: {}'.format(blob.content_language))
    print('Metadata: {}'.format(blob.metadata))
    print("Temporary hold: ",
          'enabled' if blob.temporary_hold else 'disabled')
    print("Event based hold: ",
          'enabled' if blob.event_based_hold else 'disabled')
    if blob.retention_expiration_time:
        print("retentionExpirationTime: {}"
              .format(blob.retention_expiration_time))


def video_to_audio(filename):
    video_file_path = os.path.join(settings.MEDIA_ROOT, 'video/')
    audio_file_path = os.path.join(settings.MEDIA_ROOT, 'audio/')

    filename = filename + '.mp4'
    audio_file = AudioSegment.from_file(os.path.join(video_file_path, filename), 'mp4')
    audio_file_mono = audio_file.set_channels(1)

    filename = filename.split('.')[:-1][0]
    filename = filename + '.flac'
    audio_file_mono.export(os.path.join(audio_file_path, filename), 'flac')

def audio_to_script(filename):
    conv = lambda duration : '%d.%d' % (duration.seconds, duration.nanos/100000000)
    uri = 'gs://' + settings.BUCKET_NAME + '/audio/' + filename + '.flac'
    script = collections.OrderedDict()
    script_file_path = os.path.join(settings.MEDIA_ROOT, 'script/')
    
    # audio to script configuration
    client = speech.SpeechClient()
    audio = types.RecognitionAudio(uri=uri)
    config = types.RecognitionConfig(
        encoding='FLAC',
        sample_rate_hertz=44100,
        language_code='ko-KR',
        enable_word_time_offsets=True
    )
    # recognition
    operation = client.long_running_recognize(config, audio)
    response = operation.result()
    
    # make script dict
    script['speech'] = list()
    script['inverted_idx'] = dict()
    nounWords = list()
    mecab = Mecab()
    for result in response.results:
        speechRecognition = result.alternatives[0]
        script['speech'].append({
            'transcript' : speechRecognition.transcript,
            'offset' : [conv(speechRecognition.words[0].start_time), conv(speechRecognition.words[-1].end_time)]
        })
        for word in speechRecognition.words:
            key = word.word
            noun = ''.join(mecab.nouns(key))
            for i in noun:
                nounWords.append(i)
            # 형태소 분석이 추가될 수 있음.
            if noun == '':
                pass
            else:
                if noun not in script['inverted_idx'].keys():
                    script['inverted_idx'][noun] = list()
                script['inverted_idx'][noun].append(conv(word.start_time))

    # make script file
    with open(os.path.join(script_file_path, filename+'.json'), 'w', encoding='utf-8') as script_file:
        json.dump(script, script_file, ensure_ascii=False, indent='\t')


