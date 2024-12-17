import grpc
import election_data_pb2
import election_data_pb2_grpc

def run():
    with grpc.insecure_channel('localhost:50052') as channel:
        stub = election_data_pb2_grpc.ElectionDataStub(channel)
        response = stub.GetElectionResults(election_data_pb2.ElectionRequest(region="Region1"))
        print(f"Candidate: {response.candidate}, Votes: {response.votes}")

if __name__ == '__main__':
    run()