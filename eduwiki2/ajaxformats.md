## AJAX Formats

This details the format of the AJAX requests for EduWiki. It is mostly for personal reference, but also for future clarification.

### Build

- Get Angular template **(GET /build)**
 - No format
- Post registration **(POST /build/register)**
 - regData
   - success (boolean)
   - errors (if errors)
   - name (string)
   - email (string)
 - returns user info
- Get review **(GET /build/{topic}/review)**
 - passes topic through URL
 - returns:
 - success (boolean)
 - errors (if errors, can include disambig)
 - name (string)
 - description (string)
 - distractors (array)
   - snippet (string)
   - pagetitle (string)

ETC
