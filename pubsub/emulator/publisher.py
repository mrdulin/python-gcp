
import asyncio
from time import sleep


def create_topic(project_id, topic_name):
    from google.cloud import pubsub_v1

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_name)

    topic = publisher.create_topic(topic_path)

    print("Topic created: {}".format(topic))


def publish(publisher, topic_path, data):
    sleep(1)
    return publisher.publish(topic_path, data=data)


def publish_messages(project_id, topic_name):
    from google.cloud import pubsub_v1
    from google.cloud.pubsub import types
    import datetime

    publisher = pubsub_v1.PublisherClient(
        batch_settings=types.BatchSettings(max_messages=10)
    )
    topic_path = publisher.topic_path(project_id, topic_name)

    aws = []
    for n in range(1, 50):
        date = datetime.datetime.now().isoformat()
        data = u"Message number {}".format(n)
        data = data.encode('utf-8')
        # future = publisher.publish(topic_path, data=data)
        future = publish(publisher, topic_path, data)
        # aw = ensure_future(future)
        # aws.append(aw)
        print("[{}]".format(date), future.result())

    # await asyncio.gather(*aws)

    print("Published messages.")


def ensure_future(futureLike):
    futureLike._asyncio_future_blocking = True
    futureLike.__class__._asyncio_future_blocking = True
    s2 = asyncio.wrap_future(futureLike)

    return asyncio.ensure_future(s2)


if __name__ == '__main__':
    import os
    import sys

    switch = {
        'create': create_topic,
        'publish': publish_messages
    }
    argv = sys.argv[1:]
    command = argv[0]
    topic_name = argv[1]
    project_id = os.getenv('PUBSUB_PROJECT_ID')

    switch[command](project_id, topic_name)
