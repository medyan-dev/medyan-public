# Building MEDYAN

To use MEDYAN, one needs to build it from the source code. The source code is available for download at <http://medyan.org/download.html>. One can also clone the git repository for the latest version.

## Requirements

A C++17 compatible compiler such as the following is required:

- gcc >= 7
- clang >= 5
- MSVC with Visual Studio 2017 15.7 and above

The following tools are also required:

- CMake >= 3.13
- git >= 2.7.0

`medyan` is also dependent on several external libraries, which will be automatically installed before building.

## Steps

The preferred way of building medyan is to generate the build files using CMake. From the MEDYAN root directory, use either of the following scripts to generate build files.

- `conf.sh` on Linux and MacOS. It will generate `Makefile` in the `build` directory by default.
- `conf.ps1` on Windows. It will generate the Visual Project solution in the `build` directory by default.

Under the hood, the scripts use `vcpkg` to install and configure the required external libraries, and use `cmake` to generate the build files. The external library installation normally happens only for the first build. External variables can be used to control some of the behaviors of the script.

Setting `MEDYAN_NO_GUI="true"` disables installing GUI libraries and building the GUI.
Setting `MEDYAN_CMAKE_EXTRA_ARGS` passes those arguments to the`cmake` command; for example, setting `MEDYAN_CMAKE_EXTRA_ARGS="-DCMAKE_BUILD_TYPE=Debug"` will build for debug.

On MacOS, one can also change the target build system of the CMake from `make` to Xcode project, by setting `MEDYAN_BUILD_TOOL` to be `"Xcode"`.

**Example 1**: I am building medyan on Linux, and I do not have boost installed anywhere.

```console
> ./conf.sh
> cd build
> make
```

And the medyan would be built in the `build` directory.

**Example 2**: I want to build medyan on my Mac using Xcode.

```console
> MEDYAN_BUILD_TOOL="Xcode" ./conf.sh
```

And an Xcode project file would be in the `build` directory.

**Example 3**: I want to build medyan on Windows.

```console
> .\conf.ps1
```

And a Visual Studio solution file named `medyan.sln` would be in the `build` directory.
