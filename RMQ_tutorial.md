# install RMQ (Rabbit MQ)

https://www.rabbitmq.com/download.html

You should also have Python 3.x installed

For running rust you will need rustup: https://rustup.rs/

I trust you to be able to run either Python or Rust inside a terminal window. Otherwise, Google is your best friend.
* dont forget to install `requirements.txt` with pip(3)
* or run `pip install pika`
* use `cargo run` command inside either `RustReceiver` or `RustSender` (requires rustup to be installed)

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
- Rust

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


# Lets start by looking at Python
## sending message
Open sender.py, and inspect it.

Firstly we see a block of code to get a connection and a channel from the connection.

All of the "traffic" will be delivered and received through this channel.

In the next code block we see `exchange_declare` which means we will
create 3 exchanges (mailing-sort-centers) of the 3 different types there are.
What each one does. can be read above in the Garbon section.

Then there's 3 blocks where we do `basic_publish` in which we are sending a string
to all of these exchanges.

the logs exchange is a `fanout` exchange so any message we send here gets broadcasted to all bound queues (more on this later), ignoring the routing_key.

the messages exchange is `direct` and messages get routed to the queues with
the same routing_key. 
So both the message and queue have the same routing_key.

the topic_messages exchange is `topic` based and enables a special regex-like
syntax for the routing_key for more complex routing.

`topic` routing_keys are seperated by a `.` mostly on "domain" like so:

Java.UserService.User.Registered

Lets say this message gets published whenever a new user is registered by our Java Backend:
now we can listen for this in multiple backend services to do multiple things:  
  - send him/her a mail through a NodeJS backend  
  - Add the user in our Microsoft Active Directory with C#  
  - etc.  

## receiving fanout messages
open `fanout_server.py`  

we have the same connection block,  
then we decalre our exchange **again**!  

This is considered more safe and a good practise.  
You might not know which of the 2 services would be up first.

Then, we use `queue_declare` to create a loose queue. It is not bound to any exchange and so it will never actually be used. Lets change that:

Lets `queue_bind` our queue to our exchange.
From now on any messages that enter the `logs-exchange` may be routed
to our queue.

then, by calling `basic_consume` we can listen for any messages that get inside our
queue and take it off the queue. (which is First-In-First-Out (FIFO))

And then ofcourse do something with the message.

Keep in mind that these messages will probably be some JSON of objects/events.

## receiving direct messages
open `direct_server.py`

We are gonna connect,  
declare the exchange "messages",  
create 1 queue,  
but bind 2 times!  

So we are making 1 queues but binding it 2 times with the routing_key "red" and "white".

So any published message to this exchange "messages" with the routing_key "red" or "white" will be routed to our 1 queue.

Then, in our callback function, you can see that we will print something out
based on the routing_key. This is one way of doing it. It's also common to
send JSON with a "Type" property which says to what class/object the message should
be serialized.

## receiving topic messages
open `topic_server.py`

we are gonna connect,  
declare the exchange,  
create our own queue,  
bind it to the exchange with the routing_key "JavaBackend.*"  
so only messages will be added to the queue with routing_key: "JavaBackend.<some_other_SINGLE_word>"  

like so:  
 - JavaBackend.StuffHappened  
 - JavaBackend.OtherStuffHappened  
NOT:  
 - JavaBackend.Stuff.Happened  
 - JavaBackend  


and then we can print out the message again after we have started consuming the queue.

# Using another language
I've chosen Rust as I am currently trying to learn it. What an adventure.  

open `RustReceiver/src/main.rs`

This file explains itself. Other than that it is a Rust program that listens for any messages on the Fanout logs Exchange.
The "system" and "order" of things is about the same. This counts for almost all of the languages. The general idea and manner of working is the same.

open `RustSender/src/main.rs`  

This file explains itself as well. It firstly sends 10 messages to the 'messages' exchange and then sends 100 messages to the fanout 'logs' exchange.


Now if you run the rustreceiver and the python sender in loose terminals, you could see that the 2 can interact.

Even by running any of the python `*_server.py` files and then the `sender.py` in loose terminals you can demonstrate 2 services interacting with one another.

# Event Driven Architecture & Microservices
These are VERY HEAVY subjects, very complex, very advanced.

IF you are really interested how stuff like Amazon/Netflix work...

Give these a read. Its a collection of patterns and ideas of how it *generally* works.
https://martinfowler.com/articles/201701-event-driven.html

Here are some books to download about microservices-architecture (which uses event driven architecture mostly)
https://dotnet.microsoft.com/learn/aspnet/microservices-architecture

Ofcourse you can come to me and ask away. I can talk/explain about this for hours :)

