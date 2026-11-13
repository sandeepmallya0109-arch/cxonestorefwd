# CXone Store & Forward Uploader

Single-page tool (`index.html`) for the CXone Store and Forward Generic API
(spec: https://developer.nicecxone.com/api/generic#/StoreAndForwardGeneric).

Flow: build manifest -> zip (one JSON at root) -> `POST /api/store-and-forward/v1/interaction-ingestion-jobs`
(multipart field `file`) -> `PUT` each media file to the returned pre-signed URL -> check
`GET .../{jobId}` and `GET .../{jobId}/interactions`.

## Setup

1. **Get the files:** `git clone https://github.com/sandeepmallya0109-arch/cxonestorefwd.git`
2. **Create a CXone access key:** Admin > Security > Access Keys, for a user with the
   "Upload Interactions via Voice/Digital API" permission. Copy the key ID and secret (shown once).
3. **CXone prerequisites:** a Recording Advanced Store & Forward license, and a system created under
   Third Party Systems with Integration Type **STORE AND FORWARD API**. Agents referenced in the manifest must exist in CXone.
4. **(Optional) Save your defaults** — create `config.local.js` next to `index.html` (it is gitignored, never commit it):

   ```js
   window.SF_CONFIG = {
     keyId: "YOUR_ACCESS_KEY_ID",
     keySecret: "YOUR_ACCESS_KEY_SECRET",
     authUrl: "https://api-au1.niceincontact.com/authentication/v1/token/access-key",
     baseUrl: "https://api-au1.niceincontact.com"
   };
   ```
   Replace `au1` with your area (`na1`, `eu1`, ...). Without this file, type the values into the page.
5. **Open `index.html`** by double-clicking it. No server is needed; the page calls CXone directly
   (the API host allows browser requests). Internet access is needed for the JSZip library (cdnjs).
6. Click **Request token**, load a manifest, select media files, click **Create job & upload media**.

### Optional: local proxy
If your browser or network blocks a call with a CORS/network error (for example the media upload URL),
run `python3 server.py`, open http://localhost:8080 and tick **Use local proxy**.

## Sample payloads
`sample/manifest.json` + `sample/sample-call.wav` (voice) and `sample/manifest-chat.json` + `sample/sample-attachment.txt` (chat).
Edit `systemName` and the agent `value` to match your tenant, and keep `startTime` within the last 30 days
(the **Load sample manifest** button generates fresh times).

## Manifest rules learned from the API
- `fileType` is the format name: `WAV` or `MP3` for audio (not a MIME type).
- Only `AGENT_USER` participants may have `isLeadingAgentUser`; omit it for customers. It must be a boolean.
- `systemName` must match a Third Party System of type STORE AND FORWARD API.
- Up to 400 interactions per job; `externalInteractionId` must be unique.
- The page auto-fixes the first two on submit.

## Notes
- Checksum format isn't specified in the spec; default is MD5 hex (switchable to base64).
- The bearer token is kept in memory only. Never commit `config.local.js`.
