import os
from azure.servicebus import ServiceBusClient, ServiceBusMessage

CONNECTION_STR = os.environ["PRIMARY_CONNECTION_STRING"]
TOPIC_NAME = os.environ["SERVICEBUS_TOPIC"]
SUBSCRIPTION_NAME = os.environ["SERVICEBUS_SUBSCRIPTION"]


def send_single_message(sender):
    message = ServiceBusMessage("Single Message")
    sender.send_messages(message)
    print("Sent a single message")


def send_a_list_of_messages(sender):
    messages = [ServiceBusMessage("Message in list") for _ in range(5)]
    sender.send_messages(messages)
    print("Sent a list of 5 messages")


def send_batch_message(sender):
    batch_message = sender.create_message_batch()
    for _ in range(10):
        try:
            batch_message.add_message(ServiceBusMessage(
                "Message inside a ServiceBusMessageBatch"))
        except ValueError:
            # ServiceBusMessageBatch object reaches max_size.
            # New ServiceBusMessageBatch object can be created here to send more data.
            break
    sender.send_messages(batch_message)
    print("Sent a batch of 10 messages")


def send_demo_message(client):
    with client:
        sender = client.get_topic_sender(topic_name=TOPIC_NAME)
        with sender:
            send_single_message(sender)
            send_a_list_of_messages(sender)
            send_batch_message(sender)

    print("Done sending messages")
    print("-----------------------")
    return sender


def receive_demo_message(client):
    with client:
        receiver = client.get_subscription_receiver(
            topic_name=TOPIC_NAME, subscription_name=SUBSCRIPTION_NAME, max_wait_time=5)
        with receiver:
            for msg in receiver:
                # print("Received: " + str(msg))
                yield msg
                receiver.complete_message(msg)


def main():

    client = ServiceBusClient.from_connection_string(
        conn_str=CONNECTION_STR, logging_enable=True)

    # Send message
    _ = send_demo_message(client)

    # Receive message
    # messages = receive_demo_message(client)

    # for msg in messages:
    #     print(msg)


if __name__ == "__main__":
    main()
