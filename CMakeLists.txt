find_package(OpenCV REQUIRED)
add_executable(main test.cpp)
target_link_libraries(main ${OpenCV_LIBS})
