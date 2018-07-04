define({
  "name": "GrenouilleAPI",
  "version": "1.0.5",
  "description": "API used with multiple FroggedTV services.",
  "header": {
    "title": "Presentation",
    "content": "<h1>Global</h1>\n<h3>Endpoints access</h3>\n<p>Endpoints are protected with 2 possible ways, specified in endpoint headers. API calls are limited to 200 per minutes per ip.</p>\n<p>First you can use an APIKey if the &lt;API_KEY&gt; header is present. Otherwise, if you have a logged user, you can use a auth token in the <Authorization> header. In this case, the user needs to have the appropriate user rights to use the endpoint.</p>\n<h3>Parameter format</h3>\n<p>A typical curl command to access an endpoint is:</p>\n<pre><code>curl -X &lt;COMMAND&gt; --header &quot;API_KEY: &lt;KEY&gt;&quot; -d &quot;&lt;JSON_PAYLOAD&gt;&quot; https://grenouilleapi.the-cluster.org/api/&lt;ENDPOINT&gt;\n</code></pre>\n<ul>\n<li><code>&lt;COMMAND&gt;</code> is <code>GET</code> or <code>POST</code>.</li>\n<li><code>&lt;KEY&gt;</code> is a valid API key if necessary.</li>\n<li><code>&lt;ENDPOINT&gt;</code> is a valid endpoint path.</li>\n<li><code>&lt;JSON_PAYLOAD&gt;</code> is the JSON payload in both <code>GET</code> and <code>POST</code> cases.</li>\n</ul>\n<h3>Return format</h3>\n<p>Every endpoint returns a normalized JSON answer with the following format:</p>\n<pre><code>{\n  &quot;error&quot;: &quot;&lt;&gt;&quot;, \n  &quot;payload&quot;: {}, \n  &quot;success&quot;: &quot;&lt;&gt;&quot;\n}\n</code></pre>\n<p>where <code>success</code> contains either</p>\n<ul>\n<li><code>yes</code> if the endpoint behavior is normal, then <code>payload</code> contains the object answer from the API.</li>\n<li><code>no</code> if the endpoint behavior as an error, then <code>error</code> contains the string error code.</li>\n</ul>\n<hr>\n<h1>Modules</h1>\n<h2>Authentication</h2>\n<p>User authentication module. User logs with steam, and is redirected to the website with a refresh token valid for 60 days. The refresh token is then used to get a auth token, valid for 1 hour. The auth token is the base of User-based endpoint access.</p>\n<h2>DotaBots</h2>\n<p>Bots used to host inhouse leagues.</p>\n<h2>User</h2>\n<p>User management endpoints.</p>\n<h2>Community</h2>\n<p>Community endpoints for news, calendar, comments.</p>\n<h2>StreamSystem</h2>\n<p>Endpoints used for the automatic streaming system, managing VODs and the forever running OBS.</p>\n"
  },
  "sampleUrl": false,
  "defaultVersion": "0.0.0",
  "apidoc": "0.3.0",
  "generator": {
    "name": "apidoc",
    "time": "2018-07-04T16:45:51.497Z",
    "url": "http://apidocjs.com",
    "version": "0.17.6"
  }
});
