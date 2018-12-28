cmake_minimum_required(VERSION 3.12)
project(Ripex_Interaction C)

set(CMAKE_C_STANDARD 99)
set(CMAKE_C_FLAGS -lws2_32)
#add_executable(Ripex_Interaction cTrapReceiver.c SNMP_Manager.c)
add_executable(Ripex_Interaction)