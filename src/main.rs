use std::os::raw::c_double;
use opencv::{
	highgui,
	prelude::*,
	videoio,
};

const GOAL_HEIGHT: i32 = 105;


// Camera params
const CAMERA_HEIGHT: i32 = 24;
const CAMERA_ANGLE: i32 = 45;

const VERTICAL_FOV: i32 = 41;
const HORIZONTAL_FOV: i32 = 53;

const HORIZONTAL_RESOLUTION: i32 = 1280;
const VERTICAL_RESOLUTION: i32 = 720;

fn calc_dist(y_height: i32) -> f32 {
	let height = GOAL_HEIGHT - CAMERA_HEIGHT;
	let angle : f32 = (CAMERA_ANGLE + ((y_height - VERTICAL_RESOLUTION / 2) * VERTICAL_FOV) / (VERTICAL_RESOLUTION as f32)) as f32;

	height * angle.tan()
}



fn green_filter(frame: Mat) -> Mat {
	frame
}

fn main() -> opencv::Result<()> {
	highgui::named_window("video_capture", highgui::WINDOW_AUTOSIZE)?;

	#[cfg(ocvrs_opencv_branch_32)]
	let mut cam = videoio::VideoCapture::new_default()?; // 0 is the default camera

	#[cfg(not(ocvrs_opencv_branch_32))]
	let mut cam = videoio::VideoCapture::new(0, videoio::CAP_ANY)?; // 0 is the default camera

	assert!(videoio::VideoCapture::is_opened(&cam)?, "unable to open default camera");

	loop {
		let mut frame = Mat::default();
		cam.read(&mut frame)?;
		if frame.size()?.width > 0 {
			highgui::imshow("video_capture", &mut green_filter(frame))?;
		}
		let key = highgui::wait_key(10)?;
		if key > 0 && key != 255 {
			break;
		}
	}
	Ok(())
}