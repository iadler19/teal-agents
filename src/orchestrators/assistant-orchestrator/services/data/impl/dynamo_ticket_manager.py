import time
import uuid

from ska_utils import AppConfig, strtobool

from configs import TA_VERIFY_IP, TA_ENVIRONMENT
from data.ticket_manager import TicketManager
from model.dynamo.ticket import Ticket as DynamoTicket
from model.responses import VerifyTicketResponse


class DynamoTicketManager(TicketManager):
    def __init__(self):
        cfg = AppConfig()
        self.verify_ip = strtobool(str(cfg.get(TA_VERIFY_IP.env_name)))

        if cfg.get(TA_ENVIRONMENT.env_name) == "local":
            if not DynamoTicket.exists():
                DynamoTicket.create_table(
                    read_capacity_units=1, write_capacity_units=1, wait=True
                )

    def verify_ticket(
        self, orchestrator_name: str, ticket: str, ip_address: str
    ) -> VerifyTicketResponse:
        try:
            ticket = DynamoTicket.get(orchestrator_name, ticket)
            if ticket.used:
                return VerifyTicketResponse(is_valid=False, user_id=None)
            if self.verify_ip and ticket.ip_address != ip_address:
                return VerifyTicketResponse(is_valid=False, user_id=None)
            if time.time() - ticket.timestamp > 60:
                return VerifyTicketResponse(is_valid=False, user_id=None)
            ticket.used = True
            ticket.save()
            return VerifyTicketResponse(is_valid=True, user_id=ticket.user_id)
        except DynamoTicket.DoesNotExist:
            return VerifyTicketResponse(is_valid=False, user_id=None)

    def create_ticket(
        self, orchestrator_name: str, user_id: str, ip_address: str
    ) -> str:
        ticket = DynamoTicket(
            orchestrator=orchestrator_name,
            ticket=str(uuid.uuid4()),
            user_id=user_id,
            ip_address=ip_address,
            timestamp=time.time(),
            used=False,
        )
        ticket.save()
        return ticket.ticket
