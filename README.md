# Lyrics Search API

A lightweight Flask-based REST API for retrieving song lyrics using the public [LRCLIB](https://lrclib.net/) lyrics database.

This service provides a simple JSON interface for fetching either plain or time-synced lyrics.

---

## Base URL

```
https://lyrics.syntaxly.xyz
```

---

## Endpoint

### `GET /search/<query>`

Searches for lyrics using the provided query string.

### Path Parameter

| Name    | Type   | Required | Description                              |
| ------- | ------ | -------- | ---------------------------------------- |
| `query` | string | Yes      | Song search query (e.g., artist + title) |

Example:

```
/search/eminem%20in%20your%20head
```

---

## Query Parameters

| Name   | Type   | Required | Default | Description              |
| ------ | ------ | -------- | ------- | ------------------------ |
| `type` | string | No       | `plain` | Determines lyrics format |

### `type` Values

| Value    | Description                                          |
| -------- | ---------------------------------------------------- |
| `plain`  | Returns plain text lyrics                            |
| `synced` | Returns time-synced lyrics (LRC format if available) |

---

## Example Requests

### Plain Lyrics (default)

```bash
curl "https://lyrics.syntaxly.xyz/search/eminem%20in%20your%20head"
```

### Synced Lyrics

```bash
curl "https://lyrics.syntaxly.xyz/search/eminem%20in%20your%20head?type=synced"
```

---

## Success Response

HTTP `200 OK`

```json
{
    "success": true,
    "error": null,
    "lyrics": "Lyrics content..."
}
```

---

## Error Responses

### Missing Query

HTTP `400 Bad Request`

```json
{
    "success": false,
    "error": "You must pass your search parameter (q)",
    "lyrics": null
}
```

---

### No Results Found

HTTP `404 Not Found`

```json
{
    "success": false,
    "error": "could not find lyrics for your request",
    "lyrics": null
}
```

---

### No Lyrics Available

HTTP `404 Not Found`

```json
{
    "success": false,
    "error": "no lyrics available",
    "lyrics": null
}
```

---

### Upstream Service Error (LRCLIB Failure)

HTTP `502 Bad Gateway`

```json
{
    "success": false,
    "error": "Upstream request error details...",
    "lyrics": null
}
```

---

### Unknown Endpoint

HTTP `404 Not Found`

```json
{
    "success": false,
    "error": "The endpoint you used is not registered. Please Use /search/YOUR_QUERY to search for a song",
    "lyrics": null
}
```

---

## Response Format

All responses follow this structure:

```json
{
  "success": boolean,
  "error": string | null,
  "lyrics": string | null
}
```

Key order is preserved intentionally.

---

## Notes

- The API relies on LRCLIB as the upstream lyrics provider.
- Results are based on the first search match returned by LRCLIB.
- If `type=synced` is requested but no synced lyrics exist, the API returns `404`.
- The service includes a 10-second upstream timeout.
- Errors from the upstream service are passed through with their original HTTP status codes when possible.

---


## Production Considerations

- Add caching (Redis or in-memory LRU) to reduce upstream load.
- Add rate limiting to prevent abuse.
- Add retries for upstream network instability.
- Consider logging and monitoring for production deployments.

---

## License

MIT
