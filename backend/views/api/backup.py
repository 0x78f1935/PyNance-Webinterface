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
        # serialized_data = dumps(bot)
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
            for file_name, data in packed:
                zip_file.writestr(file_name, data.getvalue())

        # return jsonify({'test': 'succes', 'serialized_data': serialized_data}), 200
        return Response(
            zip_buffer.getvalue(),
            mimetype='application/zip',
            headers={'Content-Disposition': 'attachment;filename=pynance_backup.txt'}
        )

    def post(self):
        # from backend.models.orders import OrderModel
        # data = None
        # for filename in request.files:
        #     if filename == 'backup':
        #         try:
        #             file = request.files[filename]
        #             file.seek(0)
        #             data = file.read()
        #             if data: break
        #         except Exception as e:
        #             return jsonify({'succes': False}), 200
        
        # if data is None: return jsonify({'succes': False}), 200

        # data_to_import = loads(data, OrderModel.metadata, db.session)
        # for item in data_to_import:
        #     db.session.merge(item)
        #     db.session.commit()
        return jsonify({'succes': True}), 200
