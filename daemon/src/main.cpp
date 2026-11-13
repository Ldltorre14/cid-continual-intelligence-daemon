#include <iostream>
#include <string>

#include "brain_client.hpp"


int main() {
    BrainClient client(BrainClientConfig{"localhost:50051"});
    std::string input;

    while (std::getline(std::cin, input)) {
        client.processData(input);    
    }

    return 0;
}