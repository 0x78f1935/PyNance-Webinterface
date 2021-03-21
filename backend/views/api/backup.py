from flask_classful import FlaskView, route
from flask import jsonify, request, Response

from sqlalchemy.ext.serializer import loads, dumps

from backend.utils.auth import login_required
from backend import db, pynance

class BackupAPIView(FlaskView):
    
    decorators = [ login_required ]

    def get(self):
        from backend.models.orders import OrderModel
        query = OrderModel.query.all()
        serialized_data = dumps(query)
        # return jsonify({'test': 'succes', 'serialized_data': serialized_data}), 200
        return Response(
            serialized_data,
            mimetype='text/plain',
            headers={'Content-Disposition': 'attachment;filename=pynance_backup.txt'}
        )

    def post(self):
        from backend.models.orders import OrderModel
        data = None
        for filename in request.files:
            if filename == 'backup':
                try:
                    file = request.files[filename]
                    file.seek(0)
                    data = file.read()
                    if data: break
                except Exception as e:
                    return jsonify({'succes': False}), 200
        
        if data is None: return jsonify({'succes': False}), 200

        data_to_import = loads(data, OrderModel.metadata, db.session)
        for item in data_to_import:
            db.session.merge(item)
            db.session.commit()
        return jsonify({'succes': True}), 200
