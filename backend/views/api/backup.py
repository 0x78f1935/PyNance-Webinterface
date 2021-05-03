from flask_classful import FlaskView, route
from flask import jsonify, request, Response

from sqlalchemy.ext.serializer import loads, dumps

from backend.utils.auth import login_required
from backend import db, pynance

import zipfile
import io

class BackupAPIView(FlaskView):
    
    decorators = [ login_required ]

    def get(self):
        from backend.models.bot import BotModel
        bot = BotModel.query.first()
        packed = [
            ('bot.txt', io.BytesIO(dumps(bot)),),
            ('status.txt', io.BytesIO(dumps(bot.status)),),
            ('config.txt', io.BytesIO(dumps(bot.config)),),
            ('orders.txt', io.BytesIO(dumps(bot.orders)),),
        ]

        if True if request.args.get('pwd', 'false') == 'true' else False:
            from backend.models.keys import KeysModel
            keys = KeysModel.query.all()
            packed.append(('keys.txt', io.BytesIO(dumps(keys))))
            from backend.models.system import SystemModel
            system = SystemModel.query.first()
            packed.append(('system.txt', io.BytesIO(dumps(system))))

        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
            for file_name, data in packed:
                zip_file.writestr(file_name, data.getvalue())

        return Response(
            zip_buffer.getvalue(),
            mimetype='application/zip',
            headers={'Content-Disposition': 'attachment;filename=pynance_backup.txt'}
        )

    def post(self):
        backup = None
        for filename in request.files:
            if filename == 'backup':
                try:
                    backup = request.files[filename]
                    if backup: break
                except Exception as e:
                    return jsonify({'succes': False, 'msg': 'Unable to read .pynance file'}), 200

        if backup is None: return jsonify({'succes': False, 'msg': 'Your backup seems to be empty'}), 200

        to_merge = []
        from backend.models.bot import BotModel
        with zipfile.ZipFile(backup) as zf:
            for backup_file in zf.filelist:
                with zf.open(backup_file.filename) as f:
                    data = f.read()

                from backend.models.status import StatusModel
                from backend.models.config import ConfigModel
                from backend.models.orders import OrdersModel
                from backend.models.system import SystemModel
                from backend.models.keys import KeysModel
                if 'bot' in backup_file.filename: to_merge.append(loads(data, BotModel.metadata, db.session))
                elif 'status' in backup_file.filename: to_merge.append(loads(data, StatusModel.metadata, db.session))
                elif 'config' in backup_file.filename: to_merge.append(loads(data, ConfigModel.metadata, db.session))
                elif 'system' in backup_file.filename: to_merge.append(loads(data, SystemModel.metadata, db.session))
                elif 'orders' in backup_file.filename: 
                    for item in loads(data):
                        to_merge.append(loads(dumps(item), OrdersModel.metadata, db.session))
                elif 'keys' in backup_file.filename:
                    for item in loads(data):
                        to_merge.append(loads(dumps(item), KeysModel.metadata, db.session))

        for item in to_merge:
            db.session.merge(item)
        db.session.commit()
        bot = BotModel.query.first()
        bot.update_data({'online': False})

        return jsonify({'succes': True, 'msg': 'Backup has been restored!'}), 200
