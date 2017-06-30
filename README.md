# libunwind Package Recipe for the conan Package Manager

This is an effort to make [libunwind](http://www.nongnu.org/libunwind/)
available through the [conan Package Manager](https://conan.io/).

**NOTE:**
This repository only contains the source code of the conan package recipe.
This is *not* the original libunwind source code.
The original source code is downloaded automatically
from the official libunwind website
during the package build process.
Please visit the original project's website at <http://www.nongnu.org/libunwind>.


## Hosted Packages

Recipes and binary packages built from this repository are hosted at the
[Ocean Conan Package Repository](https://bintray.com/marcokoch/ocean-conan).
To use the repository, add it to your conan remotes like this:

    conan remote add ocean-conan https://bintray.com/marcokoch/ocean-conan

The packages are available in two channels:

`libunwind/1.2.1@marcokoch/stable`:
This channel contains the latest stable package release,
built from the
[v1.2.1](https://github.com/MarcoKoch/conan-libunwind/tree/v1.2.1)
branch of this repository.
Note that 'stable' refers to the packaging only. The package is always built
from stable releases of libunwind.

`libunwind/1.2.1@marcokoch/testing`:
This channel provides recent development builds from the
[master](https://github.com/MarcoKoch/conan-libunwind/tree/master)
branch of this repository.
Feedback on these builds is highly welcome.
They may be buggy, though.

To use libunwind in your project,
use the following lines in your `conanfile.txt`:

    [requires]
    libunwind/1.2.1@marcokoch/stable

Or in your `conanfile.py`

    class MyProject(ConanFile):
        requires = "libunwind/1.2.1@marcokoch/stable"


## Package Options

The package supports the following options:

| Option                       | Possible Values | Default | Description                                       | Equivalent libunwind configure script option |
|------------------------------|-----------------|---------|---------------------------------------------------|----------------------------------------------|
| `shared`                     | `True`, `False` | `False` | Build shared libraries                            | `--enable-shared`                            |
| `enable_coredump`            | `True`, `False` | `False` | Include the unwind-coredump library               | `--enable-coredump`                          |
| `enable_ptrace`              | `True`, `False` | `False` | Include the unwind-ptrace library                 | `--enable-ptrace`                            |
| `enable_setjmp`              | `True`, `False` | `False` | Include the unwind-setjmp library                 | `--enable-setjmp`                            |
| `enable_documentation`       | `True`, `False` | `False` | Include the unwind manpages                       | `--enable-documentation`                     |
| `enable_cxx_exceptions`      | `True`, `False` | `False` | Use libunwind to handle C++ exceptions            | `--enable-cxx-exceptions`                    |
| `enable_debugframe`          | `True`, `False` | `False` | Load the ".debug_frame" section if available      | `--enable-debugframe`                        |
| `enable_block_signals`       | `True`, `False` | `False` | Block signals before performing mutext operations | `--enable-block-signals`                     |
| `enable_conservative_checks` | `True`, `False` | `False` | Validate all memory addresses before use          | `--enable-conservative-checks`               |
| `enable_msabi_support`       | `True`, `False` | `False` | Enable support for Microsoft ABI extensions       | `--enable-msabi-support`                     |
| `enable_minidebuginfo`       | `True`, `False` | `False` | Enable support for LZMA-compressed symbol tables  | `--enable-minidebuginfo`                     |


## License

This package recipe is provided under the 3-Clause BSD license.
See file [LICENSE](LICENSE) for further information.

The original libunwind project is provided under the X11 license.
Please see <https://savannah.nongnu.org/projects/libunwind>.


## Contributing

Feedback and pull requests are highly appreciated.
If you have any questions, feel free to ask in the issue tracker.

To contribute to the original libunwind project,
please interact with the official GitHub mirror at <https://github.com/libunwind/libunwind>.
