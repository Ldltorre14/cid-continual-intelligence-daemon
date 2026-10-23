pub mod brain {
    tonic::include_proto!("brain");
}

use brain::brain_service_client::BrainServiceClient;
use brain::DataRequest;
use std::io::{self, Write};

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    
    let mut client = BrainServiceClient::connect("http://[::1]:50051").await?;
    
    loop {
        let mut input = String::new();
        io::stdin().read_line(&mut input).expect("Failed at reading input");
        
        let request = tonic::Request::new(DataRequest{
            prompt: input.into()
        });
        let response = client.process_data(request).await?;

        println!("Response: {:?}", response.get_ref());   
    }
}

