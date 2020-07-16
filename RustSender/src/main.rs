use amiquip::{
    Connection, Exchange, ExchangeDeclareOptions, ExchangeType, Publish, QueueDeclareOptions,
    Result,
};
use std::fs;
use std::fs::File;
use std::io::Read;

fn main() -> Result<()> {
    // Open connection.
    let mut connection = Connection::insecure_open("amqp://localhost:5672")?;

    // Open a channel - None says let the library choose the channel ID.
    let channel = connection.open_channel(None)?;

    let direct_exchange = channel.exchange_declare(
        ExchangeType::Direct,
        "messages",
        ExchangeDeclareOptions::default(),
    )?;
    for i in 1..=10 {
        direct_exchange.publish(Publish::new(
            format!("hello there: {}", i).as_bytes(),
            "red",
        ))?;
    }

    let mut contents = String::new();
    let file = File::open("number.txt");

    let mut file = match file {
        Ok(f) => f,
        Err(_err) => File::create("number.txt").expect("couldn't create file"),
    };

    file.read_to_string(&mut contents); //.expect("couldnt read to string");

    println!("{}", contents);

    let number = contents.parse::<i32>();

    let mut number = match number {
        Ok(number) => number,
        ParseIntError => 0,
        Err(error) => panic!("Problem opening the file: {:?}", error),
    };

    // Declare the fanout exchange we will bind to.
    let exchange = channel.exchange_declare(
        ExchangeType::Fanout,
        "logs",
        ExchangeDeclareOptions::default(),
    )?;

    for i in 1..=100 {
        // Publish a message to the "hello" queue.
        exchange.publish(Publish::new(
            format!("hello from rust {}", &number + i).as_bytes(),
            "",
        ))?;
    }

    if number == 0 {
        number += 100;
    } else if number > 0 {
        number += 100;
    } else {
        number = 0;
    }
    println!("{}", format!("{}", number.to_string()));

    // save to file
    fs::write("number.txt", number.to_string()).expect("Unable to write file");

    connection.close()
}
