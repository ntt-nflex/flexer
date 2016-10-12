import base64
import tempfile
import zipfile

from flexer.utils import read_module


class NflexClient(object):
    def __init__(self, cmp_client):
        self.cmp_client = cmp_client

    def upload(self,
               name,
               description,
               event_source,
               sync,
               zip_file):
        file_type = 'zip' if zip_file else 'inline'
        data = {
            'name': name,
            'description': description,
            'file_type': file_type,
            'event_source': event_source,
            'source_code': '',
            'language': 'python',
            'sync': sync
        }
        if file_type == 'inline':
            data['source_code'] = read_module("main.py")
            return self._post('/modules', data=data)

        elif file_type == 'zip':
            module = self._post('/modules', data=data).json()
            with open(zip_file, 'rb') as zf:
                self._upload_zipfile(module['id'], zf)

            return module

    def update(self, module_id, zip_file):
        file_type = 'zip' if zip_file else 'inline'
        data = {'file_type': file_type}
        if file_type == 'inline':
            data['source_code'] = read_module("main.py")
            return self._patch('/modules/%s' % module_id, data=data)

        elif file_type == 'zip':
            self._patch('/modules/%s' % module_id, data=data)
            with open(zip_file, 'rb') as zf:
                return self._upload_zipfile(module_id, zf)

    def list(self):
        return self._get('/modules')

    def download(self, module_id):
        module = self._get('/modules/%s' % module_id)
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
        f.write(base64.b64decode(payload['file']))
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

    def _upload_zipfile(self, module_id, zf):
        return self._post_file('/modules/%s/zipfile' % module_id,
                               zip_file=zf)

    def _get(self, path, params=None):
        if params is None:
            params = {}

        response = self.cmp_client.get(path, params=params)
        response.raise_for_status()
        return response.json()

    def _post(self, path, data):
        response = self.cmp_client.post(path, data)
        response.raise_for_status()
        return response.json()

    def _post_file(self, path, zip_file):
        response = self.cmp_client.post_file(path, zip_file)
        response.raise_for_status()
        return response.json()

    def _patch(self, path, data):
        response = self.cmp_client.patch(path, data=data)
        response.raise_for_status()
        return response.json()
