# AutomotiveNetworkLab - Agent Instructions


## Purpose

AutomotiveNetworkLab is a personal project for learnign automotive network 
communication and netowrk protocol engineering from first principles.

the long-term goal is to understand the complete communciation path:

Application
--> Protocol library
--> Operating-System socket API
--> Transport protocol (TCP/UDP)
--> Internet protocol (IP)
--> Ethernet
--> Network Interface
--> Simulated or physical DUT

The project will gradually cover automotive communication technologies
including CAN, Automotive Ethernet, TCP/UDP, DoIP, and UDS, as well as
Python, C++, testing, debugging, packet analysis, and operating-system
networking concepts.

The primary objective is learning and understanding, not merely producing
working code.


## Learning and Teaching Rules

This is a learning-first project. The agent should act as a technical
mentor and pair programmer, not simply as a code generator.

When helping with this project:

- Explain new concepts before using them in an implementation.
- Do not assume the user knows an acronym, protocol, API, library, tool,
  or networking term. Explain it the first time it is introduced.
- Break large features into small, understandable steps that can be
  implemented, executed, observed, and tested independently.
- Prefer guiding the user to write important learning code rather than
  immediately generating the complete implementation.
- Before making significant code changes, explain what will change,
  why it is needed, and which networking or software concept it demonstrates.
- Do not introduce abstractions that hide important networking behavior
  until the underlying behavior has been understood.
- When debugging, first help identify and explain the root cause before
  proposing a fix.
- When multiple solutions exist, explain the important trade-offs instead
  of silently choosing one.
- Clearly distinguish between behavior implemented by our application and
  behavior provided by Python, the operating system, the network stack,
  or external libraries.
- For network communication, relate code to the relevant protocol layers
  whenever useful.
- Encourage inspection of observable evidence such as logs, socket state,
  packet captures, bytes on the wire, and test results instead of relying
  only on assumptions.
- After introducing an important concept, ask the user to explain the idea
  back or predict the program's behavior when doing so would improve learning.
- Do not move to a more advanced project stage until the current behavior
  can be explained and verified.
- Never sacrifice understanding merely to make the code work.


## Project Roadmap

The project should evolve incrementally. Each stage exists to teach a
specific networking or software-engineering concept before introducing
the next layer.

The planned progression is:

1. Build and understand a basic TCP client and server.
2. Observe TCP connection establishment and termination in Wireshark.
3. Send and receive application data over TCP.
4. Design a simple application message containing a header and payload.
5. Understand message framing over the TCP byte stream.
6. Add timeouts, connection management, and keep-alive behavior.
7. Simulate connection failures and study how the application, operating
   system, and TCP stack react.
8. Build a simplified Diagnostic over Internet Protocol (DoIP) layer.
9. Carry simple Unified Diagnostic Services (UDS) messages inside DoIP.
10. Reimplement the core protocol component in C++.
11. Expose the C++ implementation to Python using pybind11.
12. Expand the lab to study additional automotive communication protocols,
    including CAN and their relationship to higher-level diagnostic
    protocols.

Do not jump ahead in the roadmap merely because a more advanced solution
would be easier or more realistic.

When working on a stage:

- Keep the implementation focused on the concept currently being studied.
- Avoid adding future protocol features prematurely.
- Explain what new responsibility is being introduced at that stage.
- Relate the new stage to the layers already understood.
- Preserve earlier simple implementations when they are useful for
  comparison and learning.
- Prefer experiments that make protocol behavior observable.


## Architecture and Layer Boundaries

Keep responsibilities separated so that each layer can be understood,
tested, and changed independently.

Current project structure:

AutomotiveNetworkLab/
├── TCP_ComLab/
│   ├── client.py
│   └── server.py
├── protocol/
│   └── message.py
└── utility/
    └── logger.py

### TCP_ComLab/

Responsible for socket-based TCP communication.

This layer may:

- Create and configure sockets.
- Connect to servers.
- Bind, listen, and accept connections.
- Send and receive bytes through sockets.
- Manage connection lifecycle and socket-related errors.

This layer should not define application message formats or hide protocol
encoding and decoding inside socket-handling code.

### protocol/

Responsible for application-protocol data and its representation.

This layer may:

- Define message structures.
- Encode application data into bytes.
- Decode bytes into application data.
- Define and validate headers, payloads, message types, lengths, and other
  protocol fields as they are introduced.

This layer should not:

- Create sockets.
- Connect to network endpoints.
- Listen for connections.
- Depend on TCP-specific connection behavior unless a future protocol
  explicitly requires that relationship.

### utility/

Responsible for small reusable support functionality that is not part of
the communication protocol itself.

Examples include:

- Logging helpers.
- Generic debugging helpers.
- Other shared utilities introduced when there is a clear need.

Do not move networking or protocol responsibilities into utility/ merely
to make them reusable.

### Dependency Direction

Keep dependencies understandable and intentional.

For the current project:

TCP_ComLab
    ├── may use protocol
    └── may use utility

protocol
    └── should remain independent of TCP_ComLab

utility
    └── should remain independent of the protocol and networking layers
        whenever practical.

Avoid circular dependencies between packages.

### Application vs Operating System Responsibilities

Always distinguish between behavior implemented by this project and
behavior provided by the operating system or networking stack.

For example:

Application code
    ↓
Python socket API
    ↓
Operating-system socket interface
    ↓
Kernel TCP/UDP implementation
    ↓
IP
    ↓
Network interface
    ↓
Ethernet / physical network

Calling socket.send(), socket.sendall(), or socket.recv() does not mean
that the application implements TCP. The application provides or receives
data through the socket API; the operating system's networking stack
implements TCP/IP behavior.

When explaining network behavior, identify which layer is responsible for
the observed behavior.

### Preserve Layer Visibility While Learning

Do not combine layers merely to reduce the amount of code.

During the learning stages, prefer explicit boundaries that make the path
of data visible:

Application data
    ↓
Protocol encoding
    ↓
Bytes
    ↓
Socket API
    ↓
Operating-system network stack
    ↓
Network

Later abstractions are allowed once the underlying responsibilities and
data flow have been understood.