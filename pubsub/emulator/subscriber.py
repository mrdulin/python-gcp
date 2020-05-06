def create_subscription(project_id, topic_name, subscription_name):
    from google.cloud import pubsub_v1

    subscriber = pubsub_v1.SubscriberClient()
    topic_path = subscriber.topic_path(project_id, topic_name)
    subscription_path = subscriber.subscription_path(
        project_id, subscription_name
    )

    subscription = subscriber.create_subscription(
        subscription_path, topic_path
    )

    print("Subscription created: {}".format(subscription))

    subscriber.close()


def receive_messages(project_id, subscription_name, timeout=None):
    from google.cloud import pubsub_v1
    import datetime

    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(
        project_id, subscription_name
    )

    def callback(message):
        date = datetime.datetime.now().isoformat()
        print("[{}] Received message: {}".format(date, message))
        message.ack()

    streaming_pull_future = subscriber.subscribe(
        subscription_path, callback=callback
    )
    print("Listening for messages on {}..\n".format(subscription_path))

    with subscriber:
        try:
            # When `timeout` is not set, result() will block indefinitely,
            # unless an exception is encountered first.
            streaming_pull_future.result(timeout=timeout)
        except Exception as ex:
            subscriber.close()
            raise
        finally:
            streaming_pull_future.cancel()


if __name__ == '__main__':
    import os
    import sys

    project_id = os.getenv('PUBSUB_PROJECT_ID')
    argv = sys.argv[1:]
    command = argv[0]

    if command == 'create':
        topic_name = argv[1]
        subscription_name = argv[2]
        create_subscription(project_id, topic_name, subscription_name)
    elif command == 'receive':
        subscription_name = argv[1]
        receive_messages(project_id, subscription_name)
