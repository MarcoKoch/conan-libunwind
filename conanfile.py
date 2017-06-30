from conans import ConanFile, AutoToolsBuildEnvironment, tools
import os, platform


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
# Not supported for now, as we don not have a latex2man package
#"enable_documentation": [True, False],
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

    
    def _get_build_environment_str(self):
        if tools.os_info.is_linux:
            return "%s-unknown-linux" % platform.machine()
        elif tools.os_info.is_windows:
            return "%s-windows" % platform.machine()
        elif tools.os_info.is_macos:
            return "%s-macos" % platform.machine()
        else:
            return platform.machine()
    
    
    def _get_target_environment_str(self):
        if self.settings.arch == "x86":
            arch = "i686"
        else:
            arch = self.settings.arch
        
        if self.settings.os == "Linux":
            return "%s-unknown-linux" % arch
        elif self.settings.os == "Windows":
            return "%s-windows" % arch
        elif self.settings.os == "Macos":
            return "%s-macos" % arch
        else:
            return arch


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
        
        # Not supported for now, as we don not have a latex2man package
        #if not self.options.enable_documentation:
        #    configure_options.append("--disable-documentation")
        
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
            
        # Conan does not consider cross-building from x86_64 to x86 as such.
        # This causes trouble though, as the configure script screws up
        # if it has no exact host specified in such situations.
        configure_options.append("--build=%s" % self._get_build_environment_str())
        configure_options.append("--host=%s" % self._get_target_environment_str())
        configure_options.append("--target=%s" % self._get_target_environment_str())
        
        # HACK: If crosscompiling from x86_64 to x86, libunwind's configure script
        # tries to use the 64 bit compiler even though host and target platform
        # are specifed correctly. We manually add the -m32 flag to the CFLAGS
        # to enforce the correct compiler.
        if self.settings.arch == "x86" and (self.settings.compiler == "gcc" or \
                self.settings.compiler == "clang" or self.settings.compiler == "apple-clang"):
            configure_options.append("CFLAGS=-m32")
        
        with tools.chdir(self.source_archive_name):
            self.output.info("Configuring libunwind")
            
            # HACK: We can't use build_env.configure() here as that neither works on
            # Windows, nor does it play nice with libunwind's configure script
            # in cross bulding setups. Instead we call the configure script directly.
            self.run(os.path.join(os.path.curdir, "configure %s" % " ".join(configure_options)))
            
            self.output.info("Building libunwind")
            build_env.make()
            
            self.output.info("Doing a local install for packaging")
            build_env.make(["install", "prefix=%s" % os.path.join(os.getcwd(), \
                os.pardir, self.local_install_path)])
        
        # HACK: There seems to be a bug in libunwind's build system that causes
        # a broken symlink to be created when configured with --enable-shared.
        # This causes conan to drop out with an error when it tries to copy
        # that link during package(). The easiest workaround should be to just
        # delete that nonsense.
        if self.options.shared:
            broken_link = os.path.join(self.local_install_path, "lib", "libunwind-generic.a")
            if os.path.islink(broken_link):
                self.output.info("HACK: Deleting broken symlink %s" % broken_link)
                os.unlink(broken_link)
        

    def package(self):
        self.copy("*", dst=".", src=self.local_install_path, links=True)
        self.copy("COPYING", dst="licenses", src=self.source_archive_name)


    def package_info(self):
        self.cpp_info.libs = ["unwind"]
        
        if self.options.enable_coredump:
            self.cpp_info.libs.append("unwind-coredump")
        
        if self.options.enable_ptrace:
            self.cpp_info.libs.append("unwind-ptrace")
        
        if self.options.enable_setjmp:
            self.cpp_info.libs.append("unwind-setjmp")
