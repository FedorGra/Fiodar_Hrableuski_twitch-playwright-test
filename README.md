# Twitch Search Test Automation Framework

A scalable Playwright-based test automation framework for Twitch web application testing with mobile emulation support.
I created a test automation framework for Twitch with mobile emulation. Here are the steps and decisions I made during development.

1. **Architecture**
   The framework is based on the Page Object Model. I implemented a BasePage class and separate page objects for the home page, search results, and streamer page. This separation makes the code more maintainable and easier to read.

2. **Repository structure**
   The project is organized into pages, tests, and screenshots directories. Pages contain page classes, tests hold the test scenarios, and screenshots store the captured images. This structure keeps the project clean and easy to navigate.

3. **Fixtures and test isolation**
   The fixtures are set up so that the browser is launched once per session, while a new context and page are created for each test. This isolates tests from one another and improves stability.

4. **Validations**
   The framework includes multiple layers of validation: checking the URL, verifying screenshot existence and size, ensuring the video player is visible, and confirming search works correctly. These checks increase reliability.

5. **Dynamic content handling**
   I added scrolling and explicit waits to handle Twitch’s lazy-loaded content. There is also logic to close popups that may interfere with test execution.

6. **Development optimization**
   To save time I used an assistant to generate the initial project skeleton, code templates, and documentation drafts. This allowed me to focus on implementing business logic and ensuring test stability.

The result is a framework with a clear structure, reliable validations, and scalability for future scenarios.

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

*GIF*
![Test Execution Demo](demo.gif)

## 📋 Test Cases

|Test ID|Test Name                                 |Steps                                                                                                                                                          |Expected Results                                                                                                    |Validation Method                                                                                                  |
|-------|------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------|
|TC001  |Search and Capture Streamer - Basic       |1. Navigate to Twitch<br>2. Click search icon<br>3. Input “StarCraft II”<br>4. Scroll down 2 times<br>5. Select first streamer<br>6. Wait for load & screenshot|- Successfully navigates to Twitch<br>- Search functionality works<br>- Streamer page loads<br>- Screenshot captured|- URL validation (contains “twitch.tv”)<br>- Screenshot file exists<br>- File size > 10KB<br>- Video player visible|
|TC002  |Search and Capture Streamer - Parametrized|1. Navigate to Twitch<br>2. Click search icon<br>3. Input game name<br>4. Scroll N times<br>5. Select Nth streamer<br>6. Wait for load & screenshot            |- Different streamers selected<br>- All screenshots captured<br>- Handles various positions                         |- Multiple screenshots created<br>- Unique filenames<br>- File size validation<br>- URL validation                 |


## 🏗️ Repository Structure

```
twitch-test-automation/
│
├── pages/                          # Page Object Model
│   ├── __init__.py
│   ├── base_page.py               # Base page with common methods
│   └── twitch_pages.py            # Twitch-specific page objects
│
├── tests/                          # Test cases
│   ├── __init__.py
│   └── test_twitch_search.py      # Main test suite
│
├── screenshots/                    # Test screenshots output
│   └── .gitkeep
│
├── conftest.py                     # Pytest fixtures & configuration
├── pytest.ini                      # Pytest settings
├── requirements.txt                # Python dependencies
├── .gitignore                      # Git ignore rules
└── README.md                       # This file
```

## 🔧 Installation & Setup

### Prerequisites

- Python 3.8+
- pip

### Installation Steps

1. **Clone the repository**

```bash
git clone https://github.com/FedorGra/twitch-test-automation.git
cd twitch-test-automation
```

2. **Create virtual environment**

