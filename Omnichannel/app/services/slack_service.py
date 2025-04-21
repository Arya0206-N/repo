from fastapi import HTTPException
from typing import Optional, Dict, Any
import logging
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from app.core.config import settings
from app.schemas.ticket import TicketCreate
from app.db.models import Ticket
from app.queues.producer import publish_message

logger = logging.getLogger(__name__)

class SlackService:
    def __init__(self):
        self.client = WebClient(token=settings.SLACK_BOT_TOKEN)
    
    async def handle_incoming_message(self, event: Dict[str, Any]) -> Optional[Ticket]:
        """
        Process incoming Slack message and create a support ticket
        
        Args:
            event: Slack event data
            
        Returns:
            Created ticket or None if not a support request
        """
        try:
            # Extract message details
            channel_id = event.get('channel')
            user_id = event.get('user')
            text = event.get('text')
            
            if not text or not channel_id or not user_id:
                return None
                
            # Create ticket data
            ticket_data = TicketCreate(
                channel="slack",
                channel_id=channel_id,
                user_id=user_id,
                message=text,
                raw_data=event
            )
            
            # Publish to classification queue
            await publish_message(
                queue="classification.queue",
                message=ticket_data.dict()
            )
            
            # Send acknowledgement
            await self.send_acknowledgement(channel_id)
            
            return ticket_data
            
        except Exception as e:
            logger.error(f"Error processing Slack message: {str(e)}")
            raise HTTPException(status_code=500, detail="Error processing Slack message")
    
    async def send_acknowledgement(self, channel_id: str):
        """Send acknowledgement message to user"""
        try:
            response = self.client.chat_postMessage(
                channel=channel_id,
                text="We've received your message and will get back to you shortly!"
            )
            return response
        except SlackApiError as e:
            logger.error(f"Error sending Slack acknowledgement: {str(e)}")
            raise HTTPException(status_code=500, detail="Error sending acknowledgement")
    
    async def send_response(self, ticket: Ticket, message: str):
        """Send response back to Slack channel"""
        try:
            response = self.client.chat_postMessage(
                channel=ticket.channel_id,
                text=message
            )
            return response
        except SlackApiError as e:
            logger.error(f"Error sending Slack response: {str(e)}")
            raise HTTPException(status_code=500, detail="Error sending response")