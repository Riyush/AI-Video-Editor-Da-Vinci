// Learn more about Tauri commands at https://tauri.app/develop/calling-rust/

pub mod script_communication {
    pub mod initial_connect;
    pub mod maintain_stream;
    pub mod receive_socket_message;
    pub mod send_socket_message;
}
pub mod UI_communication {
    pub mod app_setup;
    pub mod commands;
    pub mod event_creation_handler;
}
pub mod App_State {
    pub mod app_state;
}

pub mod utils {
    pub mod type_check;
}