# Tic-Tac-Toe Winners count

This is a simple Tic-Tac-Toe game implemented using Python and sockets.

**How to play:**
1. **Start the server:** Run the `server.py` script.
2. **Connect clients:** Run the `client.py` script on two different machines or terminals.
3. **Play the game:** Players take turns entering their moves. The first player to get three in a row wins!
4. **Determine a winner** The player wins will be tallied until they leave the game.

**Technologies used:**
* Python
* Sockets
* JSON

# Messaging protocol
The clients need to be able to communicate with each other as well as the server. For this purpose JSON validation is done to determine what each message type is supposed to be once its sent. Each message has a Message Type that defines the action and the Message Data which is the actual contents of the message.
## Message types
* Join: when the client sends this message it tells the server they want to game. They are placed in a waiting room until another client also joins and enteres the waiting room. In this message the data is less important as it can't change anything.
* Move: This will be the message the client sends when they want to make a move in the game. The Type is "move" the data will be one of the 9 available spaces.
* Chat: This message will be whatever the client wants. The type is "data" and the data is literally anything they want to say to the other player.
* Quit: this message will be what a client sends when they are done playing the game. Again the data here is less important than the type.

# Server Responses
The server has to process the messages sent by clients. This is done by validating a JSON format. After each message is validated the server may need to respond in some way.
* Join: If a player joins a server succesfully, the server will send a confirmation response.
* Move: If a player makes a valid move, the server confirms this and updates the board.
* Win: If a players move results in a win condition, the server will send a message to both players acknowledging this.
* Invalid Command: If the server gets some command that doesn't align with any valid JSON it will send a response to notify the client of this and ask for another.
* Disconnect: When a player quits, the server will recognize this and removes them from the game.

**Additional resources:**
-TBA

# Statement of Work

**Project title:**

Tic Tac Toe Winners Count Edition

**Team:**

Sam Stolley

**Project Objective:**

* This project will demonstrate how server and client scripts interact with each other using sockets. It will 
involve at least 2 players playing a simple game while taking turns.

## **Scope**

**Inclusions:**

* This version of the game will be similair to the standard way most people are familiar with.
* The feature list may grow to include a few additional functionalities not present in the standard game.

**Exclusions**

## Deliverables
* The final product will include a set of two files.
* A single Server file which will run the game and be connected to.
* A single client file that can be replicated for each player who wishes to play.

## Timeline:
**Key Milestones**
* The first step will be to simply design the client and server so they are able to connect to each other without problems
* The second will be to begin the actual design of the game. Creating the game object and creating a simple UI to represent the board.
* The third will be to combine the two things together so that the players do not need to be on the same machine to play.
* 
**Task Breakdown**
* Create Server.py
* Create Client.py
* Create and intigrate game functionality into the two files

## Technical Requirements
**Hardware**
* This should not be more than simply having access to 3 computers capable of running .py programs.

## Software
* Currently the libraries that will definitley be required will be only socket.
* Python will be the sole language so having the language installed will be required.

## Assumptions
* The first assumption I have is that the game board itself will be represented Serverside, this will maintain the integrity of the game and help to avoid the gamestate becoming desynchronized.
* This ties into the second assumption which is that the Player object will be client side. Because the players have no direct interaction with each other and only the game board. This means they will send moves to the server, the server will check if it is valid and then check if a win condition has been reached. Otherwise it will ask the player for a legal move.

## Roles and Responsibilities
* This is a solo project so I will be entirely in charge of all tasks and there will be no communication channels save those with TA's in the event I run into a problem I can't solve myself.

## Additional Notes:
* -TBA
