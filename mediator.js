import express from "express";
import { io as ioClient } from "socket.io-client"
import { Server } from "socket.io";
import { createServer } from "http";

const app = express();
const httpServer = createServer(app);
const ioServer = new Server(httpServer);

const mediatorSocket = ioClient.connect('http://35.209.28.30:3000');

// Relay multiplayer server events to player
mediatorSocket.on('connect', () => {
    console.log('Connected to server');

    mediatorSocket.on('startGame', () => {
        ioServer.emit('startGame');
    });

    mediatorSocket.on('stopGame', () => {
        ioServer.emit('stopGame');
    });

    mediatorSocket.on('gameFull', () => {
        ioServer.emit('gameFull');
    });

    mediatorSocket.on('playerColor', (color) => {
        ioServer.emit('playerColor', color);
    });
})

// Relay player events to multiplayer server
ioServer.on('connection', (playerSocket) => {
	console.log('A client connected');
    let name = '';

    playerSocket.on('disconnect', () => {
		console.log(`${name} disconnected`);
        mediatorSocket.emit('playerDisconnect', name);
    });

    playerSocket.on('joinGame', (playerName) => {
        console.log(`${playerName} joined the game`);
        name = playerName;
        mediatorSocket.emit('joinGame', playerName);
    });

	playerSocket.on('pixels', (pixels) => {
        mediatorSocket.emit('pixels', pixels);
    });

    playerSocket.on('scoreGraph', (scoreGraph) => {
        mediatorSocket.emit('scoreGraph', scoreGraph);
    });
});

httpServer.listen(8080, () => console.log("Server started on port 8080"));
