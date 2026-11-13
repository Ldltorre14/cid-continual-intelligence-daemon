cmake_minimum_required(VERSION 3.18)
project(cid_daemon CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(Protobuf REQUIRED)
find_package(PkgConfig REQUIRED)
pkg_check_modules(GRPCPP REQUIRED IMPORTED_TARGET grpc++)
find_program(PROTOC protoc REQUIRED)
find_program(GRPC_CPP_PLUGIN grpc_cpp_plugin REQUIRED)

set(PROTO_DIR "${CMAKE_SOURCE_DIR}/../proto")
set(GEN_DIR "${CMAKE_BINARY_DIR}/generated")
file(MAKE_DIRECTORY "${GEN_DIR}")

add_custom_command(
    OUTPUT  "${GEN_DIR}/brain.pb.cc" "${GEN_DIR}/brain.pb.h"
            "${GEN_DIR}/brain.grpc.pb.cc" "${GEN_DIR}/brain.grpc.pb.h"
    COMMAND ${PROTOC}
            --proto_path=${PROTO_DIR}
            --cpp_out=${GEN_DIR}
            --grpc_out=${GEN_DIR}
            --plugin=protoc-gen-grpc=${GRPC_CPP_PLUGIN}
            ${PROTO_DIR}/brain.proto
    DEPENDS "${PROTO_DIR}/brain.proto"
)

add_executable(cid_daemon
    src/main.cpp
    "${GEN_DIR}/brain.pb.cc"
    "${GEN_DIR}/brain.grpc.pb.cc"
)
target_include_directories(cid_daemon PRIVATE
    "${GEN_DIR}"
    "${CMAKE_SOURCE_DIR}/include"
)
target_link_libraries(cid_daemon PRIVATE PkgConfig::GRPCPP protobuf::libprotobuf)