import sqlalchemy

import os
__module_path = os.path.dirname(__file__)

engine = sqlalchemy.create_engine('sqlite:///{0}/morphology.db'.format(__module_path), echo=False)