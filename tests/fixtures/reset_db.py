import pytest

from bin import init_status
from src import db, common


@pytest.fixture(scope='function')
def reset_db():
    # delete
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        db.session.execute(table.delete())
    db.session.expunge_all()
    db.session.commit()
    # create
    db.create_all()
    db.session.commit()
    # load
    init_status(status_enums=common.StatusEnum)
