import logging

from src.services import MemberService, StatService


def create_stat():
    logging.info("Starting create_stat...")
    member_service = MemberService()
    stat_service = StatService()
    members = member_service.find()
    for member in members.items:
        logging.info(member.uuid)
        _ = stat_service.create(member=member)
    logging.info("...Finishing create_stat")
