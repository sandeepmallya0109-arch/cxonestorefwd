# CXone Store & Forward Uploader

Single-page tool (`index.html`) for the CXone Store and Forward Generic API
(spec: https://developer.nicecxone.com/api/generic#/StoreAndForwardGeneric).

Flow: build manifest -> zip (one JSON at root) -> `POST /api/store-and-forward/v1/interaction-ingestion-jobs`
(multipart field `file`) -> `PUT` each media file to the returned pre-signed URL -> poll
`GET .../{jobId}` and `GET .../{jobId}/interactions`.

## Run
Open `index.html` in a browser (needs internet for JSZip from cdnjs), or `python3 -m http.server` in this folder.
Enter your API base URL (e.g. `https://api-na1.staging.niceincontact.com`) and a bearer JWT.

## Sample payload
`sample/manifest.json` + `sample/sample-call.wav` (5 s silence). Select the WAV in step 3.
Before submitting you must:
1. Set `externalIdentifier.systemName` / `value` to an agent already defined in CXone (the app's "Load sample" button uses placeholders).
2. Keep `startTime` within the last 30 days (the "Load sample" button regenerates times; the static file is dated 2026-11-12).
3. Have the "Upload Interactions via Voice/Digital API" permission and an S&F license.

## Notes / assumptions
- Checksum format is not specified in the spec; default is MD5 hex (switchable to base64). Upload `Content-MD5` header comes from the API response.
- Browsers enforce CORS. If the API or the S3-style upload URL doesn't allow your origin, calls fail in-browser; use a CORS-enabled proxy or run the same requests via curl.
