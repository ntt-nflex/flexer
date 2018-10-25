import base64
import json
import os
import tempfile
import zipfile
from datetime import datetime, timedelta

from flexer.utils import read_module

LANG_EXT = {
    "javascript": "js",
    "python": "py",
    "python3": "py",
}


class NflexClient(object):
    def __init__(self, cmp_client):
        self.cmp_client = cmp_client

    def get(self, module_id):
        return self._get('/modules/%s' % module_id).json()

    def execute(self, module_id, handler, is_async, event):
        data = {
            'async': is_async,
            'handler': "main.%s" % handler,
            'event': json.loads(event),
        }
        return self._post('/modules/%s/execute' % module_id, data=data)

    def upload(self,
               name,
               description,
               event_source,
               language,
               sync,
               zip_file):
        file_type = 'zip' if zip_file else 'inline'
        data = {
            'name': name,
            'description': description,
            'file_type': file_type,
            'event_source': event_source,
            'source_code': '',
            'language': language,
            'sync': sync
        }
        if file_type == 'inline':
            mname = "main.{}".format(LANG_EXT.get(language) or "py")
            data['source_code'] = read_module(mname)
            return self._post('/modules', data=data)

        elif file_type == 'zip':
            module = self._post('/modules', data=data)
            fname = os.path.basename(zip_file)
            with open(zip_file, 'rb') as zf:
                self._upload_zipfile(module['id'], zf, fname)

            return module

    def update(self, module_id, zip_file, language, description=None):
        file_type = 'zip' if zip_file else 'inline'
        data = {'file_type': file_type}
        if description is not None:
            data['description'] = description

        if language is not None:
            data['language'] = language

        if file_type == 'inline':
            mname = "main.{}".format(LANG_EXT.get(language) or "py")
            data['source_code'] = read_module(mname)
            return self._patch('/modules/%s' % module_id, data=data)

        elif file_type == 'zip':
            self._patch('/modules/%s?nosync=true' % module_id, data=data)
            fname = os.path.basename(zip_file)
            with open(zip_file, 'rb') as zf:
                return self._upload_zipfile(module_id, zf, fname)

    def list(self):
        params = {}
        response = self._get('/modules', params=params)
        modules = response.json()
        read = len(modules)
        total = int(response.headers.get('x-total-count', 0))
        while read < total:
            params['page'] = int(response.headers['x-page']) + 1
            response = self._get('/modules', params=params)
            modules += response.json()
            read = len(modules)

        return modules

    def delete(self, module_id):
        return self._delete('/modules/%s' % module_id)

    def logs(self, module_id):
        end = datetime.utcnow()
        start = end - timedelta(hours=24)

        params = {
            "resource_id": "nflex-module-{}".format(module_id),
            "start": start.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "end": end.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "order": "asc",
        }
        return self._get('/logs', params=params).json()

    def download(self, module_id):
        module = self._get('/modules/%s' % module_id).json()
        file_type = module['file_type']
        if file_type in ('zip', 'github'):
            self._download_zipfile(module)

        elif file_type == 'inline':
            self._download_inline_code(module)

    def _download_inline_code(self, module):
        file_name = 'main.py'
        with open(file_name, 'wb') as f:
            f.write(module['source_code'])

    def _download_zipfile(self, module):
        f = tempfile.NamedTemporaryFile(mode='wb', suffix='.zip')
        payload = self._get('/modules/%s/zipfile' % module['id'])
        f.write(base64.b64decode(payload.text))
        f.flush()
        with zipfile.ZipFile(f.name, 'r') as zf:
            args = {'path': '.'}
            if module['file_type'] == 'github':
                args['members'] = self._remove_top_level_dir(zf)

            zf.extractall(**args)

    def _remove_top_level_dir(self, zfile):
        for zipinfo in zfile.infolist()[1:]:  # omit the directory (1st one)
            zipinfo.filename = '/'.join(zipinfo.filename.split('/')[1:])
            yield zipinfo

    def _upload_zipfile(self, module_id, zf, file_name):
        return self._post_file('/modules/%s/zipfile' % module_id,
                               zip_file=zf,
                               file_name=file_name)

    def _get(self, path, params=None):
        if params is None:
            params = {}

        response = self.cmp_client.get(path, params=params)
        response.raise_for_status()
        return response

    def _post(self, path, data):
        response = self.cmp_client.post(path, data)
        response.raise_for_status()
        return response.json()

    def _post_file(self, path, zip_file, file_name):
        response = self.cmp_client.post_file(path, zip_file, file_name)
        response.raise_for_status()
        return response.json()

    def _patch(self, path, data):
        response = self.cmp_client.patch(path, data=data)
        response.raise_for_status()
        return response.json()

    def _delete(self, path):
        response = self.cmp_client.delete(path)
        response.raise_for_status()
        return response
