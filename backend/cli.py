from flask import current_app
import pathlib


def register(app):
    @app.cli.group()
    def password():
        """
        Tooling for passwords
        """
        pass

    @password.command()
    def reset():
        """
        Reset master password
        """
        from backend.models.system import SystemModel
        from backend import db
        system = SystemModel.query.first()
        if system is not None:
            system.authentication = False
            system.tos=False
            system.password = ''
            system.token = ''
            db.session.add(system)
            db.session.commit()
            print('[PyNance] Master password has been reset')
        else: print('[PyNance] Could not reset master password')
