# Tic-Tac-Toe Winners count

This is a simple Tic-Tac-Toe game implemented using Python and sockets.

**How to play:**
1. **Start the server:** Run the `server.py` script in your preffered IDE or by typing "**python server.py** " in a terminal set to the directory where the program is installed.
2. **Enter Details** You will be prompted to enter in the Host IP and port number you would like to use. Enter two valid options and the server will start and begin to listen on that port.
3. **Start the Clients** On two other devices, load the client.py into your IDE and start it, or similairly use your terminal and type "**python client.py**". You will be prompted to enter in the host and port. Entering the same as the server will connect a client. Do this twice for both clients.
4. **Play the game** Once you have two clients connected, the game will begin. Play tic tac toe as normal. When a game reaches an end state (ie. a tie or a win) a message will declare so. The board will be reset and another game can be played. Each client will have individual score counts counting ties and wins.
5. **Quitting the game** When you are ready to quit playing, simply click the disconnect button and you will be removed from the server.

**Technologies used:**
* Python
* Sockets
* JSON
* threading
* Logging
* Tkinter

# Messaging protocol
The clients need to be able to communicate with each other as well as the server. For this purpose JSON validation is done to determine what each message type is supposed to be once its sent. Each message has a Message Type that defines the action and the Message Data which is the actual contents of the message.
## Message types
* Join: when the client sends this message it tells the server they want to game. They are placed in a waiting room until another client also joins and enteres the waiting room. In this message the data is less important as it can't change anything.
* Move: This will be the message the client sends when they want to make a move in the game. The Type is "move" the data will be one of the 9 available spaces.
* Quit: this message will be what a client sends when they are done playing the game. Again the data here is less important than the type.

# Server Responses
The server has to process the messages sent by clients. This is done by validating a JSON format. After each message is validated the server may need to respond in some way.
* Join: If a player joins a server succesfully, the server will send a confirmation response.
* Move: If a player makes a valid move, the server confirms this and updates the board.
* Win: If a players move results in a win condition, the server will send a message to both players acknowledging this.
* Tie: If a game ends in a stalemate, the game will reset and increment the tie counter.
* Invalid Command: If the server gets some command that doesn't align with any valid JSON it will send a response to notify the client of this and ask for another.
* Disconnect: When a player quits, the server will recognize this and removes them from the game.

# Game State Consistency
In order to maintain the integrity of the game of tic tac toe, the server implments and maintains a game board that is synchronized
across the two people playing.
* It maintains which player is the "current" player who is in control of the current move.
* It assigns each player a unique ID to facilitate this easier.
* Turn based play helps to enforce consistency of the gameboard between the two players. If a player tries to take a move outside of there turns
the server will send an error message to them.
* When the current player finishes there move, the server checks the board for a win condition (three in a row) and declares a winner
if the condition is in fact met.
* The server additionally checks for a stalemate condition, which in this case is simply if the board is completely full without a winner, not
if no win is possible.
* Once the move is made, the game state is broadcast to both clients which updates there copy of the board. This also includes the ID of the
current player as well as a message declaring a win or stalemate.
* Should a player disconnect from the game early, the server will notify the remaining player and reset the board. 
**Additional resources:**


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

## Security/Risk Evaluation
* There is no authentication in my current implementation, which means anyone can connect including malicious actors.
* There is also no input validation currently. The JSON does only accept certain data types but does not do data validation so bad input could crash the server. For instance, the JSON may expect numbers between 0 and 8 but doesn't actually check if that is sent in the message type, just that the message is an expected type.
* This server is very vulnerable to a DDOS attack as there is no input limit so it could easily be flooded to the point of not functioning.
* There is no encryption currently which means all messages can be intercepted and potentially tampered with.
* The server is also very vulnerable to a replay attack as it does not do any uniqueness check.
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

## Retrospective
* What went right: I'm very pleased with how the UI for the client proram turned out. It's easy to use and easy to understand what each part does. Additionally, the messaging and use of JSON worked out very well for keeping the game consistent across the multiple players, by assigning the different buttons a JSON data message, it means it's difficult for users to accidentally send bad data.
* What could be improved on: There are a few bugs I was just not able to track down. The most notable one is that when a player disconnects and reconnects, sometimes but not always the board does not reset and both players get softlocked where no matter who presses which position, the game claims "invalid input or not your turn". I'm fairly sure it's caused by a desync somewhere on the server but I havent nailed it down. Additionally, I have a bug where when a player disconnects and reconnects, the original player is not removed from the list of active players which leaves a phantom second player. As far as improvements to the code itself, I could have fairly simply implemented code to allow for more than 2 players to play at once. Create a new room for every two players so multiple games can run at the same time for many players. On top of this, it wouldn't be too difficult to implement a couple new games, notably battleship as I could use the same UI and have players initially mark their board with where they want their ships and the opponent clicks spots and they are marked as hits or misses until one wins.
