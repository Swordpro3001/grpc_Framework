import grpc
from concurrent import futures
import election_data_pb2
import election_data_pb2_grpc

class ElectionDataService(election_data_pb2_grpc.ElectionDataServicer):
    def GetElectionResults(self, request, context):
        # Example data
        return election_data_pb2.ElectionResponse(candidate="John Doe", votes=1234)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    election_data_pb2_grpc.add_ElectionDataServicer_to_server(ElectionDataService(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
