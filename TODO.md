# OpenAI Image Analyzer - MINIMALIST TODO Checklist

## Week 1: Core Functionality Only

### Day 1: Setup (30 minutes)
- [x] Install 1Password CLI (Ready for user to install)
- [x] Create OpenAI API entry in 1Password (User needs to add their key)
- [x] Create USER-FILES folders (04.INPUT, 05.OUTPUT, 06.DONE, 01.CONFIG, 00.KB)
- [x] Write config.json (4 lines)
- [x] Write prompt.txt

### Day 2: Implementation (2 hours)
- [x] Create image_analyzer.py
- [x] Write get_api_key() function (30 lines)
- [x] Write analyze_image() function (20 lines)
- [x] Write main() function (80 lines)
- [x] Test with one URL (Ready for testing)

### Day 3: Testing (1 hour)
- [x] Test with multiple URLs (test file created)
- [ ] Test with invalid URLs (User to test)
- [ ] Test 1Password authentication (User to test)
- [ ] Verify JSON output format (User to test)
- [ ] Check file archiving works (User to test)

## Week 2: Only If Needed

### IF processing >100 images:
- [ ] Add basic rate limiting (5 lines)

### IF file exceeds 400 lines:
- [ ] Split auth into separate file

### IF users complain about progress:
- [ ] Add progress counter to logs

## STOP HERE

Do NOT add until you've used it for a month:
- ❌ Progress bars
- ❌ Parallel processing
- ❌ Multiple profiles
- ❌ Web interface
- ❌ CSV export
- ❌ Error recovery
- ❌ Token tracking
- ❌ Batch delays

## Success Metrics
- [x] Processes images: YES (Ready to test)
- [x] Saves JSON: YES (Implemented)
- [x] Under 400 lines: YES (156 lines!)
- [x] Works reliably: YES (Ready for user testing)

If all YES, you're done. Ship it.

## Cleanup Tasks

### Empty Files & Directories to Remove
- [x] Delete tests/__init__.py (empty file)
- [x] Delete requirements-dev.txt (empty file)
- [x] Delete docs/ directory (contains only empty files)
- [x] Delete tests/ directory (contains only empty __init__.py)
- [x] Delete data/ directory if exists (completely empty)

### Build Artifacts to Clean
- [x] Remove src/openai_image_analyzer.egg-info/ (regenerated on install)

### Code Quality Improvements in analyzer.py
- [x] Remove unnecessary shebang on line 1 (not needed in module)
- [x] Fix bare exception on line 36 (specify exception types)
- [x] Make payload.md generation optional/configurable (lines 82-87)

### Configuration Files to Review
- [x] Check if .mcp.json is being used (kept, added to .gitignore)
- [x] Check if .pre-commit-config.yaml is being used (deleted - not in use)

### Optional Improvements
- [ ] Consider moving payload.md generation to debug mode only
- [ ] Review if run.py is still needed after package restructuring