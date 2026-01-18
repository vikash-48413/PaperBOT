# Testing Guide - Large File Upload Fixes

## Quick Test Checklist

### ✅ Pre-Flight Checks
1. Server starts without errors
2. Pinecone connection works
3. No Python dependency issues

### ✅ File Upload Tests

#### Test 1: Small File (< 1MB)
- **File**: Any PDF < 1MB
- **Expected**: Fast upload (< 30s)
- **Check**: Progress bar, success message, file size shown

#### Test 2: Medium File (1-3MB)
- **File**: Research paper 1-3MB
- **Expected**: Normal processing (30-60s)
- **Check**: Optimized settings NOT activated

#### Test 3: Large File (3-5MB) ⭐ PRIMARY TEST
- **File**: Research paper ~5MB
- **Expected**: Optimized processing (1-2 min)
- **Check**: Console shows "Large file detected - using optimized settings"
- **Verify**: 
  - Chunk length: 350 words
  - Batch size: 20 chunks
  - Memory cleanup messages appear

#### Test 4: Very Large File (5-10MB)
- **File**: Long research paper 5-10MB
- **Expected**: Slower but successful (2-5 min)
- **Check**: All chunks processed, no memory errors

#### Test 5: Maximum Size (45-50MB)
- **File**: Very large document
- **Expected**: Works but takes time (5-10 min)
- **Warning**: May be slow, monitor console

#### Test 6: Oversized File (> 50MB)
- **File**: Any file > 50MB
- **Expected**: Clear error message
- **Error Text**: "File size (XXmb) exceeds maximum allowed size (50MB)"
- **HTTP Code**: 413 (Payload Too Large)

### ✅ Error Handling Tests

#### Test 7: Empty File
- **File**: Create empty .pdf file
- **Expected**: Error "File is empty"
- **HTTP Code**: 400

#### Test 8: Wrong File Type
- **File**: .exe, .zip, .mp3, etc.
- **Expected**: Error listing supported formats
- **Supported**: PDF, DOCX, DOC, TXT, MD, CSV, JSON, XLSX, XLS

#### Test 9: Corrupted PDF
- **File**: Damaged PDF file
- **Expected**: Error during content extraction
- **Check**: Proper error message, cleanup occurs

### ✅ Performance Tests

#### Test 10: Memory Usage
1. Note starting memory (Task Manager)
2. Upload 5MB file
3. Check memory during processing
4. Verify memory cleanup after completion
5. **Expected**: Memory returns near baseline

#### Test 11: Multiple Uploads
1. Upload file A (5MB)
2. Wait for completion
3. Delete file A
4. Upload file B (5MB)
5. **Expected**: Both work, no accumulation errors

#### Test 12: Upload Cancellation
1. Start uploading large file
2. Refresh page mid-upload
3. **Expected**: Cleanup occurs, no orphaned files

### ✅ Progress Tracking Tests

#### Test 13: Progress Updates
1. Upload 5MB file
2. Watch console output
3. **Check for**:
   - ✓ File type validated
   - ✓ File read successfully: X.XXmb
   - ✓ Cleared previous uploads
   - ✓ File saved to: uploads/...
   - ✓ Initializing document store
   - ✓ Converting file
   - ✓ Extracted content
   - ✓ Created X chunks
   - ✓ Batch N/M complete
   - ✓ Memory cleanup
   - ✓ Wrote X chunks to Pinecone
   - ✅ Ingestion completed successfully

#### Test 14: Frontend Progress
1. Upload any file
2. Watch progress bar
3. **Check**:
   - Shows percentage
   - Updates in real-time
   - Shows "Complete! ✓" at end

## Console Output Examples

### ✅ Successful 5MB Upload
```
📥 Upload endpoint called - Filename: research_paper.pdf
✓ File type validated: .pdf
📦 Reading file in chunks...
✓ File read successfully: 5.23MB
🧹 Clearing previous uploads...
✓ File saved to: uploads\research_paper.pdf
📤 Upload started: research_paper.pdf (5.23MB)
🔧 Initializing document store...
📊 Processing document...

📄 Starting document ingestion: research_paper.pdf
   💾 Server baseline memory: 450.2MB
   ✓ Cleared existing documents from vector store
   🔄 Converting .pdf file...
   ✓ Extracted content (1 document(s), 45230 chars)
   📊 File size: 5.23MB
   ⚡ Large file detected - using optimized settings:
      Chunk length: 350 words
      Batch size: 20 chunks
   ✂️  Splitting into chunks...
   ✓ Created 156 chunks
   🧠 Embedding chunks with parallel processing...
   📦 Processing 156 chunks in 8 batches (batch_size=20)
   ✓ Batch 1/8 complete (20 chunks, +15.2MB)
   ✓ Batch 2/8 complete (20 chunks, +14.8MB)
   ✓ Batch 3/8 complete (20 chunks, +15.1MB)
   🧹 Memory cleanup: 485.3MB
   ✓ Batch 4/8 complete (20 chunks, +15.0MB)
   ...
   ✓ Batch 8/8 complete (16 chunks, +12.1MB)
   ✓ Successfully embedded 156 chunks
   💾 Writing to vector database...
   ✓ Wrote 156 chunks to Pinecone

✅ Ingestion completed successfully!
   📊 Statistics:
   • Document: research_paper.pdf
   • Format: PDF
   • Size: 5.23MB
   • Chunks created: 156
   • Time taken: 94.32 seconds
   • Speed: 1.7 chunks/sec
   • Memory used: +45.3MB (450.2MB → 495.5MB)
⏱️  Total processing time: 94.3s
✅ Upload completed: research_paper.pdf
```

