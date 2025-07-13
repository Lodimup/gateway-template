"""
RabbitMQ brokers
"""

from faststream.rabbit import RabbitBroker

from app.app_settings import APP_SETTINGS

faststream_broker = RabbitBroker(APP_SETTINGS.FASTSTREAM_BROKER_URL)
