from datetime import datetime


def save_screenshot(driver, screenshots_dir, name_prefix="screenshot", device_name=None):
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    device_part = f"_{device_name.replace(' ', '_')}" if device_name else ""
    path = screenshots_dir / f"{name_prefix}{device_part}_{timestamp}.png"
    
    # Ensure the path is absolute for clarity in the output
    absolute_path = path.resolve()
    
    # Print the full path to the console to help with debugging
    print(f"Saving screenshot to: {absolute_path}", flush=True)
    
    driver.save_screenshot(str(absolute_path))
    return absolute_path
