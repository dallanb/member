import pytest

from src import services


@pytest.fixture(scope="function")
def seed_avatar():
    s3_filename = services.AvatarService().generate_s3_filename(member_uuid=str(pytest.member.uuid))
    pytest.avatar = services.AvatarService().create(s3_filename=s3_filename)
    services.MemberService().apply(instance=pytest.member, avatar=pytest.avatar)
