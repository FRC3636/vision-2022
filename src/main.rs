use opencv::{
    core::{in_range, Size_, Vector, BORDER_DEFAULT},
    highgui, imgproc,
    prelude::*,
    videoio,
};

const GOAL_HEIGHT: f32 = 105.0;

// Camera params
const CAMERA_HEIGHT: f32 = 24.0;
const CAMERA_ANGLE: f32 = 45.0;

const VERTICAL_FOV: f32 = 41.0;
const HORIZONTAL_FOV: f32 = 53.0;

const HORIZONTAL_RESOLUTION: u32 = 1280;
const VERTICAL_RESOLUTION: u32 = 720;

fn calc_dist(pix_y: u32) -> f32 {
    const HEIGHT: f32 = GOAL_HEIGHT - CAMERA_HEIGHT;

    let angle = (pix_y as f32 / VERTICAL_RESOLUTION as f32) * VERTICAL_FOV - (VERTICAL_FOV / 2.0);

    HEIGHT / angle.tan()
}

fn green_filter(frame: &mut Mat) -> opencv::Result<()> {
    unsafe {
        imgproc::cvt_color(
            // AFAICT there's no safe way to do this
            &*(frame as *const _),
            &mut *(frame as *mut _),
            imgproc::COLOR_BGR2HSV,
            0,
        )?;
        imgproc::gaussian_blur(
            &*(frame as *const _),
            &mut *(frame as *mut _),
            Size_ {
                width: 5,
                height: 5,
            },
            0.0,
            0.0,
            BORDER_DEFAULT,
        )?;
        in_range(
            &*(frame as *const _),
            &Vector::<u8>::from(vec![60, 25, 100]),
            &Vector::<u8>::from(vec![90, 255, 255]),
            &mut *(frame as *mut _),
        )?;
    }
    Ok(())
}

fn main() -> opencv::Result<()> {
    highgui::named_window("video_capture", highgui::WINDOW_AUTOSIZE)?;

    #[cfg(ocvrs_opencv_branch_32)]
    let mut cam = videoio::VideoCapture::new_default()?; // 0 is the default camera

    #[cfg(not(ocvrs_opencv_branch_32))]
    let mut cam = videoio::VideoCapture::new(0, videoio::CAP_ANY)?; // 0 is the default camera

    assert!(
        videoio::VideoCapture::is_opened(&cam)?,
        "unable to open default camera"
    );

    loop {
        let mut frame = Mat::default();
        cam.read(&mut frame)?;
        if frame.size()?.width > 0 {
            green_filter(&mut frame);
            highgui::imshow("video_capture", &frame)?;
        }
        let key = highgui::wait_key(10)?;
        if key > 0 && key != 255 {
            break;
        }
    }
    Ok(())
}
