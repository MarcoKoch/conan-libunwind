from conans import ConanFile, AutoToolsBuildEnvironment, tools
from glob import glob
import os, platform, re


class LibunwindConan(ConanFile):
    name = "libunwind"
    version = "1.2.1"
    license = "X11"
    url = "https://github.com/marcokoch/conan-libunwind"
    author = "Marco Koch (marco-koch@t-online.de)"
    description = "A complete open-source implementation of the libunwind API "" \
""currently exists for IA-64 Linux and is under development for Linux on x86, "" \
""x86-64, and PPC64. Partial support for HP-UX and Linux on PA-RISC also exists."
    settings = "os", "compiler", "build_type", "arch"
    options = {
"shared": [True, False],
"enable_coredump": [True, False],
"enable_ptrace": [True, False],
"enable_setjmp": [True, False],
"enable_documentation": [True, False],
"enable_cxx_exceptions": [True, False],
"enable_debugframe": [True, False],
"enable_block_signals": [True, False],
"enable_conservative_checks": [True, False],
"enable_msabi_support": [True, False],
"enable_minidebuginfo": [True, False]
    }
    default_options = '''
shared=False
enable_coredump=False
enable_ptrace=False
enable_setjmp=False
enable_documentation=False
enable_cxx_exceptions=False
enable_debugframe=False
enable_block_signals=False
enable_conservative_checks=False
enable_msabi_support=False
enable_minidebuginfo=False
'''

    source_archive_name = "libunwind-%s" % version
    source_url = "http://download.savannah.nongnu.org/releases/libunwind/%s.tar.gz" % source_archive_name
    local_install_path = "install"


    def source(self):
        self.output.info("Downloading sources from %s" % self.source_url)
        tools.get(self.source_url)


    def build(self):
        build_env = AutoToolsBuildEnvironment(self)
        configure_options = ["--prefix="]
        
        if self.settings.build_type == "Debug":
            configure_options.append("--enable-debug")
        
        if self.options.shared:
            configure_options.append("--disable-static")
        else:
            configure_options.append("--disable-shared")
        
        if not self.options.enable_coredump:
            configure_options.append("--disable-coredump")
        
        if not self.options.enable_ptrace:
            configure_options.append("--disable-ptrace")
        
        if not self.options.enable_setjmp:
            configure_options.append("--disable-setjmp")
        
        if not self.options.enable_documentation:
            configure_options.append("--disable-documentation")
        
        if self.options.enable_cxx_exceptions:
            configure_options.append("--enable-cxx-exceptions")
        
        if self.options.enable_debugframe:
            configure_options.append("--enable-debugframe")
        
        if self.options.enable_block_signals:
            configure_options.append("--enable-block-signals")
            
        if self.options.enable_conservative_checks:
            configure_options.append("--enable-conservative-checks")
        
        if self.options.enable_msabi_support:
            configure_options.append("--enable-msabi-support")
    
        if self.options.enable_minidebuginfo:
            configure_options.append("--enable-minidebuginfo")
        
        with tools.chdir(self.source_archive_name):
            self.output.info("Configuring libunwind")
                 
            # Conan does not consider cross-building from x86_64 to x86 as such.
            # This causes trouble, though, as the configure script screws up
            # if it has no exact target specified in such situations.
            # Also, there seems to be a bug in conan, which causes the build to
            # fail on windows if no explicit configuration path is specified
            # (conan calls the configure script with ./configure)
            if platform.machine() == "x86_64" and self.settings.arch == "x86":
                build_env.configure(args=configure_options, target="i686",
                    configure_dir=os.getcwd())
            else:
                build_env.configure(args=configure_options, configure_dir=os.getcwd())
            
            self.output.info("Building libunwind")
            build_env.make()
            
            self.output.info("Doing a local install for packaging")
            build_env.make(["install", "prefix=%s" % os.path.join(os.getcwd(), os.pardir, self.local_install_path)])
        
        # If cross-building, the libraries are installed with a suffix denoting
        # the target platform. We don't want that.
        if tools.cross_building(self.settings) or \
                (platform.machine() == "x86_64" and self.settings.arch =="x86"):
            with tools.chdir(os.path.join(self.local_install_path, "lib")):
                for lib in glob("*-%s.*" % self.settings.arch):
                    new_lib = re.sub("^(.+)-%s\\.(.+)$" % self.settings.arch, "\\1.\\2", lib)
                    self.output.info("Renaming %s to %s" % (lib, new_lib))
                    os.rename(lib, new_lib)
        

    def package(self):
        self.copy("*", dst=".", src=self.local_install_path)
        self.copy("COPYING", dst="licenses", src=self.source_archive_name)
        
        # libunwind does not install the libunwind header when cross-building.
        if tools.cross_building(self.settings) or \
                (platform.machine() == "x86_64" and self.settings.arch == "x86"):
            self.copy("libunwind.h", dst="include", src=os.path.join(self.source_archive_name, "include"))


    def package_info(self):
        self.cpp_info.libs = ["unwind"]
        
        if self.options.enable_coredump:
            self.cpp_info.libs.append("unwind-coredump")
        
        if self.options.enable_ptrace:
            self.cpp_info.libs.append("unwind-ptrace")
        
        if self.options.enable_setjmp:
            self.cpp_info.libs.append("unwind-setjmp")
