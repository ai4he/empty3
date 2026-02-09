================================================================================
  GEMINI QUEST: THE AWAKENING
  Interactive Narrative Videogame Prototype
================================================================================

OVERVIEW
--------
Gemini Quest is a browser-based interactive fiction / text adventure game
prototype. It features pre-generated story text, CSS-based visual scenes,
character creation, branching narrative choices across three chapters, and
comprehensive telemetry logging of all user interactions.

HOW TO OPEN
-----------
1. Open the file "index.html" in any modern web browser (Chrome, Firefox,
   Safari, or Edge).
2. Simply double-click the file, or right-click and choose "Open with"
   followed by your preferred browser.
3. No web server is required. The file is entirely self-contained.

HOW TO PLAY
-----------
1. Click "Begin Your Quest" on the title screen.
2. Enter a character name and select a class (Warrior, Mage, Rogue, or Healer).
3. Read each chapter's narrative text and make choices by clicking the
   corresponding buttons.
4. After three chapters, you will see an ending screen summarizing your
   journey and session statistics.

TELEMETRY / INTERACTION LOGS
-----------------------------
The prototype logs every user interaction (page views, button clicks,
choices made, time on each page, character creation data, session timing,
and browser info) into a JavaScript array: window.telemetryLog.

To export the logs:
  - Click the small "Export Logs" button in the bottom-right corner of the
    screen at any time.
  - You will be prompted for a participant ID.
  - A JSON file named "participant_[ID]_logs.json" will be downloaded
    containing all captured interaction data.

You can also inspect the live log array in the browser developer console by
typing: window.telemetryLog

TECHNICAL NOTES
---------------
- All HTML, CSS, and JavaScript are contained in a single index.html file.
- No external dependencies, libraries, or network requests are required.
- Visual scenes use CSS gradients as placeholder art.
- Sound/music atmosphere is described in italic text (no actual audio).
- The prototype is mobile-responsive and works on all screen sizes.

FILE LISTING
------------
  index.html   - The complete self-contained web application
  README.txt   - This file

================================================================================
