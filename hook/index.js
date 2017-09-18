var http = require('http');
var spawn = require('child_process').spawn;
var createHandler = require('github-webhook-handler');
var handler = createHandler({path: '/webhooks', secret: 'zz'});

http.createServer(function(req, res) {
	handler(req, res, function(err) {
		res.statusCode = 404;
		res.end('This location is forbidden');
	})
}).listen(8889);

handler.on('error', function(err) {
	console.error('Error:', err.message);
});

handler.on('push', function(event) {
	console.log('Received a push event fro %s to %s', event.payload.repository.name, event.payload.ref);

	runCommand('sh', ['./deploy.sh'], function(txt) {
		console.log(txt);
	});
});
// 这是为了响应ping event使用的，测试通过后可以将这段代码注释掉
handler.on('ping', function(event) {
	console.log('Received a ping event fro %s to %s', event.payload.repository.name, event.payload.ref);

	runCommand('sh', ['./deploy.sh'], function(txt) {
		console.log(txt);
	});
});

function runCommand(cmd, args, callback) {
	console.log('Running command');
	var child = spawn(cmd, args);
	var response = '';

	child.stdout.on('data', function(buffer) {response += buffer.toString();});
	child.stdout.on('end', function(){callback(response);});
}