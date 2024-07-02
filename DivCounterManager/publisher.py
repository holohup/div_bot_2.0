from dapr.aio.clients import DaprClient
import logging

logger = logging.getLogger(__name__)


async def publish_log_message(data: str, config):
    logger.info(f'Publishing {data} to "{config.channel_name}" topic')
    async with DaprClient() as client:
        await client.publish_event(
            pubsub_name=config.pubsub_name,
            topic_name=config.channel_name,
            data=data,
            data_content_type='application/json',
        )
