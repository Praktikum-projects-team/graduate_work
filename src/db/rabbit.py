from aio_pika import ExchangeType, connect_robust

from core.config import rm_config


async def get_rabbit(exchange_name: str, queue_name: str):
    connection = await connect_robust(
        host=rm_config.rm_host,
        port=rm_config.rm_port,
        login=rm_config.rm_user,
        password=rm_config.rm_password,
    )
    channel = await connection.channel()
    exchange = await channel.declare_exchange(
        name=exchange_name,
        type=ExchangeType.FANOUT,
        durable=True,
    )
    queue = await channel.declare_queue(queue_name)
    await queue.bind(exchange, '')
    return connection, queue