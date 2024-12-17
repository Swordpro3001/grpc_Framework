
## 1. Introduction

This lesson introduces the Remote Procedure Technology (RPC).

## 2. Description

This exercise is intended to demonstrate the functionality and 
implementation of Remote Procedure Call (RPC) technology using the Open Source High Performance gRPC Framework **gRPC Frameworks** ([https://grpc.io](https://grpc.io/)). It shows that this framework can be used to develop a middleware system for connecting several services developed with different programming languages.

## 3. Questions

- What is gRPC, and why does it work across languages and platforms?
    - gRPC is a Cross Language communication Framework which allows Programms to make functions Calls from another program as it was a local call via the stub
- Describe the RPC life cycle, starting with the RPC client?
    - The  Client “compiles” the Stub
    - the Stub connects to the Server
    - The Client creates a request and serializes it
    - The request is sent over HTTP
    - The Server recieves the request and deserializes it
- Describe the workflow of Protocol Buffers?
    - Define a Data Schema with a `.proto`File ending
    - Compile the file with `protoc --lang_out=. proto.proto`
    - Serialize the Data with the specific language
    - Transmit the Data via the stub
    - Deserialize the Data
- What are the benefits of using protocol buffers?
    - Efficient Serialization
    - Cross Language Support
    - Backward and Forward Compatibility
    - Strongly Typed Variables
    - Well Defined Schemas
- When is the use of protocol not recommended?
    - When human readability is important
    - When a flexible Schema is needed
    - When working on a small project
- List 3 different data types that can be used with protocol buffers?
    - double
    - float
    - int32
    - int64
    - uint32
    - uint64
    - sint32
    - sint64
    - bool
    - string
    - bytes

## 4. Code

### Create a basic Proto file with a Service and 2 messages

- A service or class is declared with the `service` tag and is filled with functions
- functions are declared with `rpc NAME (args) returns (return);`
- Argument and Return-types must be declared with the `message` tag and can be filled with variables

### Generate the Python files needed for implementation

<aside>
🧑‍💻

`python -m grpc_tools.protoc -I. --python_out=. --pyi_out=. --grpc_python_out=. ./proto.proto`

</aside>

- `-I` Path
- `--python_out` Where the basic class will be put out
- `--pyi_out` The interface out
- `--grpc_python_out` The abstract classes output
- File

### Write a [`server.py`](http://server.py) File

```python
class ElectionDataService(election_data_pb2_grpc.ElectionDataServicer):
    def GetElectionResults(self, request, context):
        return election_data_pb2.ElectionResponse(candidate="John Doe", votes=1234)
```

This Class is the Python representation from the in the Protofile declared Service.

```python
def serve():
    port = 50051
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    data.add_GigiServicer_to_server(Data(), server)
    server.add_insecure_port('[::]:{}'.format(port))
    server.start()
    print(f'Listening on port {port}')
    server.wait_for_termination()
```

Now we need to run the Server and attach the `GigiServicer` to the Server

### `client.py`

We can attach the Client to the Address and Port (localhost, 50051) and invoke functions from our Server

```python
with grpc.insecure_channel('127.0.0.1:50051') as channel:
    stub = gigi_pb2_grpc.GigiStub(channel)
    response: gigi_pb2.HeloResponse = stub.Helo(
		    gigi_pb2.HeloRequest(vname="Franz", nname="Puerto"))
    print(response.reply)
```

### Run

Now if we run the `server.py` and the `client.py` we should get an output which should look like that

## Election Data

To transfer the election data, one has to change the `proto` file

### Code change

we add following code to the service

```protobuf
service ElectionData {
  rpc GetElectionResults (ElectionRequest) returns (ElectionResponse);
}
```

and then we declare an empty request because we don’t need any

```protobuf
message ElectionRequest {
  string region = 1;
}

message ElectionResponse {
  string candidate = 1;
  int32 votes = 2;
}
```

and a response with all attributes of the election Data has

After compiling the `proto` file, we just add this function to the `server.py` file

```python
def GetElectionResults(self, request, context):
        # Example data
        return election_data_pb2.ElectionResponse(candidate="John Doe", votes=1234)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    election_data_pb2_grpc.add_ElectionDataServicer_to_server(ElectionDataService(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    server.wait_for_termination()

```

### Output

after running the `client.py` file, we get this response

```protobuf
Candidate: John Doe, Votes: 1234
```