### ❌ Failed Upload - File Too Large
```
📥 Upload endpoint called - Filename: huge_file.pdf
✓ File type validated: .pdf
📦 Reading file in chunks...
❌ Error: File size (52.34MB) exceeds maximum (50MB)
```

### ❌ Failed Upload - Empty File
```
📥 Upload endpoint called - Filename: empty.pdf
✓ File type validated: .pdf
📦 Reading file in chunks...
✓ File read successfully: 0.00MB
❌ Error: File is empty
```

## Browser Console Checks

### Successful Upload
```javascript
File selected: File {name: "paper.pdf", size: 5485760}
File: paper.pdf, Size: 5.23MB
Starting upload for: paper.pdf
Sending request to /upload_document
Processing progress: 30%
Processing progress: 50%
Processing progress: 70%
Processing progress: 90%
```

### Failed Upload
```javascript
File: huge.pdf, Size: 52.34MB
❌ File too large error shown
```

## What to Look For

### ✅ SUCCESS Indicators
- Progress bar completes to 100%
- Green success notification
- File appears in "Current Document" section
- Console shows "✅ Ingestion completed successfully"
- Can ask questions immediately

### ❌ FAILURE Indicators
- Red error notification
- Clear error message
- Console shows "❌" errors
- File automatically cleaned up
- Can upload again without issues

## Performance Benchmarks

| File Size | Expected Time | Chunks | Memory Usage |
|-----------|---------------|--------|---------------|
| 0.5 MB    | 15-20s        | 40-60  | +20-30MB      |
| 1 MB      | 25-35s        | 80-100 | +30-40MB      |
| 3 MB      | 50-70s        | 120-140| +40-60MB      |
| 5 MB      | 80-120s       | 150-180| +50-80MB      |
| 10 MB     | 150-240s      | 280-320| +80-120MB     |

*Times vary based on system specs and model choice*

## Common Issues & Solutions

### Issue: "Timeout after 10 minutes"
**Cause**: File too complex or system too slow  
**Solution**: 
- Try smaller file
- Use "fast" model in config.py
- Increase chunk size in config.py

### Issue: "Memory Error"
**Cause**: Insufficient RAM  
**Solution**:
- Close other applications
- Increase batch size in config.py
- Use "fast" model (uses less memory)

### Issue: "No chunks embedded"
**Cause**: Pinecone connection issue  
**Solution**:
- Check PINECONE_API_KEY in .env
- Verify internet connection
- Check Pinecone index exists

### Issue: "File not found after upload"
**Cause**: Permission or path issue  
**Solution**:
- Check uploads/ directory exists
- Verify write permissions
- Check disk space

## Quick Debug Commands

### Check Server Logs
```bash
# Look for errors in console
# Search for ❌ or "ERROR" or "Exception"
```

### Check File Size
```bash
# Windows PowerShell
(Get-Item "path\to\file.pdf").Length / 1MB
```

### Check Memory Usage
```bash
# Windows Task Manager
# Look for python.exe process
```

### Check Uploads Directory
```bash
# PowerShell
Get-ChildItem uploads\
```

## Success Criteria

For a 5MB file upload to be considered successful:

1. ✅ File uploads without errors
2. ✅ Optimized settings activate (console shows message)
3. ✅ All chunks process successfully
4. ✅ Data written to Pinecone
5. ✅ Memory cleanup occurs
6. ✅ Processing completes in < 5 minutes
7. ✅ Can ask questions and get answers
8. ✅ Statistics show correct file size

## Report Template

When reporting issues, include:

```
File Details:
- Name: _______
- Size: _______
- Type: _______

Error:
- Message: _______
- HTTP Code: _______
- When occurred: _______

Console Output:
[Paste last 20-30 lines]

Browser Console:
[Paste any errors]

System:
- OS: _______
- RAM: _______
- Python Version: _______
```

---

**Need Help?** Check [FIXES_APPLIED.md](FIXES_APPLIED.md) for detailed technical information.
