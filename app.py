from flask import Flask, request, Response
import requests
import os

app = Flask(__name__)

@app.route('/proxy')
def proxy():
    url = request.args.get('url')
    if not url:
        return "Missing 'url' parameter", 400

    try:
        # Add headers to mimic a real browser
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/120.0.0.0 Safari/537.36",
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": url
        }

        # Fetch the content from the target URL
        resp = requests.get(url, headers=headers, stream=True, timeout=10)

        # Copy headers but remove those that could break things
        response_headers = {k: v for k, v in resp.headers.items() 
                            if k.lower() not in ["content-encoding", "content-length", "transfer-encoding", "connection"]}

        # Add CORS and custom headers
        response_headers['Access-Control-Allow-Origin'] = '*'
        response_headers['X-Proxy-By'] = 'MyPythonProxy'

        return Response(resp.raw, headers=response_headers, status=resp.status_code)
    except requests.exceptions.RequestException as e:
        return f"Error fetching URL: {str(e)}", 500
    except Exception as e:
        return f"Unexpected error: {str(e)}", 500

# Only used for local testing
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
