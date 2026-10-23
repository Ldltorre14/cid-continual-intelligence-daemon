from brain.cid_core import CID
from config import model_name, device
from grpc_server.brain_grpc_server import BrainService
import grpc_server.brain_pb2_grpc 

import grpc 
from concurrent import futures 
import logging 



logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("main")



def serve():
    agent = CID(
            encoder_model_name=model_name,
            in_embedding_dim=768, 
            out_embedding_dim=3,
            device=device,
            backend="torch",
            model_kwargs={"dtype":"float32"}
        ) 
    
    server = grpc.server(thread_pool=futures.ThreadPoolExecutor(max_workers=3))
    grpc_server.brain_pb2_grpc.add_BrainServiceServicer_to_server(
        servicer=BrainService(agent=agent),
        server=server
    )
    server.add_insecure_port("[::]:50051")
    server.start()
    logger.info("Brain Server listening at port 50051")
    server.wait_for_termination()



if __name__=="__main__":
    serve()