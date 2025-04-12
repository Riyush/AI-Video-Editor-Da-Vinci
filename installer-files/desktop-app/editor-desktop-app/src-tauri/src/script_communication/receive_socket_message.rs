use std::os::unix::net::UnixStream;

/* This function acts as a handler receiving socket messages and calling 
    send_socket_message as needed to communicate with the script */
pub fn socket_response_handler(response:String){
    // Consider that in the future, all responses will be in JSON format
    match response{
        _ => {
            println!("Response from script: {}", response);
        }
    }
}