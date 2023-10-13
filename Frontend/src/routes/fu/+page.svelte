<script type="text/javascript">
	import { io } from "socket.io-client";
	var socket = io('http://172.21.112.249:8002');

	socket.on('connect', function () {
		socket.emit('my_event', {data:"Hello"});
	});

	socket.on('my_response', function (data) {
		console.log(data.data);
	});
</script>