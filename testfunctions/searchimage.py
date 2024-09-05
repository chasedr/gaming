import webbrowser
import pyautogui
import time
import os
import pygetwindow as gw

def open_url_in_new_window(url):
    # Open the URL in a new window
    webbrowser.open_new(url)
    # Wait for a few seconds to give the browser time to open and render the page
    time.sleep(5)

    # Perform a screenshot
    screenshot = pyautogui.screenshot()
    screenshot_path = 'screenshot.png'
    screenshot.save(screenshot_path)
    print(f"截图已保存到：{screenshot_path}")

    # Close the browser window
    close_browser_window()

def close_browser_window():
    # Get the list of all open windows
    windows = gw.getWindowsWithTitle('')

    # Find the browser window and close it
    for window in windows:
        if 'bing' in window.title.lower() or 'hello' in window.title.lower():
            window.close()
            print("浏览器窗口已关闭")
            break

if __name__ == "__main__":
    url = "https://www.bing.com/images/search?q=hello"
    open_url_in_new_window(url)

    # Simulate a delay before reopening the browser. This part can be replaced
    # with any other logic or user action that determines when to reopen.
    #time.sleep(10)  # Wait for 10 seconds
    
    # Reopen the URL in a new window
    #open_url_in_new_window(url)
