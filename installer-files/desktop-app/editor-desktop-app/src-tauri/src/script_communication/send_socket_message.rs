use serde_json::Value;
use std::collections::HashMap;
use std::io::Write;
use std::os::unix::net::UnixStream;

// This function acts as a handler that specifies custom messages sent via the unix socket
// All messages take on the same json format, but may require different preprocessing steps
pub fn send_message_via_socket(
    stream: &mut UnixStream,
    message_type: String,
    parameters: Value,          // accept any structure of dictionary
) -> std::io::Result<()> {
    let payload: Value = match message_type.as_str() {
        "GUI_Startup" => {
            // You can manipulate or preprocess parameters here if needed
            serde_json::json!({
                "type": message_type,
                "params": parameters
            })
        }
        "Basic-Edit-Job" => {
            serde_json::json!({
                "type": message_type,
                "params": parameters
            })
        }
        "Basic-Edit-Part-2-Get-Silence-Timestamps" => {
            serde_json::json!({
                "type": message_type,
                "params": parameters
            })
            // this time params includes the dictionary of silence timestamps for 
            // each media clip on the track
        }
        "Basic-Edit-Part-3-Apply-Captions" => {
            serde_json::json!({
                "type": message_type,
                "params": parameters
            })
        }
        "Get_Number_Of_Audio_Tracks" => {
            serde_json::json!({
                "type": message_type,
                "params": parameters
            })
            // No real parameters to send, but we send the message type indicating that we
            // want the number of audio tracks
        }
        _ => {
            // Default handler for other message types
            serde_json::json!({
                "type": message_type,
                "params": parameters
            })
        }
    };
    
    let serialized = format!("{}\n", payload.to_string());

    println!("Serialized payload: {}", serialized);

    stream.write_all(serialized.as_bytes())?;
    stream.flush()?;

    Ok(())
}
