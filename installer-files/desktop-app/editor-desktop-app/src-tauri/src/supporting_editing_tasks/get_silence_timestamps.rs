use std::collections::HashMap;
use std::process::{Command, Stdio};
use std::io::{self, Write};
use std::fs;
use std::env;
use std::path::{Path, PathBuf};

pub fn get_silence_timestamps_in_python(wav_files_dict: HashMap<usize, Vec<String>>) -> Result<HashMap<usize, HashMap<String, Vec<[f32; 2]>>>, Box<dyn std::error::Error>> {
    /* 
    Note the return type is a map where the key is the track and value is another hashmap
    mapping each wav file path String to a list of timestamps representing silences
    
     */
    // Get path to current executable
    let exe_path = env::current_exe()?;
    let project_root = exe_path
        .parent().unwrap() // /target/debug/
        .parent().unwrap() // /target/
        .parent().unwrap(); // src-tauri

/* THIS IS SUPER BAD. THE PYTHON file path is within the local directory rather
    than the put on the user's file system via post instal SCRIPT
    
            THIS NEEDS TO BE FIXED VERY SOON
    */
    // Path to the Python file relative to project root
    
    let py_path = project_root.join("python").join("dist").join("get_silence_timestamps").join("get_silence_timestamps");
    println!("python file path: {}", py_path.display());

    if !py_path.exists() {
        return Err(format!("Python script not found at: {}", py_path.display()).into());
    }

    let paths_str: &str = &serde_json::to_string(&wav_files_dict).unwrap();
    println!("Paths as str: {}", paths_str);

    // spawn a child process to execute the python function to get .wav files
    let mut child = Command::new(py_path)
    .stdin(Stdio::piped())
    .stdout(Stdio::piped())
    .spawn()?;

    // give the child process the paths dictionary to parse
    child.stdin.as_mut().unwrap().write_all(paths_str.as_bytes())?;
    let output = child.wait_with_output()?;

    if output.status.success() {
        // get the timestamps from the standard output of the child process
        let stdout_str = String::from_utf8(output.stdout)?;
        println!("Python script output:\n{}", stdout_str);  // 👈 see all prints + result
        
        // convert string output to finalized dictionary to be sent back to the script
        let timestamps_dict = serde_json::from_str(&stdout_str)?;
        Ok(timestamps_dict)
        
    } else {
        Err(format!(
            "Python error: {}",
            String::from_utf8_lossy(&output.stderr)
        )
        .into())
    }
}