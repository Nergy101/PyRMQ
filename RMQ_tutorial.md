# install RMQ (Rabbit MQ)

https://www.rabbitmq.com/download.html


# Explanation
Rabbit MQ (RMQ) is like a (huge) Mailbox with sorting machines and messengers inside to make message M go from A to B.

A and B could be any programs or services written in:
- Python
- Java
- Ruby
- PHP
- C#
- JavaScript
- Go
- Elixir
- Objective-C
- Swift
- Spring AMQP

Thats quite a huge list.

For the tutorial we will look at Python. Although the process will be roughly the same for every language.
That is because it all uses RMQ and AMQP, ofcourse.

RMQ uses AMQP (Advanced Message Queuing Protocol) to deliver and distribute messages across these services.

HTTP is the HypterText Transfer Protocol, which is mostly blocking and quite slow due to internet.

The AMQP aims to be a fast, lightweight protocol for messaging, primarily in an ASYNC manner, although blocking-calls (RPC) are possible.

# Garbon of this tutorial:
https://jstobigdata.com/rabbitmq/elements-of-amqp/

Publisher -> any program that publishes (sends) messages to an Exchange

Exchange -> a "sorting centre" where all messages get published to, putting them in the right queues
    Fanout -> an Exchange that publishes a message to all queues it is bound to
    Direct -> an Exchange that adds a "routing-key" to send messages to specific queues
    Topic -> an Exchange that adds a "routing-key" with extra rules to do complex message routing

Routing Key -> used by exchanges like a kind of address to route a message to a queue

Binding -> a Link between a queue and an exchange

Queues -> a literal FIFO (First-In-First-Out) Queue that is possibly persistent

Consumer -> any program that consumes (process, handles, takes) messages from some queue(s)

Look at RMQ as a specialised database for messages.
