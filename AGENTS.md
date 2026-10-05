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


## Coding and Implementation Rules

Code in this project should prioritize clarity, correctness, observability,
and learning.

### General Implementation Rules

- Prefer simple and explicit implementations over clever or highly abstract
  solutions.
- Make small, focused changes rather than large rewrites.
- Do not refactor unrelated code while implementing a feature or fixing a bug.
- Do not introduce a new framework, library, dependency, design pattern, or
  abstraction without first explaining why it is needed.
- Prefer the Python standard library when it clearly provides the functionality
  required for the current learning objective.
- Do not implement future roadmap features prematurely.
- Preserve working educational examples when they are still useful for
  understanding or comparison.
- Before replacing an existing implementation, explain what limitation of the
  current implementation requires the change.

### Python

- Use Python 3.12 unless the project explicitly changes its supported version.
- Use 4 spaces for indentation.
- Use clear and descriptive names for variables, functions, classes, and
  modules.
- Use type hints where they improve understanding of interfaces and data flow.
- Add docstrings to public functions, classes, and methods when they help
  explain purpose, inputs, outputs, or behavior.
- Keep functions focused on one clear responsibility.
- Prefer readable code over compressed one-line expressions.
- Avoid unnecessary global state.
- Use `if __name__ == "__main__":` when a module is intended to be executable
  directly.

### Networking Code

- Keep socket operations explicit while the underlying networking behavior is
  being learned.
- Do not replace direct socket programming with a higher-level networking
  framework unless explicitly requested or the underlying socket behavior has
  already been understood.
- Clearly distinguish strings, encoded bytes, protocol messages, and data
  received from sockets.
- Do not assume that one call to `send()` corresponds to one call to `recv()`.
- Do not assume that one TCP segment corresponds to one application message.
- Treat TCP as a byte-stream transport and implement application-message
  boundaries explicitly when framing is introduced.
- Make buffer sizes, timeouts, addresses, ports, and other networking values
  understandable rather than hiding them without explanation.
- Explain relevant socket errors and operating-system behavior instead of
  merely suppressing exceptions.

### Protocol Code

- Keep serialization and deserialization logic separate from socket
  communication.
- Make protocol fields and byte layouts explicit.
- When binary fields are introduced, document their size, meaning, byte order,
  and valid range.
- Validate protocol inputs where doing so makes protocol behavior clearer and
  safer.
- Encoding and decoding operations should be understandable and testable
  independently from the network.
- Do not silently discard malformed or unexpected protocol data.
- When parsing fails, make the reason observable through an appropriate error
  or diagnostic message.

### Logging and Observability

- Use the project's logging helper instead of adding unrelated logging
  mechanisms without a reason.
- Prefer meaningful log messages that describe important state transitions,
  transmitted data, received data, errors, and connection lifecycle events.
- Do not use logging as a substitute for understanding program behavior.
- When useful for protocol learning, show important byte data in a readable
  representation such as hexadecimal while preserving the original bytes.
- Never log passwords, API keys, authentication tokens, private credentials,
  or other secrets.

### Error Handling

- Do not catch exceptions only to hide them.
- Catch specific exceptions when the program can meaningfully handle or
  explain them.
- Preserve useful diagnostic information when reporting failures.
- During learning exercises, explain where an error originated and which
  software or networking layer produced it.
- Do not add retry loops, fallback behavior, or automatic recovery until the
  failure being handled has first been understood.

### Dependencies

- Do not add external Python packages merely for convenience when the standard
  library is sufficient for the learning objective.
- Before adding a dependency, explain:
  1. what problem it solves,
  2. why the existing project cannot reasonably solve that problem,
  3. what abstraction the dependency introduces, and
  4. what the user would no longer see or implement directly.
- Record required Python dependencies in the project's dependency file when
  such dependencies are introduced.

### AI-Generated Changes

- Never assume generated code is correct merely because it runs.
- Explain significant generated code before considering the task complete.
- Keep AI-generated changes small enough that the user can inspect and
  understand them.
- After changing code, review the resulting diff and identify the important
  changes.
- Verify behavior through execution, tests, logs, packet captures, or other
  appropriate evidence.
- If the user cannot explain an important part of the implementation, prefer
  teaching that part before adding more complexity.