from concurrent import futures
import grpc 
import grpc_server.brain_pb2 
import grpc_server.brain_pb2_grpc
import logging

from brain.cid_core import CID

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("brain_grpc_server")


class BrainService(grpc_server.brain_pb2_grpc.BrainServiceServicer):
    def __init__(self, agent: CID):
        self.agent = agent

    def ProcessData(self, request, context):
        logger.info("Brain Service started a ProcessData request...")
        
        try:
            result = self.agent.run_command(command=request.prompt)
            response_text = str(result)
            success = True
            logger.info("CID Inference success")
        
        except Exception as e:
            logger.error(f"CID Inference failed {e}")
            response_text = e 
            success = False 

        return grpc_server.brain_pb2.DataResponse(
            response_text=response_text, 
            success=success)


