import requests
from flask import Flask, jsonify, request


app = Flask(__name__)
app.json.sort_keys = False


@app.route("/search/<path:q>")
def search_song(q):
    q = (q or "").strip()
    if not q:
        return jsonify({
            "success": False,
            "error": "You must pass your search parameter (q)",
            "lyrics": None
        }), 400

    return_type = request.args.get('type', "plain").strip()

    try:
        r = requests.get("https://lrclib.net/api/search",
                            params={"q": q},
                            timeout=10,
                            headers={"User-Agent": "lyrics.syntaxly.xyz/1.0"}
        )
        r.raise_for_status()

        results: list[dict] = r.json()

        if not results:
            return jsonify({
                'success': False,
                'error': 'could not find lyrics for your request',
                'lyrics': None
            }), 404

        hit = results[0]

        # TODO: refactor this
        if not return_type:
            lyrics = hit.get('plainLyrics') or ""

        if return_type == "plain":
            lyrics = hit.get('plainLyrics')
        elif return_type == "synced":
            lyrics = hit.get('syncedLyrics')

        if not lyrics:
            return jsonify({
                'success': False,
                'error': 'no lyrics available',
                'lyrics': None
            }), 404

        return jsonify({
            'success': True,
            'error': None,
            'lyrics': lyrics.strip()
        }), 200

    except requests.HTTPError as err:
        status_code = err.response.status_code
        return jsonify({
            'success': False,
            'error': err.response.text,
            'lyrics': None
        }), status_code

    except requests.RequestException as err:
        return jsonify({
            'success': False,
            'error': str(err),
            'lyrics': None
        }), 502

    except Exception as ex:
        return jsonify({
            'success': False,
            'error': str(ex),
            'lyrics': None
        }), 502


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'The endpoint you used is not registered. Please Use /search/YOUR_QUERY to search for a song',
        'lyrics': None
    }), 404


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=4005, debug=True)
