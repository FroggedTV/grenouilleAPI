define({
  "name": "GrenouilleAPI",
  "version": "1.1.0",
  "description": "API used with multiple FroggedTV services.",
  "header": {
    "title": "Presentation",
    "content": "<h1>Global</h1>\n<h3>Endpoints access</h3>\n<p>Endpoints are protected in 2 possible ways, specified in endpoint headers. API calls are limited to 200 per minutes per ip.</p>\n<ul>\n<li>If the <code>API_KEY</code> header is present, you can use the endpoint with such a key. Keys will (TODO) be secured using a <code>scope</code>.</li>\n<li>If the <code>Authorization</code> header is present, you can use the endpoint as a logged user. You need to follow the authorization process to get a <code>Refresh</code> token then a <code>Auth</code> token. Endpoints are restricted using <code>UserRights</code>.</li>\n</ul>\n<h3>Parameter format</h3>\n<p>A typical curl command to access an endpoint is:</p>\n<pre><code>curl -X &lt;COMMAND&gt; --header &quot;&lt;HEADER&gt;&quot; -d &quot;&lt;JSON_PAYLOAD&gt;&quot; https://grenouilleapi.the-cluster.org/api/&lt;ENDPOINT&gt;\n</code></pre>\n<ul>\n<li><code>&lt;COMMAND&gt;</code> is <code>GET</code> or <code>POST</code>.</li>\n<li><code>&lt;HEADER&gt;</code> is either <code>API_KEY: &lt;KEY&gt;</code> with a valid key or <code>Authorization: Bearer &lt;TOKEN&gt;</code> for a user accessed endpoint.</li>\n<li><code>&lt;ENDPOINT&gt;</code> is a valid endpoint path.</li>\n<li><code>&lt;JSON_PAYLOAD&gt;</code> is the JSON payload in both <code>GET</code> and <code>POST</code> cases.</li>\n</ul>\n<h3>Return format</h3>\n<p>Every endpoint returns a normalized JSON answer with the following format:</p>\n<pre><code>{\n  &quot;error&quot;: &quot;&lt;&gt;&quot;, \n  &quot;payload&quot;: {}, \n  &quot;success&quot;: &quot;&lt;&gt;&quot;\n}\n</code></pre>\n<p>where <code>success</code> contains either</p>\n<ul>\n<li><code>yes</code> if the endpoint behavior is normal, then <code>payload</code> contains the object answer from the API.</li>\n<li><code>no</code> if the endpoint behavior as an error, then <code>error</code> contains the string error code.</li>\n</ul>\n<hr>\n<h1>Modules</h1>\n<h2>Authentication</h2>\n<p>User authentication module. User logs with Steam, and is redirected to the website with a refresh token valid for 60 days (as a parameter in the URL). The <code>Refresh</code> token is then used to get a <code>Auth</code> token, valid for 1 hour.</p>\n<h2>DotaBots</h2>\n<p>Bots used to host in-house leagues.</p>\n<h2>User</h2>\n<p>User management endpoints.</p>\n<h2>Community</h2>\n<p>Community endpoints for news, calendar, comments.</p>\n<h2>StreamSystem</h2>\n<p>Endpoints used for the automatic streaming system, managing VODs and the forever running OBS.</p>\n"
  },
  "sampleUrl": false,
  "defaultVersion": "0.0.0",
  "apidoc": "0.3.0",
  "generator": {
    "name": "apidoc",
    "time": "2018-07-08T15:21:41.778Z",
    "url": "http://apidocjs.com",
    "version": "0.17.6"
  }
});