```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scriptsctivate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Install Playwright browsers**

```bash
playwright install chromium
```

## 🚀 Running Tests

### Run all tests

```bash
pytest
```

### Run specific test

```bash
pytest tests/test_twitch_search.py::TestTwitchSearch::test_search_basic_flow
```

### Run with verbose output

```bash
pytest -v -s
```

### Run parametrized tests

```bash
pytest tests/test_twitch_search.py::TestTwitchSearch::test_search_and_capture_streamer
```

## 📱 Mobile Emulation Configuration

device = playwright.devices['iPhone 13 Pro']
Configuration is set in `conftest.py`

## ✅ Validation Strategy

### Why These Validations?

1. **Screenshot File Existence** (`os.path.exists()`)
- **Why**: Ensures the core requirement (capturing screenshot) is met
- **What it validates**: File system operation success
- 
2. **File Size Validation** (`file_size > 10000 bytes`)
- **Why**: Prevents false positives from empty/corrupted screenshots
- **What it validates**: Screenshot contains actual image data
- **Threshold**: 10KB minimum ensures valid image content
- 
3. **URL Domain Validation** (`"twitch.tv" in page.url`)
- **Why**: Confirms navigation to correct platform
- **What it validates**: No redirects to error pages or other domains
- 
4. **Video Player Visibility** (`page.is_visible("video")`)
- **Why**: Ensures stream content is actually loaded
- **What it validates**: Page reached fully loaded state with video player
- 
5. **Modal/Popup Handling** (Automated in framework)
- **Why**: Twitch shows consent banners, mature content warnings
- **What it validates**: Tests aren’t blocked by popups
- **Implementation**: Multiple selector strategies for resilience

P.S. Additional assertions have been added between each step in the basic testcase.

### Validation Trade-offs

- **Not validated**: Actual stream playback (requires audio/video analysis)
- **Not validated**: Stream quality (beyond scope)
- **Validated**: Page structure and screenshot capture success

## 🎨 Framework Design Principles

### 1. Page Object Model (POM)

- **Separation of concerns**: Locators and actions separated from tests
- **Reusability**: Page methods can be reused across multiple tests
- **Maintainability**: Changes to UI require updates in one place

### 2. Pytest Parametrize

- **Coverage**: Tests multiple streamers with single test function
- **DRY Principle**: Reduces code duplication
- **Scalability**: Easy to add new test data

### 3. Fixtures

- **Browser reuse**: Session-scoped browser for efficiency
- **Context isolation**: Function-scoped contexts prevent test interference
- **Screenshot management**: Automatic unique naming with timestamps

### 4. Error Handling

- **Graceful degradation**: Tests continue even if optional elements missing
- **Timeout management**: Explicit waits prevent flaky tests
- **Modal handling**: Proactive popup dismissal

## 🔍 Handling Test Flakiness

### Strategies Implemented

1. **Explicit Waits**
- `wait_for_selector()` instead of fixed sleeps
- `wait_for_load_state("networkidle")` for AJAX content
2. **Retry Logic for Modals**
- Multiple selector strategies for popups
- Try-except blocks for optional elements
3. **Mobile Emulation Stability**
- Consistent viewport across test runs
- Touch event support enabled
4. **Dynamic Content Handling**
- Scrolling with waits for lazy-loaded content
- Network idle state verification

## 📊 Scalability Features

### Current Scale

- ✅ Multiple game searches (parametrized)
- ✅ Multiple streamer selections
- ✅ Page Object Model for easy extension

### Future Scale

- 🔄 Add more games via parametrize data
- 🔄 Add different browsers (Firefox, Safari)
- 🔄 Add parallel execution (`pytest-xdist`)
- 🔄 Add CI/CD integration (GitHub Actions)
- 🔄 Add custom reporting (Allure)

## 🐛 Troubleshooting

### Tests fail with “Element not found”

- **Cause**: Twitch UI changed or slow network
- **Solution**: Increase timeouts in `conftest.py` or `base_page.py`

### No streamers found for StarCraft II

- **Cause**: No live streams at the moment
- **Solution**: Change game name in parametrize decorator or run during peak hours

### Screenshots are blank

- **Cause**: Page not fully loaded
- **Solution**: Check `wait_for_stream_load()` method waits

## 📝 Notes

- Tests run in **non-headless mode** by default for visibility
- Screenshots saved in `screenshots/` directory
- Slow motion (`slow_mo=500`) enabled for demonstration
- Mobile emulation matches **Google Chrome Mobile** as required

## 📧 Contact

For questions about this framework, please contact via the recruiter.

-----

**Framework Version**: 1.0.0  
**Last Updated**: October 2025  
**Python Version**: 3.8+  
**Playwright Version**: 1.40.0
