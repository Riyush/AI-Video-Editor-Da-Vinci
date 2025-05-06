/*
This file is responsible for listening for events emitted by the React Frontend and 
taking action on those events. These are essentially all the Tauri Commands the 
Backend can receive. This ffile is linked in lib.rs

 */
use crate::App_State::app_state::AppState;
use std::io::Result;


// This is a command that gets called when the frontend has fully mounted
#[tauri::command]
pub fn GUI_Loaded(state: tauri::State<AppState>) {
  println!("GUI Loaded");
  let mut gui_loaded = state.gui_loaded.lock().unwrap();
  *gui_loaded = true;
}