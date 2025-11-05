use serde_json::Value;
use serde_json;
use std::collections::HashMap;
use std::option;
use std::os::unix::net::UnixStream;
use tauri::{AppHandle, Emitter}; // Needed for `emit_all`

use crate::UI_communication::event_creation_handler::send_global_message;
use crate::supporting_editing_tasks::create_wav_files::create_wav_files_using_python;
use crate::supporting_editing_tasks::get_silence_timestamps::get_silence_timestamps_in_python;
use crate::supporting_editing_tasks::get_audio_transcripts::get_audio_transcripts_in_python;
use crate::script_communication::send_socket_message::send_message_via_socket;
use crate::utils::type_check::print_type_of;

/* This function acts as a handler receiving socket messages and calling
send_socket_message as needed to communicate with the script */
pub fn socket_response_handler(response: String, app: AppHandle, stream: &mut UnixStream) {
    // Consider that in the future, all responses will be in JSON format
    let parsed: Result<HashMap<String, Value>, _> = serde_json::from_str(&response);

    match &parsed {
    Ok(map) => println!("{:#?}", map), // Pretty-print the map
    Err(e) => eprintln!("Failed to parse JSON: {}", e),
    }

    match parsed {
        Ok(map) => {
            match map.get("type").and_then(|v| v.as_str()) {
                Some("GUI_Startup_Success") => {
                    // Script is run
                    let parameters: HashMap<String, String> = HashMap::new();
                    // Emit event prompting login page to frontend
                    send_global_message(app, "socket_success", parameters);
                }
                Some("Started_Edit_Job") => {
                    if let Some(status) = map.get("status").and_then(|v| v.as_str()) {
                        match status {
                            "success" => {
                                // ✅ SUCCESS CASE
                                println!("Started edit job successfully.");

                                if let Some(payload) = map.get("payload") {
                                    println!("Payload: {:?}", payload);

                                    // get the "Media_File_Paths" dictionary
                                    if let Some(media_file_paths) = payload.get("Media_File_Paths") {
                                        // Try to parse it into a concrete HashMap<usize, Vec<String>>
                                        let parsed_paths: Result<HashMap<usize, Vec<String>>, _> = serde_json::from_value(media_file_paths.clone());

                                        match parsed_paths {
                                            Ok(paths_hashmap) => {
                                                println!("Media File Paths: {:#?}", paths_hashmap);
                                                // Here, I need to pass the parsed_paths dict to a function that creates the wav files,
                                                // and gets silence timestamps 
                                                let json_str = create_wav_files_using_python(paths_hashmap, stream).unwrap(); // String
                                                let wav_paths: HashMap<usize, Vec<String>> = serde_json::from_str(&json_str).unwrap();
                                                
                                                // Now get silences timestamps
                                                let silence_timestamps_map= get_silence_timestamps_in_python(wav_paths, stream).unwrap();

                                                print_type_of(&silence_timestamps_map);
                                                
                                                let silence_timestamps_json_value = serde_json::to_value(silence_timestamps_map).unwrap();
                                                // need to send the timestamps back to the Script
                                                let message_type: String = String::from("Basic-Edit-Part-2-Get-Silence-Timestamps");
                                                send_message_via_socket(stream, message_type, silence_timestamps_json_value);
                                                
                                            }
                                            Err(e) => {
                                                eprintln!("Failed to parse Media_File_Paths: {}", e);
                                            }
                                        }
                                    }
                                }
                            }
                            other_status => {
                                // Need to create a message in the GUI that something failed in the future
                                // This will be done by emitting an event
                                // ❌ FAILURE or UNEXPECTED STATUS
                                println!("Edit job reported Failure: {}", other_status);

                                let mut error_payload: HashMap<String, String> = HashMap::new();
                                error_payload.insert("error".into(), format!("Edit job failed with status: {}", other_status));
                                //send_global_message(app, "edit_job_failed", error_payload);
                            }
                        }
                    } else {
                        println!("No 'status' field found in Started_Edit_Job response.");
                    }
                }
                Some("Need_Transcripts") => {
                        // ✅ Step 1: Access payload
                    if let Some(payload) = map.get("payload") {
                        // ✅ Step 2: Access wav_paths (nested list)
                        if let Some(wav_paths_val) = payload.get("wav_paths") {
                            // ✅ Step 3: Convert JSON array to Vec<String>
                            if let Some(wav_paths_array) = wav_paths_val.as_array() {
                                let wav_paths: Vec<String> = wav_paths_array
                                    .iter()
                                    .filter_map(|v| v.as_str().map(|s| s.to_string()))
                                    .collect();

                                println!("Extracted wav_paths: {:?}", wav_paths);

                                // ✅✅✅ now, we have the wav paths and we want to 
                                // trigger a subprocess to get transcripts for that track
                                let transcripts_string: String = get_audio_transcripts_in_python(wav_paths, stream).unwrap();

                                // Note, the transcripts_dict is a serialized string
                                // We send the string back to the script and let python parse it back to a dictionary
                                let serialized_transcripts:Value = serde_json::to_value(transcripts_string).unwrap();
                                let message_type: String = String::from("Basic-Edit-Part-3-Apply-Captions");

                                send_message_via_socket(stream, message_type, serialized_transcripts);
                            } else {
                                eprintln!("'wav_paths' is not an array");
                            }
                        } else {
                            eprintln!("'wav_paths' not found in payload");
                        }
                    } else {
                        eprintln!("'payload' not found in response");
                    }
                }
                // In this case, we have received the number of audio tracks 
                // and want to transmit that to the frontend
                Some("Get_Number_Of_Audio_Tracks") => {
                    if let Some(payload) = map.get("payload") {
                        if let Some(num_audio_tracks) = payload.get("Audio_Tracks_Count") {
                            // Convert serde_json::Value → int
                            if let Some(num) = num_audio_tracks.as_i64() {
                                // Get the number of audio tracks and send it back to the GUI via event
                                let command_name: &str = "Emit_Audio_Tracks_Count";
                                let mut parameters: HashMap<String, String> = HashMap::new();
                                parameters.insert("Audio_Track_Count".to_string(), num.to_string());
                                send_global_message(app, command_name, parameters);
                            }
                            else {
                                eprintln!("Audio_Tracks_Count is not an integer");
                            }
                            
                        }
                    }
                }
                // add response handling for other values of type key
                Some(other_type) => {
                    // Parse unexpectev values of type
                    println!("Received unexpected type: {}", other_type);
                }
                None => {
                    // Pase when there is no type field
                    println!("No 'type' field in response.");
                }
            }
        }
        Err(e) => {
            println!("Failed to parse response as JSON: {}", e);
        }
    }
}
