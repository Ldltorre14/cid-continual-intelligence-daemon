#include <iostream>
#include <memory>
#include <string>

#include <grpcpp/grpcpp.h>
#include "brain.grpc.pb.h"

struct BrainClientConfig{
    std::string host;
};


class BrainClient{
    private:
        std::unique_ptr<brain::BrainService::Stub> stub;
        

    public:
        BrainClient(const BrainClientConfig& config){
            auto channel = grpc::CreateChannel(config.host, grpc::InsecureChannelCredentials());
            this->stub = brain::BrainService::NewStub(channel);
        };

        void processData(const std::string& input){
            brain::DataRequest request;
            request.set_prompt(input);

            brain::DataResponse response;
            grpc::ClientContext context;

            grpc::Status status = this->stub->ProcessData(&context, request, &response);

            if (!status.ok()){
                std::cerr << "Communication with gRPC Brain Server Failed: " << status.error_message() << "\n"; 
            }
            std::cout << "Response: " << response.DebugString() << "n";
        };

};