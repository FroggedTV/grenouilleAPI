define({
  "name": "GrenouilleAPI",
  "version": "1.1.0",
  "description": "API used with multiple FroggedTV services.",
  "header": {
    "title": "Presentation",
    "content": "<hr>\n<h3>Endpoints access</h3>\n<p>Some endpoints are free to use but most of them are protected in 2 possible ways, either with a user login or an API-key. Such endpoints require a full auth process to be accessed. All API calls are limited to 200 per minutes per ip.</p>\n<ul>\n<li>If the application is a web based application where the user needs to login, this application will use the <code>RefreshTokenGetWithSteam</code> endpoint to get a <code>JWT</code>.</li>\n<li>In other cases, the application with use an application key to get a <code>JWT</code>, using <code>RefreshTokenGetWithKey</code> endpoint.</li>\n</ul>\n<p>Refresh tokens are long lived (60 days) and must be saved in a secured place. They give access to <code>AuthTokenGet</code> endpoint, generating a Auth token. This token is short lived (1 hour) and contains user scopes (endpoint restrictions).</p>\n<h3>Parameter format</h3>\n<p>A typical curl command to access an endpoint is:</p>\n<pre><code>curl -X &lt;COMMAND&gt; --header &quot;&lt;HEADER&gt;&quot; -d &quot;&lt;JSON_PAYLOAD&gt;&quot; https://grenouilleapi.the-cluster.org/api/&lt;ENDPOINT&gt;\n</code></pre>\n<ul>\n<li><code>&lt;COMMAND&gt;</code> is <code>GET</code> or <code>POST</code>.</li>\n<li><code>&lt;HEADER&gt;</code> use the format <code>Authorization: Bearer &lt;TOKEN&gt;</code> with a valid <code>JWT</code> token.</li>\n<li><code>&lt;ENDPOINT&gt;</code> is a valid endpoint path.</li>\n<li><code>&lt;JSON_PAYLOAD&gt;</code> is the JSON payload in both <code>GET</code> and <code>POST</code> cases.</li>\n</ul>\n<h3>Return format</h3>\n<p>Every endpoint returns a normalized JSON answer with the following format:</p>\n<pre><code>{\n  &quot;error&quot;: &quot;&lt;&gt;&quot;, \n  &quot;payload&quot;: {}, \n  &quot;success&quot;: &quot;&lt;&gt;&quot;\n}\n</code></pre>\n<p>where <code>success</code> contains either</p>\n<ul>\n<li><code>yes</code> if the endpoint behavior is normal, then <code>payload</code> contains the object answer from the API.</li>\n<li><code>no</code> if the endpoint behavior as an error, then <code>error</code> contains the string error code.</li>\n</ul>\n<hr>\n<h2>Authentication</h2>\n<p>Authentication module, either with Steam for a user, or with an api key for other applications.</p>\n<h2>DotaBots</h2>\n<p>Bots used to host in-house leagues.</p>\n<h2>User</h2>\n<p>User management endpoints.</p>\n<h2>Community</h2>\n<p>Community endpoints for news, calendar, comments.</p>\n<h2>StreamSystem</h2>\n<p>Endpoints used for the automatic streaming system, managing VODs and the forever running OBS.</p>\n"
  },
  "sampleUrl": false,
  "defaultVersion": "0.0.0",
  "apidoc": "0.3.0",
  "generator": {
    "name": "apidoc",
    "time": "2018-07-17T02:09:37.308Z",
    "url": "http://apidocjs.com",
    "version": "0.17.6"
  }
});
