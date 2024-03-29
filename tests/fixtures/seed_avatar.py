import pytest

from src import services


@pytest.fixture(scope="function")
def seed_avatar():
    s3_filename = services.AvatarService().generate_s3_filename(member_uuid=str(pytest.member.uuid))
    pytest.avatar = services.AvatarService().create(s3_filename=s3_filename, member=pytest.member)


@pytest.fixture(scope="function")
def seed_other_avatar():
    s3_filename = services.AvatarService().generate_s3_filename(member_uuid=str(pytest.other_member.uuid))
    pytest.other_avatar = services.AvatarService().create(s3_filename=s3_filename, member=pytest.other_member)
