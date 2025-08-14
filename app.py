from flask import Flask, request, Response
import requests

app = Flask(__name__)

@app.route('/proxy')
def proxy():
    url = request.args.get('url')
    if not url:
        return "Missing 'url' parameter", 400

    try:
        # Fetch the content from the target URL
        resp = requests.get(url)
        headers = dict(resp.headers)
        # Remove headers that may break CORS
        headers.pop('Content-Encoding', None)
        headers.pop('Content-Length', None)

        # Add CORS headers so browser allows access
        headers['Access-Control-Allow-Origin'] = '*'
        headers['X-Proxy-By'] = 'MyPythonProxy'

        return Response(resp.content, headers=headers, status=resp.status_code)
    except Exception as e:
        return f"Error fetching URL: {str(e)}", 500

if __name__ == "__main__":
    app.run(debug=True)
