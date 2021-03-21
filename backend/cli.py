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
        from backend.models.preference import PreferenceModel
        from backend import db
        preference = PreferenceModel.query.first()
        if preference is not None:
            preference.authentication = False
            preference.password = ''
            preference.token = ''
            db.session.add(preference)
            db.session.commit()
            print('[PyNance] Master password has been reset')
        else: print('[PyNance] Could not reset master password')
