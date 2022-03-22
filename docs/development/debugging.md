# Debugging MEDYAN

## VS Code

Note: On MacOS the default VS Code C++ debugger is buggy so use the CodeLLDB extension instead.

### Build MEDYAN for debug

```console
> MEDYAN_CMAKE_EXTRA_ARGS="-DCMAKE_BUILD_TYPE=Debug" ./conf.sh
> cd build
> make
```

### Set command line arguments

1. Open Run and Debug side panel and click "create a launch.json file".

1. Make `"program":` `"${workspaceFolder}/build/medyan"`.\

2. Make `"cwd":` the directory to run MEDYAN from. For example, `"${workspaceFolder}/examples/2filaments"`

2. Edit the `"args": [],` line to include the command line arguments you want to debug with. For example, `["-s", "systeminput.txt", "-i", ".", "-o", "./sampleResults"]`

1. Save `launch.json`, and now you should be able to create breakpoints and debug in VS Code.