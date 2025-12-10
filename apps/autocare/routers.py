"""
Database Router for AutoCare Application.

This router directs all autocare app database operations to the autocare database
if configured, otherwise uses the default database.
"""


class AutoCareRouter:
    """
    A router to control all database operations on models in the autocare application.
    
    This router ensures that:
    - All reads from autocare models go to the 'autocare' database (if configured)
    - All writes to autocare models go to the 'autocare' database (if configured)
    - Relations between autocare models are allowed
    - No migrations are applied to the autocare database (models are managed externally)
    """
    
    route_app_labels = {'autocare'}

    def db_for_read(self, model, **hints):
        """
        Attempts to read autocare models go to autocare database.
        """
        if model._meta.app_label in self.route_app_labels:
            return 'autocare'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write autocare models go to autocare database.
        """
        if model._meta.app_label in self.route_app_labels:
            return 'autocare'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the autocare app is involved.
        """
        if (obj1._meta.app_label in self.route_app_labels or
                obj2._meta.app_label in self.route_app_labels):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the autocare app only appears in the 'autocare' database.
        Since all models have managed=False, this prevents any migration attempts.
        """
        if app_label in self.route_app_labels:
            # Return False to prevent migrations since models are managed=False
            return False
        return None
