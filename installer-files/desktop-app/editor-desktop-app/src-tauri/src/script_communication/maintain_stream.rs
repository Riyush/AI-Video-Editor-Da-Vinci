use std::collections::HashMap;
use std::io::ErrorKind::WouldBlock;
use std::io::{BufRead, BufReader, Write};
use std::os::unix::net::UnixStream;
use std::sync::mpsc::Receiver;
use std::{thread, time::Duration};
use tauri::{AppHandle, Emitter}; // Needed for `emit_all`
use serde_json::Value;

use crate::script_communication::initial_connect::*;
use crate::script_communication::receive_socket_message::socket_response_handler;
use crate::script_communication::send_socket_message::send_message_via_socket;

/*  This function takes ownership of the socket, passes it to a spawned thread
   and continuously checks for:
       * messages from the main thread originating from the UI
       * messages from the Unix socket originating from the script
*/

pub fn check_stream(
    stream_option: Option<UnixStream>,
    app_handle: tauri::AppHandle,
    receiver: Receiver<Value>,
) {
    match stream_option {
        Some(stream) => {
            // Case where script has run
            maintain_socket_connection(stream, app_handle, receiver);
        }
        None => {
            // Case where script hasn't run, periodically try to establish connection and rerun maintain_socket_connection
            loop {
                // Continuously try to reconnect
                // Small sleep to prevent CPU from spinning
                println!("Attempting Connection");
                thread::sleep(Duration::from_millis(5000));

                let path_result = get_script_socket_path();
                let mut new_stream = attempt_connection(path_result, app_handle.clone());

                if let Some(stream) = new_stream {
                    // if we get a stream,
                    //then we jump to maintain which takes over execution
                    // If we don't the loop waits 5 seconds then tries again.

                    maintain_socket_connection(stream, app_handle.clone(), receiver);
                    // After getting a stream, we need to properly end this loop's execution
                    break; // Exit the loop after successful reconnection
                }
            }
        }
    }
}
pub fn maintain_socket_connection(
    mut stream: UnixStream,
    app_handle: tauri::AppHandle,
    receiver: Receiver<Value>,
) {
    stream
        .set_nonblocking(true)
        .expect("Couldn't set stream to non-blocking");
    let mut reader = BufReader::new(stream.try_clone().expect("Failed to clone stream"));

    loop {
        // 👂 Check for messages from the main thread's event_sender (non-blocking)
        if let Ok(msg_from_frontend) = receiver.try_recv() {

            // The user has sent an edit job via the frontend here.
            println!("Main thread says: {:#?}", msg_from_frontend);

            // Process the message into a Hashmap<String, String> to easily pass into send_message_via_socket().
            if let Value::Object(map) = msg_from_frontend {
                let processed: HashMap<String, String> = map.into_iter().filter_map(|(key, value)| {

                    let string_val = match value {
                    Value::Bool(b) => Some(b.to_string()),              // "true"/"false"
                    Value::String(s) => Some(s),                        // keep as-is
                    Value::Number(n) => Some(n.to_string()),            // optional: keep numbers
                    Value::Null => None,                                // optional: skip nulls
                    other => Some(other.to_string()),                   // optional: stringify anything else
                    };
                    string_val.map(|v| (key, v))
                }).collect();

                println!("Processed config: {:?}", processed);

                // Now we pass processed as a paramter to send_socket_message which is meant 
                let message_type = String::from("Basic-Edit-Job");
                send_message_via_socket(&mut stream, message_type, processed);
                
            } else {
                    eprintln!("Expected a JSON object");
                }
        }

        // 👂 Check for messages from the script (non-blocking read for now)
        let mut response = String::new();
        match reader.read_line(&mut response) {
            Ok(0) => {
                // Case where the script disconnects:
                println!("Script disconnected.");
                break;
            }
            Ok(_) => {
                // NEED to implement a response handler function to pass the message to
                socket_response_handler(response, app_handle.clone());
            }
            Err(ref e) if e.kind() == WouldBlock => {
                // No message yet — just skip this iteration to not block the loop
            }
            Err(e) => {
                eprintln!("Error: {}", e)
            }
        }
        // Small sleep to prevent CPU from spinning
        thread::sleep(Duration::from_millis(100));
    }
}
