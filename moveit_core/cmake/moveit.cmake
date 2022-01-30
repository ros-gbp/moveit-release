macro(moveit_build_options)
  # for Bionic
  if(CMAKE_CXX_COMPILER_ID STREQUAL "GNU" AND CMAKE_CXX_COMPILER_VERSION VERSION_LESS "9")
    if(NOT "${CMAKE_CXX_STANDARD}")
      set(CMAKE_CXX_STANDARD 14)
    endif()
    set(CMAKE_CXX_STANDARD_REQUIRED ON)
    set(CMAKE_CXX_EXTENSIONS OFF)
  endif()

  find_package(backward_ros QUIET)

  if(NOT CMAKE_CONFIGURATION_TYPES AND NOT CMAKE_BUILD_TYPE)
    message("${PROJECT_NAME}: You did not request a specific build type: Choosing 'Release' for maximum performance")
    set(CMAKE_BUILD_TYPE Release)
  endif()

  option(MOVEIT_CI_WARNINGS "Enable all warnings used by CI" ON)
  if(MOVEIT_CI_WARNINGS)
    if (CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
      add_compile_options(-Wall -Wextra -Wwrite-strings -Wunreachable-code -Wpointer-arith -Wredundant-decls -Wcast-qual)
    endif()
    if (CMAKE_CXX_COMPILER_ID STREQUAL "Clang")
      add_compile_options(-Wall -Wextra -Wwrite-strings -Wunreachable-code -Wpointer-arith -Wredundant-decls -Wcast-qual)
    endif()
  endif()
endmacro()
